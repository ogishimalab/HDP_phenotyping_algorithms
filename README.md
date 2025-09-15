# HDP phenotyping algorithms

This project implements phenotyping algorithms for Hypertensive Disorders of Pregnancy (HDP), based on the methods described in [Mizuno et al. (2024), “Development of phenotyping algorithms for hypertensive disorders of pregnancy (HDP) and their application in more than 22,000 pregnant women”](https://www.nature.com/articles/s41598-024-55914-9).

This project provides a reproducible and programmable framework for identifying cases of hypertensive disorders of pregnancy (HDP) and their subtypes with high precision from large-scale cohort datasets. By combining structured data such as blood pressure readings and proteinuria measurements with unstructured clinical notes, the algorithms enable researchers to construct accurate cohorts suitable for maternal health studies. This approach supports a wide range of applications, including epidemiological analyses, precision medicine, and genetic or phenotypic association studies, by ensuring that HDP cases are consistently and systematically defined across diverse data sources.

Phenotyping algorithms for Hypertensive Disorders of Pregnancy (HDP) are the followings:
| Algorithm       | Based on which guideline                                                            | Key additional criteria used                                                                                                                                                                          |
| --------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ACOG guideline algorithm | American College of Obstetricians and Gynecologists (ACOG) guideline) | Uses hypertensive disease history, blood pressure (BP) readings, proteinuria (PU), timing of onset, and preeclampsia-related clinical conditions.)                                       |
| JSOG guideline algorithm | Japan Society of Obstetrics and Gynecology (JSOG) guideline)          | In addition to the criteria in ACOG gudeline algorithm , includes maternal organ dysfunction and “light-for-date” (i.e. fetal growth restriction), both drawn also from unstructured clinical notes.|

[1]: https://www.nature.com/articles/s41598-024-55914-9 "Development of phenotyping algorithms for hypertensive disorders of pregnancy (HDP) and their application in more than 22,000 pregnant women | Scientific Reports"

## Requirements
Python Python 2.7.5 and Perl 5.16.3

## Input file format
- input_file.csv
	- Input file must wide format.
	- The input file is consist of structured clinical data including
		- values of systonic and diastolic blood pressure, and those collected date (corresponding header : "SBP","DBP", "Measurement date(SBP)"and "Measurement date(DBP)", respectively)
		- values of proteinuria dipstick and those collection date (corrresponding header : "PU" and "Measurement date(PU)")
			- Note
				- coding of PU is as followings; 01=-, 02=±, 03=+, 04=2+, 05=3+
				- The values and collection date must correspond in order.
		- Expected day
		- Delivery day
- clinical_notes.csv
	- Clinical notes file must narrow format. 
	- The clinical notes file is consist of unstructured clinical note and values of GOT, GPT and PLT.
	- The column 1 must item code, column 7 must values or discriptions and column 13 must ID. 
	- The item codes for clinical notes file are as followings; 
		- 000001:the interview of first visit
		- 000002:first item of clinical notes of prenatal checkup
		- 000003:second item of clinical notes of prenatal checkup
		- 000004:first clinical notes at delivery
		- 000005:second clinical notes at delivery
		- 000006:third clinical notes at delivery
		- 000007:value of GOT
		- 000008:value of GPT
		- 000009:value of PLT
	
## License
HDP phenotyoing algorithms are under [GPLv2 license](https://choosealicense.com/licenses/gpl-2.0/).
