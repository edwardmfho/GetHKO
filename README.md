# GetHKO
HKO.gov.hk was not really data-friendly, this tool is design to extract data from HKO website. 

At the very first stage, I have used selenium to scrap the rainfall data from the HKO website.

You can simply use the following code to initialize the instance:

```
# import the package
from Rainfall import Raindrop

# Set up the year you'd want to extract

BEGIN_YEAR = 1974 # BEGINNING YEAR
END_YEAR = 2021 # ENDING YEAR 

MONTHS=[i for i in range(1, 13)]
YEARS=[i for i in range(BEGIN_YEAR, END_YEAR + 1)]

# Initialize the class
rd = Raindrop(YEARS, MONTHS)

# Download the data
rd.fetch_data()
```

To do some preprocessing of the data, for now we can only convert the value "trace" into 0.00:
```
rd.preprocessing()
```

In case the scraping process failed, and you want to restart the process (rename the original output csv first):
```
BEGIN_YEAR = 2000 # BEGINNING YEAR <-- changing the starting year to 2000
END_YEAR = 2021 # ENDING YEAR 

MONTHS=[i for i in range(1, 13)]
YEARS=[i for i in range(BEGIN_YEAR, END_YEAR + 1)]

rd = Raindrop(YEARS, MONTHS)
rd.fetch_data()

# To combine the two csv file
rd.append_csv('raw_rainfall_data_original.csv', 'raw_rainfall_data.csv', export=True) # You can choose to export the file, default is False.

# This will combine the two csv file and export it into combined_rainfall.csv.

```
