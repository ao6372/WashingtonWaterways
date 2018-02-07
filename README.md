
<img src="images/salmonculvert.jpg" 
 width="240" height="200" border="10" />

## The Culvert Case 

Culverts are water crossing structures for waterways that are too small to justify a bridge. 
Culverts can support support traffic overhead and salmon migration pathways below.  Due to climate change, river behaviors are 
changing and the bankflow width is likely to vary at a higher rate than previously. Culverts are usually designed for 30-50 year lifetime 
and must be able to allow salmon migration during this period due to the court case United States v. Washington.

In the Culvert Case, Washington State government was ordered by a federal court to replace all state - owned culverts located on 
the Olympic Peninsula, in the Puget Sound Basin, or in the Chehalis River Basin that block 200 meters or more of salmon habitat. 
About 10,000 culverts are estimated to fit that description, and their replacement with culverts that pass fish is estimated to 
cost about $2.45 billion.

## Climate Change Impacts on Washington

Climate change will increase proportion of preciptiation that fallas as rain rather than snow, resulting in increased volume in peak flows. The increase in flow will alter channel morphology and thus require wider culverts.  From the latest ruling, Washington State is responsible for identifying the culverts that will not be viable for salmon migration and replace them. Given that the replacement process is already very costly and time consuming, the greatest financial loss would occur if the culvert replacement did not account for stream width change and warranted multiple replacements. 

The goal of this project is to translate large meteorological datasets into a tool that can directly be applied to the design of water crossing structures. The qualitative results must be presented in a way that conveys risk to stakeholders such as county civil engineers and lawmakers. The CIG will continue to aggregate new data and consider different carbon emissions cases. I have designed my code and model to accommodate their database structure and current data reporting formats. 


## Dataset and Preparation 

I collaborated with the University of Washington Climate Impacts group (CIG) to study meteorological data through rigorous climate change models and develop a tool to represent the probability of stream width change over the design lifetime of a culvert. There are 10 models selected by CIG and each one provides daily projected stream flow for certain latitude and longitude for the next 100 years. Multi-model ensembles are considered the best way to estimate uncertainty for climate projections. These models were developed by several academic institutions and the results vary, but are considered to be equally likely in their predictions. 

These models generated 949 Gb of raw flow data each in NetCDF format. The state of Washington is divided into 1/16 degree latitude and longitude coordinates resulting in roughly 10,000 coordinates with unique weather pattern activity.

## Model and Processing
We are examining extreme values over 100 years of data to extract an estimate for the bankfull width (stream width when at maximum capacity of the channel) of a stream for a given water year (defined as Oct 1 - Sept 30). I learned to use NetCDF4 (Python API for NetCDF) to compile the raw data and extract the most extreme flow values for each water year and model. The raw data is the daily projected volumetric flow rate (cubif feet per second) for each latitude and longitude combination in Washington State. These values are saved for each model in the reference_csv folder. 

I used scipy.stats to model a general extreme value distribution (GEV) using the past 30 years of data. The GEV is selected becuase extensive research and atmospheric science standards have shown this distribution to be the maximum likelihood estimator for climate change assesment studies. Therefore, it is the best way to fit future data. Also, the GEV combines three different distributions based on shape parameter so it is much more flexible. 

I generated a GEV for each year (2015 to 2099) using the past 30 years of data to the respective year. We chose to consider the past 30 years to make each GEV because it allows for optimal sample size and predictive ability. The L-Moments (shape, scale, and location) were calculated based on the methods from the publication "Estimation of the Generalized Extreme-Value Distribution by the Method of Probability-Weighted Moments" by Hosking in the folder reference_publications. 

To understand probability and range of values, we bootstrapped 20 out of 30 data points and made 1000 GEV distributions. There are three distinct climate regions in the Washington state (Pacific Maritime, Western Cordillera, and Columbia Plateau). The location_parameters.py file accounts for these regional situations in the calculation. Out of 1000 GEV distributions generated for each year, I gathered a sample representing the daily and 10 year storm estimates. From this data we could extract the 5 and 95th percentile values, providing a confidence bound for each model. These estimates are crucial to city design code.  

By comparing the ratio of these flow rate values each year (represented by Q in the equation below), we can calculate the bankfull width of a given stream and year. The future bankfull width is calculated as a proportion of the current bankfull width. The beta variable accounts for regional behaviors and is generated in the location_parameters.py code. 

<img src="images/BFWformula.png" 
 width="240" height="100" border="10" />
 

## Conclusion 
As a final product, I collaborated with Daniel Larsson to create a website where a civil engineer can enter in coordinates and receive the likelihood of stream width change. The website also shows the probability that a certain culvert width will fail. Since there are roughly 10,000 locations in this dataset, I built a SQL database for more efficient data access. The SQL database will allow a relative comparison of climate change activity in each region, providing a way to prioritize certain high risk culvert analysis. The website will eventually be hosted from a UW server and all the code is transitioned to the CIG. This information will help Washington state better understand their construction costs and prevent replacement costs in the future. Furthermore, this tool will will help ensure salmon migration is preserved and building plans are conscious of weather changes in the coming years. 

Further work includes studying different climate change models and adding them to the 6 that were included in this study. I included data from a moderate and reduced C02 emission case. However, the CIG is interested in generating more data for different C02 emission cases and the code is set up to process the NetCDF files for future investigations. Legislation for construction constraints has not been defined yet and this information will allow risk analysis for deciding appropriate action thresholds. 




