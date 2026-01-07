# PRIMA Core Module v3.0 Documentation Summary

## Overview

This document provides a comprehensive overview of all documentation files created during the migration of PRIMA Core Module from version 2.0 (PROV-O based) to version 3.0 (BFO-based, aligned with PMDco v3). These documents serve as a complete reference for understanding the migration, mapping changes, breaking changes, and detailed analyses of class and property transformations.

## Documentation Organization

All migration-related documentation files are organized in the `docs/` folder for easy access and reference.

---

## Documentation Files

### 1. MAPPING_TABLE.md

**Purpose**: Provides a comprehensive mapping table of all classes and properties from PRIMA v2.0 to v3.0.

**Contents**:
- Class mappings (Process, Entity, Agent, Role classes)
- Property mappings (Object and Data properties)
- Import and namespace mappings
- Summary statistics

**Use When**: You need a quick reference for how specific classes or properties changed between versions.

**Location**: `docs/MAPPING_TABLE.md`

---

### 2. BREAKING_CHANGES.md

**Purpose**: Documents all breaking changes that affect existing data and applications using PRIMA v2.0.

**Contents**:
- Critical breaking changes (class hierarchy, property changes)
- Data migration requirements
- Query pattern changes
- Impact analysis
- Migration strategies

**Use When**: You need to understand what will break when migrating from v2.0 to v3.0, or when updating existing applications.

**Location**: `docs/BREAKING_CHANGES.md`

---

### 3. MIGRATION_GUIDE.md

**Purpose**: Step-by-step guide for migrating from PRIMA v2.0 to v3.0.

**Contents**:
- Overview of migration approach
- Class hierarchy changes
- Property mapping details
- Step-by-step migration instructions
- Best practices

**Use When**: You are actively migrating data or applications from v2.0 to v3.0.

**Location**: `docs/MIGRATION_GUIDE.md`

---

### 4. MIGRATION_SUMMARY.md

**Purpose**: Comprehensive summary of the entire migration process and outcomes.

**Contents**:
- Migration overview and objectives
- Detailed class and property mappings
- Alignment verification with PMDco v3
- Implementation details
- Challenges and solutions
- Future considerations

**Use When**: You need a complete overview of the migration work, outcomes, and verification.

**Location**: `docs/MIGRATION_SUMMARY.md`

---

### 5. PRIMA_CORE_V3_PROCESS_CROSSWALK.md

**Purpose**: Detailed cross-walk analysis of PRIMA v3.0 process classes with PMDco v3 planned process subclasses.

**Contents**:
- PMDco v3 planned process structure
- Detailed analysis of Assay, Computing Process, Planned Process
- Cross-walk mapping for DataAcquisition, DataAnalysis, Study
- Evaluant role explanation and implementation
- Semantic analysis and rationale

**Use When**: You need to understand how PRIMA process classes align with PMDco v3 process classes, or need details about the evaluant role requirement.

**Location**: `docs/PRIMA_CORE_V3_PROCESS_CROSSWALK.md`

---

### 6. PRIMA_CORE_V3_ENTITY_CROSSWALK.md

**Purpose**: Detailed cross-walk analysis of PRIMA v3.0 entity classes with PMDco v3 classes.

**Contents**:
- PRIMA v3.0 entity classes overview
- PMDco v3 relevant classes (Material, Publication, Plan Specification, etc.)
- Class-by-class cross-walk analysis
- Semantic analysis and alignment decisions
- Final alignment decisions

**Use When**: You need to understand how PRIMA entity classes align with PMDco v3 classes, or need details about entity class categorization decisions.

**Location**: `docs/PRIMA_CORE_V3_ENTITY_CROSSWALK.md`

---

### 7. IAO_CLASSES_REFERENCE.md

**Purpose**: Reference guide for Information Artifact Ontology (IAO) classes used in PRIMA v3.0.

**Contents**:
- IAO namespace and source information
- Detailed definitions of IAO classes used:
  - IAO_0000030: information content entity
  - IAO_0000033: directive information entity
  - IAO_0000027: data item
  - IAO_0000310: document
  - IAO_0000311: publication
