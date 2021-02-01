# Tiltaksovervakingen: opsjon for kvalitetskontroll av analysedata

This repository contains code for quality-checking and visualising data from externel labs (VestfoldLAB and Eurofins) by comparing against historic data exported from [Vannmiljø](https://vannmiljo.miljodirektoratet.no/). 

## Project background

Since 2012, the "Tiltaksovervakingen" project has collected data to assess the effects of liming at [more than 200 stations across southern Norway](https://nivanorge.github.io/tiltaksovervakingen/pages/stn_map.html). NIVA was responsible for analysing the water chemistry data from this project between 2012 and 2015, then VestfoldLAB took over from 2016 to August 2020, and from September 2020 onwards the analyses will be carried out by Eurofins. 

Data from 2012 to 2019 have been quality checked and are available in Vannmiljø. Data from VestfoldLAB from January to August 2020 are not yet quality assessed but have been provided by VestfoldLAB in an Excel spreadsheet. We have also agreed with [Miljødirektoratet](https://www.miljodirektoratet.no/) that future data from Eurofins will be provided using a broadly similar Excel template to ensure the input format remains consistent.

**The aim of this workflow is to quality assess the "new" data and to highlight "outliers" for further investigation and reanalysis**. Since the project collects a lot of water samples, manually checking everything is not feasible. The task here is to implement semi-automatic data "screening" to identify a subset of the data for more thorough manual assessment. 

The first "new" dataset to be considered is the 2020 dataset from VestfoldLAB.

## Quality checks performed

A table summarising the quality assurance checks implemented can be found [here](https://nivanorge.github.io/tiltaksovervakingen/pages/list_quality_checks.html).

## Workflow and results

 1. **[Initial exploration and data cleaning](https://nbviewer.jupyter.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/01_data_processing.ipynb)**. An initial exploration of the data, aiming to create a tidy dataset for further analysis
 
 2. **[Station map](https://nivanorge.github.io/tiltaksovervakingen/pages/stn_map.html)**. An interactive map showing station locations
 
 3. **[Investigating distributions](https://nivanorge.github.io/tiltaksovervakingen/pages/distribution_plots.html)**.  Interactive plots showing the **overall** data distribution for each parameter and time period can be found **[here](https://nivanorge.github.io/tiltaksovervakingen/pages/distribution_plots.html)** (please allow time for the plots to load after clicking the link). The plots are generated by code in **[this](https://nbviewer.jupyter.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/02_distribution_plots.ipynb)** notebook and there is some initial interpretation **[here](https://nbviewer.jupyter.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/02_distribution_plots.ipynb#3.-Summary)**
 
 4. **[Outlier detection at water sample level](https://nbviewer.jupyter.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/03_outlier_detection.ipynb)**. Using the **[Isolation Forest](https://scikit-learn.org/stable/modules/outlier_detection.html#isolation-forest)** algorithm to detect unusual water samples based on multivariate parameter data. *Work in progress...*
 
 5. **[Exploring time series](https://nbviewer.jupyter.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/04_timeseries.ipynb)**. Checking the sampling frequency is as expected and looking for spikes and step-changes in the time series for individual stations. Interactive plots **[here](https://nivanorge.github.io/tiltaksovervakingen/pages/timeseries_plots.html)**
 
 6. **[Exploring unusual results for aluminium](https://nbviewer.jupyter.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/05_explore_al_fracs.ipynb)**. Investigating values for RAl, ILAl and LAl in 2019 and 2020
 
## Issues identified

Tables summarising the issues identifed so far (and possible resolutions, if known) are [here](https://nivanorge.github.io/tiltaksovervakingen/pages/issues_identified.html).