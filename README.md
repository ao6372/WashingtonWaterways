
<img src="images/salmonculvert.jpg" 
 width="240" height="180" border="10" />

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
We are examining extreme values over 100 years of data to extract an estimate for the bankfull width of a stream for a given year. 

\begin{equation*}
\mathbf{BFW}_2 \divide \mathbf{BFW}_1 =  \left(
\mathbf{i} & \mathbf{j} & \mathbf{k} \\

\end{equation*}
 

## Conclusion 
As a final product, I developed a website where a civil engineer can enter in coordinates and receive the likelihood of stream width change. This information will help Washington state better understand their construction costs and prevent replacement costs in the future. Furthermore, this tool will will help ensure salmon migration is preserved and building plans are conscious of weather changes in the coming years. 




