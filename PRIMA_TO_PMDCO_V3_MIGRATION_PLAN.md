# PRIMA to PMDco v3 Migration Recommendations

## Executive Summary

This document provides detailed recommendations for migrating PRIMA ontology modules (core, experiment, dataset, computational, data-analysis-lifecycle) from PMDco v2 (PROV-O based) to PMDco v3 (BFO/IAO/RO based). The migration requires systematic replacement of PROV-O classes and properties with BFO-aligned equivalents while maintaining semantic consistency.

## 1. Understanding PMDco v3 Architecture

### 1.1 Foundational Ontologies

- **BFO (Basic Formal Ontology)**: Top-level ontology providing continuants (material entities, immaterial entities) and occurrents (processes)
- **IAO (Information Artifact Ontology)**: For information content entities (data, documents, specifications)
- **RO (Relation Ontology)**: Standardized relationships between entities
- **OBI (Ontology for Biomedical Investigations)**: For organizational structures

### 1.2 PMDco v3 Core Classes

From the PMDco v3 RDF/XML structure:

- **Note**: PMDco v3 does NOT have `pmdco:Process` - use `BFO:process` (BFO_0000015) directly
- `BFO:process` (BFO_0000015) → subclass of `BFO:occurrent` (BFO_0000003)
- `BFO:Object` (BFO_0000030) → subclass of `BFO:material entity` (BFO_0000040)
- `pmdco:Device` → subclass of `BFO:Object` (BFO_0000030)
- **Note**: PMDco v3 does NOT have `pmdco:DigitalEntity` - use `IAO:information content entity` directly
- `pmdco:ValueObject` → subclass of `BFO:quality` or `IAO:information content entity`

**Note**: PMDco v3 uses `BFO:Object` directly, not a PMDco-specific Object class.

## 2. Class Migration Strategy

### 2.1 Process Classes (pmdco:Process → BFO:process)

**Current PRIMA Classes Using pmdco:Process:**

**Core Module:**
- `DataAcquisition` → `pmdco:Process` (which is `prov:Activity` in v2)
- `DataAnalysisLifecycle` → `pmdco:Process`

**Experiment Module:**
- `DataAcquisition` → `pmdco:Process`
- `ProcessingAndTreatment` → `pmdco:Process`
- `Measurement` → `ProcessingAndTreatment` → `pmdco:Process`
- `Fabrication` → `ProcessingAndTreatment` → `pmdco:Process`
- `SamplePreparation` → `ProcessingAndTreatment` → `pmdco:Process`

**Dataset Module:**
- `DataCuration` → `pmdco:Process`

**Data Analysis Lifecycle Module:**
- `DataProcessing` → `pmdco:Process`
- `DataAnalysis` → `pmdco:Process`
- `DataInterpretation` → `pmdco:Process`
- `ModelPreparation` → `pmdco:Process`

**Computational Module:**
- `Calculation` → `DataAcquisition` → `pmdco:Process`
- `Simulation` → `DataAcquisition` → `pmdco:Process`
- `ModelPreparation` → `pmdco:Process`

**Migration Action:**

- **PMDco v3 has NO `pmdco:Process`** - all process classes should be directly subclass of `BFO:process` (BFO_0000015)
- `BFO:process` (BFO_0000015) is a subclass of `BFO:occurrent` (BFO_0000003)
- **All PRIMA process classes** → subclass of `BFO:process` (BFO_0000015) directly
- **Remove** `pmdco:Process` dependency entirely
- **Remove** `prov:Activity` dependency (was used in PMDco v2)
- **Maintain** PRIMA internal hierarchy (e.g., `Measurement` → `ProcessingAndTreatment` → `BFO:process`)

### 2.2 Agent Classes (prov:Agent → BFO/IAO alignment)

**Current PRIMA Classes:**

- `ResearchUser` (subclass of `prov:Agent`)
- `Equipment` (subclass of `prov:Agent` - **INCORRECT in BFO**)
- `ResearchSoftware` (subclass of `prov:SoftwareAgent`)
- `AcquisitionSoftware` (subclass of `prov:SoftwareAgent`)
- `Institution` (subclass of `prov:Organization` → `prov:Agent`)

**Migration Actions:**

#### 2.2.1 Human Agents

