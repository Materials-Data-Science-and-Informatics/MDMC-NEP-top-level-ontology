# PMDco v3 Device, Object, and Material Entity Structure

## Class Hierarchy

Based on PMDco v3 ontology structure:

```
BFO:material entity (BFO_0000040)
    └── BFO:Object (BFO_0000030)
            └── pmdco:Device
```

## Class Definitions

### Material Entity
- **BFO Class**: `BFO:material entity` (BFO_0000040)
- **Definition**: Fundamental class in PMDco v3, aligning with BFO's material entity class
- **Scope**: Encompasses all physical entities that have material existence
- **Examples**: All physical objects, materials, equipment, instruments

### Object
- **BFO Class**: `BFO:Object` (BFO_0000030)
- **Parent**: `BFO:material entity` (BFO_0000040)
- **Definition**: Represents discrete, identifiable entities that maintain their identity over time
- **Scope**: Physical objects that are discrete and identifiable
- **Examples**: Physical samples, materials, general equipment
- **Note**: This is a BFO class, not a PMDco-specific class

### Device
- **PMDco Class**: `pmdco:Device`
- **Parent**: `BFO:Object` (BFO_0000030)
- **Definition**: Objects designed to perform specific functions, often requiring minimal user control
- **Scope**: Specialized objects with designed functionality
- **Examples**: Sensors, actuators, instruments, measurement devices

## Mapping PRIMA Classes to PMDco v3

### Equipment
- **Current PRIMA**: `Equipment` → subclass of `prov:Agent` ❌ (INCORRECT)
- **PRIMA Definition**: "Any kind of physical or virtual item, device, machine or other tool located in a Laboratory hosted by an Institution, which can be physically, virtually, and/or remotely accessed to perform any of the processes during the course of a Study, by applying a Technique."
- **PMDco v3 Mapping**: `Equipment` → subclass of `BFO:Object` (BFO_0000030) ✅
- **Rationale**: 
  - Equipment is a physical object (material entity)
  - Equipment is a general category that includes devices, machines, and tools
  - `BFO:Object` (BFO_0000030) represents discrete, identifiable physical entities
  - Equipment is broader than Device - it encompasses both devices and other physical objects
- **Recommendation**: `prima:Equipment` → `BFO:Object` (BFO_0000030) → `BFO:material entity` (BFO_0000040)

### Instrument
- **Current PRIMA**: `Instrument` → subclass of `Equipment` → `prov:Agent` ❌ (INCORRECT)
- **PRIMA Definition**: "Physical or virtual identifiable piece of Equipment used to perform a Data Acquisition and to generate Raw Data."
- **PMDco v3 Mapping**: `Instrument` → subclass of `prima:Equipment` → `BFO:Object`, AND subclass of `pmdco:Device`
- **Rationale**:
  - Instruments are a specific type of Equipment (as per PRIMA definition)
  - Instruments are designed to perform specific functions (measurement, data acquisition)
  - Instruments are specialized devices, so they should also be `pmdco:Device`
  - Instruments maintain PRIMA hierarchy (subclass of Equipment) while also being Device
- **Recommendation**: `Instrument` → `prima:Equipment` → `BFO:Object` (BFO_0000030) AND `Instrument` → `pmdco:Device` → `BFO:Object` (BFO_0000030) → `BFO:material entity` (BFO_0000040)

### SampleCarrier and SampleHolder
- **Current PRIMA**: `SampleCarrier`, `SampleHolder` → subclass of `Equipment` → `prov:Agent` ❌
- **PRIMA Definitions**:
  - SampleCarrier: "Piece of Equipment used for carrying one or more Samples and/or one or more Sample Holders"
  - SampleHolder: "Piece of Equipment used for making one or more Samples accessible for a Measurement or for holding them in place"
