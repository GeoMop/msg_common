---
name: literature
description: Find, verify, organize, and summarize scholarly literature for a defined topic or research question. Use for literature searches, reading lists, evidence maps, or gap identification. When explicitly asked and a Zotero MCP connection is available, create a Zotero collection or subcollection and add verified records; never fabricate citations or silently write to Zotero.
---

# Literature

Produce a traceable literature set rather than an unverified list of plausible
titles.

## Inputs

- **Topic:** Research question, concept, method, or application area.
- **Optional scope:** Disciplines, years, languages, publication types,
  inclusion/exclusion criteria, desired depth, and known seed papers.
- **Optional Zotero destination:** Request to create a collection or
  subcollection, plus parent collection when relevant. If the destination is
  ambiguous, ask before writing.

## Workflow

1. Translate the topic into concepts, synonyms, exclusions, and search queries.
2. Search suitable scholarly indexes, publisher pages, DOI registries, and
   authoritative repositories. Use current web research where available.
3. Verify every included record against a primary bibliographic source. Capture
   title, authors, year, venue, DOI or stable URL, and publication status.
4. Deduplicate by DOI and normalized bibliographic identity.
5. Screen results against the scope. Distinguish seminal background, recent
   developments, methods, applications, reviews, and contradictory evidence.
6. Read enough of each source to support the stated relevance. Do not infer
   detailed results from titles alone.
7. Summarize search coverage, evidence, limitations, and likely gaps.

## Zotero operation

Only perform Zotero writes when the user asks for them.

1. Detect an available Zotero MCP connection and inspect its supported
   collection and item operations.
2. If unavailable, return the verified bibliography and explain that the
   collection could not be created until a Zotero MCP server is configured.
3. Resolve the destination library and parent collection. Ask when more than one
   plausible destination exists.
4. Reuse existing records when DOI or bibliographic identity matches; do not
   create duplicates.
5. Create the requested collection or subcollection and add verified records.
   Add concise relevance notes or tags only when requested or clearly useful.
6. Report exactly what was created, reused, skipped, or could not be added.

## Boundaries

- Never fabricate a title, author, DOI, quote, result, or access status.
- Label preprints, retractions, corrections, and non-peer-reviewed sources.
- Do not upload copyrighted full text unless the tool and user's access permit
  it; prefer lawful links and metadata.
- A broad search is not a systematic review unless the user requests and the
  workflow documents databases, queries, dates, and screening decisions.

## Output

Return:

1. Scope and search strategy
2. Grouped bibliography with verified links or DOIs
3. Short relevance and evidence notes
4. Synthesis, disagreements, and gaps
5. Search limitations
6. Zotero collection result, when requested
