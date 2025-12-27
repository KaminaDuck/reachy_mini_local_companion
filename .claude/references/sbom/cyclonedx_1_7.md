---
author: unknown
category: standards
contributors: []
description: CycloneDX 1.7 SBOM standard with enhanced CBOM, citations, and patents
last_updated: '2025-10-21'
related:
- cyclonedx_1_6.md
sources:
- name: CycloneDX.org
  url: https://cyclonedx.org/news/cyclonedx-v1.7-released/
- name: CycloneDX Specification
  url: https://cyclonedx.org/docs/1.7/xml/
status: stable
subcategory: sbom
tags:
- sbom
- security
- supply-chain
- compliance
- cyclonedx
- cbom
- patents
title: CycloneDX 1.7
type: standard-spec
version: '1.7'
---

CycloneDX 1.7 released on October 21, 2025. Core themes: stronger CBOM, formal citations for provenance, first-class patents and patent families, and explicit distribution controls. ([cyclonedx.org][1])

# Scope and release facts

* Release post confirms 1.7 goals and date, plus expected ratification as ECMA-424 2nd Edition in 2025. ([cyclonedx.org][1])
* Spec artifacts for implementation and validation: JSON docs/schema, XML docs/XSD, and Protobuf. ([cyclonedx.org][2])

# 1) Cryptography BOM (CBOM) expansion

What changed

* Canonical lists for **algorithm families** and **elliptic curves** to standardize identification and audits. Release post highlights new lists and their use for PQC-readiness. ([cyclonedx.org][1])
* Protobuf adds **cryptoProperties** on components, with narrative explaining why families vs concrete variants matter; also introduces TLS fields (named groups and signature schemes) for modeling cipher-suite capabilities. ([cyclonedx.org][3])
* CBOM guide details the curated **elliptic-curve catalog** with OIDs, forms, aliases, and sourcing; includes examples. ([cyclonedx.org][4])

Why it matters

* Uniform crypto identification reduces ambiguity across toolchains and supports PQC discovery and migration planning. ([cyclonedx.org][5])

Implementation pointers

* Emit or consume `cryptoProperties` where cryptographic assets or crypto-relevant components are present. Validate against official schemas (JSON/XSD/Proto). ([cyclonedx.org][3])

# 2) Citations and provenance

What changed

* 1.7 introduces **structured citations** to attribute where BOM facts came from and how they were produced, enabling auditable multi-tool pipelines. The release post frames citations as a core 1.7 addition. ([cyclonedx.org][1])
* Provenance use-case guidance explains modeling authorship, suppliers, and distribution path; use **external references** and related fields to ground evidence. ([cyclonedx.org][6])
* Latest JSON/Proto references show the external-reference types and placement; generators should map enrichment steps to explicit references. ([cyclonedx.org][7])

Why it matters

* Downstream verifiers can trace enrichment chains and reconcile facts with evidence sources. ([cyclonedx.org][6])

Implementation pointers

* Prefer specific external reference types where available; fall back to `other` only when needed. Validate with official schemas. ([cyclonedx.org][7])

# 3) Patents and patent families

What changed

* **Patent assertions** are now first-class and can be attached to components, services, or even steps of a formulation process. ([cyclonedx.org][8])
* **Patent families** model global lineage, aligned with WIPO conventions (ST.96 context), enabling linkage to authoritative office records. ([cyclonedx.org][9])

Why it matters

* Enables legal and commercial due-diligence workflows directly from a BOM. ([cyclonedx.org][8])

Implementation pointers

* Capture assignees and legal status in the patent objects; reference public office records via external references for verification. ([cyclonedx.org][9])

# 4) Distribution controls and TLP

What changed

* New **distributionConstraints** object with **TLP classification** at BOM metadata level. XML docs and XSD show `tlp` with default `CLEAR`. ([cyclonedx.org][10])
* SBOM guide explains using distribution constraints to govern sharing and confidentiality. ([cyclonedx.org][11])

Why it matters

* Encodes sharing rules with the artifact so exchanges respect confidentiality boundaries. ([cyclonedx.org][11])

Implementation pointers

* Set `metadata.distributionConstraints.tlp` to `CLEAR`, `GREEN`, `AMBER`, or `RED` per your exchange policy. Validate against 1.7 XSD/JSON schema. ([cyclonedx.org][12])

# 5) Licensing improvements

What changed

* New **license `acknowledgement`** attribute differentiates *declared* vs *concluded* licenses; **observed** licenses live in `evidence.licenses`. XML reference documents the distinctions at length. ([cyclonedx.org][13])

Why it matters

* Separates scanner evidence from legal conclusion to tighten compliance audits. ([cyclonedx.org][13])

Implementation pointers

* Populate `acknowledgement`, keep scanner outputs in `evidence.licenses`, and retain text or expressions per 1.7 license types. ([cyclonedx.org][13])

# 6) AI/ML transparency hooks (carried in 1.7)

What changed

* Protobuf reference formalizes **modelCard** for ML models and a **data** section for data-type components. These fields support risk and bias documentation and dataset transparency. ([cyclonedx.org][3])

