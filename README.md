# Tiltaksovervakingen: opsjon for kvalitetskontroll av analysedata

This repository contains code for quality-checking and visualising data from externel labs (Vestfold Lab and Eurofins) against historic data exported from [Vannmiljø](https://vannmiljo.miljodirektoratet.no/). 

## Project background

Since 2012, the "Tiltaksovervakingen" project has collected data to assess the effects of liming at more than 200 stations across southern Norway. NIVA was responsible for analysing water chemistry data from this project between 2012 and 2015, then VestfoldLAB took over from 2016 to August 2020, and from September 2020 onwards the analyses will be carried out by Eurofins. 

Data from 2012 to 2019 have been quality checked and are available in Vannmiljø. Data from VestfoldLAB from January to August 2020 are not yet quality assessed but have been provided by VestfoldLAB. We have also agreed with Miljødirektoratet that future data from Eurofins will be provided using a broadly similar Excel template to ensure the input data format remains consistent.

**The aim of this workflow is to quality assess the "new" data and to highlight "outliers" for further investigation and possible reanalysis**. Since the project collects a lot of water samples, manually checking everything is not feasible. The task here is to implement semi-automatic data "screening" to identify a subset of the data for more thorough manual assessment. The first "new" dataset to be considered is the 2020 dataset from VestfoldLAB.

## Workflow and results

 * **[Notebook 1: Initial exploration and data cleaning](https://nbviewer.jupyter.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/01_data_processing.ipynb)**. An initial exploration of the data, aiming to create a tidy dataset for further analysis
 
 * **[Station map](https://nivanorge.github.io/tiltaksovervakingen/pages/stn_map.html)**. An interactive map showing station locations
 
 * **[Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/pages/distribution_plots.html)**. Exploring the **overall** data distribution for each parameter, by comparing 
 