# Issues identified


## 1. Issues with stations and metadata

| ID |                  Issue                  | Resolved |                       Comment                       |
|:--:|:---------------------------------------:|:--------:|:---------------------------------------------------:|
| 1  | 2 stations missing spatial co-ordinates | 1        | See e-mail from Kjetil received 08.10.2020 at 23.22 |
| 2  | 6 stations missing Vannmiljø codes      | 1        | See e-mail from Kjetil received 08.10.2020 at 23.22 |


## 2. Issues with the historic (Vannmiljø) dataset

**Note:** This project focuses primarily on quality assessing the new data, and a comprehensive review of the data in Vannmiljø is therefore beyond scope. Nevertheless, the following issues with the Vannmiljø dataset have been identified.

| ID |                                                    Issue                                                    | Resolved |                            Comment                            |
|:--:|:-----------------------------------------------------------------------------------------------------------:|:--------:|:-------------------------------------------------------------:|
| 1  | More than 1100 duplictaed samples in Vannmiljø dataset                                                      | 0        | Duplicates are currently removed from the analysis            |
| 2  | TEMP out of range in Vannmiljø dataset                                                                      | 0        | Values removed                                                |
| 3  | KOND out of range in Vannmiljø dataset                                                                      | 0        | Values removed                                                |
| 4  | LAL out of range in Vannmiljø dataset                                                                       | 0        | Values removed                                                |
| 5  | SO4 out of range in Vannmiljø dataset                                                                       | 0        | Values removed                                                |
| 6  | CA out of range in Vannmiljø dataset                                                                        | 0        | Values removed                                                |
| 7  | Possible outliers: values of ALK > 1 mmol/l reported by NIVA   (2012-15)                                    | 0        |                                                               |
| 8  | Possible outliers: values of ANC > 1000 µekv/l reported by   NIVA (2012-15)                                 | 0        |                                                               |
| 9  | Possible outliers: values of CA > 100 mg/l reported by NIVA   (2012-15)                                     | 0        |                                                               |
| 10 | Possible outliers: values of CL > 30 mg/l reported by both   NIVA (2012-15) and VestfoldLAB (2016-19)       | 0        |                                                               |
| 11 | Possible outliers: values of KOND > 100 mS/m reported by   NIVA (2012-15)                                   | 0        |                                                               |
| 12 | Possible outliers: values of K > 2 mg/l reported by   VestfoldLAB (2016-19)                                 | 0        |                                                               |
| 13 | Possible outliers: values of MG > 10 mg/l reported by NIVA   (2012-15)                                      | 0        |                                                               |
| 14 | Possible outliers: values of N-NO3 > 2000 µg/l N reported by   VestfoldLAB (2016-19)                        | 0        |                                                               |
| 15 | Possible outliers: values of N-TOT > 2000 µg/l N reported by   VestfoldLAB (2016-19)                        | 0        |                                                               |
| 16 | Possible outliers: values of NA > 10 mg/l reported by both   NIVA (2012-15) and VestfoldLAB (2016-19)       | 0        |                                                               |
| 17 | Possible outliers: values of P-TOT > 100 µg/l P reported by   both NIVA (2012-15) and VestfoldLAB (2016-19) | 0        |                                                               |
| 18 | Possible outliers: values of PH < 4 reported by NIVA   (2012-15)                                            | 0        |                                                               |
| 19 | Possible outliers: values of PH > 9.5 reported by   VestfoldLAB (2016-19)                                   | 0        |                                                               |
| 20 | Possible outliers: values of RAL > 250 µg/l Al reported by   both NIVA (2012-15) and VestfoldLAB (2016-19)  | 0        |                                                               |
| 21 | Possible outliers: values of SO4 > 5 mg/l reported by both   NIVA (2012-15) and VestfoldLAB (2016-19)       | 0        |                                                               |
| 22 | N-NO3 from VestfoldLAB (2016-19) reported as N-SNOX                                                         | 0        | Assume N-SNOX ~ N-NO3 in quality assurance workflow           |
| 23 | SIO2 from VestfoldLAB (2016-19) reported in mg/l SiO2 instead of   ug/l Si                                  | 0        | Apply correction factor of ~468 in quality assurance workflow |


## 3. Issues with the "new" (VestfoldLAB 2020) dataset

| ID |                                        Issue                                       | Resolved |                                         Comment                                         |
|:--:|:----------------------------------------------------------------------------------:|:--------:|:---------------------------------------------------------------------------------------:|
| 1  | TOC LOQ incorrectly reported in VestfoldLAB dataset                                | 1        | Change values of 0 to 0.25 (cell comment "Mindre enn verdi: <0.50")                     |
| 2  | TOC values below LOQ in VestfoldLAB dataset                                        | 1        | This is OK - see emails from Kjetil (and Roy) received 20.10.2020 at 12.12              |
| 3  | CA LOQ incorrectly reported in VestfoldLAB dataset                                 | 1        | Change values of 0 to 0.01 (cell comment "Mindre enn verdi: <0.02")                     |
| 4  | SIO2 LOQ incorrectly reported in VestfoldLAB dataset                               | 1        | Change values of 0 to 0.025 (cell comment "Mindre enn verdi: <0.05")                    |
| 5  | RAl, LAl and ILAl reported as 0 in VestfoldLAB dataset                             | 1        | Considered acceptable - see emails from Kjetil (and Roy) received 20.10.2020 at 12.12   |
| 6  | 116 duplicates in the VestfoldLAB dataset                                          | 0        | Communicated to VestfoldLAB; Duplicates are currently removed from the analysis         |
| 7  | Possible outliers: values of N-NO3 > 2000 µg/l N reported by   VestfoldLAB in 2020 | 0        |                                                                                         |
| 8  | Possible outliers: values of N-TOT > 2000 µg/l N reported by   VestfoldLAB in 2020 | 0        |                                                                                         |
| 9  | Possible outliers: values of P-TOT > 100 µg/l P reported by   VestfoldLAB in 2020  | 0        |                                                                                         |
| 10 | Possible outlier samples in VestfoldLAB dataset                                    | 0        |                                                                                         |
| 11 | Possible issues with sampling frequency in VestfoldLAB dataset                     | 0        |                                                                                         |