
# Predicting Dissolved Oxygen Levels in Streams

## Problem statement
Dissolved Oxygen is a good indicator of stream health. Using tested levels of dissolved oxygen in a relatively healthy stream we can use TimeSeries Modeling to forecast future levels of dissolved oxygen. This can be used to flag changes in the health of the stream.

## Table of Contents:
[Original Data](./Data/cmcWaterQualitySamples.csv)  
[Modeled Data](./Data/DO_data.csv)  
[CMC Data Exploration](./Water_Quality_EDA.ipynb)  
[Creating Data for Modeling](./File_creation.py)  
[Exploring Sites](./Dissolved_Oxygen_Sites_exploration.ipynb)  
[Formulas for Modeling](./my_imports.py)  
[SARIMAX Modeling](./Dissolved_Oxygen_modeling.ipynb)  
[LSTM Modeling](./Dissolved_Oxygen_modeling-LSTM.ipynb)

## What is Dissolved Oxygen and why does it matter?
Dissolved Oxygen is one of the most common measures of stream and water body quality. Fish and micro-organism require certain levels to maintain health numbers. A healthy range of dissolved oxygen is 8 mg/L to 15 mg/L. Above and below this is unhealthy for the ecosystem.

Low levels of dissolved oxygen is a large problem within the Chesapeake Watershed. Cyano bacteria consume the oxygen and create hypoxia (an environmental phenomenon where the concentration of dissolved oxygen in the water column decreases to a level that can no longer support living aquatic organisms[^1](https://gulfhypoxia.net/about-hypoxia/)) and eutrophic conditions (when a body of water becomes overly enriched with minerals and nutrients which induce excessive growth of plants and algae[^2](https://www.nature.com/scitable/knowledge/library/eutrophication-causes-consequences-and-controls-in-aquatic-102364466)). This has led to fish kills within the bay.

By monitoring levels at the subwatershed level we can try to stop issues at the source.


## Description of data
The data used for analysis was collected from 13 sites along the LeTort Spring Run by the [Letort Regional Authority](http://www.letort.org/) monthly from June 8th 1996 to December 10th 2018. Each site was aggregated together with the average of all the sites. There were 233 data points.

![](./Images/Map_1.png)

**Source:** [Chesapeake Monitoring Cooperative](https://www.chesapeakemonitoringcoop.org/) works with diverse partners to collect and share new and existing water quality data. Original data set was 10703 rows with 208 columns from 24 organizations. The LeTort Regional Authority had the most extensive collection data so was used for modeling.

|Feature|Type|Dataset|Description|                     
|---|---|---|---|
|Date|DatetimeIndex|agg_data.csv|Date of collection from 1996-06-08 to 2018-12-10
|dissolved_oxygen|float64|agg_data.csv|Averaged Dissolved Oxegen from 10 sites measure in mg/L

## Exploratory Data Analysis  

The Letort dataset contained data from 1992 to 2018. When I plotted the data I noticed a gap in the early nineties.

![](./Images/DO_sample_letort.png)

Timeseries analysis is thrown off by gaps in the data so I decided to start my analysis in 1996 where there is monthly collection until 2018.

### Time Series EDA

![](./Images/Rolling_mean_3.png)

When reviewing the rolling mean we can see that there is a slight upward tilt to the data but it is pretty stationary.

#### Dickey Fuller
The Augmented Dicky is a unit root test that checks your data for stationarity. It uses autoregression to check how much the data is defined by a trend. Doing a Augmented Dickey-Fuller test on the data without adding any lags yielded a p-value of **8.057773505476658e-20**. Since this is well below 0.05 we can say with 95% confidence that the can reject the null hypothesis. The data is stationary and does not have a unit root.

#### Auto Coorelation and Partial Auto Correlation

![](./Images/acf_pacf_12.png)

Using Auto Correlation and Partial Auto Correlation plots we can get a sense of what the we should use for variables in our model. We can see a drop off after the second lag from which we can infer a q of 2 or 1. In the partial auto correlation plot we can see the a significant negative correlation at 4 and 8 from which we might infer a p of 4. But since this is seasonal data we can also see some movement surrounding multiples of three so we need to test 3 as well. We can also see a significance at 12 which indicates that there is seasonality to this data. This makes sense with dissolved oxygen.

## Time Series Modeling

Using the ACF and PACF plots I made some assumptions of the potential variables for p, d, q, P, D, Q and S and then tested different values to see how they worked together.


|p|d|q|P|D|Q|S|AIC|                     
|---|---|---|---|---|---|---|---|
3|0|2|4|0|5|12|466.514743
3|0|1|4|0|5|12|467.403062
3|0|0|4|0|5|12|467.968364
4|0|2|4|0|5|12|468.392006
4|0|1|4|0|5|12|469.380625
4|0|0|4|0|5|12|469.956111
3|0|0|2|0|5|12|475.375037

![](./Images/SARIMAX302.png)

The average dissolved oxygen level in the test data is 10.73 mg/L.

I used Akaike information criterion(AIC) to evaluate the model. AIC reviews information loss and access the fit of the model versus the simplicity and gives it a score. The lower the AIC the better the model.

## Primary findings

#### Forecasted Data

Month|	mean |	mean_se	| mean_ci_lower |	mean_ci_upper
|---|---|---|---|---|
January|	11.554036	|1.412845|	8.784910|	14.323161
February	|11.652757|	1.412926|	8.883473|	14.422040
March|11.434735	|1.412901	|8.665500	|14.203971
April|11.105064	|1.412868|	8.335894|	13.874235
May|10.997677	|1.412860|	8.228522|	13.766833
June|11.336283	|1.412858|	8.567133|	14.105434
July|10.792287|	1.412857|	8.023138|	13.561436
August|10.979213	|1.412771|	8.210233|	13.748193
September|12.097283	|1.412650|	9.328540|	14.866026
October|12.021462|	1.412264|	9.253476|	14.789448
November|11.698560|	1.412221|	8.930657|	14.466463
December|13.482244|	1.412097|	10.714584|	16.249904

Since we know that the stream is relatively stationary we are able to use these forecasted levels for the year 2019 to keep an eye on the health of the stream.

## LSTM modeling
Long term short term memory modeling is a type of recurrent neural network that can be used to do time series analysis. It uses steps previous steps to predict forward. I created a model with a lag on 1 that has a Mean Absolute Error of 1.17 for the test data. This compares to the MAE of 1.319124 for my time series model.

![](LSTM.png)

## Next Steps

1. Look at each location individually
2. More research into why the data is flatter before 2000
3. Look at why the levels at MG1, MG2 and WL are more variable than the LT sites.
4. Compare analysis to other stream data to see how health compares.
5. Normalize the testing, test every 30 days, test at same time.
6. Increase testing frequency so spikes in levels can be addressed faster.
