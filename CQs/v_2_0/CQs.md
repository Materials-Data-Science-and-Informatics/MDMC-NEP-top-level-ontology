# Competency Questions of PRIMA
Below are the competency questions (CQs) modularized according to PRIMA modules. 

## [PRIMA-Core](#prima-core-sparql)
1. Which project(s) is the researcher member of?
2. Which study(ies) has the researcher performed?
3. Which data acquisition(s) or data analysis lifecycle(s) has the researcher performed?
4. Which research data is attributed to (e.g., created by) the researcher?
5. Which data analysis lifecycle(s) was used in a study and which data were used?
6. Which studies were done by a project and list all data acquisition and data analysis lifecycle which were done in those studies?

## [PRIMA-Data analysis lifecycle](#prima-data-analysis-lifecycle-sparql)
7. Which result(s) were obtained from the data analysis lifecycle?
8. Which data analysis(es), data processing(s) and data interpretation(s) are part of the data analysis lifecycle?
9. Which data were used and produced in the data analysis/processing/interpretation?
10. Which software was used in the data analysis/processing/interpretation?
11. Which researcher(s) did perform the data analysis/processing/interpretation?
12. Which (sub)processes to do a data analysis lifecycle, data analysis, data processing, or data intepretation?

## [PRIMA-Dataset](#prima-dataset-sparql)
13. Which project is the research data attributed to?
14. Which research data are contained in the dataset? 
15. Where is the research data/dataset/published data stored?
16. Which dataset was the publication data derived from?
17. Which metadata describes the research data?

## [PRIMA-Experiment](#prima-experiment-sparql)
18. Which fabrication(s)/sample preparation(s)/measurement(s) were performed in the study?
19. Which equipment/instrument(s) were used in the fabrication/sample preparation/measurement?
20. Which technique(s) was used in the measurement?
21. Where and when was the fabrication/sample preparation/measurement performed?
22. Which researcher(s) did perform the fabrication/sample preparation/measurement?
23. Which sample(s) was used in the measurement?
24. Which raw data was produced in the measurement?
25. Who did prepare the sample?
26. What (sub)processes taken for doing a fabrication/measurement/sample preparation?
27. Which sample component(s) is the sample made of?


# Answer to CQs via SPARQL

## PRIMA-Core SPARQL
1. Which project is researcher(s) member of?
```
PREFIX core: <https://purls.helmholtz-metadaten.de/prima/core#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?Project ?ResearchUser WHERE{
	?Project a core:Project ; 
		core:hasProjectMember ?ResearchUser .
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
	?Study prov:wasAttributedTo  ?Project  . 
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

7. Which result(s) were obtained from the data analysis lifecycle?
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
9. Which data were used and produced in the data analysis/processing/interpretation?
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
10. Which software was used in the data analysis/processing/interpretation?

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

11. Which researcher(s) did perform the data analysis/processing/interpretation?

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

12. Which (sub)processes to do a data analysis lifecycle, data analysis, data processing, or data intepretation?
```
```

## PRIMA-Dataset SPARQL

### \<still under the development\>

## PRIMA-Experiment SPARQL

18. Which fabrication(s)/sample preparation(s)/measurement(s) were performed in the study?
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
19. Which equipment/instrument(s) were used in the fabrication/sample preparation/measurement?
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
20. Which technique(s) was used in the measurement?
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
21. Where and when was the fabrication/sample preparation/measurement performed?

21a. Fabrication
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

21b. Measurement
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
21c. Sample preparation
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


22.  Which researcher(s) did perform the fabrication/sample preparation/measurement?
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
23. Which sample(s) was used in the measurement?
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
24. Which raw data was produced in the measurement?
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
25. Who did prepare the sample?
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
26. What (sub)process sequence taken for doing a fabrication/measurement/sample preparation?

26.a Fabrication
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
27. Which sample component(s) is the sample made of??
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
