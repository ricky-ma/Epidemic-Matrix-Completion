# Matrix Completion for Epidemiology
Team members: Ricky Ma, Kaiwen Hu <br/>

## Abstract
The devastating Covid-19 pandemic has caused many to be concerned about 
under-reporting and censorship in supposedly official government data, 
especially in the number of confirmed cases and deaths. With a 
motivation to shine a light on problematic and inaccurate data collection 
in public health, we explore the feasibility of data recovery and 
prediction on incomplete epidemiological data using matrix completion. 

## Introduction
Matrix completion involves filling in missing values of a partially complete
matrix. The technique has gained notoriety through the Netflix problem and
has been further refined by Hastie et. al (2015) through fast-alternating 
least squares optimization. Public health and epidemiological data often 
contain missing values due to the difficulty of collecting data 
that is both comprehensive and precise. Many factors contribute to the 
feasibility of accurate data collection, including, but not limited to cost, 
accessibility, technology, and response rate. The effects of these factors 
are multiplied in both developing and authoritarian countries - data relating 
to disease infection rates, mortality rates, and the general health of the 
population may be significantly under-reported or even absent. Our approach 
explores the possibility of predicting these absent values in epidemiological 
data using matrix completion and low-rank SVD.

## Method
### Data Preparation
Time-series Covid-19 data is provided by Johns Hopkins University, including
the number of confirmed cases and deaths in each country/region. The data for
each country was normalized by calculating the total number of cases and deaths
starting from the respective country's first case and death. This was 
calculated for each country, 20, 30, 40, and 50 days from its first case and 
death. <br/><br/>
Indicators that may affect a country's case numbers and mortality rates are 
provided by the World Bank's World Development Indicators. Ten relevant 
indicators were selected from three categories. Health indicators include the 
number of physicians per 1000 people, smoking prevalence, life expectancy,
death from communicable diseases, and death from noncommunicable diseases.
Water and sanitation indicators include access to drinking water, access to 
sanitation services, and access to basic handwashing facilities. Age and 
population indicators include the percentage of people aged 15-64 and the 
percentage of people aged 65 and up. The indicator and Covid-19 data are 
combined into one matrix with various missing values. <br/>
### Matrix Completion
We first initialize a shadow matrix **O** with binary values *o_ij*=1 if value is 
present in the original matrix, *o_ij*=0 if value is missing in the original matrix. 
The objective of the algorithm is to minimize the nuclear norm of the original matrix 
**A**. Nuclear norm is the sum of all singular values of a matrix. Singular values can be 
obtained from Singular Value Decomposition (SVD). That is, for any matrix n by d matrix **A**, 
we can decompose it such that **A** = **U S V'** where **U** is a n by n square matrix, 
**V'** is a d by d square matrix and **S** is a n by d matrix with *m*=*min(n,d)* diagonal 
entries. The diagonal entries *sigma_1*,...,*sigma_m* are singular values where 
*sigma_1 = s_11, ... ,sigma_m = s_mm* in descending order.

The recursive minimizing function first finds the minimum singular value of **A** 
(*sigma_{min}*) through Singular Value Decomposition. Then, the algorithm shrinks the 
nuclear norm by subtracting *sigma_{min}* from all other singular values. The new 
singular values will be the updated version of the **S** matrix (*S_{new}*). The algorithm 
keeps a copy of a temporary matrix **T** = **US**_{new}**V'**. Finally, the algorithm will 
update **A** by checking the shadow matrix. If the entry is *o{ij} = 0*, then the 
algorithm updates *a_ij = t_ij*. This process will terminate once the nuclear norm can 
no longer be minimized.

A final note is that this algorithm works well for any low ranked matrix. That is, this 
method can be applied to predict missing data entries for any data with few features, or 
highly collinear features.


## Experiments
To test whether the algorithm works, we used two different datasets, as stated in Section 3.1. Both datasets have a number of features less than or equal to 10, such that the matrix forms of both data are sufficiently low-ranked for the algorithm to work. We decided to test matrices of different dimensions to experiment with matrices of rank less than 10, and matrices of rank at 10 (which is at the maximum threshold).

We also chose two different types of data: time-series and non time-series. The Covid-19 cases and deaths matrix is a time-series data with increasing values while the public health indicators are non time-series, categorical data. Although we do not have a test set for our experiment, our approach to validating whether the model works is naive, yet simple; we would check whether there are values that seem to ``make sense''. For example, if there were predictions on the number of cases or deaths such that the tolls were decreasing or the value is negative, we would deem the model to be sub-optimal. Likewise, if predictions were made on specific health-indicators, then we would deem the model to be viable if the entries fall within the range of existing values of their respectable feature.

## Results
Please find the linked CSV files for matrices of incomplete and completed datasets.

[Incomplete matrix of Covid-19 cases and deaths](https://github.com/ricky-ma/Epidemic-Matrix-Completion/blob/master/output/covid_original.csv)

[Completed matrix of Covid-19 cases and deaths with predictions](https://github.com/ricky-ma/Epidemic-Matrix-Completion/blob/master/output/covid_complete.csv)

[Incomplete matrix of public health indicators](https://github.com/ricky-ma/Epidemic-Matrix-Completion/blob/master/output/ind_original.csv)

[Completed matrix of public health indicators with predictions](https://github.com/ricky-ma/Epidemic-Matrix-Completion/blob/master/output/ind_complete.csv)

## Conclusion
Although some predicted data entries from our results are flawed (such as a decreasing number 
of cases and death tolls and negative values for death tolls), our model was able to fill in 
values for missing data entries. The flawed data prediction could be a result from the difference 
in the nature of data we were handling with compared to the Netflix problem. For example, the 
matrix of Covid-19 cases and death count is a time series data while the Netflix challenge is not. 
Hence, the variance in type of data that we were working with may have diverged the result and 
performance of our model. 

The problematic predictions may also result from input rows that are too sparse, with some only 
have 1 or 2 original entries. Looking at the original data, the last 10 input rows are all very 
sparse. This may have caused inaccurate predictions for those rows, as well as negatively 
affecting/skewing predictions for other countries. 

Nevertheless, there were no values that were predicted that lied outside of the range of existing 
values in the incomplete public health indicators matrix. This shows a  promising sign for the 
algorithm. For further exploration of this model, it should be tested on different types of data 
(panel data, time-series etc.) with denser matrices (sparse rows removed) to reason whether it 
could be a viable solution for predicting missing public health and epidemic data entries. 