- `ResearchUser` → subclass of `NCBITaxon:9606` (Homo sapiens) → `BFO:material entity`
- **Alternative**: Use `OBI:human` if available in PMDco v3 imports
- **Keep** `AgentRole` hierarchy but ensure it aligns with BFO role/disposition concepts

#### 2.2.2 Software Agents

- `ResearchSoftware` → subclass of `IAO:software` or `IAO:information content entity`
- `AcquisitionSoftware` → subclass of `IAO:software` or `IAO:information content entity`
- **Remove** `prov:SoftwareAgent` dependency entirely

#### 2.2.3 Equipment (CRITICAL CHANGE)

**PMDco v3 Hierarchy:**
- `BFO:material entity` (BFO_0000040) → `BFO:Object` (BFO_0000030) → `pmdco:Device`

**PRIMA Current Hierarchy:**
- `Equipment` → `prov:Agent` ❌
  - `Instrument` → `Equipment`
  - `SampleCarrier` → `Equipment`
  - `SampleHolder` → `Equipment`

**PRIMA Equipment Definition:**
"Any kind of physical or virtual item, device, machine or other tool located in a Laboratory hosted by an Institution, which can be physically, virtually, and/or remotely accessed to perform any of the processes during the course of a Study, by applying a Technique."

**Migration Actions:**
- `Equipment` → subclass of `BFO:Object` (BFO_0000030) (NOT `prov:Agent`)
  - Equipment is a general category of physical objects
  - Equipment encompasses devices, machines, and tools
  - `BFO:Object` represents discrete, identifiable physical entities
  - Hierarchy: `Equipment` → `BFO:Object` (BFO_0000030) → `BFO:material entity` (BFO_0000040)
- `Instrument` → subclass of `prima:Equipment` AND subclass of `pmdco:Device` (multiple inheritance)
  - Maintains PRIMA hierarchy: "Instrument is a particular type of Equipment"
  - Instruments are specialized devices, so also subclass of `pmdco:Device`
  - Hierarchy: `Instrument` → `prima:Equipment` → `BFO:Object` (BFO_0000030) AND `Instrument` → `pmdco:Device` → `BFO:Object` (BFO_0000030)
- `SampleCarrier`, `SampleHolder` → keep as subclass of `prima:Equipment` → `BFO:Object`
  - Both are explicitly defined as "Piece of Equipment" in PRIMA
  - They are physical objects (containers/holders)
  - Maintains PRIMA hierarchy: `SampleCarrier`/`SampleHolder` → `prima:Equipment` → `BFO:Object` (BFO_0000030)

**Rationale**: 
- Equipment is a physical object (material entity), not an agent
- In BFO, agents are entities that can act (humans, organizations), not tools
- `prima:Equipment` matches `pmdco:Device` semantically
- PRIMA's Equipment hierarchy (Instrument, SampleCarrier, SampleHolder) should be preserved
- See `PMDCO_V3_DEVICE_OBJECT_STRUCTURE.md` for detailed hierarchy

#### 2.2.4 Organizations

- `Institution` → subclass of `OBI:organization` → `BFO:material entity`
- **Alternative**: Use appropriate BFO-aligned organization class from PMDco v3

### 2.3 Entity Classes (prov:Entity → BFO/IAO alignment)

**Current PRIMA Classes:**

- `System`, `Material`, `Sample`, `Model` (subclass of `prov:Entity` or `pmdco:Object`)
- `ResearchData`, `Dataset`, `Metadata`, `PublicationData` (subclass of `pmdco:DigitalEntity` in v2, but v3 has NO DigitalEntity)
- `Project`, `Study`, `ScientificPublication` (subclass of `prov:Entity`)
- `Settings`, `Technique`, `Specification` (subclass of `prov:Entity`)

**Migration Actions:**

#### 2.3.1 Physical Objects

- `System` → already subclass of `BFO:Object` (BFO_0000030) → verify it's `BFO:material entity` (BFO_0000040) in v3
- `Material` → subclass of `BFO:material entity` (via `BFO:Object` (BFO_0000030))
- `Sample` → subclass of `BFO:material entity` (via `BFO:Object` (BFO_0000030))
- `Consumable` → subclass of `BFO:material entity` (via `BFO:Object` (BFO_0000030))
- `Precursor`, `Input`, `SampleComponent` → subclass of `BFO:material entity`

#### 2.3.2 Digital/Information Entities

