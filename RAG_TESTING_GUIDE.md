# RAG Model Testing Guide - Sample Contract Q&A Validation

## 📋 Overview

This guide contains questions to test your RAG chatbot's accuracy and retrieval quality on the **sample_contract.txt** file. Use these to validate that the Retrieval-Augmented Generation model correctly understands contract content.

---

## 🎯 Testing Strategy

### Question Categories
1. **Basic Facts** - Direct information from contract
2. **Financial Terms** - Payment and monetary terms
3. **Dates & Timelines** - Important dates and periods
4. **Rights & Obligations** - Who has to do what
5. **Restrictions** - What's not allowed
6. **Termination Conditions** - How contract can end
7. **Dispute Resolution** - How conflicts are handled
8. **Risk & Liability** - Financial and legal risks
9. **Complex Reasoning** - Multi-clause understanding
10. **Edge Cases** - Tricky or indirect questions

---

## ✅ CATEGORY 1: BASIC FACTS

### Q1.1: What are the names of the parties in this contract?

**Expected Answer:**
- Service Provider: TechCorp Inc., a Delaware corporation
- Client: ClientCorp LLC, a Texas limited liability company

**Accuracy Criteria:**
- ✓ Both parties mentioned correctly
- ✓ Legal entity types included
- ✓ States of incorporation mentioned

---

### Q1.2: What is the effective date of this agreement?

**Expected Answer:**
January 1, 2024

**Accuracy Criteria:**
- ✓ Exact date mentioned
- ✓ Could also mention "Effective Date" terminology

---

### Q1.3: What services are being provided?

**Expected Answer:**
Professional software development and consulting services, as detailed in the Statement of Work (Exhibit A). The services include:
- Phase 1: Requirements analysis and system design
- Phase 2: Development and implementation
- Phase 3: Testing and quality assurance
- Phase 4: Deployment and support

**Accuracy Criteria:**
- ✓ Primary service area identified
- ✓ At least 2 of 4 phases mentioned
- ✓ Reference to SOW/Exhibit A

---

### Q1.4: How should services be performed according to Section 1.2?

**Expected Answer:**
All Services shall be performed in accordance with industry best practices and professional standards.

**Accuracy Criteria:**
- ✓ Both "best practices" and "professional standards" mentioned
- ✓ Or close paraphrase of this standard

---

### Q1.5: Who are the signatory representatives?

**Expected Answer:**
- Service Provider: Daniel Smith, VP Operations (TechCorp Inc.)
- Client: Jennifer Williams, CFO (ClientCorp LLC)

**Accuracy Criteria:**
- ✓ Both names mentioned
- ✓ Titles included
- ✓ Companies associated correctly

---

## 💰 CATEGORY 2: FINANCIAL TERMS

### Q2.1: What is the monthly fee for services?

**Expected Answer:**
$50,000 per month

**Accuracy Criteria:**
- ✓ Exact amount: $50,000
- ✓ Time period: monthly/per month

---

### Q2.2: What are the payment terms?

**Expected Answer:**
- Fee: $50,000 per month
- Payment: Payable in arrears (within 30 days of invoice receipt)
- Invoices: Submitted on the first business day of each month
- Method: Bank transfer to account specified by Service Provider

**Accuracy Criteria:**
- ✓ Payment timing (30 days) mentioned
- ✓ "In arrears" or payment occurs after services rendered
- ✓ Invoicing schedule mentioned

---

### Q2.3: When are invoices submitted?

**Expected Answer:**
On the first business day of each month, covering services rendered in the preceding month.

**Accuracy Criteria:**
- ✓ "First business day of each month"
- ✓ Covers previous month services

---

### Q2.4: How should payments be made?

**Expected Answer:**
Via bank transfer to the account specified in writing by Service Provider.

**Accuracy Criteria:**
- ✓ Method: bank transfer
- ✓ Account information provided by Service Provider

---

### Q2.5: What interest rate applies to late payments?

