# Competency Questions of PRIMA (v3.0)

The CQs are also mapped to the **5W + 1H** provenance facets (see the coverage table). See
`DOCS/prima-v3-rewrite-brainstorm.md` for the narrative.

## Competency Questions

### PRIMA-Core
1. Which project(s) is the researcher member of?
2. Which study(ies) has the researcher performed?
3. Which data acquisition(s) or data analysis has the researcher performed?
4. Which research data is attributed to (e.g., created by) the researcher?
5. Which data acquisition/analysis was performed in a study and which data were used?
6. Which studies were done by a project, and which data acquisitions and data analyses were done in those studies?

### PRIMA-Data analysis lifecycle
7. Which result(s) (analyzed data) were obtained from a data analysis?
8. Which data processing(s) and data analysis(es) belong to a study?
9. Which data were used and produced in a data analysis / data processing?
10. Which research software was used in a data analysis / data processing?
11. Which researcher(s) performed a data analysis / data processing?

### PRIMA-Dataset
12. Which project/researcher is the research data attributed to?
13. Which research data are contained in the dataset?
14. Where is the research data / dataset / publication data stored?
15. Which metadata describes the research data?
16. Which persistent identifier is assigned to a dataset / publication data?

### PRIMA-Experiment
17. Which processing-and-treatment(s) / measurement(s) were performed in the study?
18. Which equipment / instrument(s) were used in a processing-and-treatment / measurement?
19. Which technique(s) was used in a measurement?
20. **(Where/When)** Where and when was a processing-and-treatment / measurement performed?
21. **(Who)** Which researcher(s) performed a processing-and-treatment / measurement?
22. Which sample(s) was used in a measurement?
23. Which raw data was produced in a measurement?
24. **(How)** Which protocol / technique did a measurement execute?
25. What is the process sequence of a processing-and-treatment (which process precedes which)?
26. Which material(s) is the sample made of?

### PRIMA-Computational
27. Which calculation(s) / simulation(s) were performed, and on which model?
28. Which model(s) resulted from a model preparation, and which research data was used?

---

## 5W + 1H coverage

| Facet | Question | Covered by CQ(s) |
|---|---|---|
| **What** | kind of data/process | 3, 5, 7, 8, 9, 13, 17, 22, 23, 26, 27, 28 |
| **When** | time of process | 20 |
| **Who** | responsible agent | 1, 2, 3, 4, 11, 12, 21 |
| **Where** | location | 14 (storage), 20 (lab) |
| **Why** | scientific context | 2, 6, 8, 17 (study/project) |
| **How** | plan/protocol/technique/software | 10, 19, 24, 25 |

---

# Answers via SPARQL (v3)

Answered in CQ order. Each SPARQL block is self-contained with only the `PREFIX` declarations
it actually uses, so it can be copied and run directly. Where a v2 concept has **no v3 class/property yet**, it is
flagged ⚠ (summarised in the *Gaps* section at the end).

**CQ1 — projects the researcher is a member of**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>

SELECT ?project ?user WHERE {
  ?project a core:Project ; core:hasProjectMember ?user .
  ?user a core:ResearchUser .
}
```

**CQ2 — studies a researcher performed** (was `prov:wasAttributedTo`; now `ro:0002211` has agent)
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?study ?user WHERE {
  ?study a core:Study ; ro:0002211 ?user .
  ?user a core:ResearchUser .
}
```

**CQ3 — data acquisitions / data analyses a researcher performed**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?process ?user WHERE {
  VALUES ?type { core:DataAcquisition core:DataAnalysis }
  ?process a ?type ; ro:0002211 ?user .
  ?user a core:ResearchUser .
}
```

**CQ4 — research data attributed to a researcher** (attribution stays PROV-O)
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov:    <http://www.w3.org/ns/prov#>

SELECT ?data ?user WHERE {
  ?data a core:ResearchData ; prov:wasAttributedTo ?user .
  ?user a core:ResearchUser .
}
```

