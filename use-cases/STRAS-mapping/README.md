# About the Use Case
![Use Case 1](https://github.com/user-attachments/files/17690562/stras-use-case.pdf)

In this use case, we extend the work done by [Rodani et al., (2023)](https://direct.mit.edu/dint/article/5/1/27/112600/Towards-the-FAIRification-of-Scanning-Tunneling) by mapping its provenance data model to PRIMA. The provenance data model of STM images follows the PROV-DM standard and is serialized by the PROV-JSON serialization, i.e., the metadata is in the JSON format. Furthemore, the mapping is done by connecting JSON objects into PRIMA, so that each of JSON objects is an instance of a PRIMA class. 

The STM image data analysis lifecycle, detailed in the above figure, encompasses the following stages:

1. Raw Data: Approximately 420,000 STM images were acquired over 20 years by the STRAS research group (CNR-IOM, Trieste) using an Omicron Variable Temperature STM (VT-STM) microscope. Metadata, including measurement times and settings, were recorded for each image.
2. Processed Data: About 110,000 images were selected based on specific scanning mode settings.
3. Analysis: Human annotations and machine learning techniques were applied to extract structural and compositional information, resulting in 7,287 categorized images. Categories include Gr Ni100, Gr Ni111, and Gr Ni111, along with metadata.
4. Dataset Accessibility: Eleven key metadata fields were indexed in the STM Metadata Explorer, part of the Trieste Advanced Data Services (TriDAS) via NEP Virtual Access. This web tool enables users to visually explore, select, and download relevant images along with provenance data in JSON format.


## Folder Description

In the folder of [python-script](./python-script), there are scripts to map the [project data model](https://direct.mit.edu/dint/article/5/1/27/112600/Towards-the-FAIRification-of-Scanning-Tunneling) into PRIMA, particularly the [rdf-serializer.py](./python-script/rdf-serializer.py). The project data model can be seen in the figure below: 

![dint_a_00164 figure 4](https://github.com/user-attachments/assets/07e3114c-f647-47b4-be40-01f9cb372143)

The [data](./data) folder is the rdf data of the mentioned processes above. An excerpt of data that is mapped to PRIMA and  STM Image data model (in PROV-DM)  can be seen in the figure below

![prima-stras](https://github.com/user-attachments/files/17690569/prima-stras.pdf)



