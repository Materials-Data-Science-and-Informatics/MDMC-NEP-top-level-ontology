## Institution
1. Which Laboratories are hosted by the Institution?
2. Which Equipment is available at the Institution?
3. Which Instruments are available at the Institution?
4. Which Measurement Techniques are available at the Institution?
5. Which Experiments have been performed at the Institution?
6. Which Measurements have been performed at the Institution?
7. Which Raw Data have been produced at the Institution?

## Laboratory
8. By which Institution is the Laboratory hosted?
9. Which Equipment is available in the Laboratory?
10. Which Instruments are available in the Laboratory?
11. Which Measurement Techniques are available in the Laboratory?
12. Which Experiments have been performed in the Laboratory?
13. Which Measurements have been performed in the Laboratory?
14. Which Raw Data have been produced in the Laboratory?

## Research User
15. Which Projects is the Research User member of?
16. Which Studies has the Research User performed?
17. Which Experiments has the Research User performed?
18. Which Measurements has the Research User performed?
19. Which Instruments has the Research User used?
20. Which Samples has the Research User used?
21. Which Data Analysis Lifecycles has the Research User performed?
22. Which Data has the Research User produced?
23. Which Data has the Research User published?

## Project
24. Which Research Users are member of the Project?
25. Which Studies have been attributed to the Project?
26. Which Experiments have been attributed to the Project?
27. Which Measurements have been attributed to the Project?
28. Which Instruments have been attributed to the Project?
29. Which Samples have been attributed to the Project?
30. Which Data Analysis Lifecycles have been attributed to the Project?
31. Which Research Data have been attributed to the Project?
32. Which Publication Data have been attributed to the Project?

## Study
33. Which Project has the Study been attributed to?
34. Which Research Users have performed the Study?
35. Which Experiments have been performed in the Study?
36. Which Measurements have been performed in the Study?
37. Which Instruments have been used in the Study?
38. Which Samples have been used in the Study?
39. Which Data Analysis Lifecycles have been performed in the Study?
40. Which Research Data have been produced in the Study?
41. Which Publication Data have been produced in the Study?
42. At which Institutions has the Study been conducted?

## Experiment
43. Which Project has the Experiment been attributed to?
44. Which Study is the Experiment part of?
45. Which Measurements have been performed in the Experiment?
46. Which Equipment has been used in the Experiment?
47. Which Instruments have been used in the Experiment?
48. Which Measurement Techniques have been used in the Experiment?
49. Has the Experiment included any Sample Preparations?
50. Which Samples have been used in the Experiment?
51. Which Samples have been prepared in the Experiment?
52. Where has the Experiment been performed?
53. When has the Experiment been performed?
54. Which Research Users have performed the Experiment?
55. Which Raw Data have been produced in the Experiment?

## Measurement
56. Which Project has the Measurement been attributed to?
57. Which Study is the Measurement part of?
58. Which Experiment is the Measurement part of?
59. Which Equipment has been used in the Measurement?
60. Which Instrument has been used in the Measurement?
61. Which Measurement Technique has been used in the Measurement?
62. Which Samples have been used in the Measurement?
63. Which Samples have been prepared for the Measurement?
64. Which Sample Carrier has been used in the Measurement?
65. Which Raw Data have been produced in the Measurement?

## Sample
66. Which Project has the Sample been attributed to?
67. In which Studies has the Sample been prepared?
68. In which Studies has the Sample been used?
69. In which Experiment has the Sample been prepared?
70. In which Experiments has the Sample been used?
71. Which Measurements has the Sample been prepared for?
72. In which Measurements has the Sample been used?
73. How has the Sample been prepared?
74. Has the Sample been prepared by Research Users?
75. Which Research Users has prepared the Sample?
76. Which Sample Components is the Sample made of?
77. Which Sample Components have been used in the Sample Preparation?
78. Which Sample Components have been used in the Sample Component Synthesis?
79. Which Equipment has been used to prepare the Sample?
80. Where has the Sample been prepared?
81. When has the Sample been prepared?
82. Which Research Data have been related to the Sample?
83. Which Publication Data have been related to the Sample?

## Data Analysis Lifecycle
84. Which Project has the Data Analysis Lifecycle been attributed to?
85. Which Study is the Data Analysis Lifecycle part of?
86. Which Research Users have performed the Data Analysis Lifecycle?
87. Which Research Data have been used for the Data Analysis Lifecycle?
88. Which Results have been obtained from the Data Analysis Lifecycle?
89. Which processes have been members of the Data Analysis Lifecycle?
90. Has Data Processing been member of the Data Analysis Lifecycle?

