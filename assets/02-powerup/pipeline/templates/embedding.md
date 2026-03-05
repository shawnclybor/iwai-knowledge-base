# Template: Embedding

**Pipeline Stage:** 4 of 5
**Input:** Chunks with metadata (from chunking router)
**Output:** Chunks with vector embeddings (1536 dimensions)

---

## What This Step Does

Sends each chunk's text content to OpenAI's embedding API and gets back a 1536-dimensional vector that captures the semantic meaning. These vectors are what make similarity search possible.

## Model

- **Model:** `text-embedding-3-small`
- **Dimensions:** 1536
- **Cost:** ~$0.02 per 1M tokens
- **Batch size:** Up to 100 chunks per API call (OpenAI max is 2048)

## Process

### 1. Prepare Batches

Group chunks into batches of 100. For each chunk, the text sent to the API is the `content` field.

### 2. Call OpenAI API

```python
import openai

client = openai.OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=[chunk["content"] for chunk in batch]
)

embeddings = [item.embedding for item in response.data]
```

### 3. Attach Embeddings

Pair each embedding vector back to its chunk. The order of embeddings in the response matches the order of inputs.

### 4. Track Token Usage

Log the `usage.total_tokens` from each API response. This helps estimate costs and catch anomalies (e.g., a chunk with unexpectedly high token count).

## Error Handling

- **Rate limit (429):** Back off exponentially. Start at 1 second, double each retry, max 5 retries.
- **Token limit exceeded:** A single chunk shouldn't hit this with ~600 token max, but if it does, split the chunk and re-embed.
- **API error (500+):** Retry up to 3 times. If persistent, mark the file as `failed` in `file_metadata`.

## Environment

Requires `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY=sk-...
```

## Verification

After this step, check:
- [ ] Every chunk has a 1536-dimensional embedding
- [ ] No null embeddings
- [ ] Token usage is reasonable (~600 tokens per chunk × number of chunks)
- [ ] API costs are as expected
