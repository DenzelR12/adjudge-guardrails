# Customer Data Governance

Every analytics request must carry an authenticated tenant context. Tenant filtering is mandatory at the query-policy and database layers. Generated SQL must be parameterized, read-only, restricted to an approved semantic catalog, bounded by time/row/scan limits, and recorded with a query audit event. RAG retrieval must filter by tenant metadata before similarity ranking. Exports require a separate approval policy and data-classification check.