**Current PRIMA Hierarchy (from dataset module):**
- `ResearchData` → subclass of `pmdco:DigitalEntity` (PMDco v2)
  - `RawData` → `ResearchData`
  - `ProcessedData` → `ResearchData`
  - `AnalyzedData` → `ResearchData`
  - `ReferenceData` → `ResearchData`
- `Dataset` → subclass of `prov:Collection` AND `pmdco:DigitalEntity`
- `Metadata` → subclass of `pmdco:DigitalEntity`
- `PublicationData` → subclass of `pmdco:DigitalEntity`

**Migration Actions (PMDco v3 has NO `pmdco:DigitalEntity`):**
- `ResearchData` → subclass of `IAO:information content entity` (NOT via `pmdco:DigitalEntity`)
- `RawData`, `ProcessedData`, `AnalyzedData`, `ReferenceData` → `ResearchData` → `IAO:information content entity`
- `Dataset` → subclass of `IAO:information content entity` (remove `prov:Collection`, remove `pmdco:DigitalEntity`)
  - Use `RO:has_part` / `RO:part_of` for member relationships (replacing `prov:hadMember`)
- `Metadata` → subclass of `IAO:information content entity` (NOT via `pmdco:DigitalEntity`)
- `PublicationData` → subclass of `IAO:information content entity` (NOT via `pmdco:DigitalEntity`)

#### 2.3.3 Specifications and Settings

- `Settings` → subclass of `IAO:specification` or `IAO:information content entity`
- `Technique` → subclass of `IAO:specification` or `IAO:information content entity`
- **Note**: `Specification` from NFDI ontology already subclasses `prov:Entity` - needs migration

#### 2.3.4 Collections and Aggregates

- `Dataset` (as collection) → use `IAO:information content entity` with `RO:has_part` relationships
- **Remove** `prov:Collection` dependency
- Use `RO:has_part` / `RO:part_of` for member relationships

#### 2.3.5 Abstract Entities

- `Project` → Consider if this should be `IAO:information content entity` (plan/proposal) or `BFO:material entity` (if it represents an organization)
- `Study` → `IAO:information content entity` (research plan/design)
- `ScientificPublication` → `IAO:document` or `IAO:information content entity`
- `Conclusion` → `IAO:information content entity`
- `AgentRole` → `BFO:role` or `BFO:disposition`

### 2.4 Location Classes

- `Laboratory` → subclass of `BFO:site` or appropriate BFO spatial region
- **Remove** `prov:Location` dependency

## 3. Relationship/Property Migration Strategy

### 3.1 Process Relationships

**Current PROV-O Properties → BFO/RO Replacements:**

| PROV-O Property | PMDco v3 / BFO / RO Replacement | Usage Context |
|----------------|--------------------------------|---------------|
| `prov:wasInformedBy` | `RO:preceded_by` or `pmdco:previousProcess` | Temporal sequence between processes |
| `prov:wasGeneratedBy` | `RO:output_of` (inverse of `pmdco:output`) | Entity generated by process |
| `prov:used` | `RO:input_of` (inverse of `pmdco:input`) | Entity used in process |
| `prov:wasDerivedFrom` | `RO:derives_from` or `IAO:is_about` | Data derivation relationships |
| `prov:wasAssociatedWith` | `RO:has_participant` or custom property | Agent participation in process |
| `prov:wasAttributedTo` | `RO:bearer_of` or custom attribution | Entity attribution to agent |
| `prov:atLocation` | `RO:located_in` or `BFO:site_of` | Spatial location |

**Migration Actions:**

#### 3.1.1 Process Temporal Ordering

- Replace `prov:wasInformedBy` with `pmdco:previousProcess` / `pmdco:nextProcess` (already in use)
- For general temporal precedence: use `RO:preceded_by`

#### 3.1.2 Process Input/Output

- **Keep** `pmdco:input` and `pmdco:output` (already BFO-aligned)
- Replace `prov:wasGeneratedBy` with inverse of `pmdco:output` where appropriate
- Replace `prov:used` with `pmdco:input` or `RO:input_of`

#### 3.1.3 Agent Participation

- `prov:wasAssociatedWith` → Replace with:
  - `RO:has_participant` for agent participation in processes
  - Or create domain-specific properties like `hasResearchUser`, `performedBy`
