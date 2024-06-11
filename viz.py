
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from utils import load_data

def showViz(total_df) :
    total_df['날짜'] = pd.to_datetime(total_df['날짜'], format='mixed')

    sgg_nm = st.sidebar.selectbox('주차장명', sorted(total_df['주차장명'].unique()))
    
    plt.figure(figsize=(10, 6))
    data = load_data('한강공원 주차장 월별 이용 현황.csv')
    sns.lineplot(x='월', y='이용객수', data=data[data['주차장명'] == parking_lot])
    parking_lot = st.sidebar.selectbox('주차장명', data['주차장명'].unique())
    plt.title(f'{parking_lot} 주차장 월별 이용객수')
    plt.xlabel('월')
    plt.ylabel('이용객수')
    st.pyplot(plt)
