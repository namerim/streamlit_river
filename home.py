import pandas as pd
import streamlit as st
from millify import prettify
from utils import load_data
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns

def run_home():

    data = load_data('한강공원이용객.csv')
    data['월'] = pd.to_datetime(data['현황 일시']).dt.month.astype('string') + '월'
    data['년'] = pd.to_datetime(data['현황 일시']).dt.year

    st.markdown("## 한강공원 이용 방안 \n"
                "본 프로젝트는 한강공원을 보다 쾌적하고 편하게 하기 위해 생성한 이용 방안입니다.\n")
    st.markdown("한강공원에 이용객, 주차장 마지막으로 둘레길을 소개해드리겠습니다.")
    
    park_name = st.selectbox("한강공원", sorted(data['공원명'].unique()))
    district_name = st.selectbox("구명", sorted(data['공원 구명'].unique()))
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{park_name} 공원의 이용객 정보')
    st.markdown('공원명, 구명을 선택하면 해당 공원의 이용객 수를 확인할 수 있습니다.')

    acc_year = st.sidebar.selectbox("년도", [2018, 2019, 2020, 2021, 2022, 2023, 2024])
        
    month_dic = st.sidebar.selectbox("월", ['1월', '2월', '3월', '4월', '5월', '6월',
                 '7월', '8월', '9월', '10월', '11월', '12월'])


    filtered_data = data[(data['공원명'] == park_name) &
                         (data['공원 구명'] == district_name) &
                         (data['월'] == month_dic) &
                         (data['년'] == acc_year)]

    if filtered_data.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        st.dataframe(filtered_data)
        
    col1, col2, col3, col4 = st.columns(4)
    
    if not filtered_data.empty:
        morning_users = filtered_data['일반이용자(아침)'].sum()
        noon_users = filtered_data['일반이용자(낮)'].sum()
        evening_users = filtered_data['일반이용자(저녁)'].sum()
        bicycle_users = filtered_data['자전거'].sum()
       
        with col1:
            st.metric(label='아침 이용자 수', value=prettify(morning_users))
        with col2:
            st.metric(label='낮 이용자 수', value=prettify(noon_users))
        with col3:
            st.metric(label='저녁 이용자 수', value=prettify(evening_users))
        with col4:
            st.metric(label='자전거 이용자 수', value=prettify(bicycle_users))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{park_name} 공원의 2025년 이용자 수 예측')

    # 예측 모델 준비
    prophet_data = data[(data['공원명'] == park_name) & (data['공원 구명'] == district_name)]
    prophet_data = prophet_data.groupby('현황 일시').sum().reset_index()

    prophet_df = prophet_data[['현황 일시', '일반이용자(아침)']]
    prophet_df.columns = ['ds', 'y']

    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    forecast_2025 = forecast[(forecast['ds'].dt.year == 2025)]
    
    st.write(forecast_2025[['ds', 'yhat']])

    # 예측 결과 시각화
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=forecast_2025['ds'], y=forecast_2025['yhat'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('Predicted Users')
    plt.title(f'{park_name} 공원의 2025년 이용자 수 예측')
    plt.xticks(rotation=45)
    st.pyplot(plt)
