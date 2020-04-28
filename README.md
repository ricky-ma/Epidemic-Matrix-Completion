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
update **A** by checking the shadow matrix. If the entry is *o_{ij} = 0*, then the 
algorithm updates *a_ij = t_ij*. This process will terminate once the nuclear norm can 
no longer be minimized.

A final note is that this algorithm works well for any low ranked matrix. That is, this 
method can be applied to predict missing data entries for any data with few features, or 
highly collinear features.


## Experiments
To test whether the algorithm works, we used two different datasets as stated in 
Section 3.1. Both data have number of features less than or equal to 10, implying that 
the matrix form of both data are sufficiently low-ranked for the algorithm to work. We 
specifically decided to test matrix of different dimensions because we first wanted to 
experiment with matrix of rank sufficiently less than 10, and matrix of rank at 10 (which 
is at the maximum threshold).

Also, we chose two different types of data: time-series and non time-series. The Covid-19 
cases and deaths matrix is a time-series data with increasing values while Covid-19 health 
indicator is a non time-series categorical data. Although we do not have a test set for our 
experiment, our approach to validating whether the model works is naive yet simple; we 
would check whether there are values that seem to ``make sense''. For example, if there 
were predictions on the number of cases or deaths such that the tolls were decreasing or 
the value is negative, we would deem the model to be sub-optimal. Likewise, if predictions 
were made on specific health-indicators, then we would deem the model to be viable if the 
entries falls within the range of existing values of their respectable feature.

## Results
### Incomplete matrix of Covid-19 cases and deaths
|Country/Region                  |Cases 30 days from first case|Cases 40 days from first case|Cases 50 days from first case|Deaths 30 days from first death|Deaths 40 days from first death|Deaths 50 days from first death|
|--------------------------------|-----------------------------|-----------------------------|-----------------------------|-------------------------------|-------------------------------|-------------------------------|
|Afghanistan                     |84.0                         |299.0                        |714.0                        |36.0                           |                               |                               |
|Albania                         |400.0                        |548.0                        |                             |23.0                           |26.0                           |                               |
|Algeria                         |367.0                        |1320.0                       |2160.0                       |275.0                          |392.0                          |                               |
|Andorra                         |390.0                        |601.0                        |717.0                        |37.0                           |                               |                               |
|Angola                          |24.0                         |                             |                             |                               |                               |                               |
|Antigua and Barbuda             |21.0                         |                             |                             |                               |                               |                               |
|Argentina                       |1133.0                       |2142.0                       |                             |56.0                           |123.0                          |                               |
|Armenia                         |532.0                        |937.0                        |1339.0                       |                               |                               |                               |
|Australia                       |15.0                         |60.0                         |377.0                        |18.0                           |54.0                           |67.0                           |
|Austria                         |6909.0                       |12051.0                      |14336.0                      |337.0                          |491.0                          |                               |
|Azerbaijan                      |298.0                        |991.0                        |1436.0                       |11.0                           |                               |                               |
|Bahamas                         |49.0                         |                             |                             |                               |                               |                               |
|Bahrain                         |419.0                        |688.0                        |1528.0                       |7.0                            |                               |                               |
|Bangladesh                      |164.0                        |1838.0                       |                             |75.0                           |                               |                               |
|Barbados                        |75.0                         |                             |                             |                               |                               |                               |
|Belarus                         |94.0                         |1066.0                       |4779.0                       |                               |                               |                               |
|Belgium                         |50.0                         |886.0                        |4937.0                       |3019.0                         |5828.0                         |                               |
|Benin                           |35.0                         |                             |                             |                               |                               |                               |
|Bhutan                          |5.0                          |5.0                          |                             |                               |                               |                               |
|Bolivia                         |268.0                        |564.0                        |                             |                               |                               |                               |
|Bosnia and Herzegovina          |624.0                        |1083.0                       |                             |49.0                           |                               |                               |
|Brazil                          |3417.0                       |12161.0                      |30425.0                      |1924.0                         |                               |                               |
|Brunei                          |135.0                        |137.0                        |                             |                               |                               |                               |
|Bulgaria                        |577.0                        |846.0                        |                             |25.0                           |43.0                           |                               |
|Burkina Faso                    |443.0                        |576.0                        |                             |35.0                           |                               |                               |
|Cabo Verde                      |61.0                         |                             |                             |                               |                               |                               |
|Cambodia                        |1.0                          |1.0                          |33.0                         |                               |                               |                               |
|Cameroon                        |650.0                        |848.0                        |                             |                               |                               |                               |
|Canada                          |11.0                         |49.0                         |415.0                        |407.0                          |1399.0                         |                               |
|Central African Republic        |11.0                         |                             |                             |                               |                               |                               |
|Chad                            |33.0                         |                             |                             |                               |                               |                               |
|Chile                           |3404.0                       |7213.0                       |                             |147.0                          |                               |                               |
|China                           |75550.0                      |80136.0                      |80932.0                      |2238.0                         |2914.0                         |3172.0                         |
|Colombia                        |1485.0                       |3105.0                       |                             |196.0                          |                               |                               |
|Congo (Brazzaville)             |60.0                         |                             |                             |                               |                               |                               |
|Congo (Kinshasa)                |215.0                        |332.0                        |                             |25.0                           |                               |                               |
|Costa Rica                      |454.0                        |626.0                        |                             |4.0                            |                               |                               |
|Cote d'Ivoire                   |444.0                        |847.0                        |                             |                               |                               |                               |
|Croatia                         |495.0                        |1182.0                       |1741.0                       |39.0                           |                               |                               |
|Diamond Princess                |706.0                        |712.0                        |712.0                        |8.0                            |10.0                           |11.0                           |
|Cuba                            |620.0                        |1137.0                       |                             |31.0                           |                               |                               |
|Cyprus                          |526.0                        |761.0                        |                             |12.0                           |                               |                               |
|Czechia                         |3308.0                       |5732.0                       |6900.0                       |201.0                          |                               |                               |
|Denmark                         |2366.0                       |5266.0                       |7268.0                       |285.0                          |                               |                               |
|Djibouti                        |732.0                        |                             |                             |                               |                               |                               |
|Dominican Republic              |1109.0                       |2620.0                       |4964.0                       |196.0                          |                               |                               |
|Ecuador                         |2240.0                       |7161.0                       |10128.0                      |355.0                          |                               |                               |
|Egypt                           |110.0                        |456.0                        |1070.0                       |94.0                           |205.0                          |                               |
|El Salvador                     |190.0                        |                             |                             |                               |                               |                               |
|Equatorial Guinea               |41.0                         |                             |                             |                               |                               |                               |
|Eritrea                         |39.0                         |                             |                             |                               |                               |                               |
|Estonia                         |645.0                        |1149.0                       |1459.0                       |                               |                               |                               |
|Eswatini                        |15.0                         |                             |                             |                               |                               |                               |
|Ethiopia                        |71.0                         |                             |                             |                               |                               |                               |
|Fiji                            |17.0                         |                             |                             |                               |                               |                               |
|Finland                         |2.0                          |30.0                         |400.0                        |98.0                           |                               |                               |
|France                          |12.0                         |288.0                        |4496.0                       |149.0                          |1698.0                         |8093.0                         |
|Gabon                           |57.0                         |                             |                             |1.0                            |                               |                               |
|Gambia                          |9.0                          |                             |                             |                               |                               |                               |
|Georgia                         |83.0                         |188.0                        |348.0                        |                               |                               |                               |
|Germany                         |27.0                         |799.0                        |9257.0                       |2349.0                         |4459.0                         |                               |
|Ghana                           |566.0                        |                             |                             |9.0                            |                               |                               |
|Greece                          |966.0                        |1755.0                       |2207.0                       |92.0                           |116.0                          |                               |
|Guatemala                       |156.0                        |                             |                             |5.0                            |                               |                               |
|Guinea                          |250.0                        |                             |                             |                               |                               |                               |
|Guyana                          |45.0                         |66.0                         |                             |6.0                            |7.0                            |                               |
|Haiti                           |47.0                         |                             |                             |                               |                               |                               |
|Holy See                        |7.0                          |8.0                          |                             |                               |                               |                               |
|Honduras                        |382.0                        |477.0                        |                             |                               |                               |                               |
|Hungary                         |623.0                        |1458.0                       |                             |122.0                          |                               |                               |
|Iceland                         |1020.0                       |1616.0                       |1760.0                       |8.0                            |                               |                               |
|India                           |3.0                          |56.0                         |244.0                        |246.0                          |592.0                          |                               |
|Indonesia                       |1677.0                       |3842.0                       |7135.0                       |306.0                          |590.0                          |                               |
|Iran                            |19644.0                      |41495.0                      |66220.0                      |1433.0                         |2757.0                         |4110.0                         |
|Iraq                            |346.0                        |878.0                        |1400.0                       |54.0                           |78.0                           |                               |
|Ireland                         |2910.0                       |6574.0                       |15251.0                      |287.0                          |687.0                          |                               |
|Israel                          |883.0                        |6092.0                       |10743.0                      |177.0                          |                               |                               |
|Italy                           |1694.0                       |12462.0                      |53578.0                      |5476.0                         |13155.0                        |19468.0                        |
|Jamaica                         |63.0                         |223.0                        |                             |5.0                            |                               |                               |
|Japan                           |105.0                        |274.0                        |639.0                        |22.0                           |43.0                           |63.0                           |
|Jordan                          |299.0                        |389.0                        |                             |                               |                               |                               |
|Kazakhstan                      |951.0                        |                             |                             |                               |                               |                               |
|Kenya                           |197.0                        |                             |                             |                               |                               |                               |
|Korea, South                    |204.0                        |4335.0                       |7869.0                       |102.0                          |162.0                          |208.0                          |
|Kuwait                          |195.0                        |479.0                        |1355.0                       |                               |                               |                               |
|Kyrgyzstan                      |489.0                        |                             |                             |                               |                               |                               |
|Latvia                          |446.0                        |630.0                        |748.0                        |                               |                               |                               |
|Lebanon                         |248.0                        |479.0                        |619.0                        |19.0                           |21.0                           |                               |
|Liberia                         |59.0                         |                             |                             |                               |                               |                               |
|Liechtenstein                   |75.0                         |79.0                         |                             |                               |                               |                               |
|Lithuania                       |460.0                        |912.0                        |1239.0                       |37.0                           |                               |                               |
|Luxembourg                      |1988.0                       |3115.0                       |3550.0                       |69.0                           |                               |                               |
|Madagascar                      |121.0                        |                             |                             |                               |                               |                               |
|Malaysia                        |22.0                         |50.0                         |428.0                        |84.0                           |                               |                               |
|Maldives                        |19.0                         |28.0                         |                             |                               |                               |                               |
|Malta                           |241.0                        |412.0                        |                             |                               |                               |                               |
|Mauritania                      |7.0                          |                             |                             |                               |                               |                               |
|Mauritius                       |324.0                        |                             |                             |9.0                            |                               |                               |
|Mexico                          |848.0                        |2785.0                       |6875.0                       |546.0                          |                               |                               |
|Moldova                         |1056.0                       |2264.0                       |                             |56.0                           |                               |                               |
|Monaco                          |49.0                         |84.0                         |94.0                         |                               |                               |                               |
|Mongolia                        |16.0                         |32.0                         |                             |                               |                               |                               |
|Montenegro                      |303.0                        |                             |                             |                               |                               |                               |
|Morocco                         |654.0                        |1545.0                       |3209.0                       |97.0                           |141.0                          |                               |
|Namibia                         |16.0                         |                             |                             |                               |                               |                               |
|Nepal                           |1.0                          |1.0                          |1.0                          |                               |                               |                               |
|Netherlands                     |9819.0                       |19709.0                      |30619.0                      |1771.0                         |3145.0                         |                               |
|New Zealand                     |514.0                        |1210.0                       |1422.0                       |                               |                               |                               |
|Nicaragua                       |9.0                          |                             |                             |                               |                               |                               |
|Niger                           |648.0                        |                             |                             |                               |                               |                               |
|Nigeria                         |111.0                        |276.0                        |542.0                        |                               |                               |                               |
|North Macedonia                 |219.0                        |570.0                        |1081.0                       |55.0                           |                               |                               |
|Norway                          |3755.0                       |5865.0                       |6896.0                       |134.0                          |                               |                               |
|Oman                            |99.0                         |277.0                        |813.0                        |                               |                               |                               |
|Pakistan                        |1373.0                       |3766.0                       |6919.0                       |143.0                          |                               |                               |
|Panama                          |2528.0                       |4273.0                       |                             |66.0                           |126.0                          |                               |
|Papua New Guinea                |7.0                          |                             |                             |                               |                               |                               |
|Paraguay                        |115.0                        |199.0                        |                             |8.0                            |                               |                               |
|Peru                            |2281.0                       |11475.0                      |                             |400.0                          |                               |                               |
|Philippines                     |3.0                          |33.0                         |230.0                        |1.0                            |5.0                            |33.0                           |
|Poland                          |3383.0                       |6934.0                       |                             |208.0                          |401.0                          |                               |
|Portugal                        |8251.0                       |15987.0                      |21379.0                      |629.0                          |                               |                               |
|Qatar                           |693.0                        |2376.0                       |5448.0                       |                               |                               |                               |
|Romania                         |1292.0                       |4057.0                       |7707.0                       |498.0                          |                               |                               |
|Russia                          |2.0                          |20.0                         |306.0                        |313.0                          |                               |                               |
|Rwanda                          |127.0                        |                             |                             |                               |                               |                               |
|Saint Lucia                     |15.0                         |                             |                             |                               |                               |                               |
|Saint Vincent and the Grenadines|12.0                         |                             |                             |                               |                               |                               |
|San Marino                      |224.0                        |279.0                        |435.0                        |30.0                           |35.0                           |                               |
|Saudi Arabia                    |1720.0                       |4033.0                       |11631.0                      |                               |                               |                               |
|Senegal                         |190.0                        |278.0                        |412.0                        |                               |                               |                               |
|Serbia                          |1908.0                       |4873.0                       |                             |122.0                          |                               |                               |
|Seychelles                      |11.0                         |                             |                             |                               |                               |                               |
|Singapore                       |85.0                         |110.0                        |200.0                        |11.0                           |                               |                               |
|Slovakia                        |485.0                        |863.0                        |                             |                               |                               |                               |
|Slovenia                        |977.0                        |1220.0                       |                             |55.0                           |                               |                               |
|Somalia                         |80.0                         |                             |                             |                               |                               |                               |
|South Africa                    |1585.0                       |2415.0                       |                             |                               |                               |                               |
|Spain                           |120.0                        |2277.0                       |28768.0                      |10348.0                        |17209.0                        |                               |
|Sri Lanka                       |1.0                          |1.0                          |44.0                         |                               |                               |                               |
|Sudan                           |19.0                         |                             |                             |2.0                            |                               |                               |
|Suriname                        |10.0                         |                             |                             |                               |                               |                               |
|Sweden                          |14.0                         |500.0                        |1763.0                       |870.0                          |1580.0                         |                               |
|Switzerland                     |11811.0                      |21100.0                      |26336.0                      |666.0                          |1174.0                         |                               |
|Taiwan*                         |26.0                         |41.0                         |49.0                         |1.0                            |2.0                            |5.0                            |
|Tanzania                        |88.0                         |                             |                             |                               |                               |                               |
|Thailand                        |35.0                         |43.0                         |70.0                         |10.0                           |33.0                           |47.0                           |
|Togo                            |44.0                         |81.0                         |                             |                               |                               |                               |
|Trinidad and Tobago             |113.0                        |                             |                             |                               |                               |                               |
|Tunisia                         |495.0                        |726.0                        |                             |37.0                           |                               |                               |
|Turkey                          |47029.0                      |90980.0                      |                             |1643.0                         |                               |                               |
|Uganda                          |56.0                         |                             |                             |                               |                               |                               |
|Ukraine                         |897.0                        |2777.0                       |                             |83.0                           |                               |                               |
|United Arab Emirates            |19.0                         |45.0                         |140.0                        |41.0                           |                               |                               |
|United Kingdom                  |36.0                         |459.0                        |5067.0                       |4320.0                         |12129.0                        |                               |
|Uruguay                         |480.0                        |                             |                             |                               |                               |                               |
|US                              |15.0                         |98.0                         |1663.0                       |2978.0                         |16544.0                        |40661.0                        |
|Uzbekistan                      |1165.0                       |                             |                             |                               |                               |                               |
|Venezuela                       |189.0                        |                             |                             |                               |                               |                               |
|Vietnam                         |16.0                         |16.0                         |47.0                         |                               |                               |                               |
|Zambia                          |52.0                         |                             |                             |                               |                               |                               |
|Zimbabwe                        |25.0                         |                             |                             |                               |                               |                               |
|Dominica                        |16.0                         |                             |                             |                               |                               |                               |
|Grenada                         |14.0                         |                             |                             |                               |                               |                               |
|Mozambique                      |39.0                         |                             |                             |                               |                               |                               |
|Syria                           |42.0                         |                             |                             |                               |                               |                               |
|Timor-Leste                     |23.0                         |                             |                             |                               |                               |                               |
|Belize                          |                             |                             |                             |                               |                               |                               |
|Laos                            |                             |                             |                             |                               |                               |                               |
|Libya                           |                             |                             |                             |                               |                               |                               |
|West Bank and Gaza              |217.0                        |308.0                        |                             |                               |                               |                               |
|Guinea-Bissau                   |                             |                             |                             |                               |                               |                               |
|Mali                            |                             |                             |                             |                               |                               |                               |
|Saint Kitts and Nevis           |                             |                             |                             |                               |                               |                               |
|Kosovo                          |                             |                             |                             |                               |                               |                               |
|Burma                           |                             |                             |                             |                               |                               |                               |
|MS Zaandam                      |                             |                             |                             |                               |                               |                               |
|Botswana                        |                             |                             |                             |                               |                               |                               |
|Burundi                         |                             |                             |                             |                               |                               |                               |
|Sierra Leone                    |                             |                             |                             |                               |                               |                               |
|Malawi                          |                             |                             |                             |                               |                               |                               |
|South Sudan                     |                             |                             |                             |                               |                               |                               |
|Western Sahara                  |                             |                             |                             |                               |                               |                               |
|Sao Tome and Principe           |                             |                             |                             |                               |                               |                               |
|Yemen                           |                             |                             |                             |                               |                               |                               |

