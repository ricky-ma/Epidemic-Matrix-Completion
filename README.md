# Matrix Completion for Epidemiology
Team members: Ricky Ma, Kaiwen Hu <br/>

## Abstract
The devastating Covid-19 pandemic has caused many to be concerned about 
under-reporting and censorship in supposedly official government data, 
especially the number of confirmed cases and deaths. With a 
motivation to shine a light on problematic data collection and inaccurate 
reporting in public health, we explore the feasibility of data recovery and 
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
Several paragraphs describing the approach you took to solving the problem. 
Highlight in particular how you worked around the small training data problem.
Transfer learning is likely something you will want to read about.

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
