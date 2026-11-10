import numpy as np
import pandas as pd

def pm25_sub_index(x):
    if pd.isna(x):
        return np.nan

    if x <= 30:
        return (50/30) * x
    elif x <= 60:
        return 50 + (x-30) * (50/30)
    elif x <= 90:
        return 100 + (x-60) * (100/30)
    elif x <= 120:
        return 200 + (x-90) * (100/30)
    elif x <= 250:
        return 300 + (x-120) * (100/130)
    elif x <= 500:
        return 400 + (x-250) * (100/250)
    else:
        return 500
    
def pm10_sub_index(x):
    if pd.isna(x):
        return np.nan

    if x <= 50:
        return (50/50) * x
    elif x <= 100:
        return 50 + (x-50) * (50/50)
    elif x <= 250:
        return 100 + (x-100) * (100/150)
    elif x <= 350:
        return 200 + (x-250) * (100/100)
    elif x <= 430:
        return 300 + (x-350) * (100/80)
    elif x <= 600:
        return 400 + (x-430) * (100/170)
    else:
        return 500  

def no2_sub_index(x):
    if pd.isna(x):
        return np.nan

    if x <= 40:
        return (50/40) * x
    elif x <= 80:
        return 50 + (x-40) * (50/40)
    elif x <= 180:
        return 100 + (x-80) * (100/100)
    elif x <= 280:
        return 200 + (x-180) * (100/100)
    elif x <= 400:
        return 300 + (x-280) * (100/120)
    elif x <= 1000:
        return 400 + (x-400) * (100/600)
    else:
        return 500 
    
def so2_sub_index(x):
    if pd.isna(x):
        return np.nan

    if x <= 40:
        return (50/40) * x
    elif x <= 80:
        return 50 + (x-40) * (50/40)
    elif x <= 380:
        return 100 + (x-80) * (100/300)
    elif x <= 800:
        return 200 + (x-380) * (100/420)
    elif x <= 1600:
        return 300 + (x-800) * (100/800)
    elif x <= 2000:
        return 400 + (x-1600) * (100/400)
    else:
        return 500
    
def o3_sub_index(x):
    if pd.isna(x):
        return np.nan

    if x <= 50:
        return (50/50) * x
    elif x <= 100:
        return 50 + (x-50) * (50/50)
    elif x <= 168:
        return 100 + (x-100) * (100/68)
    elif x <= 208:
        return 200 + (x-168) * (100/40)
    elif x <= 748:
        return 300 + (x-208) * (100/540)
    elif x <= 1000:
        return 400 + (x-748) * (100/252)
    else:
        return 500
    
def co_sub_index(x):
    if pd.isna(x):
        return np.nan

    if x <= 1:
        return (50/1) * x
    elif x <= 2:
        return 50 + (x-1) * (50/1)
    elif x <= 10:
        return 100 + (x-2) * (100/8)
    elif x <= 17:
        return 200 + (x-10) * (100/7)
    elif x <= 34:
        return 300 + (x-17) * (100/17)
    elif x <= 50:
        return 400 + (x-34) * (100/16)
    else:
        return 500