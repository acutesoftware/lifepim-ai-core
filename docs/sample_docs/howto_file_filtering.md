## Tips on Filtering files for RAG LLM's

You only want the latest version of files - this is tricky to achieve in practice, but one method is to have an additional step after initial vector search for large results TOP_K = 800, then rerank based on file modified date with higher score for recent files (and add any other business rules here). Then pass the TOP 5 back to the RAG which should give better results.


## Methods to filter

### Filter excludes in filenames
- exclude %_BACKUP_%' in filenames
- exclude folder backups '%\BACKUP%'

### Explicit Includes of files
- have only files that match be included in the RAG (eg good_documents\* , sus_documents\good_overview.md, public\web_copy.pdf)

### Manual cleanup (last resort)
- ensure duplicates or backup files are consistently named so the above filters exclude them (manual and difficult)

- create a copy of curated documents used only for the RAG (nasty for versioning, but this works well for RAG)

