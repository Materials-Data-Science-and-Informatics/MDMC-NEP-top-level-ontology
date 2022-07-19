from ctypes import Structure
from curses import raw
from random import sample
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

    Jane = example['Jane']
    sample_1_component_Ni = example['sample_1_component_Ni']
    sample_holder_1 = example['sample_holder_1']
    Graphene_growth_sample_preparation = example['Graphene_growth_sample_preparation']
    graphene_Ni_sample = example['graphe_sample']
    sputter_gun_1 = example['sputter_gun_1']
    heating_stage_1 = example['heating_gun_1']
    ethylene_1 = example['ethylene_1']
    gas_line_1 = example['gas_line_1']
    sample_quality_check_1 = example['sample_quality_check']
    LEED_instrument = example['LEED_instrument']
    g.add((Jane, RDF.type, MDMC.ResearchUser))
    g.add((sample_1_component_Ni, RDF.type, MDMC.SampleComponent))
    g.add((sample_holder_1, RDF.type, MDMC.SampleHolder))
    g.add((Graphene_growth_sample_preparation, RDF.type, MDMC.SamplePreparation))
    g.add((graphene_Ni_sample, RDF.type, MDMC.Sample))
    g.add((sputter_gun_1, RDF.type, MDMC.Equipment))
    g.add((heating_stage_1,RDF.type, MDMC.Equipment))
    g.add((ethylene_1,RDF.type, MDMC.SampleComponent))
    g.add((gas_line_1,RDF.type, MDMC.Equipment))
    g.add((LEED_instrument, RDF.type, MDMC.Instrument))
    g.add((sample_quality_check_1,RDF.type,MDMC.Measurement))
    g.add((sample_1_component_Ni, MDMC.isHeldBy, sample_holder_1))
    g.add((graphene_Ni_sample, PROV.wasGeneratedBy, Graphene_growth_sample_preparation))
    g.add((Graphene_growth_sample_preparation, PROV.used, sample_1_component_Ni))
    g.add((Graphene_growth_sample_preparation, PROV.used, ethylene_1))
    g.add((Graphene_growth_sample_preparation, PROV.wasAssociatedWith, sputter_gun_1))
    g.add((Graphene_growth_sample_preparation, PROV.wasAssociatedWith, heating_stage_1))
    g.add((Graphene_growth_sample_preparation, PROV.wasAssociatedWith, gas_line_1))
    g.add((sample_quality_check_1, PROV.wasAssociatedWith, LEED_instrument))
    g.add((sample_quality_check_1, PROV.used, graphene_Ni_sample))
    g.add((VT_STM_meas_1998_1, PROV.used, graphene_Ni_sample))
    g.add((STM_experiment_1998, MDMC.hasSamplePreparation, Graphene_growth_sample_preparation))    
    
    return g

