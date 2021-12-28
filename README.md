# HDP_phenotyping_algorithms
Phenotyping algorithms for Hypertensive Disorders of Pregnancy (HDP)
* Algorithm 1 
The implecation of a HDP phenotyping algorithm according to American college of obstetricians and gynecologists (ACOG) guidline. 
* Algorithm 2
The implecation of a HDP phenotyping algorithm according to Japan society of obestrics and gynecology (JSOG) guidline. 

# Requirements
Python Python 2.7.5 and Perl 5.16.3

# Input file format
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
	
# License
HDP phenotyoing algorithms are under [GPLv2 license](https://choosealicense.com/licenses/gpl-2.0/).