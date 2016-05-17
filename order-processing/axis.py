import pandas as pd
import matplotlib.pyplot as mp
import pandas.io.data
from pandas import DataFrame


df=pd.read_csv('price-rates.csv',index_col='DATE',parse_dates= True)



close_at=df["CLOSE"]

close_at.plot()
mp.show()
