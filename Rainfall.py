import requests
import time
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


from bs4 import BeautifulSoup

from constant import month_dict

BEING_YEAR = 1974 # BEGINNING YEAR
END_YEAR = 2021 # ENDING YEAR 

MONTHS=[i for i in range(1, 13)]
YEARS=[i for i in range(BEING_YEAR, END_YEAR + 1)]


class Raindrop:
	def __init__(self,
				 years,
				 months):
		self.years = years
		self.months = months
		self.daily_rainfall = []
		self.df = None

	def initialize(self):
		"""
		Initialize

		Initialize Selenium Driver
		"""
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--incognito')
		options.add_argument('--headless')
		driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)


	def base_url(self, year, month):
		return f'https://www.hko.gov.hk/en/cis/dailyExtract.htm?y={year}&m={month}'

	def fetch_data(self):
		"""
		fetch_data

		Extract Rainfall data from HKO website using selenium. 
		"""
		for year in YEARS:
			for month in MONTHS:
				print(f'Currently processing {month_dict[month]}/{year}')
				driver.get(self.base_url(year, month))
				time.sleep(3)

				page_source = driver.page_source
				soup = BeautifulSoup(page_source, 'html.parser')

				for i, row in enumerate(soup.find_all(id='dataTable')[0].find('table').find_all('tr')):
					print(f'Attempting to extract {i} data')
					try:

						daily_data = {
							'year': year,
							'month': month,
							'day': int((row.find_all('td')[0]).text), 
							'rainfall': (row.find_all('td')[8]).text
						}
						self.daily_rainfall.append(daily_data)
					except:
						print('skipped')

		self.export_csv(pd.DataFrame(self.daily_rainfall), 'raw_rainfall_data.csv')


	def export_csv(self, df, filename):
		df.to_csv(filename)

	def append_csv(self, original, delta, export=False):
		"""
		Append CSV

		In case the extracter failed you need to rename the file and combine the csv again
		"""
		df_original = pd.read_csv(original)
		df_delta = pd.read_csv(delta)

		# Appending the delta into original df and ignoring the index
		self.df = pd.concat([df_original, df_delta], ignore_index=True)
		self.df = self.df.drop('Unnamed: 0', axis=1).sort_values('year').reset_index().drop('index', axis=1)
		if export:
			self.export_csv(self.df, 'combined_rainfall.csv')

	def convert_trace(self, row):
		if row == 'Trace':
			return 0.0
		else:
			return row

	def preprocessing(self):
		self.df['rainfall'] = self.df['rainfall'].apply(lambda row: self.convert_trace(row))

if __name__ == '__main__':
	rd = Raindrop(YEARS, MONTHS)
	rd.fetch_data()
	rd.export_csv()