**CQ5 — data acquisition/analysis in a study and the data it used**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?study ?process ?input WHERE {
  { ?study core:hasDataAcquisition ?process . } UNION { ?study core:hasDataAnalysis ?process . }
  ?process ro:0002233 ?input .
}
```

**CQ6 — studies of a project and their data acquisitions / analyses**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>

SELECT ?project ?study ?acquisition ?analysis WHERE {
  ?project a core:Project ; core:hasStudy ?study .
  OPTIONAL { ?study core:hasDataAcquisition ?acquisition . }
  OPTIONAL { ?study core:hasDataAnalysis ?analysis . }
}
```

**CQ7 — results (analyzed data) obtained from a data analysis**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?analysis ?output WHERE {
  ?analysis a core:DataAnalysis ; ro:0002234 ?output .
}
```

**CQ8 — data processing(s) and data analysis(es) belonging to a study**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal:     <https://purls.helmholtz-metadaten.de/prima/dal#>

SELECT ?study ?process ?processType WHERE {
  VALUES (?relation ?processType) {
    (core:hasDataAnalysis    core:DataAnalysis)
    (dal:hasDataProcessing   dal:DataProcessing)
  }
  ?study a core:Study ; ?relation ?process .
  ?process a ?processType .
}
```

**CQ9 — data used and produced in a data analysis / data processing** (was `pmd:input/output`)
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal:     <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?process ?input ?output WHERE {
  VALUES ?type { core:DataAnalysis dal:DataProcessing }
  ?process a ?type ;
           ro:0002233 ?input ;     # has input
           ro:0002234 ?output .    # has output
}
```

**CQ10 — research software used in a data analysis / data processing**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal:     <https://purls.helmholtz-metadaten.de/prima/dal#>

SELECT ?process ?software WHERE {
  VALUES ?type { core:DataAnalysis dal:DataProcessing }
  ?process a ?type ; core:usesResearchSoftware ?software .
}
```

**CQ11 — researchers who performed a data analysis / data processing**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal:     <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?process ?user WHERE {
  VALUES ?type { core:DataAnalysis dal:DataProcessing }
  ?process a ?type ; ro:0002211 ?user .
  ?user a core:ResearchUser .
}
```

**CQ12 — researcher the research data is attributed to**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov:    <http://www.w3.org/ns/prov#>

SELECT ?data ?user WHERE {
  ?data a core:ResearchData ; prov:wasAttributedTo ?user .
}
```
> ⚠ Project-level attribution is not modelled in v3 (`prov:wasAttributedTo` ranges over
> `core:ResearchUser`). Add a project-attribution link if project-level credit is required.

**CQ13 — research data contained in a dataset**
```sparql
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?dataset ?part WHERE {
  ?dataset a dataset:Dataset ; dcterms:hasPart ?part .
}
```

**CQ14 — where research data / datasets / publication data are stored**
```sparql
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>

SELECT ?item ?store WHERE {
  ?item dataset:isStoredIn ?store .
}
```

**CQ15 — metadata describing the research data**
```sparql
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>

SELECT ?item ?metadata WHERE {
  ?item dataset:hasMetadata ?metadata .
  ?metadata a dataset:Metadata .
}
```

**CQ16 — persistent identifier assigned to a dataset / publication data**
```sparql
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>

SELECT ?item ?pid WHERE {
  ?item dataset:hasPersistentIdentifier ?pid .
  ?pid a dataset:PersistentIdentifier .
}
```

**CQ17 — processing-and-treatments / measurements performed in a study**
```sparql
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?study ?process WHERE {
  { ?study exp:hasMeasurement ?process . }
  UNION
  { ?study exp:hasProcessingAndTreatment ?process . }
}
```

**CQ18 — equipment / instruments used in a processing-and-treatment / measurement**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?process ?equipment WHERE {
  VALUES ?type { exp:Measurement exp:ProcessingAndTreatment }
  ?process a ?type ; core:usesEquipment ?equipment .
}
```

**CQ19 — technique used in a measurement**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?measurement ?technique WHERE {
  ?measurement a exp:Measurement ; core:hasTechnique ?technique .
}
```

