# Source Files

Documents to ingest through the RAG pipeline. These represent the kind of files a client's knowledge base would contain — HR policies, compliance checklists, templates, and reference data.

## File Inventory

### Markdown (reused from Lesson 1)

| File | Content | Origin |
|------|---------|--------|
| `construction-safety-policy.md` | Multi-state construction safety policy (NC/SC/VA) | Lesson 1 sample client file |
| `medical-hipaa-compliance-checklist.md` | HIPAA compliance checklist for healthcare employers | Lesson 1 sample client file |
| `restaurant-employee-handbook-draft.md` | Restaurant employee handbook with tip pooling, scheduling | Lesson 1 sample client file |
| `tech-startup-offer-letter-template.md` | Offer letter template with equity vesting, at-will language | Lesson 1 sample client file |

### Markdown (new for Lesson 2)

| File | Content | Based On (from Drive inventory) |
|------|---------|--------------------------------|
| `handbook-nc-current.md` | NC employee handbook — canonical version | Handbook - NC - CURRENT.docx (Keep) |
| `anti-harassment-policy-2024.md` | Updated anti-harassment policy with EEOC 2024 guidance | Anti-Harassment Policy - updated 2024.docx (Keep) |
| `fmla-policy-2023.md` | FMLA policy for covered employers (50+ employees) | FMLA Policy 2023.docx (Keep) |
| `subcontractor-classification-memo.md` | Subcontractor vs employee classification guidance | Subcontractor Classification Memo.docx (Keep) |
| `onboarding-checklist-consultant.md` | New consultant onboarding checklist | Onboarding Checklist - Consultant.docx (Update) |

### Word Documents (.docx)

| File | Content | Based On |
|------|---------|----------|
| `drug-testing-policy-dot.docx` | DOT-regulated drug testing policy | Drug Testing - DOT Regulated.docx (Keep) |
| `pto-policy-unlimited.docx` | Unlimited PTO policy template | PTO Policy - Unlimited.docx (Keep) |

### PDF Files (.pdf)

| File | Content | Based On |
|------|---------|----------|
| `dol-overtime-rule-2024.pdf` | DOL overtime rule summary (federal guidance) | DOL Overtime Rule 2024.pdf (Keep) |
| `eeoc-harassment-guidance-2024.pdf` | EEOC harassment prevention guidance | EEOC Guidance - Harassment 2024.pdf (Keep) |

### CSV Files (.csv)

| File | Content | Based On |
|------|---------|----------|
| `workers-comp-state-reference.csv` | Workers compensation rates and rules by state | Workers Comp State-by-State Reference.xlsx (Keep, "fully trusted") |
| `i9-audit-checklist.csv` | I-9 verification audit checklist with status tracking | I-9 Audit Checklist.xlsx (Keep) |

## Why These Files

The mix covers all 4 file types the pipeline supports (md, docx, pdf, csv) and spans the client's key domains: HR policies, compliance, construction, medical, tech startups. The chunking router will use different strategies depending on file type and structure.

## Lesson 1 Files

The 4 markdown files from Lesson 1 are referenced by path, not copied:

```
../01-core/raw-client-files/sample-client-files/
```

The pipeline's file intake step should scan both this folder and the Lesson 1 path.