## Data 
91. Which Research Data have been used in Data Processing?
92. Which Research Data have been produced in Data Processing?
93. Which Software has been used in Data Processing?
94. Which Research Users have performed the Data Processing?
95. Has Data Analysis been member of the Data Analysis Lifecycle?

## Data Analysis
96. Which Research Data have been used in Data Analysis?
97. Which Research Data have been produced in Data Analysis?
98. Which Data Analysis Software has been used in Data Analysis?
99. Which Research Users have performed the Data Analysis?

## Data Interpretation
100. Has Data Interpretation been member of the Data Analysis Lifecycle?
101. Which Research Data have been used in Data Interpretation?
102. Which Reference Data have been used in Data Interpretation?
103. Which Software have been used in Data Interpretation?
104. Which Research Users have performed the Data Interpretation?
105. Which Result have been obtained from the Data Interpretation?

## Data
106. Which Project have the Research Data been attributed to?
107. Which Research Users have produced the Research Data?
108. At which Institutions have the Raw Data been produced?
109. In which Study have the Research Data been produced?
110. In which Experiments have the Raw Data been produced?
111. In which Measurements have the Raw Data been produced?
112. Which Instruments have been used to produce the Raw Data?
113. Which Samples have been used in the Measurement to produce the Raw Data?
114. Which Data Analysis have been performed to produce the Analysed Data?
115. Which Data Analysis software has been used to produce the Analysed Data?
116. Which Research Data does the Dataset collects?
117. In which Data Collaboration Platform is Research Data stored?
118. In which Data Repository is Research Data stored?
119. Which Dataset has been Publication Data derived from?
120. Which Metadata has described Research Data?



## Answer to CQs via SPARQL

CQ39. Which Data Analysis Lifecycles have been performed in the Study?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?data_analysis_lifecycle ?study WHERE{
	?study mdmc:hasDataAnalysisLifeCycle ?data_analysis_lifecycle

}
```
CQ40. Which Research Data have been produced in the Study?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?research_data ?study WHERE{
	?study mdmc:hasExperiment ?experiment. 
	?experiment mdmc:hasMeasurement ?measurement.
	?research_data prov:wasGeneratedBy ?measurement.
	?research_data a mdmc:ResearchData.
	
}
```
CQ43. Which Project has the Experiment been attributed to?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?project ?experiment WHERE{
	?project mdmc:hasStudy ?study.
	?study mdmc:hasExperiment ?experiment.
	?experiment a mdmc:Experiment.
	
}
```
CQ44. Which Study is the Experiment part of?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?study ?experiment WHERE{
	?study mdmc:hasExperiment ?experiment.
	?experiment a mdmc:Experiment.
	
}
```
CQ46. Which Equipment has been used in the Experiment?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?equipment ?experiment WHERE{
	?experiment mdmc:hasMeasurement ?measurement. 
	?measurement prov:wasAssociatedWith ?equipment. 
	?equipment a mdmc:Equipment. 	
}
```
CQ47. Which Instruments have been used in the Experiment?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?instrument ?experiment WHERE{
	?experiment mdmc:hasMeasurement ?measurement. 
	?measurement prov:wasAssociatedWith ?instrument. 
	?instrument a mdmc:Instrument. 	
}
```
CQ53. When has the Experiment been performed?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  

