# Competency Questions of PRIMA
Below is competency questions (CQs) modularized according to PRIMA modules. 

## [PRIMA-Core](#prima-core-sparql)
1. Which project is researcher(s) member of?
2. Which study has researcher(s) performed?
3. Which experiment has researcher(s) performed?
4. Which research data that is attributed to (e.g., created by) the researcher(s)?
5. Which data analysis lifecycle used in a study and which data are used?
6. Which studies are done by a project and list all experiments are done in those studies?

## [PRIMA-Data analysis lifecycle](#prima-data-analysis-lifecycle-sparql)
1. Which results have been obtained from the data analysis lifecycle?
2. Which data analysis, data processing and data interpretation are part of a data analysis lifecycle?
3. Which data have been used and produced in a data analysis/processing/intreptation?
4. Which software has been used in a data analysis/processing/interpretation?
5. Which researcher(s) have performed the data analysis/processing/interpretation?
6. Which process to do a data analysis lifecycle, data analysis, data processing, or data intepretation?

## [PRIMA-Dataset](#prima-dataset-sparql)
1. Which project have the data been attributed to?
2. Which data does the dataset collects?
3. In which data collaboration platform is the data stored?
4. In which data repository is the data stored?
5. Which dataset has been the publication data derived from?
5. Which metadata has described the data?

## [PRIMA-Experiment](#prima-experiment-sparql)
1. Which measurements/sample preparation/fabrication have been performed in an experiment?
2. Which equipment/instrument has been used in an experiment/in a measurement/in a sample preparation/in a fabrication?
3. Which measurement techniques have been used in a measurement?
4. Where and when has the experiment been performed?
5. Which researcher(s) have performed an experiment/measurement/sample preparation/fabrication?
6. Which samples have been used/prepared in a measurement?
7. Which raw data have been produced in a measurement?
8. Who has prepared the samples?
9. What process sequence taken for doing an experiment/measurement/sample preparation?
10. Which sample components is the sample made of?


# Answer to CQs via SPARQL

## PRIMA-Core SPARQL
1. Which project is researcher(s) member of?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?Project ?ResearchUser WHERE{
	?Project a core:Project ; 
		prov:wasAttributedTo ?ResearchUser .
	?ResearchUser a core:ResearchUser ; 
		core:performsAgentRole ?role . 
	?role a core:ProjectMemberRole .
}
```

2. Which study has researcher(s) performed?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?Study ?ResearchUser WHERE{
	?Project a core:Project ; 
		core:hasStudy ?Study.
	?Study prov:wasAttributedTo ?ResearchUser.
	?ResearchUser a core:ResearchUser .
}
```

3. Which experiment has researcher(s) performed?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?Experiment ?ResearchUser WHERE{
	?Experiment a core:Experiment ; 
		prov:wasAssociatedWith ?ResearchUser.
}
```
4. Which research data that is attributed to (e.g., created by) the researcher(s)?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?ResearchData ?ResearchUser WHERE{
	?ResearchData a core:ResearchData ; 
		prov:wasAttributedTo ?ResearchUser.
	?ResearchUser a core:ResearchUser . 
}
```
5. Which data analysis lifecycle used in a study and which data are used?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Study ?DataAnalysisLifecycle ?ResearchData WHERE{
	?Study a core:Study; 
		core:hasDataAnalysisLifecycle ?DataAnalysisLifecycle.
	?DataAnalysisLifecycle pmd:input ?ResearchData .
	?ResearchData a core:ResearchData.
}
```
6. Which studies are done by a project and list all experiments are done in those studies?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Project ?Study ?Experiment WHERE{
	?Project  core:hasStudy ?Study . 
	?Study core:hasExperiment  ?Experiment . 
}
```

## PRIMA-Data analysis lifecycle SPARQL

