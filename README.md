# The PRIMA Ontology
This repository collects the ongoing work towards the development of the top-level ontology based on common terms defined for the Joint Lab  "Integrated Model and Data Driven Materials Characterization" (MDMC) and for the "Nanoscience Foundries and Fine Analysis Europe Pilot" (NEP). The top-level glossary defining the terms is available (as a living document which can be constantly updated) on the NEP website: https://www.nffa.eu/apply/data-policy/glossary

The aim of this joint activity is to develop the **PRovenance Information in MAterials science** (PRIMA) which can be initially adopted by MDMC and NEP. PRIMA is an ontology that captures the provenance information in the materials science domain.
In future, it might also be adopted by other Materials Science projects. 
This will have the huge advantage of having a **common** description of concepts and relationships in the domain of Materials Science. 
This will offer a set of metadata which, in turn, will increase the interoperability and the reuse of data.


## Table of content
  1. [PRIMA Documentation](#prima-documentation)
  2. [Use Cases](#use-cases)
  3. [Usage](#usage)
  4. [Future Extensions](#future-extensions)
  5. [Contact](#contact)
  6. [License](#license)
  7. [Acknowledgements](#acknowledgements)


## PRIMA Documentation

PRIMA is a modular ontology consisting of four modules: 

1. [PRIMA-Core module](https://purls.helmholtz-metadaten.de/prima/core): The PRIMA-Core module consists of top-level classes and properties that can be reused in other modules. The core module is developed to provide general provenance information in the materials science domain, especially in the experimental workflow.

2. [PRIMA-Data Analysis Lifecycle module](https://purls.helmholtz-metadaten.de/prima/dal): In the Data Analysis Lifecyle module, the classes and properties related to a data flow are described.

3. [PRIMA-Dataset](https://purls.helmholtz-metadaten.de/prima/dataset): This module describe the classes and properties related to the structure of the dataset in the context of research. 

4. [PRIMA-Experiment](https://purls.helmholtz-metadaten.de/prima/experiment): In the Experiment module, the classes and properties related to an experiment are described

5. The ontology combining all the above modules is [PRIMA-complete](https://purls.helmholtz-metadaten.de/prima/complete)

## Use Cases
So far, we have demonstrated the broad applicability of PRIMA by presenting two different use cases: (i) the mapping of the FAIRification workflow applied to Scanning Tunneling Microscope (STM) images from data acquisition to data analysis and (ii) the PRIMA alignment of the fabrication processes ontologies applied to metallic biomaterials recorded in the Herbie Electronic Laboratory Notebook (ELN).

### Use case 1: Scanning Tunneling Microscopy (STM) Images 

In this use case, we extend the work done by [Rodani et al., (2023)](https://direct.mit.edu/dint/article/5/1/27/112600/Towards-the-FAIRification-of-Scanning-Tunneling) by mapping its provenance data model to PRIMA. The provenance data model of STM images follows the PROV-DM standard and is serialized by the PROV-JSON serialization, i.e., the metadata is in the JSON format. Furthemore, the mapping is done by connecting JSON objects into PRIMA, so that each of JSON objects is an instance of a PRIMA class.

The use case including the mapped ontology and the RDF data can be accessed [here](./use-cases/STRAS-mapping).

### Use case 2: Metallic Biomaterials Fabrication in the Herbie ELN
[Herbie](https://doi.org/10.5281/zenodo.12205430) is a hybrid system between an ELN and a research database developed at the Helmholtz-Zentrum Hereon. Herbie is tailored to cover and interlink the heterogeneous process chain of metallic biomaterials research, including materials development, biological characterization, and synchrotron imaging; nevertheless, due to its modular structure, it can be adapted to other fields. 

In this use case, the Herbie ontology, an ontology is used in Herbie, is extended to be aligned to PRIMA. A successful ontology alignment involves identifying relationships between entities in different ontologies to establish links and similarities between the source and target ontologies. The analysis focuses on concepts that overlap but may have different names (synonyms) or types in the ontologies. This alignment supports the generation of linked data and boasts more interoperability of Herbie within the materials science data.

The use case including the extended Herbie ontology and RDF data generated from it can be accessed [here](./use-cases/Herbie-ELN).

## Usage
* We recommend to use [Protégé 5.5.0](https://protege.stanford.edu/products.php#desktop-protege) to be able to view and navigate classes and properties in PRIMA.
* We recommend also to use HermiT as a reasoner for PRIMA. You can select it through the menu *Reasoner* in Protégé software.

## PRIMA SKOS Monitoring

This repository includes an automated workflow to monitor changes in the PRIMA SKOS vocabulary hosted on [SKOSMOS](https://matwerk.datamanager.kit.edu/skosmos/prima/en/). The monitoring system automatically detects changes such as new concepts, modified definitions, or updated relationships.

**Note:** We encourage you to use [`uv`](https://github.com/astral-sh/uv) for managing Python dependencies and virtual environments. After cloning the repository, run `uv sync` to set up the environment.

### Automated Monitoring

A GitHub Actions workflow runs weekly (and can be manually triggered) to:
- Download the latest PRIMA SKOS vocabulary from SKOSMOS
- Compare it with the previous snapshot
- Create a GitHub issue if changes are detected
- Store versioned snapshots in `monitor_utils/skos_snapshots/`

The workflow is defined in `.github/workflows/skos-monitor.yml`.

### Manual Usage

You can also use the monitoring tools manually via the command-line interface:

```bash
# Download the latest SKOS vocabulary
python -m monitor_utils.prima_skos_monitor.cli download --output prima.rdf

# Compare two versions
python -m monitor_utils.prima_skos_monitor.cli compare \
  --baseline monitor_utils/skos_snapshots/latest.rdf \
  --new prima.rdf \
  --output change_report.md

# Download and save as snapshot
python -m monitor_utils.prima_skos_monitor.cli download \
  --save-snapshot \
  --snapshot-dir monitor_utils/skos_snapshots
```

### Change Detection

The monitor detects:
- **New concepts**: Concepts added to the vocabulary
- **Deleted concepts**: Concepts removed from the vocabulary
- **Modified concepts**: Changes to definitions, relationships, labels, or metadata

When changes are detected, a detailed markdown report is generated with links to the affected concepts on SKOSMOS.

## Future extensions

* We aim at facilitating the interoperability of PRIMA with other existing domain ontologies in materials science and at promoting its use. 


## Contact
You may contact one of the authors of PRIMA via a.ihsan@fz-juelich.de

## License
The code is licensed under the [MIT license](./LICENSE). Copyright © 2025.

## Acknowledgements

This work has been supported by the Joint Lab “Integrated Model and Data Driven Materials Characterization” ([MDMC](https://jl-mdmc-helmholtz.de)), Helmholtz Metadata Collaboration ([HMC](https://helmholtz-metadaten.de/en)) within the Hub Information at the Forschungszentrum Jülich, the German Research Foundation (Deutsche Forschungsgemeinschaft, DFG) in the framework of the project FAIRmat (Project ID: 460197019); the DFG under the National Research Data Infrastructure – NFDI 38/1 – project number 460247524, the research programs “Engineering Digital Futures” and “Materials System Engineering” of the Helmholtz Association of German Research Centers, NFFA-Europe Pilot ([NEP](https://www.nffa.eu)) Joint Activities and the Use case 1 of EOSC-Pillar ([EOSC-Pillar](https://www.eosc-pillar.eu/)) project.