###Completed matrix of Covid-19 cases and deaths with predictions
|Country/Region                  |0      |1      |2      |3      |4      |5      |
|--------------------------------|-------|-------|-------|-------|-------|-------|
|Afghanistan                     |84.0   |299.0  |714.0  |36.0   |86.14  |94.05  |
|Albania                         |400.0  |548.0  |449.11 |23.0   |26.0   |18.04  |
|Algeria                         |367.0  |1320.0 |2160.0 |275.0  |392.0  |287.72 |
|Andorra                         |390.0  |601.0  |717.0  |37.0   |88.17  |80.24  |
|Angola                          |24.0   |65.12  |63.9   |51.86  |27.93  |6.71   |
|Antigua and Barbuda             |21.0   |66.45  |58.23  |2.4    |27.24  |10.3   |
|Argentina                       |1133.0 |2142.0 |1611.58|56.0   |123.0  |238.87 |
|Armenia                         |532.0  |937.0  |1339.0 |72.37  |135.49 |145.68 |
|Australia                       |15.0   |60.0   |377.0  |18.0   |54.0   |67.0   |
|Austria                         |6909.0 |12051.0|14336.0|337.0  |491.0  |971.38 |
|Azerbaijan                      |298.0  |991.0  |1436.0 |11.0   |67.61  |147.75 |
|Bahamas                         |49.0   |92.1   |79.18  |22.87  |17.39  |5.64   |
|Bahrain                         |419.0  |688.0  |1528.0 |7.0    |44.39  |142.33 |
|Bangladesh                      |164.0  |1838.0 |1187.91|75.0   |100.84 |102.9  |
|Barbados                        |75.0   |71.35  |65.94  |12.42  |4.6    |10.72  |
|Belarus                         |94.0   |1066.0 |4779.0 |425.39 |729.32 |651.99 |
|Belgium                         |50.0   |886.0  |4937.0 |3019.0 |5828.0 |4586.6 |
|Benin                           |35.0   |36.59  |40.4   |9.02   |7.59   |11.52  |
|Bhutan                          |5.0    |5.0    |22.45  |9.25   |12.11  |8.78   |
|Bolivia                         |268.0  |564.0  |417.53 |18.79  |20.99  |28.69  |
|Bosnia and Herzegovina          |624.0  |1083.0 |806.47 |49.0   |19.61  |32.42  |
|Brazil                          |3417.0 |12161.0|30425.0|1924.0 |3655.16|3874.31|
|Brunei                          |135.0  |137.0  |131.9  |-49.37 |24.99  |19.67  |
|Bulgaria                        |577.0  |846.0  |670.28 |25.0   |43.0   |86.71  |
|Burkina Faso                    |443.0  |576.0  |514.5  |35.0   |99.23  |47.38  |
|Cabo Verde                      |61.0   |85.78  |75.76  |0.27   |11.69  |8.96   |
|Cambodia                        |1.0    |1.0    |33.0   |-8.87  |2.62   |10.07  |
|Cameroon                        |650.0  |848.0  |669.38 |7.94   |10.75  |20.13  |
|Canada                          |11.0   |49.0   |415.0  |407.0  |1399.0 |1478.53|
|Central African Republic        |11.0   |44.36  |42.63  |1.1    |12.65  |6.37   |
|Chad                            |33.0   |77.01  |62.71  |-35.73 |15.44  |5.96   |
|Chile                           |3404.0 |7213.0 |5131.37|147.0  |97.3   |235.22 |
|China                           |75550.0|80136.0|80932.0|2238.0 |2914.0 |3172.0 |
|Colombia                        |1485.0 |3105.0 |2328.92|196.0  |200.99 |155.74 |
|Congo (Brazzaville)             |60.0   |96.88  |86.88  |37.35  |25.56  |9.39   |
|Congo (Kinshasa)                |215.0  |332.0  |260.5  |25.0   |0.46   |7.0    |
|Costa Rica                      |454.0  |626.0  |474.47 |4.0    |-22.11 |7.71   |
|Cote d'Ivoire                   |444.0  |847.0  |624.7  |30.82  |21.89  |31.77  |
|Croatia                         |495.0  |1182.0 |1741.0 |39.0   |91.46  |171.64 |
|Diamond Princess                |706.0  |712.0  |712.0  |8.0    |10.0   |11.0   |
|Cuba                            |620.0  |1137.0 |839.3  |31.0   |17.32  |43.4   |
|Cyprus                          |526.0  |761.0  |583.96 |12.0   |-1.01  |26.34  |
|Czechia                         |3308.0 |5732.0 |6900.0 |201.0  |416.04 |641.17 |
|Denmark                         |2366.0 |5266.0 |7268.0 |285.0  |596.32 |778.1  |
|Djibouti                        |732.0  |702.99 |519.37 |7.93   |-6.65  |3.41   |
|Dominican Republic              |1109.0 |2620.0 |4964.0 |196.0  |431.86 |560.13 |
|Ecuador                         |2240.0 |7161.0 |10128.0|355.0  |736.21 |1094.86|
|Egypt                           |110.0  |456.0  |1070.0 |94.0   |205.0  |167.02 |
|El Salvador                     |190.0  |219.97 |170.62 |-30.6  |16.74  |8.02   |
|Equatorial Guinea               |41.0   |66.02  |62.19  |-0.39  |11.12  |8.38   |
|Eritrea                         |39.0   |65.08  |60.97  |0.33   |12.19  |9.24   |
|Estonia                         |645.0  |1149.0 |1459.0 |90.64  |144.28 |155.79 |
|Eswatini                        |15.0   |53.79  |56.97  |42.61  |27.44  |9.36   |
|Ethiopia                        |71.0   |110.22 |97.23  |43.25  |26.22  |8.45   |
|Fiji                            |17.0   |36.57  |38.98  |5.17   |14.63  |10.99  |
|Finland                         |2.0    |30.0   |400.0  |98.0   |152.81 |86.94  |
|France                          |12.0   |288.0  |4496.0 |149.0  |1698.0 |8093.0 |
|Gabon                           |57.0   |92.13  |83.38  |1.0    |22.92  |12.2   |
|Gambia                          |9.0    |48.75  |42.32  |-46.53 |16.2   |10.61  |
|Georgia                         |83.0   |188.0  |348.0  |44.55  |57.25  |44.27  |
|Germany                         |27.0   |799.0  |9257.0 |2349.0 |4459.0 |3547.86|
|Ghana                           |566.0  |574.94 |432.77 |9.0    |4.59   |5.6    |
|Greece                          |966.0  |1755.0 |2207.0 |92.0   |116.0  |147.75 |
|Guatemala                       |156.0  |179.17 |138.3  |5.0    |3.86   |8.06   |
|Guinea                          |250.0  |290.34 |216.67 |-13.76 |25.57  |13.13  |
|Guyana                          |45.0   |66.0   |61.95  |6.0    |7.0    |-42.12 |
|Haiti                           |47.0   |86.66  |79.9   |40.05  |25.59  |8.77   |
|Holy See                        |7.0    |8.0    |22.52  |1.45   |13.05  |11.34  |
|Honduras                        |382.0  |477.0  |395.61 |43.52  |25.27  |14.1   |
|Hungary                         |623.0  |1458.0 |1094.23|122.0  |109.4  |78.05  |
|Iceland                         |1020.0 |1616.0 |1760.0 |8.0    |39.21  |138.45 |
|India                           |3.0    |56.0   |244.0  |246.0  |592.0  |569.21 |
|Indonesia                       |1677.0 |3842.0 |7135.0 |306.0  |590.0  |753.28 |
|Iran                            |19644.0|41495.0|66220.0|1433.0 |2757.0 |4110.0 |
|Iraq                            |346.0  |878.0  |1400.0 |54.0   |78.0   |96.31  |
|Ireland                         |2910.0 |6574.0 |15251.0|287.0  |687.0  |1262.33|
|Israel                          |883.0  |6092.0 |10743.0|177.0  |611.75 |1187.29|
|Italy                           |1694.0 |12462.0|53578.0|5476.0 |13155.0|19468.0|
|Jamaica                         |63.0   |223.0  |163.46 |5.0    |14.19  |18.96  |
|Japan                           |105.0  |274.0  |639.0  |22.0   |43.0   |63.0   |
|Jordan                          |299.0  |389.0  |316.9  |-16.48 |12.11  |21.85  |
|Kazakhstan                      |951.0  |932.29 |679.79 |-6.87  |-0.97  |3.51   |
|Kenya                           |197.0  |218.68 |172.34 |28.8   |24.09  |12.87  |
|Korea, South                    |204.0  |4335.0 |7869.0 |102.0  |162.0  |208.0  |
|Kuwait                          |195.0  |479.0  |1355.0 |110.7  |183.24 |179.63 |
|Kyrgyzstan                      |489.0  |465.06 |348.58 |9.11   |-1.8   |7.05   |
|Latvia                          |446.0  |630.0  |748.0  |36.56  |67.21  |77.76  |
|Lebanon                         |248.0  |479.0  |619.0  |19.0   |21.0   |55.83  |
|Liberia                         |59.0   |86.03  |77.11  |23.84  |25.26  |14.3   |
|Liechtenstein                   |75.0   |79.0   |87.83  |54.26  |32.27  |9.38   |
|Lithuania                       |460.0  |912.0  |1239.0 |37.0   |125.61 |138.01 |
|Luxembourg                      |1988.0 |3115.0 |3550.0 |69.0   |147.26 |299.48 |
|Madagascar                      |121.0  |157.3  |123.39 |-16.48 |21.88  |10.63  |
|Malaysia                        |22.0   |50.0   |428.0  |84.0   |109.75 |75.17  |
|Maldives                        |19.0   |28.0   |47.32  |41.82  |30.47  |10.8   |
|Malta                           |241.0  |412.0  |317.01 |-19.47 |25.44  |18.13  |
|Mauritania                      |7.0    |15.06  |24.35  |5.71   |10.18  |11.83  |
|Mauritius                       |324.0  |332.02 |267.59 |9.0    |21.58  |15.25  |
|Mexico                          |848.0  |2785.0 |6875.0 |546.0  |945.18 |910.71 |
|Moldova                         |1056.0 |2264.0 |1608.16|56.0   |15.25  |66.59  |
|Monaco                          |49.0   |84.0   |94.0   |3.67   |17.57  |13.87  |
|Mongolia                        |16.0   |32.0   |40.78  |1.42   |13.21  |8.89   |
|Montenegro                      |303.0  |306.06 |232.37 |-2.3   |9.0    |9.23   |
|Morocco                         |654.0  |1545.0 |3209.0 |97.0   |141.0  |175.75 |
|Namibia                         |16.0   |40.87  |44.05  |-7.54  |19.33  |9.95   |
|Nepal                           |1.0    |1.0    |1.0    |0.97   |10.8   |9.63   |
|Netherlands                     |9819.0 |19709.0|30619.0|1771.0 |3145.0 |3591.08|
|New Zealand                     |514.0  |1210.0 |1422.0 |61.47  |134.13 |157.16 |
|Nicaragua                       |9.0    |8.54   |6.14   |-0.03  |-0.18  |-0.09  |
|Niger                           |648.0  |655.69 |486.93 |29.26  |12.31  |4.32   |
|Nigeria                         |111.0  |276.0  |542.0  |60.45  |88.92  |76.45  |
|North Macedonia                 |219.0  |570.0  |1081.0 |55.0   |165.64 |144.84 |
|Norway                          |3755.0 |5865.0 |6896.0 |134.0  |296.18 |581.46 |
|Oman                            |99.0   |277.0  |813.0  |105.55 |136.77 |111.65 |
|Pakistan                        |1373.0 |3766.0 |6919.0 |143.0  |400.06 |726.55 |
|Panama                          |2528.0 |4273.0 |3221.44|66.0   |126.0  |257.01 |
|Papua New Guinea                |7.0    |45.64  |47.69  |47.31  |32.72  |14.08  |
|Paraguay                        |115.0  |199.0  |144.84 |8.0    |-19.6  |1.12   |
|Peru                            |2281.0 |11475.0|7518.35|400.0  |348.83 |505.83 |
|Philippines                     |3.0    |33.0   |230.0  |1.0    |5.0    |33.0   |
|Poland                          |3383.0 |6934.0 |5165.21|208.0  |401.0  |596.59 |
|Portugal                        |8251.0 |15987.0|21379.0|629.0  |1348.81|2076.53|
|Qatar                           |693.0  |2376.0 |5448.0 |385.95 |694.68 |690.53 |
|Romania                         |1292.0 |4057.0 |7707.0 |498.0  |897.01 |953.23 |
|Russia                          |2.0    |20.0   |306.0  |313.0  |375.34 |136.31 |
|Rwanda                          |127.0  |171.48 |137.89 |64.4   |36.05  |10.74  |
|Saint Lucia                     |15.0   |45.69  |44.01  |-0.8   |11.48  |7.34   |
|Saint Vincent and the Grenadines|12.0   |54.89  |49.86  |4.28   |9.73   |-4.31  |
|San Marino                      |224.0  |279.0  |435.0  |30.0   |35.0   |-30.18 |
|Saudi Arabia                    |1720.0 |4033.0 |11631.0|874.32 |1542.46|1466.53|
|Senegal                         |190.0  |278.0  |412.0  |2.27   |42.97  |46.35  |
|Serbia                          |1908.0 |4873.0 |3414.05|122.0  |130.82 |186.42 |
|Seychelles                      |11.0   |31.89  |35.54  |-8.57  |15.84  |15.26  |
|Singapore                       |85.0   |110.0  |200.0  |11.0   |28.83  |30.87  |
|Slovakia                        |485.0  |863.0  |635.74 |5.38   |4.19   |29.49  |
|Slovenia                        |977.0  |1220.0 |985.07 |55.0   |30.48  |35.3   |
|Somalia                         |80.0   |110.77 |90.87  |-0.19  |10.11  |6.23   |
|South Africa                    |1585.0 |2415.0 |1808.13|9.9    |10.45  |57.94  |
|Spain                           |120.0  |2277.0 |28768.0|10348.0|17209.0|11723.92|
|Sri Lanka                       |1.0    |1.0    |44.0   |19.01  |11.21  |15.75  |
|Sudan                           |19.0   |55.51  |41.81  |2.0    |-3.02  |0.61   |
|Suriname                        |10.0   |53.45  |55.42  |43.12  |26.98  |8.66   |
|Sweden                          |14.0   |500.0  |1763.0 |870.0  |1580.0 |1195.93|
|Switzerland                     |11811.0|21100.0|26336.0|666.0  |1174.0 |2094.07|
|Taiwan*                         |26.0   |41.0   |49.0   |1.0    |2.0    |5.0    |
|Tanzania                        |88.0   |110.82 |93.45  |0.18   |10.87  |8.48   |
|Thailand                        |35.0   |43.0   |70.0   |10.0   |33.0   |47.0   |
|Togo                            |44.0   |81.0   |83.47  |52.71  |31.23  |10.03  |
|Trinidad and Tobago             |113.0  |159.02 |124.35 |-13.72 |25.96  |10.0   |
|Tunisia                         |495.0  |726.0  |598.83 |37.0   |70.76  |46.81  |
|Turkey                          |47029.0|90980.0|65373.76|1643.0 |857.1  |2655.45|
|Uganda                          |56.0   |73.33  |65.98  |-2.28  |17.79  |15.66  |
|Ukraine                         |897.0  |2777.0 |1935.49|83.0   |118.76 |120.44 |
|United Arab Emirates            |19.0   |45.0   |140.0  |41.0   |108.63 |44.55  |
|United Kingdom                  |36.0   |459.0  |5067.0 |4320.0 |12129.0|12131.3|
|Uruguay                         |480.0  |468.73 |350.7  |-32.09 |1.69   |12.19  |
|US                              |15.0   |98.0   |1663.0 |2978.0 |16544.0|40661.0|
|Uzbekistan                      |1165.0 |1150.45|843.87 |33.68  |2.73   |-1.98  |
|Venezuela                       |189.0  |224.43 |170.3  |-19.68 |22.61  |9.84   |
|Vietnam                         |16.0   |16.0   |47.0   |2.78   |16.17  |10.22  |
|Zambia                          |52.0   |71.8   |70.64  |16.6   |20.94  |10.95  |
|Zimbabwe                        |25.0   |59.32  |50.36  |-39.79 |3.35   |0.42   |
|Dominica                        |16.0   |43.78  |45.16  |27.46  |25.72  |13.54  |
|Grenada                         |14.0   |13.42  |24.68  |6.66   |9.89   |12.78  |
|Mozambique                      |39.0   |59.46  |54.21  |-7.53  |17.96  |13.14  |
|Syria                           |42.0   |71.74  |64.35  |0.48   |11.92  |6.64   |
|Timor-Leste                     |23.0   |22.46  |31.13  |10.04  |7.2    |11.49  |
|Belize                          |19.97  |50.56  |48.42  |52.13  |33.48  |12.31  |
|Laos                            |10.91  |41.54  |43.28  |34.82  |28.16  |12.75  |
|Libya                           |2.34   |17.82  |24.87  |-6.3   |18.58  |12.85  |
|West Bank and Gaza              |217.0  |308.0  |253.58 |28.87  |27.42  |19.67  |
|Guinea-Bissau                   |-2.19  |-4.76  |10.38  |-6.69  |3.09   |13.09  |
|Mali                            |-3.54  |22.94  |25.44  |-1.71  |23.29  |13.48  |
|Saint Kitts and Nevis           |-16.15 |14.74  |21.47  |-5.52  |8.43   |5.02   |
|Kosovo                          |14.34  |48.2   |48.83  |46.09  |28.44  |9.05   |
|Burma                           |7.78   |37.36  |40.7   |26.97  |25.32  |12.81  |
|MS Zaandam                      |-20.94 |5.46   |16.04  |-23.43 |3.39   |3.41   |
|Botswana                        |16.25  |9.5    |17.75  |0.51   |6.48   |3.68   |
|Burundi                         |8.67   |46.49  |45.91  |42.49  |29.09  |11.11  |
|Sierra Leone                    |9.58   |42.52  |44.27  |37.37  |25.68  |9.09   |
|Malawi                          |2.7    |37.19  |37.1   |26.05  |28.33  |14.73  |
|South Sudan                     |2.97   |15.15  |24.41  |1.74   |13.43  |10.29  |
|Western Sahara                  |-12.04 |17.78  |23.55  |-18.49 |17.1   |10.31  |
|Sao Tome and Principe           |-17.99 |18.61  |24.28  |0.3    |12.26  |8.13   |
|Yemen                           |-20.26 |17.09  |22.95  |-0.54  |10.62  |6.56   |