- **Current usage**: `DataAcquisition wasAssociatedWith ResearchUser`
- **Migration**: `DataAcquisition RO:has_participant ResearchUser` OR keep custom property `hasResearchUser`

#### 3.1.4 Attribution

- `prov:wasAttributedTo` → Replace with:
  - `RO:bearer_of` for qualities/roles
  - Custom property `attributedTo` or `createdBy` for authorship
- **Current usage**: `ResearchData wasAttributedTo ResearchUser`
- **Migration**: Use custom property `createdBy` or `RO:bearer_of` if appropriate

#### 3.1.5 Derivation

- `prov:wasDerivedFrom` → Replace with:
  - `RO:derives_from` for data lineage
  - `IAO:is_about` for information about relationships
- **Current usage**: `ProcessedData wasDerivedFrom RawData`
- **Migration**: `ProcessedData RO:derives_from RawData`

#### 3.1.6 Location

- `prov:atLocation` → Replace with:
  - `RO:located_in` for spatial containment
  - `BFO:site_of` for site relationships
- **Current usage**: `Equipment atLocation Laboratory`
- **Migration**: `Equipment RO:located_in Laboratory`

### 3.2 Collection Relationships

- `prov:hadMember` → Replace with `RO:has_part` / `RO:part_of`
- **Current usage**: `Dataset hadMember ResearchData`
- **Migration**: `Dataset RO:has_part ResearchData`

### 3.3 Temporal Properties

- `prov:startedAtTime` → Keep as datatype property (not PROV-O specific)
- `prov:endedAtTime` → Keep as datatype property (not PROV-O specific)
- **Alternative**: Use `RO:has_beginning` / `RO:has_end` with temporal entities

## 4. Specific PRIMA Module Migrations

### 4.1 PRIMA Core Module

**Classes to Migrate:**

- `ResearchUser`: `prov:Agent` → `NCBITaxon:9606` or `OBI:human`
- `Equipment`: `prov:Agent` → `BFO:Object` (BFO_0000030) (**CRITICAL**)
- `Instrument`: `prov:Agent` (via Equipment) → `prima:Equipment` → `BFO:Object` (BFO_0000030) AND `pmdco:Device` (**CRITICAL** - multiple inheritance)
- `ResearchSoftware`: `prov:SoftwareAgent` → `IAO:software`
- `Project`: `prov:Entity` → `IAO:information content entity` or `BFO:material entity`
- `Study`: `prov:Entity` → `IAO:information content entity`
- `System`: Already `pmdco:Object` → verify BFO alignment
- `ResearchData`: `pmdco:DigitalEntity` (v2) → `IAO:information content entity` (v3) (**CRITICAL** - no DigitalEntity in v3)
- `Settings`: `Specification` → `IAO:specification`
- `Technique`: `Specification` → `IAO:specification`

**Properties to Migrate:**

- `wasAssociatedWith` → `RO:has_participant` or custom property
- `wasAttributedTo` → custom property or `RO:bearer_of`
- `performsAgentRole` → `RO:bearer_of` (role bearer relationship)

### 4.2 PRIMA Experiment Module

**Classes to Migrate:**

- `Measurement`: Already `DataAcquisition` → verify process alignment
- `Fabrication`, `ProcessingAndTreatment`, `SamplePreparation`: Verify process alignment
- `Sample`, `Material`, `Precursor`, `Input`: Verify material entity alignment
- `Consumable`: Verify material entity alignment
- `AcquisitionSoftware`: `prov:SoftwareAgent` → `IAO:software`
- `Laboratory`: `prov:Location` → `BFO:site` or spatial region
- `Institution`: `prov:Organization` → `OBI:organization`

**Properties to Migrate:**

- `atLocation` → `RO:located_in`
- `wasGeneratedBy` → inverse of `pmdco:output`
- `wasDerivedFrom` → `RO:derives_from`
- `uses` (for consumables) → `RO:has_participant` or keep as custom

### 4.3 PRIMA Dataset Module

**Classes to Migrate:**

