from rdflib import Graph, Literal
from rdflib.namespace import  Namespace, RDF, XSD, DCTERMS, PROV

EXP = Namespace("https://purls.helmholtz-metadaten.de/prima/experiment#")
CORE = Namespace("https://purls.helmholtz-metadaten.de/prima/core#")
DAL = Namespace("https://purls.helmholtz-metadaten.de/prima/dal#")
DATASET = Namespace("https://purls.helmholtz-metadaten.de/prima/dataset#")
PMD = Namespace("https://w3id.org/pmd/co/")



def rdf_serializer(iri):
    example = Namespace(iri)
    g = Graph()
    g.parse("../../PRIMA/core/ver_2_0/prima-core.owl", format='xml')
    g.parse("../../PRIMA/data-analysis-lifecycle/ver_2_0/prima-data-analysis-lifecycle.owl", format='xml')
    g.parse("../../PRIMA/dataset/ver_2_0/prima-dataset.owl", format='xml')
    g.parse("../../PRIMA/experiment/ver_2_0/prima-experiment.owl", format='xml')

    g.bind("ex", example)
    g.bind("prima-core", CORE)
    g.bind("prima-exp", EXP)
    g.bind("prima-dal", DAL)
    g.bind("prima-dataset", DATASET)
    g.bind("pmd", PMD)
    g.bind("dcterms", DCTERMS)
    g.bind("prov", PROV)

    # objects generation
    STRAS_research_group = example['STRAS_Research_Group']
    VT_STM_Microscopy = example['VT_STM_Microscopy']
    analysis_software = example['Analysis_Software']
    alice = example['Alice']
    bob = example['Bob']
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
    VT_STM_meas_1998_1 = example['VT_STM_measurement_1998_1']
    project_member_role = example['project_member_role']

    g.add((STRAS_research_group, RDF.type, CORE.ResearchUser))
    g.add((VT_STM_Microscopy, RDF.type, CORE.Instrument))
    g.add((analysis_software, RDF.type, CORE.ResearchSoftware))
    g.add((project_member_role, RDF.type, CORE.ProjectMemberRole))
    g.add((alice, RDF.type, CORE.ResearchUser))
    g.add((alice, CORE.performsAgentRole, project_member_role))
    g.add((bob, RDF.type, CORE.ResearchUser))
    g.add((bob, CORE.performsAgentRole, project_member_role))
   
    g.add((VT_STM_meas_1998_1, RDF.type, EXP.Measurement))
    g.add((VT_STM_meas_1998_1, PROV.startedAtTime, Literal('1998-04-20', datatype=XSD.date)))
    g.add((VT_STM_meas_1998_1, PROV.endedAtTime, Literal('1998-05-20', datatype=XSD.date)))
    VT_STM_meas_1998_2 = example['VT_STM_measurement_1998_2']
    image_labelling_process_1 = example['image_labelling_process_1']
    g.add((image_labelling_process_1, RDF.type, CORE.DataAnalysisLifecycle))
    g.add((VT_STM_meas_1998_2, RDF.type, EXP.Measurement))
    g.add((VT_STM_meas_1998_2, PROV.startedAtTime, Literal('1998-04-21', datatype=XSD.date)))
    g.add((VT_STM_meas_1998_2, PROV.endedAtTime, Literal('1998-05-21', datatype=XSD.date)))
    image_selection_and_retrievement_1 = example['image_selection_and_retrievement_1']
    g.add((image_selection_and_retrievement_1, RDF.type, DAL.DataProcessing))
    g.add((image_labelling_process_1, DAL.hasDataProcessing, image_selection_and_retrievement_1))
    image_selection_and_retrievement_2 = example['image_selection_and_retrievement_2']
    g.add((image_selection_and_retrievement_2, RDF.type, DAL.DataProcessing))
    g.add((image_labelling_process_1, DAL.hasDataProcessing, image_selection_and_retrievement_2))
    metadata_selection_1 = example['metadata_selection_1']
    g.add((metadata_selection_1, RDF.type, DAL.DataProcessing))
    g.add((image_labelling_process_1, DAL.hasDataProcessing, metadata_selection_1))
    raw_data_1998_1 = example['raw_data_1998_1']
    g.add((raw_data_1998_1, RDF.type, DATASET.RawData))
    raw_data_1998_2 = example['raw_data_1998_2']
    g.add((raw_data_1998_2, RDF.type, DATASET.RawData))
    reference_dataset_1 = example['Reference_Dataset_1']
    g.add((reference_dataset_1, RDF.type, CORE.ResearchData))
    Structured_and_FAIR_dataset_1 = example['Structured_and_FAIR_dataset_1']
    g.add((Structured_and_FAIR_dataset_1, RDF.type, CORE.ResearchData))
    filtered_image_1 = example['filtered_image']
    g.add((filtered_image_1, RDF.type, DATASET.ProcessedData))
    towards_fairification_stm_data = example['towards_fairification_stm_data']
    g.add((towards_fairification_stm_data, RDF.type, CORE.Project))
    g.add((towards_fairification_stm_data, PROV.wasAttributedTo, STRAS_research_group))
    g.add((towards_fairification_stm_data, CORE.hasProjectMember, alice))
    g.add((towards_fairification_stm_data, CORE.hasProjectMember, bob))
    study_1 = example['study_1']
    study_2 = example['study_2']
    g.add((study_1, PROV.wasAssociatedWith, towards_fairification_stm_data))
    g.add((study_2, PROV.wasAssociatedWith, towards_fairification_stm_data))
    g.add((study_1, CORE.hasDataAnalysisLifecycle, image_labelling_process_1))
    g.add((study_1, RDF.type, CORE.Study))
    g.add((study_2, RDF.type, CORE.Study))
    g.add((study_1, EXP.hasMeasurement, VT_STM_meas_1998_1))
    g.add((study_2, EXP.hasMeasurement, VT_STM_meas_1998_2))
    g.add((raw_data_1998_1, PMD.outputOf, VT_STM_meas_1998_1))
    g.add((raw_data_1998_2, PMD.outputOf, VT_STM_meas_1998_2))
    g.add((image_selection_and_retrievement_1, PMD.input, raw_data_1998_1))
    g.add((image_selection_and_retrievement_1, PMD.input, raw_data_1998_2))
    g.add((image_selection_and_retrievement_1, PMD.output, reference_dataset_1))
    g.add((image_labelling_process_1, PMD.input, reference_dataset_1))
    g.add((image_labelling_process_1, PMD.output, Structured_and_FAIR_dataset_1))
    g.add((metadata_selection_1, PMD.input, Structured_and_FAIR_dataset_1))
    g.add((filtered_image_1, PROV.wasDerivedFrom, Structured_and_FAIR_dataset_1))
    g.add((filtered_image_1, PMD.outputOf, metadata_selection_1))
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

    g.add((sample_1_component_Ni, RDF.type, EXP.SampleComponent))
    g.add((sample_holder_1, RDF.type, EXP.SampleHolder))
    g.add((Graphene_growth_sample_preparation, RDF.type, EXP.SamplePreparation))
    g.add((graphene_Ni_sample, RDF.type, EXP.Sample))
    g.add((sputter_gun_1, RDF.type, CORE.Equipment))
    g.add((heating_stage_1,RDF.type, CORE.Equipment))
    g.add((ethylene_1,RDF.type, EXP.SampleComponent))
    g.add((gas_line_1,RDF.type, CORE.Equipment))
    g.add((LEED_instrument, RDF.type, CORE.Instrument))
    g.add((sample_quality_check_1,RDF.type,EXP.Measurement))
    g.add((sample_1_component_Ni, EXP.isHeldBy, sample_holder_1))
    g.add((graphene_Ni_sample, PMD.outputOf, Graphene_growth_sample_preparation))
    g.add((Graphene_growth_sample_preparation, PMD.input, sample_1_component_Ni))
    g.add((Graphene_growth_sample_preparation, PMD.input, ethylene_1))
    g.add((Graphene_growth_sample_preparation,CORE.usesEquipment, sputter_gun_1))
    g.add((Graphene_growth_sample_preparation,CORE.usesEquipment, heating_stage_1))
    g.add((Graphene_growth_sample_preparation,CORE.usesEquipment, gas_line_1))
    g.add((sample_quality_check_1,CORE.usesEquipment, LEED_instrument))
    g.add((sample_quality_check_1, PMD.input, graphene_Ni_sample))
    g.add((VT_STM_meas_1998_1, PMD.input, graphene_Ni_sample))
    
    return g