1. Which research data resulted from the data analysis lifecycle?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_analysis_lifecycle ?Research_data WHERE{
	{	
		?Data_analysis_lifecycle a core:DataAnalysisLifecycle ;  
		    pmd:output ?Research_data.
		?Research_data a core:ResearchData.
	}
	UNION
	{	
		?Data_analysis_lifecycle a core:DataAnalysisLifecycle ;
			dal:hasDataProcessing ?data_processing . 
		?data_processing pmd:output ?Research_data . 
		?Research_data a core:ResearchData . 
		
	}
	UNION
	{   
        ?Data_analysis_lifecycle a core:DataAnalysisLifecycle ;
		    dal:hasDataAnalysis ?data_analysis. 
		?data_analysis pmd:output ?Research_data.
		?Research_data a core:ResearchData . 
	}
	UNION
	{
		?Data_analysis_lifecycle a core:DataAnalysisLifecycle ;
            dal:hasDataInterpretation ?data_interpretation. 
		?data_interpretation pmd:output ?Research_data.
		?Research_data a core:ResearchData . 
	}

}
```
2. Which data analysis, data processing and data interpretation are part of a data analysis lifecycle?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_analysis_lifecycle ?data_processing ?data_analysis ?data_interpretation  WHERE{	
	
	{
		?Data_analysis_lifecycle a core:DataAnalysisLifecycle ;
			dal:hasDataProcessing ?data_processing . 
	}
	UNION
	{   
        ?Data_analysis_lifecycle a core:DataAnalysisLifecycle ;
		    dal:hasDataAnalysis ?data_analysis. 
	}
	UNION
	{
		?Data_analysis_lifecycle a core:DataAnalysisLifecycle ;
            dal:hasDataInterpretation ?data_interpretation. 
	}
}
```
3. Which data have been used and produced in a data analysis/processing/intreptation?
3a. Data analysis
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_analysis ?input ?output WHERE{	
	?Data_analysis a dal:DataAnalysis ; 
        pmd:input ?input ;
        pmd:output ?output.	
}
```

3b. Data processing
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_processing ?input ?output WHERE{	
	?Data_processing a dal:DataProcessing ; 
        pmd:input ?input ;
        pmd:output ?output.	
}
```

3c. Data interpretation
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_interpretation ?input ?output WHERE{	
	?Data_interpretation a dal:DataInterpretation ; 
        pmd:input ?input ;
        pmd:output ?output.	
}
```
4. Which software has been used in a data analysis/processing/interpretation?

4a. Data analysis
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_analysis ?software WHERE{	
	?Data_analysis a dal:DataAnalysis ; 
        dal:usesResearchSoftware ?software.	
}
```

4b. Data processing
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_processing ?software WHERE{	
	?Data_processing a dal:DataProcessing ; 
        dal:usesResearchSoftware ?software.	
}
```

4c. Data interpretation
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_interpretation ?software WHERE{	
	?Data_interpretation a dal:DataInterpretation ; 
        dal:usesResearchSoftware ?software.	
}
```

5. Which researcher(s) have performed the data analysis/processing/interpretation?

5a. Data analysis
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_analysis ?research_user WHERE{	
	?Data_analysis a dal:DataAnalysis ; 
        prov:wasAssociatedWith ?research_user.
    ?research_user a core:ResearchUser.	
}
```

5b. Data processing
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_processing ?research_user WHERE{	
	?Data_processing a dal:DataProcessing ; 
        prov:wasAssociatedWith ?research_user.
    ?research_user a core:ResearchUser.	
}
```

5c. Data interpretation
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Data_interpretation ?software WHERE{	
	?Data_interpretation a dal:DataInterpretation ; 
        prov:wasAssociatedWith ?research_user.
    ?research_user a core:ResearchUser.		
}
```

6. Which process to do a data analysis lifecycle, data analysis, data processing, or data intepretation?
```
```

## PRIMA-Dataset SPARQL


## PRIMA-Experiment SPARQL

1. Which measurements/sample preparation/fabrication have been performed in an experiment?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Experiment ?Measurement ?Sample_preparation ?Fabrication WHERE {
    {
        ?Experiment a core:Experiment;
            exp:hasMeasurement ?Measurement .
    }
    UNION
    {
        ?Experiment a core:Experiment;
            exp:hasSamplePreparation ?Sample_preparation .
    }
    UNION
    {
        ?Experiment a core:Experiment;
            exp:hasFabrication ?Fabrication .
    }
	

}
```
2. Which equipment/instrument has been used in an experiment/in a measurement/in a sample preparation?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Equipment ?Experiment ?Measurement ?Sample_preparation ?Fabrication  WHERE {
    {
        ?Experiment a core:Experiment;
            exp:usesEquipment ?Equipment.
        ?Equipment a exp:Equipment.
    }
    UNION
    {
        ?Measurement a exp:Measurement;
            exp:usesEquipment ?Equipment.
        ?Equipment a exp:Equipment.
    }
    UNION
    {
        ?Sample_preparation a exp:SamplePreparation;
            exp:usesEquipment ?Equipment.
        ?Equipment a exp:Equipment.
    }
    UNION
    {
        ?Fabrication a exp:Fabrication; 
        	exp:usesEquipment ?Equipment.
        ?Equipment a exp:Equipment .
    }
}

