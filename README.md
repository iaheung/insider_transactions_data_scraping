# Insider Trading Dashboard

Having access to insider transactions can allow investors to learn more about the internal happenings in a company. Insider decisions can influence stock prices and allow us from the outside to better understand the confidence company officials have in their own business. This project aims to help investors make decisions based on insider transactions using interactive data visualizations made in Tableau.

In this project, I have split the project into two phases, the first phase being the web scraping part of the project, and the second phase being the interactive dashboard constructed on Tableau. 

## Table of Contents
- Contents and Usage
- Required Software and Packages
- Web Scraping
- Data Cleaning and Processing
- Tableau Dashboard
- Conclusions

## Contents and Usage
To get insider data, there are two .bat files to run the scripts. If you are on a Mac/Linux device, a separate version of the .bat files is written in .sh files.

Use a Task Scheduler to run the batch file every day in order to update the data with the previous day's trading data. Here is a [video](https://www.youtube.com/watch?v=EInOL6D5f3Q) on how to use Windows Task Scheduler. Likewise, for Mac, here is a guide on how to use [Automator](https://www.youtube.com/watch?v=nVlOapHc-kg).

## Required Software and Packages
Here is the list of required Python packages:

- pandas
- requests
- yfinance

Anaconda
```
conda install pandas requests -c conda-forge yfinance
```

Pip
```
pip install pandas yfinance requests
```

I used Tableau Public since it is free. If you wish to, Tableau Desktop can be used. To download Tableau Public, you will need to fill in your information, then download the application through this [link](https://www.tableau.com/products/public/download).

## Web Scraping
The data was scraped from openinsider.com, where all transactions processed under the SEC Form 4 will be listed. The requests package was used to obtain the data. Information such as company ticker, shares traded, transaction type, etc. was collected. 

## Data Cleaning and Processing
After scraping the data, before it can be put onto the Tableau Dashboard, the data needs to be cleaned. Some tickers have extra characters, so those are cleaned, and the stock prices and transaction value amounts are read in as strings with dollar signs and commas, so they are converted into floats.

## Tableau Dashboard (Note to self: add KPIs for number of transactions)
The Tableau Dashboard's role is to highlight key performance indicators (KPIs) that show an overview of the insider transactions across a time period. Along with KPIs, there are interactive charts and tables to help investors key in on specific trends, such as sector specific transactions, insiders with the highest transaction value, and buy vs sell trends.



## Conclusions
