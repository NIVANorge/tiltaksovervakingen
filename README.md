# Tiltaksovervakingen: opsjon for kvalitetskontroll av analysedata

This repository contains code for quality-checking and visualising data from external labs (VestfoldLAB and Eurofins) by comparing against historic data exported from [Vannmiljø](https://vannmiljo.miljodirektoratet.no/). 

## Project background

Since 2012, the "Tiltaksovervakingen" project has collected data to assess the effects of liming at [more than 200 stations across southern Norway](https://nivanorge.github.io/tiltaksovervakingen/pages/stn_map.html). NIVA was responsible for analysing the water chemistry data from this project between 2012 and 2015, then VestfoldLAB took over from 2016 to August 2020, and from September 2020 onwards the analyses will be carried out by Eurofins. 

Data from 2012 to 2019 have been previously quality checked and are available in Vannmiljø. Data from VestfoldLAB from January to August 2020 were provided by VestfoldLAB in an Excel spreadsheet, and we have agreed with [Miljødirektoratet](https://www.miljodirektoratet.no/) that future data from Eurofins will be provided using the same template.

**The aim of this workflow is to quality assess the "new" data and to highlight "outliers" for further investigation and reanalysis**.

## Stations

An interactive map showing station locations is [here](https://nivanorge.github.io/tiltaksovervakingen/pages/stn_map.html).

## Quarterly quality checking

Each quarter, the lab submits data for assessment. The initial dataset is labelled "v1". Various tests are performed to identify data issues and the feedback provided to the lab. Following reanalysis, a second dataset may be provided ("v2"). When available, this is checked again to ensure problems highlighted in v1 have been fixed.

**Note:** In many cases, reanalysis by the lab will confirm the original extreme values. In such cases, many of the outliers will still be present in v2 of the dataset. The aim of this workflow is to highlight outliers and possible bad data, but it is up to the lab (not NIVA) to decide which data are ultimately submitted to Vannmiljø. 

### Eurofins 2020 Q4 (v1)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2020_q4/01_data_processing.ipynb#9.-Version-1-summary)
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2020_q4_v1/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2020_q4_v1/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2020_q4_v1/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2020_q4_v1/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2020_q4_v1/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2020_q4_v1/al_fracs_displots_by_period.png) 

### Eurofins 2021 Q1 (v1)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q1/01_data_processing.ipynb#9.-Version-1-summary)
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q1_v1/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q1_v1/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q1_v1/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q1_v1/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q1_v1/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q1_v1/al_fracs_displots_by_period.png)
 
### Eurofins 2021 Q1 (v2)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q1/01_data_processing.ipynb#10.-Version-2-summary-(02.02.2022))
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q1_v2/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q1_v2/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q1_v2/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q1_v2/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q1_v2/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q1_v2/al_fracs_displots_by_period.png) 
 
### Eurofins 2021 Q2 (v1)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q2/01_data_processing.ipynb#9.-Version-1-summary)
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q2_v1/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q2_v1/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q2_v1/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q2_v1/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q2_v1/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q2_v1/al_fracs_displots_by_period.png) 
 
### Eurofins 2021 Q2 (v2)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q2/01_data_processing.ipynb#10.-Version-2-summary-(02.02.2022))
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q2_v2/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q2_v2/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q2_v2/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q2_v2/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q2_v2/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q2_v2/al_fracs_displots_by_period.png) 
 
### Eurofins 2021 Q3 (v1)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q3/01_data_processing.ipynb#9.-Version-1-summary)
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q3_v1/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q3_v1/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q3_v1/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q3_v1/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q3_v1/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q3_v1/al_fracs_displots_by_period.png) 
 
### Eurofins 2021 Q3 (v2)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q3/01_data_processing.ipynb#10.-Version-2-summary-(02.02.2022))
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q3_v2/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q3_v2/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q3_v2/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q3_v2/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q3_v2/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q3_v2/al_fracs_displots_by_period.png)
 
### Eurofins 2021 Q4 (v1)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q4/01_data_processing.ipynb#9.-Version-1-summary)
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q4_v1/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q4_v1/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q4_v1/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q4_v1/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q4_v1/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q4_v1/al_fracs_displots_by_period.png) 
 
### Eurofins 2021 Q4 (v2)

 * [Summary of basic checks](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q4/01_data_processing.ipynb#10.-Version-2-summary-(25.02.2022))
 * [Distribution plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q4_v2/distribution_plots.html) 
 * [Time series outlier plots](https://nivanorge.github.io/tiltaksovervakingen/output/eurofins_2021_q4_v2/timeseries_plots.html)  
 * [Table of time series outliers](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q4_v2/timerseries_outliers.csv)
 * Water sample level outliers ([table](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q4_v2/isoforest_ca_ph.csv) and [plot](https://github.com/NIVANorge/tiltaksovervakingen/blob/master/output/eurofins_2021_q4_v2/isoforest_ca_ph_plot.png))
 * [Distributions for aluminium](https://raw.githubusercontent.com/NIVANorge/tiltaksovervakingen/master/output/eurofins_2021_q4_v2/al_fracs_displots_by_period.png) 

## Workflow details

The notebooks below are run each quarter.

 1. [Initial exploration and data cleaning](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q1/01_data_processing.ipynb)
 
 2. [Investigating distributions](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q1/02_distribution_plots.ipynb)
 
 3. [Outlier detection at water sample level](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q1/03_outlier_detection.ipynb)
 
 4. [Outlier detection for time series](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q1/04_timeseries.ipynb)
 
 5. [Exploring distributions for aluminium](https://nbviewer.org/github/NIVANorge/tiltaksovervakingen/blob/master/notebooks/eurofins_2021_q1/05_explore_al_fracs.ipynb)