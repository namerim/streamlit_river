
import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data

def showStat(total_df):
    st.markdown("통계 데이터를 보여줍니다.")

def plot_data(data, parking_lot):
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='월', y='이용객수', data=data[data['주차장명'] == parking_lot])
    plt.title(f'{parking_lot} 주차장 월별 이용객수')
    plt.xlabel('월')
    plt.ylabel('이용객수')
    st.pyplot(plt)

def forecast_usage(data, parking_lot):
    data['월'] = pd.to_datetime(data['날짜'],format='mixed').dt.month
    model = ExponentialSmoothing(data['이용객수'], seasonal='add', seasonal_periods=12).fit()
    forecast = model.forecast(steps=12)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data['이용객수'], label='실제 이용객수')
    sns.lineplot(data=forecast, label='예측 이용객수')
    plt.title(f'{parking_lot} 주차장 월별 이용객수 예측')
    plt.xlabel('월')
    plt.ylabel('이용객수')
    st.pyplot(plt)
    st.dataframe(forecast.reset_index().rename(columns={0: '예측 이용객수'}))

def run_forecast_app(total_df3):
    st.markdown("## 한강공원 주차장 월별 이용객 예측")
    data = load_data('C:\\task\\한강지천길.csv')
    parking_lot = st.sidebar.selectbox('주차장명', data['주차장명'].unique())
    plot_data(data, parking_lot)
    forecast_usage(data, parking_lot)


