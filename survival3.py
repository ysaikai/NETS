from __future__ import division

# Generate survival rates for Age1-5 for each county for each year
# Use bFIPS.csv, which contains: FIPS.csv + FirstYear, LastYear,
# bFIPS (FIPS at birth). Beforehand, removed all FirstYear = 1989 entries
# from bFIPS as they are not used.

def survival():
	# Born on 1/1 in FirstYear. Died on 1/1 in LastYear.
	# Summary made on 12/31 in each 'year'.
	# 1990 is the first point for Age1(FirstYear = 1990) to exist.
	for year in range(1990,2012):
		for age in range(1,6):
			birthyear = year - age + 1
			
			if birthyear <= 1989:
				rate[age - 1] = None
			else:
				# df_county contains only ones with the bfips being processed
				# n.b. data in df in string. So, even for numerical comparison,
				# convert the data type of 'year' and 'birthyear'
				df = df_county[df_county.FirstYear == str(birthyear)]
				
				########################################################
				# Remained located where the summary is taken
				########################################################
				# Two cases: 1. Moved 2. Died
				# If dead, df['FIPS'+yy] is empty but not NaN.
				# So, df['FIPS'+yy].isnull() doesn't work.

				# The denominator.
				# those staying in bfips or died during 5 years
				
				# bfips is already FIPS**, where ** = FirstYear + 1
				# So, skip checking the first year's FIPS
				for yyyy in range(birthyear+1,year+1):
					yy = str(yyyy + 1)[2:4]
					df = df[(df['FIPS'+yy]==str(bfips)) | (df['FIPS'+yy]=='')]

				total = df[DN].count()
				
				df = df[df.LastYear > str(year)]
				alive = df[DN].count()
				rate[age - 1] = round(alive / total, 3)
		
		x = [bfips, year] # temporarily store to use .extend
		x.extend(rate) # to concatenate rate without nesting
		op.append(x)

import pandas as pd
import csv
import re

path_bFIPS = '/home/saikai/subsets/bFIPS2.csv'
# path_survival = '/home/saikai/subsets/survival4.csv'
path_survival = '/home/saikai/subsets/survival5.csv'

DN = 'DunsNumber'
op_cols = ['FIPS','Year','Age1','Age2','Age3','Age4','Age5']

op = []
table = []
rate = [None] * 5 # contains 5 survival rates

total = 42479791 # the total rows after removing FirstYear=1989
cnt = 0
pcnt = 0
bfips = 1001 # the smallest FIPS in the bFIPS

# bFIPS file is pre-sorted in ascending order of bFIPS
with open(path_bFIPS) as f:
# 	next(f) # skip the header
	cols = re.split(',', f.readline())
	cols[27] = cols[27].rstrip()

	for line in f:
		cnt += 1
		pcnt += 1
		row = re.split(',', line)
		row[27] = row[27].rstrip()
		
		if int(row[27]) != int(bfips):
			df_county = pd.DataFrame(table, columns=cols)
			survival()
			
			bfips = int(row[27])
			table = []
		
		table.append(row)
		
		if pcnt == 500000:
			print "%d/%d (%d%%)" %(cnt, total, 100*cnt/total)
# 			print str(cnt)+'/'+str(total)+' ('+str(int(100*cnt/total))+'%)'
			pcnt = 0
		
# Output
with open(path_survival, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(op_cols) # writerow
    writer.writerows(op) # writerows
