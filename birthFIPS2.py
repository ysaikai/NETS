# Add to FIPS data FirstYear, LastYear, bFIPS (FIPS at birth)

import pandas as pd
import time # use time.clock() to get the time at that point
start = time.clock()

path_fips = '/NETS/Data/NETS2012_US_FIPS.csv'
path_misc = '/NETS/Data/NETS2012_US_Misc.csv'
path_fips = '/NETS/Data/MillionSample/NETS2012_US_FIPS.csv'
path_misc = '/NETS/Data/MillionSample/NETS2012_US_Misc.csv'
path_bFIPS = '/home/saikai/subsets/bFIPS2.csv'
path_bFIPS = '/home/saikai/subsets/bFIPS_test.csv'

DN = 'DunsNumber'
FY = 'FirstYear'
LY = 'LastYear'

fips = pd.read_csv(path_fips)
misc = pd.read_csv(path_misc)

misc = misc[[DN,FY,LY]]
bFIPS = misc.merge(fips, on=DN)
# Ignore FirstYear = 1989, which means 'exist before 1990'
bFIPS = bFIPS[bFIPS[FY] >= 1990]

total = bFIPS[DN].count()
cnt = 0
pcnt = 0 # print counter

# Set FIPS** as a birthFIPS, where ** is FirstYear + 1
result = []
for index, row in bFIPS.iterrows():
	cnt += 1
	pcnt += 1

	y = str(int(row[FY]) + 1)[2:4]
	f = row['FIPS'+y]

	f = int(f) # Remove .0
# 	if f < 10000: f = '0' + str(f) # Add '0' if it's in 4 digits
	result.append(f)
	
	if pcnt == 500000:
		print str(int(100 * cnt / total)) + '%'
		pcnt = 0

# bFIPS = bFIPS[[DN,FY,LY]]
bFIPS['bFIPS'] = result
bFIPS = bFIPS.sort('bFIPS')

bFIPS = bFIPS.set_index(DN)
bFIPS.to_csv(path_bFIPS)

end = time.clock()
print 'It took ' + str(int(end - start)) + ' seconds.'