###Incomplete matrix of public health indicators
|SH.DTH.COMM.ZS                  |SH.DYN.NCOM.ZS|SH.H2O.SMDW.ZS|SH.MED.PHYS.ZS|SH.STA.SMSS.ZS|SH.PRV.SMOK|SH.STA.HYGN.ZS|SP.DYN.LE00.IN|SP.POP.65UP.TO.ZS|SP.POP.1564.TO.ZS|
|--------------------------------|--------------|--------------|--------------|--------------|-----------|--------------|--------------|-----------------|-----------------|
|                                |              |              |1.12          |              |           |              |76.15         |13.55            |68.65            |
|36.4                            |29.8          |              |0.28          |              |           |37.75         |64.49         |2.58             |54.32            |
|63.4                            |16.5          |              |0.21          |              |           |26.66         |60.78         |2.22             |50.97            |
|2.9                             |17.0          |70.02         |1.2           |39.86         |28.7       |              |78.46         |13.74            |68.58            |
|                                |              |90.64         |3.33          |100.0         |33.5       |              |              |                 |                 |
|19.97                           |20.71         |              |1.1           |53.4          |21.96      |70.17         |71.62         |4.56             |62.66            |
|6.5                             |16.8          |              |2.39          |96.28         |28.9       |              |77.81         |1.09             |84.31            |
|15.9                            |15.8          |              |3.96          |              |21.8       |              |76.52         |11.12            |64.12            |
|2.8                             |22.3          |86.48         |2.9           |48.22         |24.1       |94.04         |74.94         |11.25            |68.11            |
|                                |              |12.58         |0.78          |              |           |              |              |                 |                 |
|11.9                            |22.6          |              |2.76          |              |           |              |76.89         |8.8              |69.12            |
|4.6                             |9.1           |              |3.59          |75.64         |14.7       |              |82.75         |15.66            |65.15            |
|2.6                             |11.4          |98.91         |5.14          |96.75         |29.6       |              |81.64         |19.0             |66.7             |
|8.8                             |22.2          |73.56         |3.45          |              |20.8       |83.24         |72.86         |6.2              |70.44            |
|55.8                            |22.9          |              |0.05          |              |           |6.14          |61.25         |2.25             |52.25            |
|7.9                             |11.4          |99.52         |3.32          |97.1          |28.2       |              |81.6          |18.79            |64.16            |
|54.1                            |19.6          |              |0.16          |              |6.4        |11.03         |61.47         |3.25             |54.3             |
|56.3                            |21.7          |              |0.06          |              |12.5       |11.88         |61.17         |2.41             |52.64            |
|25.6                            |21.6          |55.44         |0.53          |              |23.0       |34.81         |72.32         |5.16             |67.14            |
|2.2                             |23.6          |96.95         |3.99          |64.41         |37.0       |              |74.87         |21.02            |64.38            |
|6.9                             |11.3          |98.98         |0.93          |96.0          |26.4       |              |77.16         |2.43             |78.32            |
|16.9                            |15.5          |              |1.94          |              |11.5       |              |73.75         |7.26             |70.26            |
|1.8                             |17.8          |88.84         |2.0           |21.55         |38.9       |97.16         |77.26         |16.47            |68.76            |
|2.5                             |23.7          |94.52         |4.08          |80.52         |26.7       |              |74.18         |14.85            |68.29            |
|19.4                            |22.1          |              |1.13          |              |           |90.08         |74.5          |4.74             |64.98            |
|                                |              |              |1.77          |              |           |              |81.65         |                 |                 |
|22.4                            |17.2          |              |1.61          |22.94         |           |25.38         |71.24         |7.19             |61.73            |
|13.9                            |16.6          |              |2.15          |49.28         |13.9       |              |75.67         |8.92             |69.74            |
|13.0                            |16.2          |              |2.49          |              |7.8        |88.47         |79.08         |15.8             |66.85            |
|7.8                             |16.6          |              |1.77          |              |16.9       |              |75.72         |4.87             |72.1             |
|20.9                            |23.3          |36.16         |0.37          |              |           |79.81         |71.46         |6.0              |68.23            |
|46.0                            |20.3          |              |0.37          |              |20.0       |              |69.28         |4.22             |61.66            |
|63.7                            |23.1          |              |0.06          |              |           |16.6          |52.8          |2.83             |52.88            |
|5.6                             |9.8           |98.86         |2.61          |82.32         |14.3       |              |81.95         |17.23            |66.9             |
|4.02                            |19.38         |93.97         |2.88          |86.13         |30.39      |              |77.03         |18.46            |66.4             |
|4.3                             |8.6           |95.46         |4.24          |99.54         |25.7       |              |83.55         |18.62            |66.47            |
|                                |              |91.98         |1.52          |90.0          |           |              |82.93         |17.3             |67.51            |
|8.1                             |12.4          |98.64         |1.08          |77.46         |37.8       |              |80.04         |11.53            |68.72            |
|3.8                             |17.0          |              |1.79          |72.08         |25.6       |              |76.7          |10.92            |71.2             |
|52.4                            |29.1          |36.55         |0.23          |              |           |19.35         |57.42         |2.86             |55.2             |
|53.9                            |21.6          |              |0.09          |              |           |9.4           |58.92         |2.73             |54.64            |
|61.7                            |19.4          |              |0.09          |              |           |4.47          |60.37         |3.02             |50.82            |
|55.5                            |16.7          |45.35         |0.12          |              |26.9       |47.96         |64.29         |2.68             |55.55            |
|10.1                            |15.8          |73.23         |2.08          |16.99         |9.0        |65.39         |77.11         |8.48             |68.44            |
|47.4                            |22.9          |              |0.17          |              |14.0       |15.57         |64.12         |3.01             |57.45            |
|19.5                            |17.2          |              |0.77          |              |9.1        |              |72.78         |4.61             |66.61            |
|6.4                             |11.5          |93.8          |1.15          |              |11.9       |83.84         |80.1          |9.55             |69.13            |
|12.62                           |19.1          |              |1.57          |              |           |76.2          |73.52         |8.8              |67.49            |
|8.4                             |16.4          |              |8.19          |44.34         |35.2       |85.2          |78.73         |15.19            |68.6             |
|                                |              |              |              |              |           |              |78.02         |16.68            |64.43            |
|                                |              |              |1.94          |              |           |              |82.19         |                 |                 |
|4.1                             |11.3          |99.61         |1.95          |75.46         |36.4       |              |80.83         |13.72            |69.49            |
|5.4                             |15.0          |97.88         |4.31          |94.46         |34.3       |              |78.98         |19.42            |64.99            |
|4.8                             |12.1          |99.8          |4.21          |97.23         |30.6       |              |80.99         |21.46            |64.92            |
|45.2                            |19.6          |              |0.22          |36.44         |13.1       |              |66.58         |4.53             |65.9             |
|                                |              |              |1.08          |              |           |              |76.6          |                 |                 |
|6.5                             |11.3          |96.73         |4.46          |94.84         |19.1       |              |81.35         |19.81            |63.73            |
|15.8                            |19.0          |              |1.56          |              |13.7       |55.18         |73.89         |7.08             |64.94            |
|14.8                            |14.2          |              |1.83          |17.69         |15.6       |83.74         |76.69         |6.36             |63.49            |
|8.72                            |18.69         |              |1.48          |70.95         |26.71      |              |74.99         |9.5              |70.0             |
|24.94                           |22.27         |              |0.94          |              |17.03      |59.49         |70.26         |5.82             |65.28            |
|9.03                            |17.67         |              |1.58          |63.51         |26.23      |              |75.87         |10.74            |69.49            |
|4.95                            |23.07         |78.12         |3.05          |62.61         |30.98      |              |73.4          |12.05            |66.91            |
|5.27                            |16.82         |91.76         |3.37          |67.39         |29.29      |              |77.74         |16.35            |65.64            |
|15.1                            |13.0          |75.07         |2.05          |42.01         |7.1        |80.63         |76.8          |7.16             |64.81            |
|10.2                            |27.7          |              |0.79          |60.74         |25.2       |89.83         |71.82         |5.23             |60.97            |
|5.42                            |11.1          |98.07         |3.85          |93.94         |29.13      |              |81.95         |20.6             |64.33            |
|42.9                            |23.9          |              |0.06          |              |5.7        |              |65.94         |4.08             |55.74            |
|5.1                             |9.9           |98.44         |4.07          |96.62         |29.3       |              |83.33         |19.38            |65.95            |
|2.8                             |17.0          |93.33         |3.47          |97.36         |31.3       |              |78.54         |19.63            |64.02            |
|49.0                            |18.3          |11.44         |0.1           |              |4.4        |7.96          |66.24         |3.5              |55.72            |
|5.11                            |12.82         |97.19         |3.69          |92.37         |29.07      |              |80.97         |20.16            |64.69            |
|50.36                           |22.69         |              |0.39          |              |           |38.01         |61.5          |3.38             |55.64            |
|1.3                             |10.2          |99.63         |3.81          |99.21         |20.4       |              |81.83         |21.72            |62.13            |
|10.1                            |30.6          |              |0.84          |              |22.6       |              |67.34         |5.45             |65.04            |
|6.0                             |10.6          |97.85         |3.23          |88.37         |32.7       |              |82.53         |20.03            |62.01            |
|                                |              |              |              |              |           |              |82.55         |                 |                 |
|18.5                            |26.1          |              |0.18          |              |           |              |67.76         |4.0              |64.3             |
|49.9                            |14.4          |              |0.36          |              |           |              |66.19         |3.56             |59.41            |
|7.7                             |10.9          |99.99         |2.81          |97.75         |22.3       |              |81.36         |18.4             |63.93            |
|2.7                             |24.9          |79.99         |5.1           |27.17         |28.8       |              |73.6          |14.87            |65.34            |
|47.5                            |20.8          |36.41         |0.18          |              |3.9        |41.05         |63.78         |3.07             |59.34            |
|                                |              |100.0         |              |              |           |              |              |                 |                 |
|55.7                            |22.4          |              |0.08          |              |           |17.45         |61.18         |2.93             |53.22            |
|54.8                            |20.4          |              |0.11          |              |15.5       |7.88          |61.74         |2.59             |53.14            |
|62.1                            |20.0          |              |0.2           |              |           |6.4           |58.0          |2.82             |54.84            |
|53.4                            |22.0          |              |0.4           |              |           |24.64         |58.4          |2.46             |60.43            |
|10.9                            |12.4          |100.0         |4.59          |90.39         |43.4       |              |81.29         |21.66            |64.27            |
|11.9                            |21.4          |87.12         |1.45          |              |           |              |72.38         |9.62             |66.82            |
|                                |              |96.75         |1.14          |94.84         |           |              |70.85         |                 |                 |
|25.1                            |14.9          |55.99         |0.36          |              |           |76.67         |74.06         |4.81             |60.75            |
|                                |              |99.54         |1.08          |              |           |              |79.86         |9.85             |65.69            |
|20.0                            |30.5          |              |0.8           |              |           |77.16         |69.77         |6.45             |65.34            |
|6.69                            |12.14         |98.73         |3.0           |86.03         |24.1       |              |80.69         |17.93            |65.54            |
|                                |              |100.0         |1.32          |91.77         |           |              |84.93         |16.88            |71.22            |
|14.0                            |14.0          |              |0.31          |              |2.0        |84.17         |75.09         |4.69             |63.57            |
|52.91                           |21.03         |              |0.16          |              |           |19.53         |62.75         |3.03             |54.12            |
|2.3                             |16.7          |89.96         |3.0           |58.5          |37.0       |              |78.07         |20.45            |65.04            |
|30.3                            |26.5          |              |0.23          |              |12.7       |22.86         |63.66         |4.95             |61.81            |
|1.8                             |23.0          |89.57         |3.23          |95.68         |30.6       |              |75.82         |19.16            |66.43            |
|14.17                           |19.81         |              |1.46          |              |21.0       |              |73.2          |8.48             |67.93            |
|22.99                           |20.23         |              |1.21          |              |19.84      |              |70.86         |7.22             |65.29            |
|47.36                           |22.16         |              |0.44          |              |14.82      |35.63         |63.96         |3.56             |57.59            |
|50.08                           |22.82         |30.85         |0.72          |              |14.16      |46.04         |62.0          |3.5              |57.76            |
|20.7                            |26.4          |              |0.38          |              |39.4       |64.2          |71.51         |5.86             |67.59            |
|45.8                            |21.81         |              |0.3           |              |15.28      |30.15         |64.97         |3.59             |57.51            |
|                                |              |97.21         |1.45          |              |           |              |77.97         |                 |                 |
|26.0                            |23.3          |              |0.78          |              |11.5       |59.55         |69.42         |6.18             |66.77            |
|                                |              |              |              |              |           |              |              |                 |                 |
|5.1                             |10.3          |97.32         |3.09          |82.41         |24.3       |              |82.61         |13.87            |64.73            |
|7.9                             |14.8          |91.8          |1.14          |              |11.0       |              |76.48         |6.18             |69.34            |
|16.8                            |21.3          |58.83         |0.82          |41.07         |           |94.58         |70.45         |3.32             |58.29            |
|4.4                             |9.1           |100.0         |3.97          |81.76         |14.7       |              |82.66         |14.8             |65.37            |
|10.0                            |9.6           |99.38         |3.22          |93.67         |25.2       |              |82.8          |11.98            |60.1             |
|4.9                             |9.5           |95.04         |4.09          |96.21         |23.7       |              |82.95         |22.75            |63.92            |
|11.2                            |14.7          |              |1.32          |              |16.8       |66.42         |74.37         |8.8              |67.45            |
|10.7                            |19.2          |93.82         |2.34          |80.55         |           |              |74.4          |3.85             |61.91            |
|12.7                            |8.4           |98.45         |2.41          |98.76         |22.1       |              |84.21         |27.58            |59.73            |
|4.5                             |26.8          |89.51         |3.25          |              |24.0       |99.0          |73.15         |7.39             |64.15            |
|63.3                            |13.4          |              |0.2           |              |10.7       |24.65         |66.34         |2.34             |57.88            |
|9.6                             |24.9          |68.22         |1.88          |              |26.5       |89.22         |71.4          |4.49             |63.15            |
|25.6                            |21.1          |25.85         |0.17          |              |17.2       |66.23         |69.57         |4.57             |64.23            |
|28.7                            |28.4          |              |0.2           |              |47.0       |              |68.12         |3.95             |60.51            |
|                                |              |              |2.52          |              |           |              |71.34         |                 |                 |
|10.1                            |7.8           |98.21         |2.37          |99.9          |23.3       |              |82.63         |14.42            |72.61            |
|14.8                            |17.4          |100.0         |2.58          |100.0         |22.5       |              |75.4          |2.55             |75.91            |
|13.85                           |16.13         |              |2.19          |43.54         |13.58      |              |75.08         |8.24             |66.99            |
|31.4                            |27.0          |16.08         |0.5           |58.05         |28.9       |49.84         |67.61         |4.08             |63.32            |
|3.6                             |17.9          |47.7          |2.27          |21.76         |33.8       |              |78.88         |7.0              |66.9             |
|58.5                            |17.6          |              |0.04          |              |9.8        |1.19          |63.73         |3.25             |55.62            |
|8.0                             |20.1          |              |2.16          |26.11         |           |              |72.72         |4.39             |67.29            |
|9.7                             |18.8          |              |0.11          |              |           |87.2          |76.06         |9.81             |71.66            |
|13.63                           |16.01         |74.29         |2.17          |31.33         |14.35      |              |75.28         |8.44             |67.01            |
|47.55                           |21.63         |              |0.26          |              |15.88      |28.28         |64.71         |3.54             |57.03            |
|50.12                           |21.69         |26.68         |0.32          |              |           |23.22         |63.39         |3.29             |54.82            |
|                                |              |100.0         |              |99.65         |           |              |83.75         |                 |                 |
|7.5                             |17.4          |              |0.96          |              |13.0       |              |76.81         |10.47            |65.33            |
|30.25                           |23.21         |53.66         |0.75          |              |17.36      |57.33         |68.32         |5.53             |64.29            |
|23.12                           |20.3          |              |1.22          |              |19.76      |              |70.8          |7.16             |65.29            |
|59.3                            |26.6          |              |0.07          |              |26.7       |2.12          |53.7          |4.9              |62.38            |
|5.88                            |17.65         |              |1.95          |67.45         |24.75      |              |76.0          |10.72            |70.26            |
|3.6                             |20.7          |92.04         |4.34          |91.31         |28.8       |              |76.29         |19.71            |65.41            |
|4.9                             |10.0          |99.72         |3.03          |96.64         |23.5       |              |82.1          |14.18            |69.94            |
|2.7                             |21.9          |95.19         |3.19          |85.82         |37.0       |              |74.68         |20.04            |63.96            |
|                                |              |100.0         |1.56          |              |           |              |84.12         |10.48            |75.86            |
|                                |              |              |              |              |           |              |79.87         |                 |                 |
|14.0                            |12.4          |70.27         |0.73          |38.75         |23.4       |              |76.45         |7.01             |65.78            |
|                                |              |100.0         |6.56          |100.0         |           |              |              |                 |                 |
|4.2                             |24.9          |72.88         |3.2           |              |24.2       |86.98         |71.81         |11.47            |72.67            |
|46.2                            |22.9          |              |0.18          |              |           |50.54         |66.68         |2.99             |56.35            |
|8.0                             |13.4          |              |1.04          |              |28.3       |95.8          |78.63         |3.7              |76.15            |
|12.05                           |18.86         |77.77         |1.26          |34.74         |19.48      |              |73.9          |5.18             |64.93            |
|9.8                             |15.7          |42.87         |2.25          |50.41         |14.0       |87.85         |74.99         |7.22             |66.22            |
|                                |              |              |0.46          |              |           |82.5          |65.24         |                 |                 |
|19.5                            |20.19         |              |1.32          |              |20.26      |              |71.7          |7.64             |66.59            |
|1.9                             |20.3          |81.01         |2.87          |16.56         |           |              |75.69         |13.67            |69.81            |
|60.6                            |24.6          |              |0.14          |18.71         |12.3       |52.23         |58.89         |2.51             |49.95            |
|6.4                             |10.8          |100.0         |3.83          |92.98         |25.5       |              |82.35         |20.35            |65.37            |
|23.6                            |24.2          |              |0.86          |              |20.3       |79.29         |66.87         |5.78             |67.84            |
|12.24                           |19.57         |              |1.07          |              |19.44      |              |73.39         |5.38             |63.51            |
|1.4                             |20.6          |93.6          |2.33          |              |45.9       |              |76.77         |14.97            |66.82            |
|9.7                             |30.2          |23.72         |2.89          |              |25.6       |71.18         |69.69         |4.08             |65.51            |
|                                |              |90.24         |0.44          |              |           |              |              |                 |                 |
|65.3                            |18.4          |              |0.07          |              |16.6       |12.23         |60.16         |2.89             |52.44            |
|53.4                            |18.1          |              |0.18          |              |           |43.0          |64.7          |3.14             |56.78            |
|6.5                             |22.6          |              |2.02          |              |21.6       |              |74.42         |11.47            |70.73            |
|59.7                            |16.4          |              |0.02          |              |14.5       |8.7           |63.8          |2.65             |53.45            |
|17.5                            |17.2          |93.33         |1.51          |88.63         |21.5       |              |76.0          |6.67             |69.33            |
|5.23                            |14.09         |99.03         |2.6           |79.79         |21.03      |              |78.91         |15.95            |65.63            |
|49.3                            |21.3          |              |0.37          |              |21.4       |44.6          |63.37         |3.64             |59.45            |
|                                |              |96.66         |1.98          |              |           |              |77.15         |9.17             |68.08            |
|62.7                            |20.0          |              |0.05          |9.6           |7.7        |9.31          |62.02         |2.6              |47.42            |
|62.7                            |22.5          |20.13         |0.38          |26.65         |5.8        |41.95         |54.33         |2.75             |53.39            |
|10.9                            |14.2          |51.6          |1.01          |              |           |              |74.28         |5.25             |64.55            |
|5.2                             |11.2          |99.95         |3.51          |97.47         |25.8       |              |81.76         |19.2             |64.7             |
|7.3                             |9.2           |98.34         |4.63          |76.32         |20.2       |              |82.81         |17.05            |65.4             |
|25.0                            |21.8          |27.24         |0.65          |              |22.8       |47.78         |70.48         |5.73             |63.86            |
|                                |              |              |1.24          |              |40.0       |              |              |                 |                 |
|4.6                             |10.1          |100.0         |3.03          |88.68         |16.0       |              |81.86         |15.65            |64.69            |
|6.68                            |12.43         |92.7          |2.89          |86.9          |23.65      |              |80.14         |17.12            |65.05            |
|10.5                            |17.8          |90.28         |1.97          |              |11.1       |              |77.63         |2.39             |75.36            |
|39.53                           |18.38         |              |0.77          |              |23.21      |              |68.21         |5.49             |64.57            |
|34.9                            |24.7          |35.31         |0.98          |              |20.1       |59.61         |67.11         |4.31             |60.42            |
|15.6                            |13.0          |              |1.57          |              |6.1        |              |78.33         |8.1              |64.83            |
|20.3                            |12.6          |50.35         |1.27          |42.76         |4.8        |              |76.52         |8.09             |66.12            |