SELECT  ?experiment ?start_time ?end_time WHERE{
	?experiment prov:startedAtTime ?start_time ;
	prov:endedAtTime ?end_time.	
}
```
CQ55. Which Raw Data have been produced in the Experiment?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?raw_data ?experiment WHERE{
	?experiment mdmc:hasMeasurement ?measurement.
	?raw_data prov:wasGeneratedBy ?measurement;
	 a mdmc:RawData.
}
```
CQ56. Which Project has the Measurement been attributed to?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT   ?measurement ?project WHERE{
	?project mdmc:hasStudy ?study.
	?study mdmc:hasExperiment ?experiment.
	?experiment mdmc:hasMeasurement ?measurement.
}
```
CQ57. Which Study is the Measurement part of?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT    ?study ?measurement WHERE{
	?study mdmc:hasExperiment ?experiment.
	?experiment mdmc:hasMeasurement ?measurement.
}
```
CQ58. Which Experiment is the Measurement part of?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT    ?experiment ?measurement WHERE{
	?experiment mdmc:hasMeasurement ?measurement.
}
```
CQ59. Which Equipment has been used in the Measurement?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?equipment ?measurement WHERE{ 
	?measurement prov:wasAssociatedWith ?equipment. 
	?equipment a mdmc:Equipment. 	
}
```
CQ60. Which Instrument has been used in the Measurement?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?instrument ?measurement WHERE{ 
	?measurement prov:wasAssociatedWith ?instrument. 
	?instrument a mdmc:Instrument. 	
}
```
CQ65. Which Raw Data have been produced in the Measurement?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT  ?equipment ?measurement WHERE{ 
	?measurement prov:wasAssociatedWith ?equipment. 
	?equipment a mdmc:Equipment. 	
}
```
CQ84. Which Project has the Data Analysis Lifecycle been attributed to?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?project ?data_analysis_lifecycle WHERE{
	?project a mdmc:Project;
        mdmc:hasStudy ?study. 
    ?study mdmc:hasDataAnalysisLifeCycle ?data_analysis_lifecycle .
}
```
CQ85. Which Study is the Data Analysis Lifecycle part of?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?study ?data_analysis_lifecycle WHERE{
	?study a mdmc:Study; 
        mdmc:hasDataAnalysisLifeCycle ?data_analysis_lifecycle .
}
```
CQ86. Which Research Users have performed the Data Analysis Lifecycle?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?research_user ?data_analysis_lifecycle WHERE{
    ?data_analysis_lifecycle a mdmc:DataAnalysisLifeCycle ; 
        prov:wasAssociatedWith ?research_user . 
	
}
```
CQ87. Which Research Data have been used for the Data Analysis Lifecycle?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?data_analysis_lifecycle ?research_data WHERE{
	?data_analysis_lifecycle a mdmc:DataAnalysisLifeCycle ; 
        prov:used ?research_data. 
    ?research_data a mdmc:ResearchData.
}
```
CQ88. Which Results have been obtained from the Data Analysis Lifecycle?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?data_analysis_lifecycle_member ?result_data WHERE{
    ?result_data prov:wasGeneratedBy ?data_analysis_lifecycle_member .
    ?data_analysis_lifecycle_member mdmc:isMemberOf ?data_analysis_life_cycle .  
}

```
CQ89. Which processes have been members of the Data Analysis Lifecycle?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?process ?data_analysis_lifecycle WHERE{
	?process mdmc:isMemberOf ?data_analysis_lifecycle .


}
```
CQ90. Has Data Processing been member of the Data Analysis Lifecycle?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?data_processing ?data_analysis_lifecycle WHERE{
	?data_processing a mdmc:DataProcessing ; 
        mdmc:isMemberOf ?data_analysis_lifecycle.

}
```
CQ91. Which Research Data have been used in Data Processing?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?Research_Data ?Data_Processing WHERE{
         ?Data_Processing a mdmc:DataProcessing ; 
        prov:used ?Research_Data. 
       ?Research_Data a mdmc:ResearchData
}
```
CQ92. Which Research Data have been produced in Data Processing?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?Research_Data ?Data_Processing WHERE{
         ?Research_Data a mdmc:ResearchData ; 
        prov:wasGeneratedBy ?Data_Processing. 
   
}
```
CQ93. Which Software has been used in Data Processing?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 
SELECT ?Software ?Data_Processing WHERE{
	?software a prov:SoftwareAgent ; 
        prov:used ?Data_processing. 
    ?Data_processing a mdmc:DataProcessing.
}
```
CQ94. Which Research Users have performed the Data Processing
```
CQ95. Has Data Analysis been member of the Data Analysis Lifecycle?
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?data_Analysis ?data_analysis_lifecycle WHERE{
	?data_Analysis a mdmc:DataAnalysis ; 
        mdmc:isMemberOf ?data_analysis_lifecycle.
        ?data_analysis_lifecycle a mdmc:DataAnalysisLifeCycle

}
```
CQ96. Which Research Data have been used in Data Analysis?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?Research_Data ?Data_Analysis WHERE{
         ?Data_Analysis a mdmc:DataAnalysis ; 
        prov:used ?Research_Data. 
        ?Research_Data a mdmc:ResearchData
   
}
```
CQ97. Which Research Data have been produced in Data Analysis?
```
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?Research_Data ?Data_Analysis WHERE{
         ?Research_Data a mdmc:ResearchData ; 
        prov:wasGeneratedBy ?Data_Analysis. 
        ?Data_Analysis a mdmc:DataAnalysis
   
}
```
CQ98. Which Data Analysis Software has been used in Data Analysis?
```
CQ99. Which Research Users have performed the Data Analysis?
PREFIX mdmc: <https://raw.githubusercontent.com/Materials-Data-Science-and-Informatics/MDMC-NEP-top-level-ontology/master/mdmc-nep-top-level-ontology.owl#>
PREFIX prov: <http://www.w3.org/ns/prov#> 

SELECT ?research_user ?data_analysis WHERE{
    ?data_analysis a mdmc:DataAnalysis ; 
        prov:wasAssociatedWith ?research_user . 
	
}
```
