# Deduplication & Conflict Resolution Instructions

This document tells you how to handle conflicting, duplicate, or overlapping content when generating KB files from raw discovery materials.

---

## When Dedup Applies

You'll encounter conflicts in three situations:

1. **Multiple versions of the same document** — The file inventory may show several folders containing overlapping templates or policies with different names, dates, or locations
2. **Contradictory information across sources** — An interview statement might conflict with what a document shows
3. **Overlapping content across KB files** — The same topic might be relevant to more than one workflow

---

## Rule 1: KUAD Tags Are Authoritative

If a document inventory with KUAD tags (Keep / Update / Archive / Delete) is included in the raw files, those tags are the source of truth for document status:

- **Keep** — This is the canonical current version. Use its content directly.
- **Update** — Content is valuable but needs revision. Use the content but flag specific items that need updating with `[NEEDS UPDATE — reason]`.
- **Archive** — Superseded by a newer version. Do not use this content. Reference the "Keep" version instead.
- **Delete** — Duplicate, erroneous, or obsolete. Ignore completely. Do not reference in any KB file.

If you encounter a document in the raw files that doesn't appear in the inventory, flag it: `[NOT IN INVENTORY — status unknown, requires audit]`.

If no KUAD-tagged inventory exists, proceed to Rules 2–3 to resolve conflicts.

---

## Rule 2: Recency Wins (With Exceptions)

When two sources provide different information on the same topic and no KUAD tag resolves it:

1. **Check dates.** The more recent source is generally more reliable for compliance information, regulations, and process descriptions.
2. **Exception: Interviews trump outdated documents.** If a stakeholder described a current practice in the interview that contradicts an older document, use the interview version — it reflects how things actually work today.
3. **Exception: Regulatory changes.** If a document contains a region-specific rule and you know from context that the rule may have changed, flag it: `[VERIFY — regulation may have changed since source was last updated on DATE]`.

---

## Rule 3: Specificity Wins Over Generality

When a general document and a specific document both address the same topic:

- A **region-specific** version takes priority over a generic version for that region
- An **industry-specific** version takes priority over a generic version for that industry
- A **role-specific** version takes priority over a generic version for that role

When generating KB files, note which version you chose and why:
```
Using region-specific handbook template (KUAD: Keep) over generic version (KUAD: Archive). [Dedup: specificity]
```

---

## Rule 4: Single Source of Truth Per Topic

Each piece of information should live in exactly one KB file. When the same topic is relevant to multiple workflows:

1. **Decide the primary home.** Put the detailed content in the KB file where it's most relevant.
2. **Cross-reference from other files.** Other KB files that touch the same topic should point to the primary file rather than duplicating the content.

After completing the source assessment (see `instructions.md`, Step 3), create a primary home assignment table mapping topics to their primary KB file. This prevents duplication across the deliverables.

---

## Rule 5: Flag Rather Than Guess

When you encounter a genuine conflict that the rules above don't resolve:

- Do not pick a side silently
- Do not average or blend the conflicting information
- Instead, present both versions and flag it for human resolution:

```
[CONFLICT — Source A (content-audit.md) says this was last updated April 2023.
Source B (stakeholder-interview-transcript-2025-01-13.txt — Name) says it was updated in January 2024.
Recommend: Verify with stakeholder which date is accurate.]
```

---

## Rule 6: Mislabeled Files

Content audits frequently surface mislabeled files — documents whose filenames don't match their actual contents. When you encounter information from a mislabeled file:

- Use the **correct** description of what the file actually contains, not what the filename says
- Note the mislabel so it can be corrected: `[NOTE: File "filename.ext" is actually [correct description], not what the filename suggests]`

Check the storage inventory and content audit notes for any mislabeled files identified during the audit. If additional mislabels are discovered during KB generation, flag them the same way.

---

## Rule 7: Deprecated Folders and Files

If the raw materials identify folders or files that are explicitly deprecated (marked "do not use," "old," "archived," etc.):

- **Never reference content from deprecated sources** in any KB file
- If a topic is only documented in a deprecated source and nowhere else, treat it as a content gap: `[CONTENT GAP — only version found in deprecated source. Requires new content creation.]`
- In any index or catalog KB file, include a note warning that the deprecated source exists and should not be used
