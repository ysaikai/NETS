from __future__ import division

# Generate survival rates for Age1-5 for each county for each year
# Use bFIPS.csv, which contains DN, FirstYear, LastYear, bFIPS
# It's easier to remove all FirstYear = 1989 entries from bFIPS in advance.

def survival():
	# 1991 is the first point for Age1(FirstYear = 1990) to exist.
	for year in range(1991,2012): # 1991-2011
		for age in range(1,6): # 1-5
			birthyear = year - age
			# Ignore FirstYear = 1989, which means 'exist before 1990'
			if birthyear <= 1989:
				rate[age - 1] = None
			else:
# n.b. data in df in string. So, even for numerical comparison,
# convert the data type of 'year' and 'birthyear'
				df = df_county[df_county.FirstYear == str(birthyear)]
				total = df[DN].count()
####################################################################
# LastYear: the final year of activity i.e. died on 1/1 in (LastYear+1)
# This makes Age1 = 1 (useless) bc strictly FirstYear < LastYear. To modify,
# use df.LastYear > str(year) instead of df.LastYear >= str(year).
####################################################################
				df = df[df.LastYear >= str(year)]
				alive = df[DN].count()
				rate[age - 1] = round(alive / total, 3)
	
		x = [bfips, year] # temporarily store to use .extend
		x.extend(rate) # to concatenate rate without nesting
		op.append(x)

import pandas as pd
import csv
import re

path_bFIPS = '/home/saikai/subsets/bFIPS.csv'
path_survival = '/home/saikai/subsets/survival2.csv'

DN = 'DunsNumber'
cols = [DN,'FirstYear','LastYear','bFIPS']
op_cols = ['FIPS','Year','Age1','Age2','Age3','Age4','Age5']

op = []
table = []
rate = [None] * 5 # contains 5 survival rates

# FirstYear = 1989 has been removed from the original bFIPS
total = 42479792 # the total rows after the removal
cnt = 0
pcnt = 0
bfips = 1001 # 01001 is the smallest FIPS in the bFIPS

# bFIPS file is pre-sorted in ascending order of bFIPS column
with open(path_bFIPS) as f:
	next(f) # skip the header
	for line in f:
		cnt += 1
		pcnt += 1
		row = re.split(',', line)
		row[3] = row[3].rstrip()
		
		if int(row[3]) != int(bfips):
			df_county = pd.DataFrame(table, columns=cols)
			survival()
			
			bfips = int(row[3])
			table = []
		
		table.append(row)
		
		if pcnt == 500000:
			print str(cnt)+'/'+str(total)+' ('+str(int(100*cnt/total))+'%)'
			pcnt = 0
	
# Output
with open(path_survival, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(op_cols) # writerow
    writer.writerows(op) # writerows
