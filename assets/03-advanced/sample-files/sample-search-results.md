# Sample Search Results

Expected output when searching the knowledge base through the MCP server.

---

## Hybrid Search (Default)

**Query:** "What are the FMLA eligibility requirements?"
**Mode:** hybrid | **Results:** 5 | **Latency:** 89ms

### 1. fmla-policy-2023.md
**Score:** 0.8742 (vector: 0.8921, text: 0.8324)

Employees are eligible for FMLA leave if they meet the following criteria: (1) Have worked for the employer for at least 12 months; (2) Have at least 1,250 hours of service during the 12-month period immediately preceding the leave...

---

### 2. handbook-nc-current.md
**Score:** 0.6518 (vector: 0.7012, text: 0.5364)

Leave policies are governed by both federal and state requirements. For FMLA-eligible employees, Truepoint HR Solutions provides up to 12 weeks of unpaid, job-protected leave...

---

## Vector-Only Search

**Query:** "What are the FMLA eligibility requirements?"
**Mode:** vector | **Results:** 5 | **Latency:** 62ms

### 1. fmla-policy-2023.md
**Score:** 0.8921

(Same content but ranked by vector similarity only — no keyword boost)

---

## Hybrid + Reranking

**Query:** "What are the FMLA eligibility requirements?"
**Mode:** hybrid + reranking | **Results:** 5 | **Latency:** 1240ms

### 1. fmla-policy-2023.md
**Score:** 0.8742 | **Rerank:** 0.95

(Reranking confirmed this result as highly relevant — GPT-4o-mini scored it 0.95)

### 2. handbook-nc-current.md
**Score:** 0.6518 | **Rerank:** 0.72

(Reranking identified this as moderately relevant — mentions FMLA but focuses on general leave)

---

## Comparison Notes

| Mode | Top Result | Latency | Notes |
|------|-----------|---------|-------|
| Hybrid | fmla-policy-2023.md (0.87) | ~90ms | Best balance of speed and quality |
| Vector | fmla-policy-2023.md (0.89) | ~60ms | Fastest, but misses keyword-specific matches |
| Hybrid + Rerank | fmla-policy-2023.md (rerank: 0.95) | ~1200ms | Best precision, highest latency |

Reranking adds ~1 second per query (10 LLM calls). Use it when precision matters more than speed.
