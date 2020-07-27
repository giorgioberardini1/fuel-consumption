# Fuel Consumption


The dataset we are going to work with contains transactions about a company that manages 82 gas stations located in Italy for the years 2018 and 2019.

**It's crucial for the sales department to quantify how much fuel needs to be reloaded into a single gas station.**

Why? 

Let's assume for simplicity that the company capital is $1 million and number of the store is 4.  
                
               
The first idea is to divide $1 million by four and reload each tank for that amount of fuel. Assuming that the cost of one liter is 0.669 we can summarize our problem as follow:

                  
|   | store 1 |  store 2 | store 3 | store 4 |
| --- | --- | --- | --- | --- |     
| re-loading cost ($) | 250K | 250K | 250K | 250K |
| new liters availability (L) | 374K | 374K | 374K | 374K |




_savings($): 0_
                  

What's wrong with this approach? 

Imagine an hot italian summer day: everyone is moving from city to the sea and, since store 1 and 2 are located close to the sea, they ruin out its fuel faster than the ones located in non-sea city.



**What if we know beforehand how much fuel will be consumed in each store?**

 
We can base the reloading cost on the prediction. 

                  
|   | store 1 |  store 2 | store 3 | store 4 |
| --- | --- | --- | --- | --- |
| re-loading cost ($) | 167K | 134K | 67K | 67K |
| prediction (L) | 300K | 250K | 100K | 100K |




_savings ($): 489000_



**With this approach we are re-loading the tank of the exactly quantity needed by saving capital that could be spent on others stores.**


In a real scenario there are multiple factors that might affects the fuel consuption, in this projects we are going to explore them in order to find a Regressor that can handle this problem. 