**Expected Answer:**
1.5% per month, or the maximum rate permitted by law, whichever is lower.

**Accuracy Criteria:**
- ✓ Rate: 1.5% per month
- ✓ Legal maximum caveat mentioned

---

### Q2.6: What happens if Client doesn't pay on time?

**Expected Answer:**
Late payments accrue interest at 1.5% per month (or maximum rate permitted by law, whichever is lower).

**Accuracy Criteria:**
- ✓ Interest accrual mentioned
- ✓ Rate specified

---

## 📅 CATEGORY 3: DATES & TIMELINES

### Q3.1: What is the initial term of this agreement?

**Expected Answer:**
Twelve (12) months from the Effective Date (January 1, 2024, through January 1, 2025)

**Accuracy Criteria:**
- ✓ 12 months or one year
- ✓ Starting from Effective Date

---

### Q3.2: How long is the confidentiality period?

**Expected Answer:**
Five (5) years from the date of disclosure.

**Accuracy Criteria:**
- ✓ Exactly 5 years
- ✓ From date of disclosure

---

### Q3.3: What is the notice period for termination without cause?

**Expected Answer:**
Ninety (90) days written notice.

**Accuracy Criteria:**
- ✓ 90 days
- ✓ Must be written notice

---

### Q3.4: How many days does the other party have to cure a material breach?

**Expected Answer:**
Thirty (30) days from receiving written notice of the breach.

**Accuracy Criteria:**
- ✓ 30 days
- ✓ Cure period from notice

---

### Q3.5: How long can Force Majeure prevent performance before allowing termination?

**Expected Answer:**
More than sixty (60) days. If a Force Majeure Event prevents performance for more than 60 days, either party may terminate.

**Accuracy Criteria:**
- ✓ 60 days threshold
- ✓ After this period, termination becomes possible

---

## 🤝 CATEGORY 4: RIGHTS & OBLIGATIONS

### Q4.1: What personnel-related obligation does Service Provider have?

**Expected Answer:**
Service Provider shall assign qualified personnel to perform the Services. Client may request replacement of Service Provider personnel upon reasonable notice if performance is unsatisfactory.

**Accuracy Criteria:**
- ✓ Must assign "qualified personnel"
- ✓ Client can request replacement
- ✓ Reasonable notice required

---

### Q4.2: What are Service Provider's warranty obligations?

**Expected Answer:**
Service Provider warrants that:
- It has the right and authority to enter into this Agreement
- The Services will be performed in a professional and workmanlike manner
- It will comply with all applicable laws and regulations

**Accuracy Criteria:**
- ✓ At least 2 of 3 warranties mentioned
- ✓ Covers authority, professional performance, and legal compliance

---

### Q4.3: Who owns the work product created under this agreement?

**Expected Answer:**
Client owns all work product created specifically for Client under this Agreement, provided all fees and expenses have been paid in full.

**Accuracy Criteria:**
- ✓ Client owns Work Product
- ✓ Conditional on full payment

---

### Q4.4: What license does Service Provider receive?

**Expected Answer:**
Client grants Service Provider a non-exclusive, perpetual license to use any methodologies, tools, or processes developed during the performance of Services for other clients.

**Accuracy Criteria:**
- ✓ Non-exclusive license
- ✓ For methodologies/tools/processes
- ✓ For use with other clients
- ✓ Perpetual (ongoing)

---

### Q4.5: What is Service Provider's indemnification obligation?

