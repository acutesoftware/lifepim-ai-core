## Adaptive Local Retrieval Engine for AI Systems

LifePIM AI Core is a local retrieval engine designed to adapt AI search and RAG systems to existing document corpora. 

It analyses document structure and content to inform chunking, indexing, and retrieval strategies, allowing AI systems to be tuned to the data they operate on rather than requiring documents to be restructured. 

The engine is fully local, inspectable, and intended for developers building custom AI workflows.

## What LifePIM AI Core Does

LifePIM AI Core provides the foundational capabilities required to build adaptive, local AI retrieval systems on top of existing document corpora.

Specifically, the core:

- ### Analyses document structure and content
Inspects files in place to extract descriptive structural and semantic signals that inform retrieval behaviour.

- ### Exposes corpus-level metadata and signals
Builds a local, inspectable view of document characteristics such as size, layout, density, and overlap, enabling informed tuning rather than guesswork.

- ### Implements adaptive chunking strategies
Creates retrieval units based on document structure and content, allowing chunking behaviour to be adjusted to suit different corpora and use cases.

- ### Provides local indexing and retrieval pipelines
Supports local vector stores and retrieval workflows optimised for on-device inference and predictable performance.

- ### Offers tunable retrieval parameters
Exposes configuration points that allow developers to adjust chunking, indexing, and retrieval behaviour without modifying source documents.

- ### Integrates cleanly into other systems
Designed as infrastructure with programmatic interfaces, not as a standalone application or user-facing tool.


All processing is performed locally, with no required external services.
The core’s purpose is to make retrieval behaviour understandable, adaptable, and inspectable, forming a stable foundation for higher-level systems.


## LifePIM AI Core does NOT aim to:

- ### Guarantee answer correctness or factual accuracy
The core provides retrieval mechanisms and signals but does not assert that AI outputs are correct or suitable for decision-making.

- ### Provide compliance, policy, or regulatory enforcement
It does not interpret legal requirements, enforce document policies, or certify compliance outcomes.

- ### Score or judge document quality
While descriptive metadata and structural signals are exposed, the core does not classify documents as “good”, “bad”, compliant, or non-compliant.

- ### Offer benchmarking, evaluation, or regression testing
Measuring retrieval quality, tracking performance over time, and detecting degradation are intentionally out of scope.

- ### Include end-user interfaces or workflow tooling
LifePIM AI Core is infrastructure intended for integration into other systems, not a standalone application.

- ### Replace document management or content governance systems
The engine adapts to existing repositories and does not require documents to be restructured or managed in a specific way.


## How LifePIM Products Fit Together

- ### LifePIM AI Core  
  The shared, local retrieval engine that adapts AI systems to existing document corpora.  
  LifePIM AI Core is fully usable on its own and is not feature-gated or dependent on any commercial product.  
  Open source and licensed under Apache 2.0.  
  https://github.com/acutesoftware/lifepim-ai-core

- ### LifePIM Desktop  
  A local-first personal knowledge management application for individual use.  
  Built on LifePIM AI Core and distributed as free and open source software under the GPL.  
  https://github.com/acutesoftware/lifepim

- ### LifePIM Business  
  A commercial product that builds on LifePIM AI Core by adding evaluation, governance, and operational confidence features for organisational use.  
  These additions are focused on auditability and long-term reliability rather than core retrieval functionality.  
  Available from https://www.lifepim.com/business


Each product is designed to stand on its own, while sharing a common retrieval engine where appropriate.

