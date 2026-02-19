# Connector Setup — Builder Project

This document explains how to verify and, if needed, set up a connection between the builder project and the client's cloud storage.

---

## Check First: Is the Connector Already Working?

If the consultant asks for help setting up the connector, or if you need to access the client's files and the connector isn't working, start here.

First, ask the consultant what storage platform the client's files are in (Google Drive, SharePoint, Dropbox, etc.). Then check whether a **native** connector for that platform is available in this conversation. For Google Drive, this means Claude's built-in Google Drive connector — not Zapier or any other third-party integration.

- **If the native connector tools are available:** The connector is already set up — confirm it's working and move on. Skip to "What to Connect" below if the consultant needs guidance on which folders to connect.
- **If the native connector tools are not available:** The connector needs to be set up. Continue to "Setting Up the Connector" below.

---

## Troubleshooting a Failed Connection

If the connector is set up but isn't returning expected files, check:
- Is the connector added to this specific project (not just your account)?
- Is the authenticated account the one with access to the client's files?
- Are the relevant files shared with that account?

---

## Setting Up the Connector

This section only applies if the connector is not yet configured.

### Why a Connector Is Required

This builder project is designed to be lightweight and reusable. Only the builder tools (claude.md, formatting-rules.md, dedup-instructions.md, and this file) are uploaded to the project. The client's raw discovery materials stay in the client's cloud storage.

A connector is how Claude accesses those materials. Without it, there's nothing to process.

### Google Drive

**Always use Claude's native Google Drive connector.** Do not use Zapier, third-party integrations, or any other workaround for Google Drive access. If Zapier-based Google Drive tools exist in the project, ignore them for this purpose.

To add the native connector:

1. Click the **+** button in the chat window
2. Hover over **Connectors**
3. Click **Manage Connectors**
4. Find **Google Drive** in the main list. If you don't see it, click **Browse Connectors** and search for it.
5. Click **Connect**
6. Select the Google account that has access to the client's files and authorize access

Once connected, Claude can search for and read files in the linked Google Drive directly within this project's conversations.

**Note:** Connector access is read-only. Claude can find and read files but cannot create, move, rename, or delete anything in Drive.

### Microsoft 365 (SharePoint, OneDrive)

The Microsoft 365 connector is **only available on Claude Team and Enterprise plans.** It will not appear in the connector directory on Pro or Free plans.

If the consultant has a Team or Enterprise plan:

1. Click the **+** button in the chat window
2. Hover over **Connectors**
3. Click **Manage Connectors**
4. Search for **Microsoft 365** — if it doesn't appear, the plan doesn't support it
5. Click **Connect** and authenticate with the Microsoft account that has access to the client's SharePoint/OneDrive

If the consultant is on a Pro plan and the client uses SharePoint/OneDrive, use the direct upload fallback below.

### Other Storage Platforms

Not all platforms have native connectors. To check:

1. Click the **+** button in the chat window
2. Hover over **Connectors**
3. Click **Manage Connectors**
4. Click **Browse Connectors** and search for the platform name

If the platform isn't listed, use the direct upload fallback below.

### Fallback: Direct Upload

If no connector exists for the client's platform (or the connector requires a higher-tier plan):

1. Have the consultant download the discovery materials from the client's storage
2. Upload them directly to the project conversation or as project knowledge files
3. Prefer markdown, CSV, or plain text formats — Claude cannot read `.xlsx` files natively, so spreadsheets should be exported to CSV or copied into markdown before uploading

This bypasses the connector-based workflow and makes the project harder to maintain, so use it only when a connector isn't available.

---

## What to Connect

Connect the storage locations that contain:

**Required — discovery materials:**
- The folder(s) with interview transcripts, inventories, audits, gap analyses, and question lists

**Recommended — client operational documents:**
- Template and document folders
- Compliance and policy folders
- Any folders referenced in the discovery materials

**Do not connect or use:**
- Folders marked as deprecated in the discovery materials (see dedup-instructions.md, Rule 7)
- Personal folders unrelated to the knowledge base content

---

## How Claude Uses Storage Access

When generating KB files, Claude reads source materials through the connector. Priority order:

1. **Discovery materials** (interview transcripts, audits, inventories, gap analyses) — Primary sources for synthesizing KB content
2. **Client operational documents** (templates, policies, handbooks) — Used to verify details, populate indexes, and fill gaps
3. **Interview context** — Use stakeholder statements to interpret ambiguous document content

### Not Permitted

- Browsing storage without a specific purpose related to KB file generation
- Treating file names as authoritative when the document inventory has different metadata (the inventory was manually audited and is more reliable)

---

## For the Deliverable Project

The client-facing deliverable project (Project B) will also use a connector, but for a different purpose:

- **Builder project (this project):** Connector access is how Claude reads raw materials to generate KB files
- **Deliverable project:** Connector access lets the client's team ask Claude to find and reference specific documents during daily work

The deliverable project's connector setup should be documented separately as part of the deliverables.