- **PMDco v3 Mapping**: `SampleCarrier`, `SampleHolder` → subclass of `prima:Equipment` → `BFO:Object`
- **Rationale**:
  - Both are explicitly defined as "Piece of Equipment" in PRIMA
  - They maintain the PRIMA hierarchy: Equipment → SampleCarrier/SampleHolder
  - They are physical objects (containers/holders), not necessarily specialized devices
  - They can be simple physical objects, so `BFO:Object` is appropriate
- **Recommendation**: `SampleCarrier`/`SampleHolder` → `prima:Equipment` → `BFO:Object` (BFO_0000030) → `BFO:material entity` (BFO_0000040)

### Consumable
- **Current PRIMA**: `Consumable` → subclass of `pmdco:Object` (already correct)
- **PMDco v3 Mapping**: `Consumable` → subclass of `pmdco:Object` ✅
- **Status**: Already aligned with PMDco v3

## Updated Migration Strategy

### Equipment and Instrument Migration

1. **Remove PROV-O Agent dependency**
   - Remove: `Equipment rdfs:subClassOf prov:Agent`
   - Remove: `Instrument rdfs:subClassOf prov:Agent` (via Equipment)
   - Remove: `SampleCarrier rdfs:subClassOf prov:Agent` (via Equipment)
   - Remove: `SampleHolder rdfs:subClassOf prov:Agent` (via Equipment)

2. **Add PMDco v3 Material Entity alignment**
   - Add: `Equipment rdfs:subClassOf BFO:Object` (BFO_0000030) (Equipment is a physical object)
   - Keep: `Instrument rdfs:subClassOf prima:Equipment` (maintains PRIMA hierarchy)
   - Add: `Instrument rdfs:subClassOf pmdco:Device` (Instruments are specialized devices)
   - Keep: `SampleCarrier rdfs:subClassOf prima:Equipment` (maintains PRIMA hierarchy)
   - Keep: `SampleHolder rdfs:subClassOf prima:Equipment` (maintains PRIMA hierarchy)

3. **Update property relationships**
   - Equipment participates in processes via `RO:has_participant` (not as agent)
   - Equipment is used by agents (ResearchUser) via `usesEquipment` property
   - Equipment has capabilities/dispositions, not agency

## Class Hierarchy After Migration

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
- `prima:Instrument` has multiple inheritance:
  - Subclass of `prima:Equipment` (maintains PRIMA hierarchy)
  - Subclass of `pmdco:Device` (Instruments are specialized devices)
- This allows Instruments to be both Equipment (PRIMA) and Device (PMDco v3)

## Key Points

1. **Equipment is NOT an Agent**: Equipment is a physical object (material entity), not an agent that can act
2. **Equipment is Object, not Device**: `prima:Equipment` is a subclass of `pmdco:Object` - Equipment is a general category of physical objects
3. **Instrument is both Equipment and Device**: 
   - Instruments are a type of Equipment (PRIMA hierarchy)
   - Instruments are also specialized devices (PMDco v3 Device)
   - Use multiple inheritance: `Instrument` → `Equipment` AND `Instrument` → `Device`
4. **Material Entity is the Foundation**: All physical objects must be subclasses of BFO:material entity
5. **PRIMA Hierarchy Preserved**: 
   - Equipment → Instrument (maintains PRIMA's "Instrument is a particular type of Equipment")
   - Equipment → SampleCarrier, SampleHolder (both are "Piece of Equipment")
6. **Object vs Device**: 
   - Use `BFO:Object` (BFO_0000030) for general physical objects (Equipment, SampleCarrier, SampleHolder)
   - Use `pmdco:Device` for objects with designed functionality (Instrument)
   - Note: `BFO:Object` is a BFO class, not a PMDco-specific class

## References

- PMDco v3 Documentation: https://materialdigital.github.io/core-ontology/docs/
- BFO Material Entity: http://purl.obolibrary.org/obo/BFO_0000040
- BFO Object: http://purl.obolibrary.org/obo/BFO_0000030