- BFO hierarchy for each class
- Usage examples in PRIMA v3.0
- Summary table

**Use When**: You need to understand what IAO classes are used in PRIMA v3.0 and their definitions.

**Location**: `docs/IAO_CLASSES_REFERENCE.md`

---

### 8. PRIMA_AXIOM_COMPARISON_REPORT.md

**Purpose**: Comprehensive comparison of axioms between PRIMA v2.0 and v3.0 for all modified/mapped classes.

**Contents**:
- Executive summary with statistics
- Complete property mapping table
- Class-by-class axiom comparison:
  - Process classes (DataAcquisition, DataAnalysis, Study)
  - Entity classes (System, Material, Project, ScientificPublication, ResearchData, Settings, Technique)
  - Agent classes (ResearchUser, Equipment, Instrument, ResearchSoftware)
  - Role classes (AgentRole, UserRole)
- Property declaration changes
- New axioms introduced (evaluant role)
- Summary tables

**Use When**: You need detailed information about how axioms changed for specific classes, or need to analyze property mappings and new properties.

**Location**: `docs/PRIMA_AXIOM_COMPARISON_REPORT.md`

---

### 9. HAS_INPUT_VS_HAS_SPECIFIED_INPUT.md

**Purpose**: Explains the differences between "has input" (RO_0002233) and "has specified input" (OBI_0000293) properties.

**Contents**:
- Definitions of both properties
- Key characteristics and differences
- When to use which property
- Usage examples in PRIMA v3.0 DataAcquisition
- Semantic relationship between properties
- Practical implications

**Use When**: You need to understand the semantic difference between these two input properties and when to use each one.

**Location**: `docs/HAS_INPUT_VS_HAS_SPECIFIED_INPUT.md`

---

## Quick Reference Table

| Document | Purpose | Key Audience |
|----------|---------|--------------|
| [MAPPING_TABLE.md](MAPPING_TABLE.md) | Quick reference for class/property mappings | Developers, Ontologists |
| [BREAKING_CHANGES.md](BREAKING_CHANGES.md) | Breaking changes and impact | Developers, Data Managers |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | Step-by-step migration instructions | Developers, Data Engineers |
| [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md) | Complete migration overview | Project Managers, Ontologists |
| [PRIMA_CORE_V3_PROCESS_CROSSWALK.md](PRIMA_CORE_V3_PROCESS_CROSSWALK.md) | Process class alignment analysis | Ontologists, Researchers |
| [PRIMA_CORE_V3_ENTITY_CROSSWALK.md](PRIMA_CORE_V3_ENTITY_CROSSWALK.md) | Entity class alignment analysis | Ontologists, Researchers |
| [IAO_CLASSES_REFERENCE.md](IAO_CLASSES_REFERENCE.md) | IAO classes reference | Developers, Ontologists |
| [PRIMA_AXIOM_COMPARISON_REPORT.md](PRIMA_AXIOM_COMPARISON_REPORT.md) | Detailed axiom comparison | Ontologists, Researchers |
| [HAS_INPUT_VS_HAS_SPECIFIED_INPUT.md](HAS_INPUT_VS_HAS_SPECIFIED_INPUT.md) | Property difference explanation | Ontologists, Developers |

---

## Documentation Structure

```
docs/
├── core_module_documentation_summary.md  (this file)
├── MAPPING_TABLE.md
├── BREAKING_CHANGES.md
├── MIGRATION_GUIDE.md
├── MIGRATION_SUMMARY.md
├── PRIMA_CORE_V3_PROCESS_CROSSWALK.md
├── PRIMA_CORE_V3_ENTITY_CROSSWALK.md
├── IAO_CLASSES_REFERENCE.md
├── PRIMA_AXIOM_COMPARISON_REPORT.md
└── HAS_INPUT_VS_HAS_SPECIFIED_INPUT.md
```

---

## Usage Guide

### For Developers Migrating Applications

