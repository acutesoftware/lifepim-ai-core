## Tips on Filtering files for RAG LLM's

You only want the latest version of files


## Methods to filter

### Filter excludes in filenames
- exclude %_BACKUP_%' in filenames
- exclude folder backups '%\BACKUP%'

### Explicit Includes of files
- have only files that match be included in the RAG (eg good_documents\* , sus_documents\good_overview.md, public\web_copy.pdf)

### Manual cleanup (last resort)
- ensure duplicates or backup files are consistently named so the above filters exclude them (manual and difficult)

- create a copy of curated documents used only for the RAG (nasty for versioning, but this works well for RAG)