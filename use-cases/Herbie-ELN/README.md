# About the Use Case

Metal fabrication techniques in materials manufacturing include metal forming, casting, welding, and machining, often requiring multiple methods for a finished product. This use case focuses on casting and extrusion:

1. Casting: Liquid material is poured into a mold and solidifies into a specific shape.
2. Extrusion: The cast material is heated and forced through a die, creating a continuous profile with the die's cross-sectional shape.

The workflow involves shaping the material through casting, heating it, and processing it via extrusion to achieve the desired profile.

These processes are documented using Herbie, a hybrid system combining an Electronic Lab Notebook (ELN) and a research database, developed at Helmholtz-Zentrum Hereon. Herbie supports metallic biomaterials research, interlinking materials development, biological characterization, and synchrotron imaging. Its modular design allows adaptation to other fields.

In this use case, the Herbie ontology is extended to align with PRIMA. Successful ontology alignment involves identifying relationships and similarities between entities in the source and target ontologies, focusing on overlapping concepts that may have different names (synonyms) or types. This alignment enhances linked data generation and improves Herbie's interoperability within materials science data.


## Folder Description

In the [data-model](./data-model), you may find a data model/ontology used in Herbie. This can be accessed [here](./data-model/herbie.ttl). In this folder also, two PRIMA modules exists, and they are Core and Experiment.

The folder of [input-without-prima](./input-without-prima) is folder comprising the data from fabrication processes, e.g., casting and extrusion. These processes are serialized into two formats: TriG and Turtle. **Please note that the data hasn't been mapped to PRIMA.**

The last folder is [merged](./merged) folder, which is a folder containing data that has been mapped to PRIMA. This folder comprises three RDF data about casting, extrusion, and combined processes of casting and extrusion named [all.ttl](./merged/all.ttl). Below figure is the excerpt of two combined processses in Metal Fabrication. 

![prima-herbie.pdf](https://github.com/user-attachments/files/17690637/prima-herbie.pdf)