1. **Start with**: `BREAKING_CHANGES.md` - Understand what will break
2. **Then read**: `MIGRATION_GUIDE.md` - Follow step-by-step instructions
3. **Reference**: `MAPPING_TABLE.md` - Quick lookup for specific mappings
4. **Check**: `PRIMA_AXIOM_COMPARISON_REPORT.md` - Understand axiom changes

### For Ontologists and Researchers

1. **Start with**: `MIGRATION_SUMMARY.md` - Complete overview
2. **Deep dive**: `PRIMA_CORE_V3_PROCESS_CROSSWALK.md` - Process class analysis
3. **Deep dive**: `PRIMA_CORE_V3_ENTITY_CROSSWALK.md` - Entity class analysis
4. **Reference**: `IAO_CLASSES_REFERENCE.md` - IAO class definitions
5. **Reference**: `HAS_INPUT_VS_HAS_SPECIFIED_INPUT.md` - Property semantics

### For Project Managers

1. **Read**: `MIGRATION_SUMMARY.md` - Complete overview and outcomes
2. **Review**: `BREAKING_CHANGES.md` - Impact assessment
3. **Reference**: `MAPPING_TABLE.md` - Summary statistics

---

## Key Migration Highlights

### Foundation Change
- **v2.0**: PROV-O (Provenance Ontology) based
- **v3.0**: BFO (Basic Formal Ontology) based, aligned with PMDco v3

### Process Classes
- `DataAcquisition` → `obi:assay` (OBI_0000070)
- `DataAnalysis` → `pmd:computing_process` (PMD_0000583)
- `Study` → `obi:planned_process` (OBI_0000011)

### Entity Classes
- `System` → `bfo:material entity` (BFO_0000040)
- `Project` → `obi:organization` (OBI_0000245)
- `ScientificPublication` → `iao:publication` (IAO_0000311)
- `ResearchData` → `iao:data item` (IAO_0000027)

### Property Mappings
- `prov:wasAssociatedWith` → `ro:has_agent` (RO_0002211)
- `prov:wasAttributedTo` → `ro:has_participant` (RO_0000053) or `ro:has_agent`
- `pmd:input` → `ro:has_input` (RO_0002233)
- `pmd:output` → `ro:has_output` (RO_0002234)

### New Requirements
- **Evaluant Role**: DataAcquisition requires System inputs to bear evaluant role (`OBI_0000067`)

---

## Document Relationships

```
MIGRATION_SUMMARY.md (Overview)
    ├── MAPPING_TABLE.md (Quick Reference)
    ├── BREAKING_CHANGES.md (Impact Analysis)
    ├── MIGRATION_GUIDE.md (Implementation)
    │
    ├── PRIMA_CORE_V3_PROCESS_CROSSWALK.md (Process Analysis)
    │   └── HAS_INPUT_VS_HAS_SPECIFIED_INPUT.md (Property Details)
    │
    ├── PRIMA_CORE_V3_ENTITY_CROSSWALK.md (Entity Analysis)
    │   └── IAO_CLASSES_REFERENCE.md (IAO Reference)
    │
    └── PRIMA_AXIOM_COMPARISON_REPORT.md (Detailed Axiom Analysis)
```

---

## Statistics

- **Total Documentation Files**: 9 files
- **Total Pages**: ~200+ pages of documentation
- **Classes Documented**: 20+ classes
- **Properties Documented**: 15+ properties
- **Cross-Walk Analyses**: 2 (Process and Entity)
- **Reference Guides**: 2 (IAO Classes, Property Differences)

---

## Maintenance

These documentation files were created during the PRIMA Core Module v2.0 to v3.0 migration (January 2025). They should be updated if:

- Additional classes are migrated
- Property mappings are refined
- New alignment decisions are made
- PMDco v3 structure changes

---

## Contact and References

- **PRIMA Ontology**: https://purls.helmholtz-metadaten.de/prima/core
- **PMDco v3**: https://w3id.org/pmd/co/
- **Repository**: https://github.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology

---

*Last Updated: January 2025*