###Completed matrix of public health indicators with predictions
|6                               |7      |8      |9      |10     |11     |12     |13   |14   |15   |
|--------------------------------|-------|-------|-------|-------|-------|-------|-----|-----|-----|
|21.19                           |18.56  |60.39  |1.12   |47.86  |20.05  |45.42  |76.15|13.55|68.65|
|36.4                            |29.8   |37.53  |0.28   |30.64  |17.65  |37.75  |64.49|2.58 |54.32|
|63.4                            |16.5   |30.79  |0.21   |34.73  |10.09  |26.66  |60.78|2.22 |50.97|
|2.9                             |17.0   |70.02  |1.2    |39.86  |28.7   |54.27  |78.46|13.74|68.58|
|8.09                            |14.06  |90.64  |3.33   |100.0  |33.5   |42.96  |74.6 |15.52|62.61|
|19.97                           |20.71  |61.37  |1.1    |53.4   |21.96  |70.17  |71.62|4.56 |62.66|
|6.5                             |16.8   |91.53  |2.39   |96.28  |28.9   |57.97  |77.81|1.09 |84.31|
|15.9                            |15.8   |63.44  |3.96   |51.12  |21.8   |46.01  |76.52|11.12|64.12|
|2.8                             |22.3   |86.48  |2.9    |48.22  |24.1   |94.04  |74.94|11.25|68.11|
|5.88                            |2.87   |12.58  |0.78   |25.75  |3.67   |11.41  |6.61 |0.05 |6.36 |
|11.9                            |22.6   |61.59  |2.76   |46.3   |20.87  |53.15  |76.89|8.8  |69.12|
|4.6                             |9.1    |80.19  |3.59   |75.64  |14.7   |46.81  |82.75|15.66|65.15|
|2.6                             |11.4   |98.91  |5.14   |96.75  |29.6   |51.35  |81.64|19.0 |66.7 |
|8.8                             |22.2   |73.56  |3.45   |52.9   |20.8   |83.24  |72.86|6.2  |70.44|
|55.8                            |22.9   |25.4   |0.05   |26.44  |12.35  |6.14   |61.25|2.25 |52.25|
|7.9                             |11.4   |99.52  |3.32   |97.1   |28.2   |48.82  |81.6 |18.79|64.16|
|54.1                            |19.6   |74.36  |0.16   |89.96  |6.4    |11.03  |61.47|3.25 |54.3 |
|56.3                            |21.7   |26.0   |0.06   |26.21  |12.5   |11.88  |61.17|2.41 |52.64|
|25.6                            |21.6   |55.44  |0.53   |44.26  |23.0   |34.81  |72.32|5.16 |67.14|
|2.2                             |23.6   |96.95  |3.99   |64.41  |37.0   |54.37  |74.87|21.02|64.38|
|6.9                             |11.3   |98.98  |0.93   |96.0   |26.4   |51.66  |77.16|2.43 |78.32|
|16.9                            |15.5   |77.64  |1.94   |81.85  |11.5   |70.67  |73.75|7.26 |70.26|
|1.8                             |17.8   |88.84  |2.0    |21.55  |38.9   |97.16  |77.26|16.47|68.76|
|2.5                             |23.7   |94.52  |4.08   |80.52  |26.7   |53.27  |74.18|14.85|68.29|
|19.4                            |22.1   |59.98  |1.13   |40.91  |20.62  |90.08  |74.5 |4.74 |64.98|
|24.29                           |17.96  |59.91  |1.77   |47.32  |18.98  |45.44  |81.65|10.08|66.52|
|22.4                            |17.2   |42.14  |1.61   |22.94  |14.07  |25.38  |71.24|7.19 |61.73|
|13.9                            |16.6   |62.93  |2.15   |49.28  |13.9   |47.13  |75.67|8.92 |69.74|
|13.0                            |16.2   |63.96  |2.49   |36.82  |7.8    |88.47  |79.08|15.8 |66.85|
|7.8                             |16.6   |63.25  |1.77   |46.86  |16.9   |50.81  |75.72|4.87 |72.1 |
|20.9                            |23.3   |36.16  |0.37   |26.0   |18.08  |79.81  |71.46|6.0  |68.23|
|46.0                            |20.3   |53.88  |0.37   |55.03  |20.0   |38.67  |69.28|4.22 |61.66|
|63.7                            |23.1   |257.96 |0.06   |285.11 |95.75  |16.6   |52.8 |2.83 |52.88|
|5.6                             |9.8    |98.86  |2.61   |82.32  |14.3   |49.21  |81.95|17.23|66.9 |
|4.02                            |19.38  |93.97  |2.88   |86.13  |30.39  |49.39  |77.03|18.46|66.4 |
|4.3                             |8.6    |95.46  |4.24   |99.54  |25.7   |46.99  |83.55|18.62|66.47|
|12.14                           |14.37  |91.98  |1.52   |90.0   |25.76  |47.52  |82.93|17.3 |67.51|
|8.1                             |12.4   |98.64  |1.08   |77.46  |37.8   |52.33  |80.04|11.53|68.72|
|3.8                             |17.0   |77.96  |1.79   |72.08  |25.6   |53.3   |76.7 |10.92|71.2 |
|52.4                            |29.1   |36.55  |0.23   |30.66  |17.17  |19.35  |57.42|2.86 |55.2 |
|53.9                            |21.6   |28.49  |0.09   |29.74  |12.58  |9.4    |58.92|2.73 |54.64|
|61.7                            |19.4   |24.36  |0.09   |27.17  |11.11  |4.47   |60.37|3.02 |50.82|
|55.5                            |16.7   |45.35  |0.12   |43.8   |26.9   |47.96  |64.29|2.68 |55.55|
|10.1                            |15.8   |73.23  |2.08   |16.99  |9.0    |65.39  |77.11|8.48 |68.44|
|47.4                            |22.9   |34.6   |0.17   |32.14  |14.0   |15.57  |64.12|3.01 |57.45|
|19.5                            |17.2   |55.19  |0.77   |43.5   |9.1    |49.2   |72.78|4.61 |66.61|
|6.4                             |11.5   |93.8   |1.15   |70.57  |11.9   |83.84  |80.1 |9.55 |69.13|
|12.62                           |19.1   |63.46  |1.57   |45.8   |20.4   |76.2   |73.52|8.8  |67.49|
|8.4                             |16.4   |70.14  |8.19   |44.34  |35.2   |85.2   |78.73|15.19|68.6 |
|19.52                           |16.77  |61.96  |2.59   |49.29  |20.25  |43.89  |78.02|16.68|64.43|
|24.33                           |18.06  |60.33  |1.94   |47.64  |19.11  |45.77  |82.19|10.23|66.94|
|4.1                             |11.3   |99.61  |1.95   |75.46  |36.4   |54.09  |80.83|13.72|69.49|
|5.4                             |15.0   |97.88  |4.31   |94.46  |34.3   |47.67  |78.98|19.42|64.99|
|4.8                             |12.1   |99.8   |4.21   |97.23  |30.6   |46.97  |80.99|21.46|64.92|
|45.2                            |19.6   |41.2   |0.22   |36.44  |13.1   |32.84  |66.58|4.53 |65.9 |
|23.2                            |16.99  |57.65  |1.08   |47.18  |17.69  |41.47  |76.6 |9.14 |62.57|
|6.5                             |11.3   |96.73  |4.46   |94.84  |19.1   |11.54  |81.35|19.81|63.73|
|15.8                            |19.0   |56.59  |1.56   |41.38  |13.7   |55.18  |73.89|7.08 |64.94|
|14.8                            |14.2   |50.43  |1.83   |17.69  |15.6   |83.74  |76.69|6.36 |63.49|
|8.72                            |18.69  |74.74  |1.48   |70.95  |26.71  |48.61  |74.99|9.5  |70.0 |
|24.94                           |22.27  |84.65  |0.94   |85.06  |17.03  |59.49  |70.26|5.82 |65.28|
|9.03                            |17.67  |72.48  |1.58   |63.51  |26.23  |48.68  |75.87|10.74|69.49|
|4.95                            |23.07  |78.12  |3.05   |62.61  |30.98  |52.02  |73.4 |12.05|66.91|
|5.27                            |16.82  |91.76  |3.37   |67.39  |29.29  |51.33  |77.74|16.35|65.64|
|15.1                            |13.0   |75.07  |2.05   |42.01  |7.1    |80.63  |76.8 |7.16 |64.81|
|10.2                            |27.7   |68.63  |0.79   |60.74  |25.2   |89.83  |71.82|5.23 |60.97|
|5.42                            |11.1   |98.07  |3.85   |93.94  |29.13  |46.94  |81.95|20.6 |64.33|
|42.9                            |23.9   |33.33  |0.06   |27.09  |5.7    |31.54  |65.94|4.08 |55.74|
|5.1                             |9.9    |98.44  |4.07   |96.62  |29.3   |47.52  |83.33|19.38|65.95|
|2.8                             |17.0   |93.33  |3.47   |97.36  |31.3   |47.78  |78.54|19.63|64.02|
|49.0                            |18.3   |11.44  |0.1    |19.66  |4.4    |7.96   |66.24|3.5  |55.72|
|5.11                            |12.82  |97.19  |3.69   |92.37  |29.07  |51.94  |80.97|20.16|64.69|
|50.36                           |22.69  |36.26  |0.39   |35.71  |14.37  |38.01  |61.5 |3.38 |55.64|
|1.3                             |10.2   |99.63  |3.81   |99.21  |20.4   |121.05 |81.83|21.72|62.13|
|10.1                            |30.6   |54.63  |0.84   |41.36  |22.6   |49.61  |67.34|5.45 |65.04|
|6.0                             |10.6   |97.85  |3.23   |88.37  |32.7   |62.56  |82.53|20.03|62.01|
|18.46                           |17.8   |58.16  |2.02   |44.96  |16.41  |69.25  |82.55|11.29|68.39|
|18.5                            |26.1   |111.55 |0.18   |122.89 |14.0   |75.99  |67.76|4.0  |64.3 |
|49.9                            |14.4   |36.72  |0.36   |32.72  |12.13  |28.41  |66.19|3.56 |59.41|
|7.7                             |10.9   |99.99  |2.81   |97.75  |22.3   |47.73  |81.36|18.4 |63.93|
|2.7                             |24.9   |79.99  |5.1    |27.17  |28.8   |57.36  |73.6 |14.87|65.34|
|47.5                            |20.8   |36.41  |0.18   |28.61  |3.9    |41.05  |63.78|3.07 |59.34|
|1.99                            |11.92  |100.0  |2.72   |70.08  |23.28  |47.78  |71.49|13.89|60.21|
|55.7                            |22.4   |19.53  |0.08   |23.66  |8.89   |17.45  |61.18|2.93 |53.22|
|54.8                            |20.4   |29.22  |0.11   |30.97  |15.5   |7.88   |61.74|2.59 |53.14|
|62.1                            |20.0   |24.46  |0.2    |26.55  |11.82  |6.4    |58.0 |2.82 |54.84|
|53.4                            |22.0   |30.86  |0.4    |28.68  |13.96  |24.64  |58.4 |2.46 |60.43|
|10.9                            |12.4   |100.0  |4.59   |90.39  |43.4   |48.39  |81.29|21.66|64.27|
|11.9                            |21.4   |87.12  |1.45   |61.16  |23.94  |49.43  |72.38|9.62 |66.82|
|4.24                            |11.07  |96.75  |1.14   |94.84  |24.4   |42.16  |70.85|14.07|59.55|
|25.1                            |14.9   |55.99  |0.36   |40.04  |16.8   |76.67  |74.06|4.81 |60.75|
|9.9                             |14.45  |99.54  |1.08   |72.0   |23.83  |54.68  |79.86|9.85 |65.69|
|20.0                            |30.5   |53.11  |0.8    |35.54  |22.59  |77.16  |69.77|6.45 |65.34|
|6.69                            |12.14  |98.73  |3.0    |86.03  |24.1   |47.79  |80.69|17.93|65.54|
|10.54                           |15.08  |100.0  |1.32   |91.77  |26.64  |50.06  |84.93|16.88|71.22|
|14.0                            |14.0   |56.83  |0.31   |36.19  |2.0    |84.17  |75.09|4.69 |63.57|
|52.91                           |21.03  |29.37  |0.16   |27.6   |12.85  |19.53  |62.75|3.03 |54.12|
|2.3                             |16.7   |89.96  |3.0    |58.5   |37.0   |52.96  |78.07|20.45|65.04|
|30.3                            |26.5   |46.99  |0.23   |46.5   |12.7   |22.86  |63.66|4.95 |61.81|
|1.8                             |23.0   |89.57  |3.23   |95.68  |30.6   |50.88  |75.82|19.16|66.43|
|14.17                           |19.81  |59.5   |1.46   |45.44  |21.0   |47.14  |73.2 |8.48 |67.93|
|22.99                           |20.23  |52.99  |1.21   |41.42  |19.84  |42.64  |70.86|7.22 |65.29|
|47.36                           |22.16  |35.24  |0.44   |29.67  |14.82  |35.63  |63.96|3.56 |57.59|
|50.08                           |22.82  |30.85  |0.72   |28.86  |14.16  |46.04  |62.0 |3.5  |57.76|
|20.7                            |26.4   |59.08  |0.38   |44.41  |39.4   |64.2   |71.51|5.86 |67.59|
|45.8                            |21.81  |35.41  |0.3    |30.4   |15.28  |30.15  |64.97|3.59 |57.51|
|21.72                           |19.07  |97.21  |1.45   |108.48 |21.75  |65.27  |77.97|9.68 |67.51|
|26.0                            |23.3   |51.11  |0.78   |38.25  |11.5   |59.55  |69.42|6.18 |66.77|
|0.01                            |0.0    |0.02   |-0.0   |0.02   |0.01   |-0.01  |-0.0 |-0.0 |-0.0 |
|5.1                             |10.3   |97.32  |3.09   |82.41  |24.3   |49.17  |82.61|13.87|64.73|
|7.9                             |14.8   |91.8   |1.14   |63.14  |11.0   |51.15  |76.48|6.18 |69.34|
|16.8                            |21.3   |58.83  |0.82   |41.07  |19.73  |94.58  |70.45|3.32 |58.29|
|4.4                             |9.1    |100.0  |3.97   |81.76  |14.7   |56.45  |82.66|14.8 |65.37|
|10.0                            |9.6    |99.38  |3.22   |93.67  |25.2   |45.94  |82.8 |11.98|60.1 |
|4.9                             |9.5    |95.04  |4.09   |96.21  |23.7   |56.8   |82.95|22.75|63.92|
|11.2                            |14.7   |70.04  |1.32   |54.94  |16.8   |66.42  |74.37|8.8  |67.45|
|10.7                            |19.2   |93.82  |2.34   |80.55  |23.82  |47.67  |74.4 |3.85 |61.91|
|12.7                            |8.4    |98.45  |2.41   |98.76  |22.1   |41.77  |84.21|27.58|59.73|
|4.5                             |26.8   |89.51  |3.25   |82.01  |24.0   |99.0   |73.15|7.39 |64.15|
|63.3                            |13.4   |30.6   |0.2    |29.54  |10.7   |24.65  |66.34|2.34 |57.88|
|9.6                             |24.9   |68.22  |1.88   |55.12  |26.5   |89.22  |71.4 |4.49 |63.15|
|25.6                            |21.1   |25.85  |0.17   |41.6   |17.2   |66.23  |69.57|4.57 |64.23|
|28.7                            |28.4   |56.81  |0.2    |52.34  |47.0   |46.98  |68.12|3.95 |60.51|
|18.37                           |15.78  |61.58  |2.52   |55.97  |16.39  |47.0   |71.34|9.63 |59.02|
|10.1                            |7.8    |98.21  |2.37   |99.9   |23.3   |42.41  |82.63|14.42|72.61|
|14.8                            |17.4   |100.0  |2.58   |100.0  |22.5   |47.8   |75.4 |2.55 |75.91|
|13.85                           |16.13  |58.56  |2.19   |43.54  |13.58  |46.23  |75.08|8.24 |66.99|
|31.4                            |27.0   |16.08  |0.5    |58.05  |28.9   |49.84  |67.61|4.08 |63.32|
|3.6                             |17.9   |47.7   |2.27   |21.76  |33.8   |52.88  |78.88|7.0  |66.9 |
|58.5                            |17.6   |38.65  |0.04   |49.23  |9.8    |1.19   |63.73|3.25 |55.62|
|8.0                             |20.1   |51.56  |2.16   |26.11  |17.07  |51.07  |72.72|4.39 |67.29|
|9.7                             |18.8   |75.23  |0.11   |59.88  |21.07  |87.2   |76.06|9.81 |71.66|
|13.63                           |16.01  |74.29  |2.17   |31.33  |14.35  |50.56  |75.28|8.44 |67.01|
|47.55                           |21.63  |34.81  |0.26   |30.56  |15.88  |28.28  |64.71|3.54 |57.03|
|50.12                           |21.69  |26.68  |0.32   |26.82  |12.98  |23.22  |63.39|3.29 |54.82|
|11.19                           |14.55  |100.0  |2.96   |99.65  |27.17  |48.32  |83.75|15.45|69.54|
|7.5                             |17.4   |62.09  |0.96   |46.17  |13.0   |48.43  |76.81|10.47|65.33|
|30.25                           |23.21  |53.66  |0.75   |41.64  |17.36  |57.33  |68.32|5.53 |64.29|
|23.12                           |20.3   |239.81 |1.22   |329.53 |19.76  |-14.8  |70.8 |7.16 |65.29|
|59.3                            |26.6   |27.24  |0.07   |30.04  |26.7   |2.12   |53.7 |4.9  |62.38|
|5.88                            |17.65  |74.37  |1.95   |67.45  |24.75  |49.88  |76.0 |10.72|70.26|
|3.6                             |20.7   |92.04  |4.34   |91.31  |28.8   |48.02  |76.29|19.71|65.41|
|4.9                             |10.0   |99.72  |3.03   |96.64  |23.5   |49.62  |82.1 |14.18|69.94|
|2.7                             |21.9   |95.19  |3.19   |85.82  |37.0   |72.2   |74.68|20.04|63.96|
|11.4                            |17.53  |100.0  |1.56   |70.02  |25.03  |56.13  |84.12|10.48|75.86|
|23.75                           |17.57  |58.71  |1.78   |46.39  |18.61  |44.44  |79.87|9.89 |65.07|
|14.0                            |12.4   |70.27  |0.73   |38.75  |23.4   |48.07  |76.45|7.01 |65.78|
|4.53                            |12.11  |100.0  |6.56   |100.0  |26.41  |45.58  |77.57|17.19|64.04|
|4.2                             |24.9   |72.88  |3.2    |48.04  |24.2   |86.98  |71.81|11.47|72.67|
|46.2                            |22.9   |38.84  |0.18   |31.58  |15.77  |50.54  |66.68|2.99 |56.35|
|8.0                             |13.4   |235.14 |1.04   |300.22 |28.3   |95.8   |78.63|3.7  |76.15|
|12.05                           |18.86  |77.77  |1.26   |34.74  |19.48  |51.71  |73.9 |5.18 |64.93|
|9.8                             |15.7   |42.87  |2.25   |50.41  |14.0   |87.85  |74.99|7.22 |66.22|
|7.57                            |17.85  |57.28  |0.46   |38.33  |18.77  |82.5   |65.24|6.55 |58.09|
|19.5                            |20.19  |80.76  |1.32   |23.44  |20.26  |152.93 |71.7 |7.64 |66.59|
|1.9                             |20.3   |81.01  |2.87   |16.56  |21.27  |59.18  |75.69|13.67|69.81|
|60.6                            |24.6   |82.15  |0.14   |18.71  |12.3   |52.23  |58.89|2.51 |49.95|
|6.4                             |10.8   |100.0  |3.83   |92.98  |25.5   |46.63  |82.35|20.35|65.37|
|23.6                            |24.2   |52.63  |0.86   |35.31  |20.3   |79.29  |66.87|5.78 |67.84|
|12.24                           |19.57  |57.23  |1.07   |43.05  |19.44  |46.93  |73.39|5.38 |63.51|
|1.4                             |20.6   |93.6   |2.33   |69.22  |45.9   |55.0   |76.77|14.97|66.82|
|9.7                             |30.2   |23.72  |2.89   |19.56  |25.6   |71.18  |69.69|4.08 |65.51|
|2.47                            |10.93  |90.24  |0.44   |62.78  |20.66  |43.28  |64.63|11.69|54.77|
|65.3                            |18.4   |24.41  |0.07   |26.48  |16.6   |12.23  |60.16|2.89 |52.44|
|53.4                            |18.1   |33.49  |0.18   |27.77  |13.19  |43.0   |64.7 |3.14 |56.78|
|6.5                             |22.6   |64.38  |2.02   |48.01  |21.6   |51.4   |74.42|11.47|70.73|
|59.7                            |16.4   |28.35  |0.02   |29.61  |14.5   |8.7    |63.8 |2.65 |53.45|
|17.5                            |17.2   |93.33  |1.51   |88.63  |21.5   |45.42  |76.0 |6.67 |69.33|
|5.23                            |14.09  |99.03  |2.6    |79.79  |21.03  |49.31  |78.91|15.95|65.63|
|49.3                            |21.3   |36.69  |0.37   |30.31  |21.4   |44.6   |63.37|3.64 |59.45|
|8.74                            |15.22  |96.66  |1.98   |68.15  |23.19  |51.26  |77.15|9.17 |68.08|
|62.7                            |20.0   |15.23  |0.05   |9.6    |7.7    |9.31   |62.02|2.6  |47.42|
|62.7                            |22.5   |20.13  |0.38   |26.65  |5.8    |41.95  |54.33|2.75 |53.39|
|10.9                            |14.2   |51.6   |1.01   |40.28  |15.85  |45.84  |74.28|5.25 |64.55|
|5.2                             |11.2   |99.95  |3.51   |97.47  |25.8   |46.7   |81.76|19.2 |64.7 |
|7.3                             |9.2    |98.34  |4.63   |76.32  |20.2   |48.94  |82.81|17.05|65.4 |
|25.0                            |21.8   |27.24  |0.65   |25.81  |22.8   |47.78  |70.48|5.73 |63.86|
|6.97                            |14.04  |38.71  |1.24   |32.54  |40.0   |27.16  |38.01|7.88 |34.18|
|4.6                             |10.1   |100.0  |3.03   |88.68  |16.0   |47.66  |81.86|15.65|64.69|
|6.68                            |12.43  |92.7   |2.89   |86.9   |23.65  |46.74  |80.14|17.12|65.05|
|10.5                            |17.8   |90.28  |1.97   |61.07  |11.1   |53.49  |77.63|2.39 |75.36|
|39.53                           |18.38  |45.89  |0.77   |38.72  |23.21  |35.67  |68.21|5.49 |64.57|
|34.9                            |24.7   |35.31  |0.98   |27.23  |20.1   |59.61  |67.11|4.31 |60.42|
|15.6                            |13.0   |57.96  |1.57   |43.7   |6.1    |44.68  |78.33|8.1  |64.83|
|20.3                            |12.6   |50.35  |1.27   |42.76  |4.8    |41.65  |76.52|8.09 |66.12|

## Conclusion
Although some predicted data entries are flawed from our result (such as decreasing 
number of cases and death tolls and negative values for death tolls), our model was able 
to fill in values for missing data entries. The flawed data prediction could be a result 
from the difference in the nature of data we were handling with compared to the Netflix 
problem. For example, the matrix of Covid-19 cases and death count is a time series data 
while the Netflix challenge is not. Hence, the variance in type of data that we were 
working with may have diverged the result and performance of our model.

Nevertheless, there were no values that were predicted that lied outside of the range of 
existing values in the incomplete public health indicators matrix. This shows promising 
sign for the algorithm. For further exploration of this model, it should be tested on 
different types of data (panel data, time-series etc.) to reason why or why not it could 
be a viable solution for predicting missing data entries. 