Why it matters

* Brings model governance into the same exchange artifact as software and crypto. ([cyclonedx.org][3])

Implementation pointers

* For `type: machine-learning-model`, add `modelCard`; for `type: data`, emit `data` blocks with lineage and constraints. Validate with 1.7 Proto/JSON. ([cyclonedx.org][3])

# 7) Cross-format specs and validation

Primary references for 1.7

* **News/overview**: 1.7 release post. ([cyclonedx.org][1])
* **JSON reference** and **JSON Schema**: `docs/latest/json` and `schema/bom-1.7.schema.json` (linked from the SBOM guide). ([cyclonedx.org][2])
* **XML reference**: `docs/1.7/xml/`. **XSD**: `schema/bom-1.7.xsd`. ([cyclonedx.org][13])
* **Protobuf reference**: `docs/1.7/proto/`. **.proto** schema linked in SBOM guide. ([cyclonedx.org][3])
* **Guides**: SBOM 3rd ed., CBOM 2nd ed., Attestations. ([cyclonedx.org][2])
* **Project/milestone**: 1.7 milestone and spec repo for change discussions and test data. ([GitHub][14])

# Migration checklist (practical)

* Update generators and validators to 1.7 schemas. Confirm your libraries target the 1.7 docs and XSD/JSON/Proto. ([cyclonedx.org][2])
* Start emitting **license.acknowledgement** and keep **observed** licenses under `evidence.licenses`. ([cyclonedx.org][13])
* Add **distributionConstraints.tlp** to govern sharing. ([cyclonedx.org][10])
* For crypto-sensitive components, include **cryptoProperties** and TLS groups/signature schemes where relevant. ([cyclonedx.org][3])
* Use **citations** and provenance external references to attribute enrichment sources. ([cyclonedx.org][1])
* For IP workflows, model **patent assertions** and **patent families**, linking to office records. ([cyclonedx.org][8])

# Direct links (ready for engineers)

* Release note: CycloneDX v1.7. ([cyclonedx.org][1])
* JSON docs/schema: see SBOM guide page 14 for canonical URLs. ([cyclonedx.org][2])
* XML docs: [https://cyclonedx.org/docs/1.7/xml/](https://cyclonedx.org/docs/1.7/xml/) ; XSD: [https://cyclonedx.org/schema/bom-1.7.xsd](https://cyclonedx.org/schema/bom-1.7.xsd) . ([cyclonedx.org][13])
* Protobuf docs: [https://cyclonedx.org/docs/1.7/proto/](https://cyclonedx.org/docs/1.7/proto/) ; .proto: linked in SBOM guide. ([cyclonedx.org][3])
* Guides index: [https://cyclonedx.org/guides/](https://cyclonedx.org/guides/) . ([cyclonedx.org][15])
* CBOM guide: [https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-CBOM-en.pdf](https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-CBOM-en.pdf) . ([cyclonedx.org][4])
* SBOM guide: [https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-SBOM-en.pdf](https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-SBOM-en.pdf) . ([cyclonedx.org][2])
* Patent assertions: [https://cyclonedx.org/use-cases/patent-assertions/](https://cyclonedx.org/use-cases/patent-assertions/) ; Patent families: [https://cyclonedx.org/use-cases/patent-families/](https://cyclonedx.org/use-cases/patent-families/) . ([cyclonedx.org][8])


[1]: https://cyclonedx.org/news/cyclonedx-v1.7-released/ "CycloneDX v1.7 Delivers Advanced Cryptography, Intellectual Property, and Data Provenance Transparency for the Software Supply Chain | CycloneDX"
[2]: https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-SBOM-en.pdf "Authoritative Guide to SBOM"
[3]: https://cyclonedx.org/docs/1.7/proto/ "CycloneDX v1.7 Protobuf Reference"
[4]: https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-CBOM-en.pdf "Authoritative Guide to CBOM"
[5]: https://cyclonedx.org/capabilities/cbom/ "Cryptography Bill of Materials (CBOM)"
[6]: https://cyclonedx.org/use-cases/provenance/ "Security Use Case: Provenance"
[7]: https://cyclonedx.org/docs/latest "CycloneDX v1.7 JSON Reference"
[8]: https://cyclonedx.org/use-cases/patent-assertions/ "Legal and Compliance Use Case: Patent Assertions"
[9]: https://cyclonedx.org/use-cases/patent-families/ "Legal and Compliance Use Case: Global Patent Lineage"
[10]: https://cyclonedx.org/docs/1.7/xml/ "CycloneDX v1.7 XML Reference"
[11]: https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-SBOM-en.pdf "Authoritative Guide to SBOM"
[12]: https://cyclonedx.org/schema/bom-1.7.xsd "https://cyclonedx.org/schema/bom-1.7.xsd"
[13]: https://cyclonedx.org/docs/1.7/xml/ "CycloneDX v1.7 XML Reference"
[14]: https://github.com/CycloneDX/specification/milestone/8 "1.7 · Milestone #8 · CycloneDX/specification"
[15]: https://cyclonedx.org/guides/ "Guides and Resources"