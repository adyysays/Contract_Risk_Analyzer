"""
RAG (Retrieval-Augmented Generation) Chatbot module
Implements semantic search and answer generation for contract queries
"""

import logging
import numpy as np
from typing import List, Tuple, Dict
import faiss
import google.generativeai as genai

logger = logging.getLogger(__name__)


class TextChunker:
    """Chunks text into overlapping segments for RAG"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize Text Chunker
        
        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            start += (self.chunk_size - self.chunk_overlap)
        
        return chunks


class SimpleEmbedder:
    """Embedding using Google's embedding API for semantic understanding"""
    
    def __init__(self, embedding_dim: int = 768):
        """
        Initialize embedder using Google's Gemini embeddings
        
        Args:
            embedding_dim: Dimension of embeddings (overridden by API)
        """
        self.embedding_dim = embedding_dim
        self.vocab = {}
        self.vocab_size = 0
    
    def build_vocab(self, texts: List[str]):
        """
        Build vocabulary from texts (not used with Google embeddings)
        
        Args:
            texts: List of texts to build vocab from
        """
        pass  # Not needed for Google embeddings
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Create embedding using Google's embedding API
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            # Use Google's embedding API
            response = genai.embed_content(
                model="models/embedding-001",
                content=text[:2000],  # Limit to 2000 chars for embedding
                task_type="RETRIEVAL_DOCUMENT"
            )
            embedding = np.array(response['embedding']).astype(np.float32)
            return embedding
        except Exception as e:
            logger.warning(f"Error embedding with Google API: {e}, using fallback")
            # Fallback: simple TF-IDF if API fails
            words = text.lower().split()
            embedding = np.random.randn(768).astype(np.float32)
            for word in words[:50]:  # Use first 50 words
                embedding += np.random.RandomState(hash(word) % 2**32).randn(768).astype(np.float32)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            return embedding


class RAGChatbot:
    """RAG-based Chatbot for contract Q&A"""
    
    def __init__(self, gemini_client):
        """
        Initialize RAG Chatbot
        
        Args:
            gemini_client: Instance of GeminiClient for answer generation
        """
        self.gemini_client = gemini_client
        self.chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
        self.embedder = SimpleEmbedder(embedding_dim=384)
        self.chunks = []
        self.embeddings = None
        self.index = None
        self.initialized = False
    
    def build_index(self, contract_text: str):
        """
        Build FAISS index from contract text
        
        Args:
            contract_text: Full contract text
        """
        try:
            # Chunk the text
            self.chunks = self.chunker.chunk_text(contract_text)
            
            if not self.chunks:
                logger.warning("No chunks created from contract text")
                return
            
            # Build vocabulary from chunks
            self.embedder.build_vocab(self.chunks)
            
            # Create embeddings for all chunks
            embeddings_list = []
            for chunk in self.chunks:
                embedding = self.embedder.embed_text(chunk)
                embeddings_list.append(embedding)
            
            self.embeddings = np.array(embeddings_list)
            
            # Create FAISS index
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.embeddings)
            
            self.initialized = True
            logger.info(f"RAG index built with {len(self.chunks)} chunks")
        
        except Exception as e:
            logger.error(f"Error building RAG index: {e}")
            self.initialized = False
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Retrieve most relevant chunks for a query
        
        Args:
            query: User query
            top_k: Number of top results to retrieve
            
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        if not self.initialized or self.index is None:
            logger.warning("RAG index not initialized")
            return []
        
        try:
            # Embed the query
            query_embedding = self.embedder.embed_text(query)
            query_embedding = np.array([query_embedding])
            
            # Search the index
            distances, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
            
            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if idx < len(self.chunks):
                    # Convert L2 distance to similarity score (0-1)
                    similarity = 1 / (1 + distance)
                    results.append((self.chunks[idx], float(similarity)))
            
            return results
        
        except Exception as e:
            logger.error(f"Error retrieving chunks: {e}")
            return []
    
    def answer_question(self, question: str) -> Tuple[str, List[Tuple[str, float]]]:
        """
        Answer a question about the contract using RAG
        
        Args:
            question: User question
            
        Returns:
            Tuple of (answer, retrieved_chunks)
        """
        if not self.initialized:
            return "Contract index not initialized. Please upload a contract first.", []
        
        try:
            # Retrieve relevant chunks (increased from 5 to 10 for better coverage)
            relevant_chunks = self.retrieve_relevant_chunks(question, top_k=10)
            
            if not relevant_chunks:
                return "No relevant information found in the contract.", []
            
            # Combine chunks for context
            context = "\n\n".join([chunk for chunk, _ in relevant_chunks])
            
            # Generate answer using Gemini
            answer = self.gemini_client.answer_question(
                text="",
                question=question,
                context=context
            )
            
            return answer, relevant_chunks
        
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return f"Error processing your question: {str(e)}", []
    
    def get_answered_questions(self, sample_size: int = 5) -> List[str]:
        """
        Get sample questions that could be answered about the contract
        
        Args:
            sample_size: Number of sample questions
            
        Returns:
            List of sample questions
        """
        sample_questions = [
            "What are the payment terms in this contract?",
            "What are the conditions for termination?",
            "Who are the parties involved in this contract?",
            "What confidentiality obligations are imposed?",
            "What happens in case of a breach?",
            "What is the contract duration?",
            "Are there any liability limitations?",
            "What are the warranty provisions?",
            "How are disputes resolved?",
            "Are there any obligations for either party?",
        ]
        
        return sample_questions[:sample_size]
