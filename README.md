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
death. <br/>
Indicators that may affect a country's case numbers and mortality rates are 
provided by the World Bank's World Development Indicators. Ten relevant 
indicators were selected from three categories. Health indicators include the 
number of physicians per 1000 people, smoking prevalence, life expectancy,
death from communicable diseases, and death from noncommunicable diseases.
Water and sanitation indicators include access to drinking water, access to 
sanitation services, and access to basic handwashing facilities. Age and 
population indicators include the percentage of people aged 15-64 and the 
percentage of people aged 65 and up. <br/>
The indicator and Covid-19 data are combined into one matrix with various
missing values. This matrix is filled in using low-rank SVD, optimized with
fast alternating least-squares.


## Experiments
Several paragraphs describing the experiments you ran in the process of developing your Kaggle competition final entry.

## Results
Input matrix: <br/>

| Country               | Indicator |
| -------------       |:-------------:|
|               |           |

Output matrix:

## Conclusion
Several paragraphs describing what you learned in attempting to solve this problem, why your team is ranked where it is on the leader board, how you might have changed the problem to make its solution more valuable, etc.
