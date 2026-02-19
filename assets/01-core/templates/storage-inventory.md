# Storage Inventory

Use this template to document the current state of a client's file storage (Google Drive, SharePoint, Dropbox, etc.) as found during discovery. The output provides a structured snapshot that feeds into gap analysis and KB file planning.

---

## When to Use

Use this template when you need to document a client's storage structure. This can be done via MCP connector, client-provided screenshots, file/folder exports, or a screen-sharing walkthrough.

---

## Required Inputs

- **Access to the client's storage** — Via MCP connector, screenshots, exported file list, or screen-sharing session.

---

## How to Document

Walk through the client's storage and record:

1. **Top-level folder structure** — List all top-level folders in a tree format. Flag overlapping folders, unclear naming, personal folders, and deprecated folders.
2. **Key folder details** — For folders that contain templates, policies, compliance docs, client files, or anything the knowledge base will draw from, expand into a detailed file listing with tree structure. Skip or summarize folders that are clearly out of scope (marketing, personal, etc.).
3. **Auditor notes** — Add bracketed notes throughout flagging: version confusion, mislabeled files, duplicate content across folders, files that shouldn't exist, and anything that will affect KB planning.
4. **Summary statistics** — Count total folders, files, duplicates, and other metrics that characterize the state of the storage.

### MCP Connector: Complete Traversal

When documenting storage via an MCP connector (Google Drive, SharePoint, etc.), the connector returns paginated results. **You must get the complete picture:**

- **Always follow page tokens.** If a folder listing returns a page token or continuation token, keep requesting the next page until there are no more results. A partial listing will miss files and produce an incomplete inventory.
- **Always drill into subfolders.** After listing a folder's contents, open every subfolder and list its contents too. Continue recursively until you've reached the bottom of the tree. Do not stop at the top level.
- **Do not assume a folder is empty.** If a listing returns no results for a folder you expect to have contents, try again or flag it — the connector may have hit a permissions issue or timeout.
- **Track your progress.** For large storage structures, work through folders systematically (e.g., alphabetically or by the order they appear) so you don't accidentally skip any.

---

## Output Format

Produce a single markdown file:

````
# [Client Name] — Storage Inventory

*Snapshot of the client's file storage taken during content audit. This documents the current state of the client's shared drive or document repository as found during discovery.*

**Source method:** [How this inventory was created — pick one]
- [ ] Direct connection via MCP connector (Google Drive, SharePoint, etc.)
- [ ] Screenshots provided by client
- [ ] File/folder list exported by client
- [ ] Manual walkthrough with client sharing screen

**Date captured:** [YYYY-MM-DD]
**Storage platform:** [Google Drive / SharePoint / Dropbox / etc.]
**Auditor:** [Consultant name]

---

## Top-Level Folder Structure

```
[Client Shared Drive or Root Folder Name]/
├── [Folder Name]/
├── [Folder Name]/
├── [Folder Name]/
└── [Folder Name]/
```

[Auditor notes in brackets. Flag: overlapping folders, unclear naming, personal folders, deprecated folders, anything that stands out.]

---

## [Folder Name]/

```
[Folder Name]/
├── [Subfolder or file]/
│   ├── [file.ext]
│   └── [file.ext]
└── [Subfolder or file]/
```

[Auditor notes: what's here, what condition it's in, any version confusion, mislabeled files, etc.]

---

[Repeat for each folder worth documenting. Not every folder needs full detail — focus on folders that contain templates, policies, compliance docs, client files, and anything the knowledge base will draw from. Skip or summarize folders that are clearly out of scope.]

---

## Summary Statistics

| Metric | Count |
|---|---|
| Total top-level folders | [#] |
| Estimated total files | [#] |
| Duplicate/overlapping folders | [#] |
| Client folders | [#] |
| Files with no date or version indicator | [#] |
| Files last modified before [cutoff year] | [#] |
| Known mislabeled or incorrect files | [#] |
| Personal/individual folders | [#] |

---

## Auditor Notes

[Summary observations: overall organization level, biggest risks, folders that need immediate attention, folders that are well-maintained, anything that will affect knowledge base planning.]
````

---

## Quality Checks

Before delivering the output:

- All top-level folders are accounted for, even if some are just noted as out of scope
- Key folders (templates, compliance, client files) have detailed file listings
- Auditor notes flag specific concerns, not just vague observations
- Summary statistics are reasonable estimates, not guesses
- Deprecated or "do not use" folders are clearly identified
