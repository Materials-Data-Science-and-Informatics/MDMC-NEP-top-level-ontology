from ctypes import Structure
from curses import raw
from rdflib import Graph, Literal
from rdflib.namespace import  Namespace, RDF, XSD, DCTERMS, PROV

MDMC = Namespace("https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#")


def rdf_serializer(iri):
    example = Namespace(iri)
    g = Graph()
    g.parse("../mdmc-nep-top-level-ontology.owl", format='xml')

    g.bind("ex", example)
    g.bind("mdmc", MDMC)
    g.bind("dcterms", DCTERMS)
    g.bind("prov", PROV)

    # objects generation

    STRAS_research_group = example['STRAS_Research_Group']
    g.add((STRAS_research_group, RDF.type, MDMC.ResearchUser))
    VT_STM_Microscopy = example['VT_STM_Microscopy']
    g.add((VT_STM_Microscopy, RDF.type, MDMC.Instrument))
    analysis_software = example['Analysis_Software']
    g.add((analysis_software, RDF.type, MDMC.ResearchSoftware))
    alice = example['Alice']
    g.add((alice, RDF.type, MDMC.ResearchUser))
    bob = example['Bob']
    g.add((bob, RDF.type, MDMC.ResearchUser))
    VT_STM_meas_1998_1 = example['VT_STM_measurement_1998_1']
    g.add((VT_STM_meas_1998_1, RDF.type, MDMC.Measurement))
    g.add((VT_STM_meas_1998_1, PROV.startedAtTime, Literal('1998-04-20', datatype=XSD.date)))
    g.add((VT_STM_meas_1998_1, PROV.endedAtTime, Literal('1998-05-20', datatype=XSD.date)))
    VT_STM_meas_1998_2 = example['VT_STM_measurement_1998_2']
    image_labelling_process_1 = example['image_labelling_process_1']
    g.add((image_labelling_process_1, RDF.type, MDMC.DataAnalysisLifeCycle))
    g.add((VT_STM_meas_1998_2, RDF.type, MDMC.Measurement))
    g.add((VT_STM_meas_1998_2, PROV.startedAtTime, Literal('1998-04-21', datatype=XSD.date)))
    g.add((VT_STM_meas_1998_2, PROV.endedAtTime, Literal('1998-05-21', datatype=XSD.date)))
    image_selection_and_retrievement_1 = example['image_selection_and_retrievement_1']
    g.add((image_selection_and_retrievement_1, RDF.type, MDMC.DataProcessing))
    g.add((image_selection_and_retrievement_1, MDMC.isMemberOf, image_labelling_process_1))
    image_selection_and_retrievement_2 = example['image_selection_and_retrievement_2']
    g.add((image_selection_and_retrievement_2, RDF.type, MDMC.DataProcessing))
    g.add((image_selection_and_retrievement_2, MDMC.isMemberOf, image_labelling_process_1))
    metadata_selection_1 = example['metadata_selection_1']
    g.add((metadata_selection_1, RDF.type, MDMC.DataProcessing))
    g.add((metadata_selection_1, MDMC.isMemberOf, image_labelling_process_1))
    raw_data_1998_1 = example['raw_data_1998_1']
    g.add((raw_data_1998_1, RDF.type, MDMC.RawData))
    raw_data_1998_2 = example['raw_data_1998_2']
    g.add((raw_data_1998_2, RDF.type, MDMC.RawData))
    reference_dataset_1 = example['Reference_Dataset_1']
    g.add((reference_dataset_1, RDF.type, MDMC.ProcessedDataOrAnalysedData))
    Structured_and_FAIR_dataset_1 = example['Structured_and_FAIR_dataset_1']
    g.add((Structured_and_FAIR_dataset_1, RDF.type, MDMC.ProcessedDataOrAnalysedData))
    filtered_image_1 = example['filtered_image']
    g.add((filtered_image_1, RDF.type, MDMC.ProcessedData))
    towards_fairification_stm_data = example['towards_fairification_stm_data']
    g.add((towards_fairification_stm_data, RDF.type, MDMC.Project))
    g.add((towards_fairification_stm_data, PROV.wasAttributedTo, STRAS_research_group))
    g.add((alice, PROV.actedOnBehalfOf, STRAS_research_group))
    study_1 = example['study_1']
    study_2 = example['study_2']
    g.add((towards_fairification_stm_data, MDMC.hasStudy, study_1))
    g.add((towards_fairification_stm_data, MDMC.hasStudy, study_2))
    g.add((study_1, MDMC.hasDataAnalysisLifeCycle, image_labelling_process_1))
    STM_experiment_1998 = example['STM_experiment_1998']
    g.add((STM_experiment_1998, RDF.type, MDMC.Experiment))
    STM_experiment_2010 = example['STM_experiment_2010']
    g.add((STM_experiment_2010, RDF.type, MDMC.Experiment))
    g.add((study_1, RDF.type, MDMC.Study))
    g.add((study_1, MDMC.hasExperiment, STM_experiment_1998))
    g.add((STM_experiment_1998, PROV.startedAtTime, Literal('1998-04-20', datatype=XSD.date)))
    g.add((STM_experiment_1998, PROV.endedAtTime, Literal('1998-05-20', datatype=XSD.date)))
    g.add((study_2, RDF.type, MDMC.Study))
    g.add((study_2, MDMC.hasExperiment, STM_experiment_2010))
    g.add((STM_experiment_2010, PROV.startedAtTime, Literal('2010-04-20', datatype=XSD.date)))
    g.add((STM_experiment_2010, PROV.startedAtTime, Literal('2010-05-20', datatype=XSD.date)))
    g.add((STM_experiment_1998, MDMC.hasMeasurement, VT_STM_meas_1998_1))
    g.add((STM_experiment_1998, MDMC.hasMeasurement, VT_STM_meas_1998_2))
    g.add((raw_data_1998_1, PROV.wasGeneratedBy, VT_STM_meas_1998_1))
    g.add((raw_data_1998_2, PROV.wasGeneratedBy, VT_STM_meas_1998_2))
    g.add((image_selection_and_retrievement_1, PROV.used, raw_data_1998_1))
    g.add((image_selection_and_retrievement_1, PROV.used, raw_data_1998_2))
    g.add((image_labelling_process_1, PROV.used, reference_dataset_1))
    g.add((Structured_and_FAIR_dataset_1, PROV.wasGeneratedBy, image_selection_and_retrievement_1))
    g.add((metadata_selection_1, PROV.used, Structured_and_FAIR_dataset_1))
    g.add((filtered_image_1, PROV.wasDerivedFrom, Structured_and_FAIR_dataset_1))
    g.add((filtered_image_1, PROV.wasGeneratedBy, metadata_selection_1))
    g.add((filtered_image_1, PROV.wasAttributedTo, alice))
    g.add((metadata_selection_1, PROV.wasAttributedTo, alice))
    g.add((Structured_and_FAIR_dataset_1, PROV.wasAttributedTo, STRAS_research_group))
    g.add((Structured_and_FAIR_dataset_1, PROV.wasAttributedTo, bob))
    g.add((image_labelling_process_1, PROV.wasAssociatedWith, STRAS_research_group))
    g.add((image_labelling_process_1, PROV.wasAssociatedWith, bob))
    g.add((reference_dataset_1, PROV.wasAssociatedWith, STRAS_research_group))
    g.add((reference_dataset_1, PROV.wasAssociatedWith, bob))
    g.add((image_selection_and_retrievement_1, PROV.wasAssociatedWith, bob))
    g.add((reference_dataset_1, PROV.wasAttributedTo, STRAS_research_group))
    g.add((VT_STM_meas_1998_1, PROV.wasAssociatedWith, STRAS_research_group))
    g.add((VT_STM_meas_1998_1, PROV.wasAssociatedWith, VT_STM_Microscopy))
    
    
    return g

