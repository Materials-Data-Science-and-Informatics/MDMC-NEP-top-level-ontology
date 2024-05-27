# Competency Questions of PRIMA
Below is competency questions (CQs) modularized according to PRIMA modules. 

## [PRIMA-Core](#prima-core-sparql)
1. Which project is researcher(s) member of?
2. Which study has researcher(s) performed?
3. Which data acqusition or data analysis lifecycle has researcher(s) performed?
4. Which research data that is attributed to (e.g., created by) the researcher(s)?
5. Which data analysis lifecycle used in a study and which data are used?
6. Which studies are done by a project and  list all data acquisition and data analysis lifecycle are done in those studies?

## [PRIMA-Data analysis lifecycle](#prima-data-analysis-lifecycle-sparql)
7. Which results have been obtained from the data analysis lifecycle?
8. Which data analysis, data processing and data interpretation are part of a data analysis lifecycle?
9. Which data have been used and produced in a data analysis/processing/intreptation?
10. Which software has been used in a data analysis/processing/interpretation?
11. Which researcher(s) have performed the data analysis/processing/interpretation?
12. Which process to do a data analysis lifecycle, data analysis, data processing, or data intepretation?

## [PRIMA-Dataset](#prima-dataset-sparql)
13. Which project have the data been attributed to?
14. Which data does the dataset collects?
15. In which data collaboration platform is the data stored?
16. In which data repository is the data stored?
17. Which dataset has been the publication data derived from?
18. Which metadata has described the data?

## [PRIMA-Experiment](#prima-experiment-sparql)
19. Which fabrication/measurements/sample preparation have been performed in a study?
20. Which equipment/instrument has been used in an in a fabrication/in a measurement/in a sample preparation?
21. Which measurement techniques have been used in a measurement?
22. Where and when has the fabrication/measurement/sample preparation been performed?
23. Which researcher(s) have performed an fabrication/measurement/sample preparation?
24. Which samples have been used/prepared in a measurement?
25. Which raw data have been produced in a measurement?
26. Who has prepared the samples?
27. What process sequence taken for doing a fabrication/measurement/sample preparation?
28. Which sample components is the sample made of?


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

3. Which data acqusition or data analysis lifecycle has researcher(s) performed?

3a. Data acquisition
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?DataAcquisition ?ResearchUser WHERE{
	
	?DataAcquisition a core:DataAcquisition ; 
		prov:wasAssociatedWith ?ResearchUser.
	
}
```

3b. Data analysis lifecycle
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?DataAnalysisLifecycle ?ResearchUser WHERE{
	
	?DataAcquisition a core:DataAcquisition ; 
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
5. Which data analysis lifecycle or data acquisition used in a study and which data are used?

5a. Data analysis lifecycle 
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

5b. Data acqusition
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Study ?DataAcquisition ?ResearchData WHERE{
	?Study a core:Study; 
		core:hasDataAcquisition ?DataAcquisition.
	?DataAcquisition pmd:input ?ResearchData .
	?ResearchData a core:ResearchData.
}
```
6. Which studies are done by a project and list all data acquisition and data analysis lifecycle are done in those studies?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT  ?Project ?Study ?DataAnalysisLifecycle ?DataAcquisition WHERE{
	?Project  core:hasStudy ?Study . 
	?Study a core:Study.
	{
		?Study core:hasDataAnalysisLifecycle  ?DataAnalysisLifecycle . 
	}
	UNION
	{	
		?Study core:hasDataAcquisition  ?DataAcquisition . 
	}
}
```

## PRIMA-Data analysis lifecycle SPARQL

7. Which research data resulted from the data analysis lifecycle?
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
8. Which data analysis, data processing and data interpretation are part of a data analysis lifecycle?
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
9. Which data have been used and produced in a data analysis/processing/intreptation?
9a. Data analysis
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

9b. Data processing
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

9c. Data interpretation
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
10. Which software has been used in a data analysis/processing/interpretation?

10a. Data analysis
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

10b. Data processing
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

10c. Data interpretation
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

11. Which researcher(s) have performed the data analysis/processing/interpretation?

11a. Data analysis
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

11b. Data processing
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

11c. Data interpretation
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

12. Which process to do a data analysis lifecycle, data analysis, data processing, or data intepretation?
```
```

## PRIMA-Dataset SPARQL


## PRIMA-Experiment SPARQL

19. Which measurements/sample preparation/fabrication have been performed in a study?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Experiment ?Measurement ?Sample_preparation ?Fabrication WHERE {
    {
        ?Study a core:Study;
            exp:hasMeasurement ?Measurement .
    }
    UNION
    {
        ?Study a core:Study;
            exp:hasSamplePreparation ?Sample_preparation .
    }
    UNION
    {
        ?Study a core:Study;
            exp:hasFabrication ?Fabrication .
    }
	

}
```
20. Which equipment/instrument has been used in an Fabrication/in a measurement/in a sample preparation?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Equipment ?Fabrication ?Measurement ?Sample_preparation WHERE {
    {
        ?Fabrication a exp:Fabrication;
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
   
}

```
21. Which measurement techniques have been used in a measurement?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Measurement ?Technique  WHERE {
  ?Measurement a exp:Measurement;
    core:hasTechnique ?Technique.
}
```
22. Where and when has the fabrication/measurement/sample preparation been performed?

22a. Fabrication
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

22b. Measurement
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
22c. Sample preparation
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


23. Which researcher(s) have performed a fabrication/measurement/sample preparation?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX dal: <https://purls.helmholtz-metadaten.de/prima/dal#>
PREFIX dataset: <https://purls.helmholtz-metadaten.de/prima/dataset#>
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?Fabrication ?Measurement ?Sample_preparation  ?Research_user WHERE{
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
24. Which samples have been used in a measurement?
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
25. Which raw data have been produced in a measurement?
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
26. Who has prepared the samples in the sample preparation step?
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
27. What process sequence taken for doing an Fabrication/measurement/sample preparation?

27.a Fabrication
```
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>
PREFIX pmd: <https://w3id.org/pmd/co/>

SELECT ?last_action_lbl ?current_action_lbl  WHERE{ 
	?last_action a exp:Fabrication; 
		pmd:nextProcess ?action ;
		rdfs:label ?last_action_lbl. 

	?action rdfs:label ?current_action_lbl . 
	
}
```
28. Which sample components is the sample made of?
```
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?Sample ?Sample_component WHERE{
	?Sample a exp:Sample ; 
		exp:hasSampleComponent ?Sample_component . 
}
```

OR 

```
PREFIX exp: <https://purls.helmholtz-metadaten.de/prima/experiment#>

SELECT ?Sample ?Sample_name ?Sample_component ?Sample_comp_name WHERE{
	?Sample a exp:Sample ; 
	rdfs:label ?Sample_name ; 
		exp:hasSampleComponent ?Sample_component . 
	?Sample_component rdfs:label ?Sample_comp_name.
}
```