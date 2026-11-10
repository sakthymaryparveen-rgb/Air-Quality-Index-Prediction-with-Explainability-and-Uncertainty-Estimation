import streamlit as st
import pandas as pd
import os
from data.ppb_to_ugm3 import conversion
from data.aqi_computation import computation
from data.missing_verify import handle_missing

st.title('AQI Dataset Upload')

pollutant_file=st.file_uploader(
    'Upload Pollutant Dataset',
    type=['csv','xlsx'])

#save files
os.makedirs("uploads", exist_ok=True)

def save_file(file):

    path = os.path.join("uploads", file.name)

    with open(path,"wb") as f:
        f.write(file.getbuffer())

    return path

#load files
def get_file(pollutant_file):
    if pollutant_file is None:
        return None

    pollutant_path = save_file(pollutant_file)

    if pollutant_file.name.endswith(".csv"):
        pollutant_df = pd.read_csv(pollutant_path)
    else:
        pollutant_df = pd.read_excel(pollutant_path)

    return pollutant_df

pollutant_df=get_file(pollutant_file)
if pollutant_df is None:
    st.info('Upload dataset')
    st.stop()
#prepares data


poll_df=conversion(pollutant_df)
poll_before_aqi=handle_missing(poll_df)
poll_data=computation(poll_before_aqi)
poll_data['Date'] = pd.to_datetime(poll_data['Date'])
cols=['Date','Station','CO','NO2','SO2','O3','PM10','PM2.5',
      'AQI','Dominant_Pollutant','AQI_Category'
]
poll_data=poll_data[cols]

poll_data.to_pickle('D:/mywork/data/model_data.pkl')

st.subheader('Prepared Dataset')
st.dataframe(poll_data.head())
st.write('Total rows:',len(poll_data))