**CQ20 — where and when a measurement / processing-and-treatment was performed**
```sparql
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov:    <http://www.w3.org/ns/prov#>

SELECT ?process ?lab ?start ?end WHERE {
  VALUES ?type { exp:Measurement exp:ProcessingAndTreatment }
  ?process a ?type ; prov:atLocation ?lab .
  OPTIONAL { ?process prov:startedAtTime ?start ; prov:endedAtTime ?end . }
}
```
> ⚠ `prov:startedAtTime`/`prov:endedAtTime` are declared in v3 but not yet attached to the process
> classes — wire them onto `exp:Measurement`/`exp:ProcessingAndTreatment` for the **When** facet.

**CQ21 — who performed a measurement / processing-and-treatment**
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?process ?user WHERE {
  VALUES ?type { exp:Measurement exp:ProcessingAndTreatment }
  ?process a ?type ; ro:0002211 ?user .
  ?user a core:ResearchUser .
}
```

**CQ22 — sample used in a measurement**
```sparql
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?measurement ?sample WHERE {
  ?measurement a exp:Measurement ; ro:0002233 ?sample .
  ?sample a exp:Sample .
}
```

**CQ23 — raw data produced in a measurement**
```sparql
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?measurement ?raw WHERE {
  ?measurement a exp:Measurement ; ro:0002234 ?raw .
  ?raw a dataset:RawData .
}
```

**CQ24 — protocol / technique a measurement executes** (Protocol is new in v3)
```sparql
PREFIX core:    <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?measurement ?protocol ?technique WHERE {
  ?measurement a exp:Measurement .
  OPTIONAL { ?measurement core:executesProtocol ?protocol . ?protocol a core:Protocol . }
  OPTIONAL { ?measurement core:hasTechnique ?technique . ?technique a core:Technique . }
}
```

**CQ25 — process sequence of a processing-and-treatment** (was `pmd:nextProcess`; now BFO ordering)
```sparql
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX bfo:     <http://purl.obolibrary.org/obo/BFO_>

SELECT ?earlier ?later WHERE {
  ?later a exp:ProcessingAndTreatment ; bfo:0000062 ?earlier .   # 'preceded by'
}
```

**CQ26 — materials a sample is made of** (v2 `hasSampleComponent` → v3 `exp:hasMaterial`)
```sparql
PREFIX exp:     <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?sample ?material WHERE {
  ?sample a exp:Sample ; exp:hasMaterial ?material .
}
```

**CQ27 — calculations / simulations and their model**
```sparql
PREFIX comp:    <https://purls.helmholtz-metadaten.de/prima/computational#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?run ?model WHERE {
  VALUES ?type { comp:Calculation comp:Simulation }
  ?run a ?type ; ro:0002233 ?model .
  ?model a comp:Model .
}
```

**CQ28 — models resulting from a model preparation, and the research data used**
```sparql
PREFIX comp:    <https://purls.helmholtz-metadaten.de/prima/computational#>
PREFIX ro:      <http://purl.obolibrary.org/obo/RO_>

SELECT ?prep ?model ?input WHERE {
  ?prep a comp:ModelPreparation ; ro:0002234 ?model .
  ?model a comp:Model .
  OPTIONAL { ?prep ro:0002233 ?input . }
}
```

---

## Gaps surfaced (v2 CQ concepts without a v3 class/property yet)

Resolve during the rewrite (reformulate or extend the ontology):

- **DataAnalysisLifecycle aggregator** (v2 CQ5–8, 12): v3 has `core:DataAnalysis` and
  `dal:DataProcessing` but **no `DataAnalysisLifecycle` class** linking them — CQs reformulated
  around the individual processes / `core:Study`.
- **DataInterpretation** (v2 CQ8–12): class removed in v3 — dropped from the CQs.
- **Project-level attribution** (CQ12): `prov:wasAttributedTo` ranges over `core:ResearchUser` only.
- **Data derivation** (v2 "which dataset was the publication data derived from"): v3 has no
  `prov:wasDerivedFrom`; only `dcterms:references` / `dcterms:hasPart`. Consider re-introducing a
  derivation property for the lineage facet.
- **When** (CQ20): `prov:startedAtTime`/`endedAtTime` declared but not attached to processes.