- `Dataset`: `prov:Collection` + `pmdco:DigitalEntity` (v2) → `IAO:information content entity` (v3)
  - Remove `prov:Collection` dependency
  - Remove `pmdco:DigitalEntity` (doesn't exist in v3)
  - Use `RO:has_part` for member relationships
- `Metadata`: `pmdco:DigitalEntity` (v2) → `IAO:information content entity` (v3)
- `PublicationData`: `pmdco:DigitalEntity` (v2) → `IAO:information content entity` (v3)
- `PersistentIdentifier`: `prov:Entity` → `IAO:information content entity` or `IAO:identifier`
- All data types (RawData, ProcessedData, AnalyzedData, ReferenceData): `ResearchData` → `IAO:information content entity`

**Properties to Migrate:**

- `hadMember` → `RO:has_part`
- `wasDerivedFrom` → `RO:derives_from`
- `wasGeneratedBy` → inverse of `pmdco:output`

### 4.4 PRIMA Computational Module

**Classes to Migrate:**

- `Calculation`, `Simulation`: Already `DataAcquisition` → verify process alignment
- `Model`: Already `System` → verify material entity or information entity alignment
- `ModelPreparation`: Verify process alignment

**Properties to Migrate:**

- Same as other process modules

### 4.5 PRIMA Data Analysis Lifecycle Module

**Classes to Migrate:**

- `DataProcessing`, `DataAnalysis`, `DataInterpretation`: Verify process alignment
- `Conclusion`: `prov:Entity` → `IAO:information content entity`

**Properties to Migrate:**

- Same process relationship migrations

## 5. ODK Repository Setup

### 5.1 Repository Structure

Following PMDco User Guide recommendations:

```
prima-ontology/
├── src/
│   └── ontology/
│       ├── prima-edit.owl          # Editable ontology
│       ├── prima-imports/          # Imported ontologies
│       └── prima.Makefile          # ODK configuration
├── .github/
│   └── workflows/                  # CI/CD for validation
└── README.md
```

### 5.2 ODK Configuration (prima.yaml)

```yaml
id: prima
title: PRIMA Ontology
namespace: https://purls.helmholtz-metadaten.de/prima/
github_org: Materials-Data-Science-and-Informatics
repo: prima-ontology
```

**Import Strategy:**

- Import PMDco v3 as base ontology
- Import BFO, IAO, RO, OBI as dependencies
- Remove PROV-O imports

### 5.3 Module Organization

Consider maintaining modular structure:

- `prima-core-edit.owl`
- `prima-experiment-edit.owl`
- `prima-dataset-edit.owl`
- `prima-computational-edit.owl`
- `prima-dal-edit.owl`

Or single unified ontology with clear module annotations.

## 6. Migration Checklist

### Phase 1: Preparation

- [ ] Set up ODK repository structure
- [ ] Import PMDco v3.0.0 as base
- [ ] Import BFO, IAO, RO, OBI
- [ ] Remove PROV-O imports
- [ ] Create migration tracking document

### Phase 2: Class Migration

- [ ] Migrate all `pmdco:Process` subclasses to `BFO:process` (BFO_0000015) (**CRITICAL** - no pmdco:Process in v3)
- [ ] Remove `pmdco:Process` class definitions from all modules
- [ ] Remove `prov:Activity` dependencies
- [ ] Migrate `ResearchUser` to BFO material entity (human)
- [ ] Migrate `Equipment` from `prov:Agent` to `BFO:Object` (BFO_0000030) (**PRIORITY**)
- [ ] Keep `Instrument` as subclass of `Equipment` → `BFO:Object` (BFO_0000030) (**PRIORITY** - maintains PRIMA hierarchy)
- [ ] Add `Instrument` as subclass of `pmdco:Device` (multiple inheritance - Instruments are specialized devices)
- [ ] Keep `SampleCarrier` and `SampleHolder` as subclasses of `Equipment` → `BFO:Object` (BFO_0000030)
- [ ] Migrate software classes to `IAO:software`
- [ ] Migrate organization classes to `OBI:organization`
- [ ] Migrate digital entities to `IAO:information content entity`
- [ ] Migrate location classes to BFO spatial regions
- [ ] Remove all `prov:Entity` direct subclassing

### Phase 3: Property Migration

- [ ] Replace `prov:wasInformedBy` with `pmdco:previousProcess` or `RO:preceded_by`
- [ ] Replace `prov:wasGeneratedBy` with inverse of `pmdco:output`
- [ ] Replace `prov:used` with `pmdco:input` or `RO:input_of`
- [ ] Replace `prov:wasAssociatedWith` with `RO:has_participant` or custom property
- [ ] Replace `prov:wasAttributedTo` with custom property or `RO:bearer_of`
- [ ] Replace `prov:wasDerivedFrom` with `RO:derives_from`
- [ ] Replace `prov:atLocation` with `RO:located_in`
- [ ] Replace `prov:hadMember` with `RO:has_part`
- [ ] Review temporal properties (`startedAtTime`, `endedAtTime`)

### Phase 4: Validation

- [ ] Run ODK validation workflows
- [ ] Check logical consistency with HermiT/Pellet
- [ ] Validate against PMDco v3 patterns
- [ ] Review with domain experts
- [ ] Update documentation

### Phase 5: Documentation

- [ ] Update class definitions
- [ ] Document migration changes
- [ ] Create mapping table (PROV-O → BFO/RO)
- [ ] Update examples and use cases

## 7. Critical Considerations

### 7.1 Equipment as Agent Issue

**Current Problem**: `Equipment` is subclass of `prov:Agent`, which is semantically incorrect in BFO.

**Solution**:

- Equipment is a `BFO:material entity` (BFO_0000040) (physical object)
- Equipment → subclass of `BFO:Object` (BFO_0000030) (general physical objects)
- Instrument → subclass of `prima:Equipment` → `BFO:Object` (BFO_0000030) AND subclass of `pmdco:Device` (multiple inheritance)
- Equipment *participates* in processes via `RO:has_participant` (not as agent)
- Equipment is *used by* agents (ResearchUser) via custom property `usesEquipment`
- Equipment *has* capabilities/dispositions, not agency

**PMDco v3 Hierarchy:**
```
BFO:material entity (BFO_0000040)
    └── BFO:Object (BFO_0000030)
            ├── prima:Equipment
            │       ├── prima:Instrument (also subclass of pmdco:Device)
            │       ├── prima:SampleCarrier
            │       └── prima:SampleHolder
            └── pmdco:Device
                    └── prima:Instrument (multiple inheritance)
```

**Note**: 
- `prima:Equipment` is a subclass of `pmdco:Object` (general physical objects)
- `prima:Instrument` uses multiple inheritance:
  - Subclass of `prima:Equipment` (maintains PRIMA hierarchy)
  - Subclass of `pmdco:Device` (Instruments are specialized devices)
- This allows Instruments to be both Equipment (PRIMA) and Device (PMDco v3)

See `PMDCO_V3_DEVICE_OBJECT_STRUCTURE.md` for detailed structure and mapping.

### 7.2 Agent Role Modeling

**Current**: `AgentRole` as separate class with `performsAgentRole` property.

**BFO Alignment**:

- Roles are `BFO:role` (subclass of `BFO:realizable entity`)
- Agents *bear* roles via `RO:bearer_of`
- Consider if roles should be dispositions instead

### 7.3 Process vs Activity

- BFO distinguishes `process` (occurrent) from `activity` (disposition)
- Ensure all process classes are properly classified
- Some "activities" might be better as dispositions

### 7.4 Information vs Material

- Clear distinction: physical objects vs information about objects
- `Model` (computational) might be information entity, not material
- `Dataset` is information, not physical collection

## 8. Recommended Migration Order

1. **Start with Core Module** - establishes foundation
2. **Migrate Experiment Module** - most complex, tests patterns
3. **Migrate Dataset Module** - simpler, validates information entity patterns
4. **Migrate Computational Module** - validates model/information distinctions
5. **Migrate Data Analysis Lifecycle** - completes process chains

## 9. Testing Strategy

- Use ODK automated testing
- Validate against PMDco v3 application ontologies (VTO, TTO, HTO)
- Compare with NFDI MatWerk ontology patterns
- Test with existing use cases (Herbie-ELN, STRAS-mapping)

## 10. Resources

- PMDco v3 Documentation: https://materialdigital.github.io/core-ontology/docs/
- PMDco User Guide: https://materialdigital.github.io/core-ontology/docs/PMDco%20User%20Guide/
- PMDco v3 RDF: https://raw.githubusercontent.com/materialdigital/core-ontology/main/pmdco.owl
- ODK Template: https://github.com/materialdigital/application-ontology-template
- PMDco v3 Device/Object Structure: See `PMDCO_V3_DEVICE_OBJECT_STRUCTURE.md` in this repository

