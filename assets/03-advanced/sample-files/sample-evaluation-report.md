# Sample Evaluation Report

Expected output from running `python evaluate.py`.

---

## Terminal Output

```
Lesson 3 — Evaluation Harness
Langfuse host: https://cloud.langfuse.com

Loaded 15 test queries from truepoint-queries.json

  [1/15] What are the FMLA eligibility requirements?...
  [2/15] Workers compensation requirements in North Carolina...
  [3/15] How should we classify subcontractors vs employees...
  [4/15] What is the DOT drug testing policy for CDL driver...
  [5/15] What are the new overtime salary thresholds for 20...
  [6/15] What does the anti-harassment policy cover?...
  [7/15] What is the onboarding process for new consultants...
  [8/15] What are the PTO policy details for unlimited time...
  [9/15] What does the EEOC harassment guidance say about e...
  [10/15] What items are on the I-9 audit checklist?...
  [11/15] How does North Carolina handle workplace safety r...
  [12/15] What are the steps for properly classifying indep...
  [13/15] What types of leave are available under company p...
  [14/15] What compliance training is required for new hire...
  [15/15] How do state workers comp requirements differ?...

================================================================================
EVALUATION SUMMARY
================================================================================

#    Question                                       Faith   Relev    Prec   Src
--------------------------------------------------------------------------------
1    What are the FMLA eligibility requireme...     0.920   0.885   0.950   hit
2    Workers compensation requirements in No...     0.850   0.810   0.780   hit
3    How should we classify subcontractors v...     0.910   0.870   0.900   hit
4    What is the DOT drug testing policy for...     0.880   0.860   0.850   hit
5    What are the new overtime salary thresh...     0.840   0.790   0.820   hit
6    What does the anti-harassment policy co...     0.930   0.900   0.920   hit
7    What is the onboarding process for new ...     0.870   0.830   0.810   hit
8    What are the PTO policy details for unl...     0.890   0.850   0.870   hit
9    What does the EEOC harassment guidance ...     0.810   0.780   0.760   hit
10   What items are on the I-9 audit checkli...     0.860   0.820   0.840   hit
11   How does North Carolina handle workplac...     0.830   0.790   0.770   hit
12   What are the steps for properly classif...     0.900   0.860   0.890   hit
13   What types of leave are available under...     0.870   0.840   0.800   hit
14   What compliance training is required fo...     0.850   0.810   0.780   hit
15   How do state workers comp requirements ...     0.820   0.780   0.750   hit
--------------------------------------------------------------------------------
AVG                                                 0.869   0.832   0.833  15/15
================================================================================

View traces in Langfuse: https://cloud.langfuse.com
Navigate to Traces to see detailed spans and scores for each query.
```

## What to Look For in Langfuse

After running the evaluation, open your Langfuse dashboard:

1. **Traces view** — each test query appears as a trace with timing and scores
2. **Click a trace** — see the spans: embedding → retrieval → generation → scoring
3. **Scores tab** — aggregate scores across all traces, identify weak queries
4. **Filter by score** — find queries where faithfulness < 0.8 (potential hallucination)

## Interpreting the Scores

| Metric | Average | Assessment |
|--------|---------|------------|
| Faithfulness | 0.869 | Good — answers are well-grounded in retrieved context |
| Answer Relevancy | 0.832 | Good — answers address the questions asked |
| Context Precision | 0.833 | Good — relevant chunks are ranked near the top |
| Source Accuracy | 15/15 | All queries found their expected source files |

**Action items for improvement:**
- Queries 9, 11, 15 have lower context precision — consider reranking for these query types
- PDF-sourced queries (9, 5) score slightly lower — check PDF chunking quality
