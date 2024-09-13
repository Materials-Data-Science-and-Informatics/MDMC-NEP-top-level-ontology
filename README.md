## The PRIMA Ontology

This repository collects the ongoing work towards the development of the top-level ontology based on common terms defined for the Joint Lab  "Integrated Model and Data Driven Materials Characterization" (MDMC) and for the "Nanoscience Foundries and Fine Analysis Europe Pilot" (NEP). The top-level glossary defining the terms is available (as a living document which can be constantly updated) on the NEP website: https://www.nffa.eu/apply/data-policy/glossary

The first ontology that we develop is **PRovenance Information in MAterials science** ([PRIMA](https://github.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/tree/master/PRIMA)). PRIMA is an ontology that captures the provenance information in the materials science domain. PRIMA consists of 4 modules: 

1. [PRIMA-Core module](https://purls.helmholtz-metadaten.de/prima/core): The PRIMA-Core module consists of top-level classes and properties that can be reused in other modules. The core module is developed to provide general provenance information in the materials science domain, especially in the experimental workflow.

2. [PRIMA-Data Analysis Lifecycle module](https://purls.helmholtz-metadaten.de/prima/dal): In the Data Analysis Lifecyle module, the classes and properties related to a data flow are described.

3. [PRIMA-Dataset](https://purls.helmholtz-metadaten.de/prima/dataset): This module describe the classes and properties related to the structure of the dataset in the context of research. 

4. [PRIMA-Experiment](https://purls.helmholtz-metadaten.de/prima/experiment): In the Experiment module, the classes and properties related to an experiment are described

5. The ontology combining all the above modules is [PRIMA-complete](https://purls.helmholtz-metadaten.de/prima/complete)
## Aim

The aim of this joint activity is to develop the PRIMA ontology which can be initially adopted by MDMC and NEP. 
In future, it might also be adopted by other Materials Science projects. 
This will have the huge advantage of having a **common** description of concepts and relationships in the domain of Materials Science. 
This will offer a set of metadata which, in turn, will increase the interoperability and the reuse of data.

## Future extensions

The top-level ontology is planned to be extended thanks to the adoption of fine-grained ontologies already existing, 
e.g. the Material Science Lab Equipment (MSLE) Ontology. 

## Use Cases

* Materials science/nanoscience case study on Scanning Tunneling Microscopy (STM) images from Use Case 1 of the EOSC-Pillar project.

## Acknowledgements

* This work has been supported by the Joint Lab “Integrated Model and Data Driven Materials Characterization” ([MDMC](https://jl-mdmc-helmholtz.de)), Helmholtz Metadata Collaboration ([HMC](https://helmholtz-metadaten.de/en)) within the Hub Information at the Forschungszentrum Jülich, the research programs “Engineering Digital Futures” and “Materials System Engineering” of the Helmholtz Association of German Research Centers, NFFA-Europe Pilot ([NEP](https://www.nffa.eu)) Joint Activities and the Use case 1 of EOSC-Pillar ([EOSC-Pillar](https://www.eosc-pillar.eu/)) project. 

