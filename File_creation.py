import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Reading in csv
water_qual = pd.read_csv('./Data/cmcWaterQualitySamples.csv',)
#filter out columns with more than 50% null values
water_qual2 = water_qual.loc[:, water_qual.isnull().mean() < .50]
#dropping null rows
water_qual_5000 = water_qual2.dropna()
#renaming columns
water_qual_5000.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
water_qual_5000.columns = water_qual_5000.columns.str.lower()
#Setting the index as a datetime
water_qual_5000.set_index('date', inplace=True)
water_qual_5000.index = pd.DatetimeIndex(water_qual_5000.index,freq='infer')
letort = water_qual_5000['groupname'] == 'LeTort Regional Authority'
#there is gaps in the data from 1992 to 1996 so we removed that
gap_less = water_qual_5000[letort].loc['1996-06-08':'2018-12-10']
