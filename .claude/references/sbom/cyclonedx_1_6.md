---
author: unknown
category: standards
contributors: []
description: CycloneDX 1.6 SBOM standard with CBOM and attestations support
last_updated: '2024-06-01'
related:
- cyclonedx_1_7.md
sources:
- name: CycloneDX.org
  url: https://cyclonedx.org/news/cyclonedx-v1.6-released/
- name: ECMA-424 Standard
  url: https://ecma-international.org/publications-and-standards/standards/ecma-424/
status: stable
subcategory: sbom
tags:
- sbom
- security
- supply-chain
- compliance
- cyclonedx
- cbom
- attestations
title: CycloneDX 1.6
type: standard-spec
version: '1.6'
---

CycloneDX 1.6 released 9 Apr 2024. Focus: CBOM, Attestations, and AI/ML transparency upgrades. Ratified as ECMA-424 1st edition in June 2024. ([CycloneDX][1])

# Scope and release facts

* Official announcement and date. ([CycloneDX][1])
* Standardization: ECMA-424, 1st ed. June 2024, with downloadable spec. ([ecma-international.org][2])
* Docs and schemas for 1.6: XML reference and XSD; JSON reference; repo notes show 1.6 basis and additions. ([CycloneDX][3])

# What’s new in 1.6

## A) Cryptographic Bill of Materials (CBOM)

* Purpose: inventory crypto assets to enable weak-algorithm discovery and PQC migration planning (NIST, CNSA 2.0 context). ([CycloneDX][1])
* Modeling: `cryptoProperties` describes families vs specific variants for accurate risk reasoning. ([CycloneDX][3])
* Outcome: supports audits and policy compliance for crypto agility. ([CycloneDX][1])

## B) CycloneDX Attestations (CDXA)

* Capability: represent standards, requirements, claims, evidence, and signatures as machine-readable “compliance as code.” ([CycloneDX][1])
* Launch context: prefilled mappings for OWASP SCVS/ASVS/MASVS and NIST SSDF; extensible to internal policies. ([owasp.org][4])
* Core structures appear in the 1.6 XML reference under requirements, targets, affirmation, signatories, and external references. ([CycloneDX][3])

## C) AI/ML transparency upgrades

* `modelCard` for `machine-learning-model` and `data` for `data` components are first-class; 1.6 adds environmental considerations (energy/CO₂) spanning training through inference. ([CycloneDX][3])

# Deep-link reference map (implementation targets)

**Standards and overview**

* 1.6 release post. ([CycloneDX][1])
* ECMA-424 page and PDF (1st ed., June 2024). ([ecma-international.org][2])
* Spec overview page (capabilities across software, hardware, services, ML). ([CycloneDX][5])

**Specs and schemas**

* XML reference for 1.6. ([CycloneDX][3])
* XSD: `bom-1.6.xsd`. ([CycloneDX][6])
* JSON reference (1.6). ([CycloneDX][7])
* Specification repo notes and “JSON Schema is reference implementation.” ([GitHub][8])

**Capabilities and guides**

* CBOM purpose in 1.6 announcement. ([CycloneDX][1])
* Attestations overview. ([CycloneDX][9])
* BOM-Link for cross-BOM traceability. ([CycloneDX][10])

**Ecosystem and commentary**

* FOSSA “What’s new” summary and schema scale note. ([FOSSA][11])
* Third-party write-ups on 1.6’s supply-chain impact. ([ReversingLabs][12])

# Field-level anchors (where to look in the spec)

* **Crypto**: `cryptoProperties` under components/crypto assets. Use family vs variant to express security level differences (e.g., AES vs AES-128-GCM; SHA-1 vs HMAC-SHA1). ([CycloneDX][3])
* **Attestations**: `requirements` trees with identifiers, titles, text, descriptions, CRE links; `targets` over components/services; `affirmation` with `statement` and `signatories`. ([CycloneDX][3])
* **ML**: `modelCard` content and `data` section applicability rules. ([CycloneDX][3])

# Migration checklist for teams moving to 1.6

1. **Update validators and generators** to 1.6 JSON Schema/XSD; if your validator inlines subschemas, account for SPDX and signature refs as downstreams like GitLab did. ([CycloneDX][6])
2. **Emit CBOM** where crypto appears: record algorithm family and concrete variant; ensure coverage of keys, certs, protocols if modeled. ([CycloneDX][1])
3. **Adopt CDXA** for audits: define standards, map requirements, attach evidence, and sign. Prefer BOM-Link if evidence is large or split across BOMs. ([CycloneDX][9])
4. **Add ML transparency**: include `modelCard`; attach environmental metrics if available. ([CycloneDX][1])
5. **Declare media types** or schema URLs for explicit versioning in pipelines. ([GitHub][8])

# Quick start links for engineers

* **Announcement**: CycloneDX v1.6 released. ([CycloneDX][1])
* **Standard**: ECMA-424 1st edition (CycloneDX v1.6). ([ecma-international.org][2])
* **XML ref**: 1.6 XML docs. **XSD**: `bom-1.6.xsd`. ([CycloneDX][3])
* **JSON ref**: 1.6 JSON docs. ([CycloneDX][7])
* **Attestations guide**: CDXA. ([CycloneDX][9])
* **BOM-Link**: cross-BOM linkage. ([CycloneDX][10])
* **Tooling**: sbom-utility validator supports specVersion `1.6`. ([GitHub][13])


[1]: https://cyclonedx.org/news/cyclonedx-v1.6-released/ "CycloneDX v1.6 Released, Advances Software Supply Chain Security with Cryptographic Bill of Materials and Attestations | CycloneDX"
[2]: https://ecma-international.org/publications-and-standards/standards/ecma-424/ "ECMA-424"
[3]: https://cyclonedx.org/docs/1.6/xml/ "CycloneDX v1.6 XML Reference"
[4]: https://owasp.org/blog/2023/12/06/CycloneDX-attestations "CycloneDX v1.6 Introduces Support for Attestations of ..."
[5]: https://cyclonedx.org/specification/overview/ "Specification Overview"
[6]: https://cyclonedx.org/schema/bom-1.6.xsd "https://cyclonedx.org/schema/bom-1.6.xsd"
[7]: https://cyclonedx.org/docs/1.6/json/ "CycloneDX 1.6 JSON Reference"
[8]: https://github.com/CycloneDX/specification "CycloneDX/specification"
[9]: https://cyclonedx.org/capabilities/attestations/ "CycloneDX Attestations (CDXA)"
[10]: https://cyclonedx.org/capabilities/bomlink/ "BOM-Link"
[11]: https://fossa.com/blog/whats-new-cyclonedx-1-6/ "What's New in CycloneDX 1.6? | FOSSA Blog"
[12]: https://www.reversinglabs.com/blog/cyclonedx-16-upgraded-for-the-evolving-software-supply-chain-security-era "OWASP looks to future-proof software bills of materials with ..."
[13]: https://github.com/CycloneDX/sbom-utility "CycloneDX/sbom-utility"