**Expected Answer:**
Service Provider shall defend, indemnify, and hold harmless Client from any third-party claims that the Work Product or Services infringe any patent, copyright, or trade secret rights (subject to Client's prompt notification and granting Service Provider sole control of defense).

**Accuracy Criteria:**
- ✓ Covers IP infringement claims
- ✓ Must defend and hold harmless
- ✓ Subject to conditions

---

### Q4.6: What confidentiality obligations exist?

**Expected Answer:**
The Receiving Party shall:
- Keep all Confidential Information strictly confidential
- Not disclose it to third parties without prior written consent
- Use it solely for purposes of performing or evaluating the Services

**Accuracy Criteria:**
- ✓ At least 2 of 3 obligations mentioned
- ✓ Covers non-disclosure and limited use

---

## 🚫 CATEGORY 5: RESTRICTIONS & PROHIBITIONS

### Q5.1: When CAN'T either party terminate the agreement?

**Expected Answer:**
- Cannot terminate for cause without the other party having 30 days to cure a material breach
- Cannot terminate without cause without providing 90 days notice
- Cannot terminate for Force Majeure situations in the first 60 days

**Accuracy Criteria:**
- ✓ Cure period requirement mentioned
- ✓ Notice requirement for termination without cause

---

### Q5.2: What limitations exist on liability?

**Expected Answer:**
- Neither party is liable for indirect, incidental, consequential, special, or punitive damages
- Total liability capped at fees paid by Client in the 12 months preceding the liability event
- Exceptions: breaches of confidentiality, indemnification obligations, gross negligence, or willful misconduct

**Accuracy Criteria:**
- ✓ Liability cap mentioned
- ✓ Excludes certain damages
- ✓ Exceptions noted

---

### Q5.3: What does Service Provider disclaim?

**Expected Answer:**
Service Provider disclaims all implied warranties except those expressly set forth in the Agreement, specifically disclaiming:
- Warranties of merchantability
- Fitness for a particular purpose
- Non-infringement

**Accuracy Criteria:**
- ✓ Implied warranty disclaimer mentioned
- ✓ At least 1 specific disclaimer included

---

### Q5.4: Can either party assign this agreement to someone else?

**Expected Answer:**
Neither party may assign this Agreement without the prior written consent of the other party, EXCEPT Service Provider may assign to an affiliate.

**Accuracy Criteria:**
- ✓ Generally cannot assign
- ✓ Exception for Service Provider affiliates

---

### Q5.5: What happens to pre-existing intellectual property of Service Provider?

**Expected Answer:**
All pre-existing intellectual property of Service Provider remains the exclusive property of Service Provider. Service Provider can use it for other clients.

**Accuracy Criteria:**
- ✓ Service Provider retains ownership
- ✓ Pre-existing IP excluded from Work Product

---

## 🛑 CATEGORY 6: TERMINATION CONDITIONS

### Q6.1: What are the ways this agreement can be terminated?

**Expected Answer:**
1. **Without Cause:** Either party may terminate with 90 days written notice
2. **For Cause (Material Breach):** Immediate termination if the other party breaches and fails to cure within 30 days
3. **Force Majeure:** Either party may terminate if Force Majeure prevents performance for more than 60 days

**Accuracy Criteria:**
- ✓ At least 2 termination methods mentioned
- ✓ Includes timing for each

---

### Q6.2: What must happen to payments upon termination?

**Expected Answer:**
Client shall pay Service Provider:
- For all Services rendered through the termination date
- Plus any reasonable out-of-pocket expenses incurred

**Accuracy Criteria:**
- ✓ Payment for services through termination date
- ✓ Expenses covered

---

### Q6.3: What happens if Work Product is found to infringe IP rights?

**Expected Answer:**
Service Provider shall, at its option and expense:
- Obtain the right for Client to continue using it, OR
- Replace or modify it to be non-infringing, OR
- If neither option is commercially practical, terminate the agreement and refund fees for the infringing Work Product

**Accuracy Criteria:**
- ✓ At least 2 options mentioned
- ✓ Refund option included

---

## ⚖️ CATEGORY 7: DISPUTE RESOLUTION

### Q7.1: Where will disputes be resolved according to this contract?

**Expected Answer:**
Disputes shall be submitted to binding arbitration administered by the American Arbitration Association in New York, New York, in accordance with the Commercial Arbitration Rules.

**Accuracy Criteria:**
- ✓ Arbitration mentioned (not court)
- ✓ AAA (American Arbitration Association) specified
- ✓ Location: New York, New York

---

### Q7.2: What is the first step to resolve disputes?

**Expected Answer:**
Good faith negotiation between senior executives of each party.

**Accuracy Criteria:**
- ✓ Negotiation required first
- ✓ Between senior executives

---

### Q7.3: Which state's laws govern this agreement?

**Expected Answer:**
Delaware state law (without regard to its conflict of law provisions).

**Accuracy Criteria:**
- ✓ Delaware
- ✓ No conflict of law application

---

### Q7.4: What jury trial rights do the parties waive?

**Expected Answer:**
Each party waives:
- Any right to jury trial
- Any right to bring claims on a class action basis

**Accuracy Criteria:**
- ✓ Jury trial waived
- ✓ Class action waived

---

## ⚠️ CATEGORY 8: RISK & LIABILITY

### Q8.1: What insurance must Service Provider maintain?

**Expected Answer:**
Professional liability insurance with minimum coverage of:
- $1,000,000 per claim
- $2,000,000 aggregate

**Accuracy Criteria:**
- ✓ $1,000,000 per claim
- ✓ $2,000,000 aggregate
- ✓ Professional liability mentioned

---

### Q8.2: What is the maximum liability either party faces?

**Expected Answer:**
Total cumulative liability cannot exceed the fees paid by Client in the 12 months preceding the event giving rise to liability. (In this case, maximum $600,000 in Year 1: $50,000 × 12 months)

**Accuracy Criteria:**
- ✓ Liability cap at 12 months of fees
- ✓ Or calculated amount: $600,000

---

### Q8.3: What exceptions exist to the liability limitations?

**Expected Answer:**
The liability limitations do NOT apply to:
- Breaches of confidentiality obligations
- Indemnification obligations
- Either party's gross negligence or willful misconduct

**Accuracy Criteria:**
- ✓ At least 2 exceptions mentioned
- ✓ Includes confidentiality breach exception

---

### Q8.4: What happens if Client's materials infringe third-party IP?

**Expected Answer:**
Client shall indemnify Service Provider against claims that Client's material or specifications provided to Service Provider infringe third-party rights.

**Accuracy Criteria:**
- ✓ Client indemnifies Service Provider
- ✓ For Client-provided materials

---

### Q8.5: What constitutes a Force Majeure Event?

**Expected Answer:**
Causes beyond reasonable control of either party, including:
- Acts of God
- Natural disasters
- War
- Terrorism
- Pandemics
- Government action

**Accuracy Criteria:**
- ✓ At least 3 examples provided
- ✓ "Beyond reasonable control" concept

---

## 🧩 CATEGORY 9: COMPLEX REASONING

### Q9.1: If Service Provider staff member is underperforming, what's the process?

**Expected Answer:**
1. Client may request replacement upon reasonable notice
2. Client must indicate performance is unsatisfactory
3. Service Provider must assign replacement qualified personnel

**Accuracy Criteria:**
- ✓ Client initiates request
- ✓ Reasonable notice required
- ✓ Replacement must be qualified

---

### Q9.2: What's the relationship between the SOW (Exhibit A) and the main agreement?

**Expected Answer:**
- Exhibit A (SOW) is attached to and part of the main Agreement
- Services described in Exhibit A define what work is to be performed
- The entire agreement (including Exhibit A) constitutes the complete agreement

**Accuracy Criteria:**
- ✓ SOW is part of/attached to Agreement
- ✓ SOW defines services
- ✓ Together they form the complete contract

---

### Q9.3: If a pandemic prevents performance for 90 days, what can happen?

**Expected Answer:**
- Service Provider has 90 days to resume performance (counts as Force Majeure)
- After 60 days, either party may terminate the agreement
- So after 60 days (before 90), either could terminate; after 90 days, Service Provider is in breach

**Accuracy Criteria:**
- ✓ 60-day threshold for termination right
- ✓ After 60 days, termination becomes an option
- ✓ Service Provider must resume by 90 days or face breach

---

### Q9.4: Can Service Provider use methodologies developed for Client on other projects?

**Expected Answer:**
Yes. The methodologies, tools, and processes developed during Services can be used for other clients. However, any modifications or improvements specifically funded by Client remains Client's property.

**Accuracy Criteria:**
- ✓ Service Provider can reuse methodologies
- ✓ Client gets exclusive ownership of funded work
- ✓ Distinguishes pre-existing vs. funded work

---

### Q9.5: What happens to Client's confidential information after 6 years?

**Expected Answer:**
After 5 years, Confidential Information protection expires. After 6 years, it's technically no longer protected under this agreement (unless it qualifies as a trade secret under law).

**Accuracy Criteria:**
- ✓ 5-year protection period mentioned
- ✓ After 5 years, protection ends

---

## 🎲 CATEGORY 10: EDGE CASES & TRICKY QUESTIONS

### Q10.1: Can Client and Service Provider both sue each other in court over a dispute?

**Expected Answer:**
No. Both parties waive their right to jury trial. Disputes must go to binding arbitration with AAA in New York, not court.

**Accuracy Criteria:**
- ✓ No court litigation
- ✓ Arbitration required
- ✓ AAA process mandatory

---

### Q10.2: Who decides if information is "publicly available" under the confidentiality clause?

**Expected Answer:**
The contract doesn't specify, but information that "is or becomes publicly available through no breach of this Agreement" is excluded from confidentiality protection. This would typically require mutual agreement or legal determination.

**Accuracy Criteria:**
- ✓ Notes the contract doesn't specify
- ✓ References public availability exception
- ✓ Acknowledges ambiguity

---

### Q10.3: If Service Provider goes bankrupt, can Client's work be seized?

**Expected Answer:**
The contract doesn't specifically address bankruptcy. As Client owns the Work Product, it should be Client's property. However, Service Provider's pre-existing IP would remain with Service Provider or potentially with a trustee.

**Accuracy Criteria:**
- ✓ Notes contract limitation
- ✓ References Work Product ownership
- ✓ Acknowledges uncertainty

---

### Q10.4: What if neither party cures their breach within 30 days - what happens?

**Expected Answer:**
The Agreement becomes immediately terminable by the non-breaching party at the end of the 30-day cure period. Upon termination, the breaching party may owe damages (subject to liability caps) and termination payments.

**Accuracy Criteria:**
- ✓ Termination becomes available
- ✓ Breach continues = material breach
- ✓ Liability caps still apply

---

### Q10.5: Can the agreement be signed in counterparts (separately)?

**Expected Answer:**
Yes. Section 12.7 explicitly states: "This Agreement may be executed in counterparts, each of which shall be deemed an original and all together shall constitute one instrument."

**Accuracy Criteria:**
- ✓ Counterparts allowed
- ✓ Each counts as original
- ✓ Together = one instrument

---

## 📊 RAG ACCURACY SCORING MATRIX

### Question Difficulty Levels

| Level | Questions | Scoring |
|-------|-----------|---------|
| **Easy** | Q1.1-1.5, Q2.1, Q3.1 | 1 point each (7 total) |
| **Medium** | Q2.2-2.6, Q4.1-4.6, Q5.1-5.3 | 2 points each (21 total) |
| **Hard** | Q6.1-6.3, Q7.1-7.4, Q8.1-8.5, Q9.1-9.5 | 3 points each (36 total) |
| **Expert** | Q10.1-10.5 | 4 points each (20 total) |
| **TOTAL** | 50 questions | **84 points** |

---

## 🎯 SCORING INTERPRETATION

```
Score Range          | RAG Model Quality
--------------------|--------------------------------------------------
76-84 (91-100%)      | ✅ Excellent - Production ready
66-75 (79-90%)       | ✅ Good - Minor improvements needed
56-65 (67-78%)       | ⚠️ Fair - Moderate improvements needed
46-55 (55-66%)       | ❌ Poor - Significant work required
Below 46 (<55%)      | ❌ Not Ready - Needs major fixes
```

---

## 🧪 TESTING BEST PRACTICES

### How to Test Effectively

1. **Ask questions naturally** - Use your conversational tone, not the exact wording
2. **Vary phrasing** - Ask the same fact in different ways
3. **Check reasoning** - Verify RAG explains WHY, not just WHAT
4. **Test boundaries** - Ask questions about information NOT in the contract
5. **Complex queries** - Combine multiple sections in one question

### Example Variant Phrasings

**Original:** "What are the payment terms?"

**Variants:**
- "How often do I get paid?"
- "When should invoice be paid?"
- "Tell me about money in this contract"
- "What are the fees?"
- "How much does Client owe per month?"

### Success Criteria for Each Answer

✅ **Accuracy**: Answer matches expected answer
✅ **Completeness**: All key details included
✅ **Sources**: RAG cites which section
✅ **Clarity**: Easy to understand
✅ **Relevance**: Directly answers the question

---

## 📝 TESTING LOG TEMPLATE

When testing, track results:

```
Question: [Your Question]
Expected Answer: [From this guide]
RAG Answer: [What chatbot responded]
Accuracy: ☐ Exact ☐ Good ☐ Partial ☐ Wrong ☐ Hallucinated
Notes: [Additional observations]
```

---

## 🚀 Quick Test Session (30 minutes)

For a quick validation, test these 10 key questions:

1. Q1.1 - Party names
2. Q2.1 - Monthly fee
3. Q3.1 - Initial term
4. Q4.3 - Work product ownership
5. Q6.1 - Termination methods
6. Q7.1 - Dispute resolution location
7. Q8.1 - Insurance coverage
8. Q9.1 - Staff replacement process
9. Q9.3 - Force Majeure timeline
10. Q10.1 - Jury trial rights

**If RAG scores 8/10+ on these:** Model is working well for basic understanding
**If RAG scores 6-7/10:** Model needs some tuning
**If RAG scores <6/10:** Major issues to address

---

## 💡 Common RAG Errors to Watch For

### 1. **Hallucination** ❌
- RAG invents information not in contract
- Example: "The fee is $75,000" (should be $50,000)

### 2. **Incompleteness** ❌
- RAG mentions only part of the answer
- Example: Only mentions $50,000 but not "per month"

### 3. **Wrong Section** ⚠️
- RAG references wrong clause number
- Example: Cites Section 7.1 instead of Section 2.1 for payment terms

### 4. **Confusion** ❌
- RAG confuses two similar concepts
- Example: Confuses Client-owned Work Product with Service Provider IP

### 5. **Reasoning Error** ⚠️
- RAG gets facts right but reasoning wrong
- Example: "Termination is not allowed" (should be "90 days notice required")

---

## ✨ Sample Conversation to Test

**You:**
> "What happens if the work developed by TechCorp gets stolen - can ClientCorp sue?"

**Expected RAG Response (Good):**
> "Yes, ClientCorp can sue. TechCorp has an indemnification obligation for IP infringement. According to Section 8.1, TechCorp must defend, indemnify, and hold harmless ClientCorp from any third-party claims that the Work Product infringes patent, copyright, or trade secret rights. If the Work Product is deemed infringing, TechCorp has three options under Section 8.2: obtain the right to continue using it, replace or modify it, or terminate and refund the fees paid."

**Poor RAG Response:** ❌
> "I don't know" or "They can sue anyone"

---

## 📞 Questions to Refine Testing

After running the test suite, consider:

1. **Which questions confused the RAG model?** (Improvement areas)
2. **Were answers too verbose or too terse?** (Calibration needed)
3. **Did RAG cite sources correctly?** (Retrieval quality)
4. **Were edge cases handled gracefully?** (Robustness)
5. **Did RAG acknowledge uncertainty?** (Honesty)

---

**Happy testing! Use these 50 questions to validate your RAG model's accuracy.** 🚀
