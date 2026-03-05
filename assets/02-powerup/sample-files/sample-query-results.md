# Sample Query Results

These are example outputs from running `/calibrate` against a fully ingested knowledge base. Use these to verify your pipeline is producing similar results.

---

## Query 1: "What are the workers compensation requirements in North Carolina?"

| Rank | Score | File | Section |
|------|-------|------|---------|
| 1 | 0.847 | workers-comp-state-reference.csv | Rows 1-8 (state, coverage_threshold...) |
| 2 | 0.812 | handbook-nc-current.md | Workers' Compensation |
| 3 | 0.634 | onboarding-checklist-consultant.md | Week 1 |

**Expected behavior:** The CSV reference table should rank highest because it directly contains NC workers' comp thresholds (3+ employees, compulsory, NC Rate Bureau, $1.42 per $100). The handbook section provides the policy language.

---

## Query 2: "How should we classify subcontractors vs employees?"

| Rank | Score | File | Section |
|------|-------|------|---------|
| 1 | 0.891 | subcontractor-classification-memo.md | IRS 20-Factor Test |
| 2 | 0.856 | subcontractor-classification-memo.md | DOL Economic Reality Test |
| 3 | 0.743 | subcontractor-classification-memo.md | Construction-Specific Red Flags |

**Expected behavior:** The classification memo should dominate results since it's the only document focused on this topic. Multiple chunks from the same document appearing is expected and correct.

---

## Query 3: "What is the DOT drug testing policy for CDL drivers?"

| Rank | Score | File | Section |
|------|-------|------|---------|
| 1 | 0.878 | drug-testing-policy-dot.docx | Types of Testing |
| 2 | 0.841 | drug-testing-policy-dot.docx | Covered Employees |
| 3 | 0.723 | drug-testing-policy-dot.docx | Substances Tested |

**Expected behavior:** The DOT drug testing policy should be the primary result. This tests the DOCX conversion pipeline — if the file wasn't properly converted, these chunks won't exist.

---

## Query 4: "What are the new overtime salary thresholds?"

| Rank | Score | File | Section |
|------|-------|------|---------|
| 1 | 0.865 | dol-overtime-rule-2024.pdf | New Salary Thresholds |
| 2 | 0.802 | dol-overtime-rule-2024.pdf | What This Means for Employers |
| 3 | 0.654 | handbook-nc-current.md | Compensation and Pay Practices |

**Expected behavior:** The DOL overtime PDF should rank highest. This tests the PDF conversion pipeline. The specific threshold numbers ($58,656, $151,164) should be present in the chunk content.

---

## Query 5: "FMLA eligibility requirements"

| Rank | Score | File | Section |
|------|-------|------|---------|
| 1 | 0.882 | fmla-policy-2023.md | Eligibility |
| 2 | 0.831 | handbook-nc-current.md | Family and Medical Leave (FMLA) |
| 3 | 0.612 | onboarding-checklist-consultant.md | Day 1 |

**Expected behavior:** The dedicated FMLA policy should rank first, with the handbook's FMLA section as a strong second result. Both contain the eligibility criteria (50+ employees, 12 months employment, 1,250 hours).

---

## Notes

- Scores are approximate and will vary based on exact chunking boundaries and embedding model behavior
- Scores above 0.8 indicate strong semantic relevance
- Scores between 0.6-0.8 indicate moderate relevance
- If your results differ significantly, check the chunking output for the relevant files