```
3. Which measurement techniques have been used in a measurement?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Measurement ?Measurement_technique  WHERE {
  ?Measurement a exp:Measurement;
    exp:hasMeasurementTechnique ?Measurement_technique.
}
```
4. Where and when has the experiment/measurement/sample preparation/fabrication been performed?

4a. Experiment
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Experiment ?At_time ?Start_time ?End_time ?Location  WHERE {
    {
		?Experiment a core:Experiment;
    		prov:startedAtTime ?Start_time;
        	prov:endedAtTime ?End_time.
	}
    OPTIONAL
    {
        ?Experiment  prov:atLocation ?Location.
    }
	OPTIONAL
	{
		?Experiment a core:Experiment;
    		prov:atTime ?At_time.
	}
}
```
4b. Measurement
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Measurement ?At_time ?Start_time ?End_time ?Location  WHERE {
    {
		?Measurement  a exp:Measurement ;
    		prov:startedAtTime ?Start_time;
        	prov:endedAtTime ?End_time.
	}
    OPTIONAL
    {
        ?Measurement   prov:atLocation ?Location.
    }
	OPTIONAL
	{
		?Measurement t a exp:Measurement ;
    		prov:atTime ?At_time.
	}
}
```
4c. Sample preparation
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Sample_preparation ?At_time ?Start_time ?End_time ?Location  WHERE {
    {
		?Sample_preparation   a exp:SamplePreparation ;
    		prov:startedAtTime ?Start_time;
        	prov:endedAtTime ?End_time.
	}
    OPTIONAL
    {
        ?Sample_preparation    prov:atLocation ?Location.
    }
	OPTIONAL
	{
		?Sample_preparation a exp:SamplePreparation ;
    		prov:atTime ?At_time.
	}
}
```
4d. Fabrication
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Fabrication ?At_time ?Start_time ?End_time ?Location  WHERE {
    {
		?Fabrication   a exp:Fabrication  .
	}
	OPTIONAL
	{
		?Fabrication prov:startedAtTime ?Start_time;
        	prov:endedAtTime ?End_time.
	}
    OPTIONAL
    {
        ?Fabrication    prov:atLocation ?Location.
    }
	OPTIONAL
	{
    	?Fabrication	prov:atTime ?At_time.
	}
}
```

5. Which researcher(s) have performed an experiment?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Experiment ?Measurement ?Sample_preparation ?Fabrication ?Research_user WHERE{
	{
	?Experiment a core:Experiment ; 
		prov:wasAssociatedWith ?Research_user .
	?Research_user a core:ResearchUser . 
	}
	UNION
	{
	?Measurement a exp:Measurement ; 
		prov:wasAssociatedWith ?Research_user .
	?Research_user a core:ResearchUser . 
	}
	UNION
	{
	?Sample_preparation a exp:SamplePreparation; 
		prov:wasAssociatedWith ?Research_user .
	?Research_user a core:ResearchUser . 
	}
	UNION
	{
	?Fabrication a exp:Fabrication ; 
		prov:wasAssociatedWith ?Research_user .
	?Research_user a core:ResearchUser . 
	}
}

```
6. Which samples have been used in a measurement?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Measurement ?Sample WHERE{
	?Measurement a exp:Measurement ; 
		pmd:input ?Sample .
}
```
7. Which raw data have been produced in a measurement?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Measurement ?Raw_data WHERE{
	?Measurement a exp:Measurement ; 
		pmd:output ?Raw_data .
}
```
8. Who has prepared the samples in the sample preparation step?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Sample_preparation ?Research_user WHERE{
	?Sample_preparation a exp:SamplePreparation ; 
		prov:wasAssociatedWith ?Research_user . 
	?Research_user a core:ResearchUser .
}
```
9. What process sequence taken for doing an experiment/measurement/sample preparation?
```
```
10. Which sample components is the sample made of?
```
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?Sample ?Sample_component WHERE{
	?Sample a exp:Sample ; 
		exp:hasSampleComponent ?Sample_component . 
}
```

```
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?Sample ?Sample_name ?Sample_component ?Sample_comp_name WHERE{
	?Sample a exp:Sample ; 
	rdfs:label ?Sample_name ; 
		exp:hasSampleComponent ?Sample_component . 
	?Sample_component rdfs:label ?Sample_comp_name.
}
```