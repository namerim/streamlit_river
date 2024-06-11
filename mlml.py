import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def parking_create_chart(total_df):

    # 사용자 선택에 따라 데이터 필터링
    parking_lot = st.sidebar.selectbox("주차장명", sorted(total_df['주차장명'].unique()), key='parking_lot')
    filtered_data = total_df[total_df['주차장명'] == parking_lot]
    
    if filtered_data.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        st.markdown(f"## {parking_lot}의 월별 이용 예측")

        # 날짜를 datetime 형식으로 변환
        filtered_data['날짜'] = pd.to_datetime(filtered_data['날짜'], format='%Y/%m')
        
        # 선택한 년도 데이터만 필터링 (2024년도 데이터 사용)
        filtered_data = filtered_data[filtered_data['날짜'].dt.year <= 2024]
        
        # 월별 주차대수 합계 계산
        monthly_usage = filtered_data.groupby(filtered_data['날짜'].dt.strftime('%Y-%m'))[['주차대수']].sum().reset_index()
        
        # 예측 데이터 생성
        forecast_months = 12  # 2025년 12개월 예측
        model_park = ExponentialSmoothing(monthly_usage['주차대수'], trend='add', seasonal='add', seasonal_periods=12).fit()
        
        forecast_park = model_park.forecast(forecast_months)
        
        forecast_dates = pd.date_range(start='2025-01-01', periods=forecast_months, freq='M')
        forecast_df = pd.DataFrame({'날짜': forecast_dates, '주차대수': forecast_park})
        
        # y축을 가진 그래프 생성
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        # 예측된 주차대수 선 그래프 추가
        fig.add_trace(
            go.Scatter(x=forecast_df['날짜'], y=forecast_df['주차대수'], name='2025년도 예측 주차대수', mode='lines+markers', line=dict(dash='dash')),
            secondary_y=False,
        )
        
        # y축 레이블 설정
        fig.update_yaxes(title_text="주차대수 (대)", secondary_y=False)
        
        # 레이아웃 업데이트
        fig.update_layout(
            title=f'{parking_lot}의 2025년 월별 주차대수 예측',
            xaxis_title='날짜',
            width=800, height=600,
            template='plotly_white'
        )
        
        st.plotly_chart(fig)

    # 데이터 로드
parking_file_path = 'C:\\task\\한강공원 주차장 월별 이용 현황.csv'
parking_data = pd.read_csv(parking_file_path, encoding='cp949')

# 날짜를 datetime 형식으로 변환
parking_data['날짜'] = pd.to_datetime(parking_data['날짜'], format='%Y/%m')

# Streamlit 앱 실행
parking_create_chart(parking_data)

import streamlit as st
import pandas as pd

def parking_usage_and_fee(total_df):
    
    # 사용자가 선택한 주차장
    selected_parking = st.sidebar.selectbox("주차장 선택", total_df['주차장별'].unique())
    
    # 선택한 주차장의 데이터 필터링
    selected_data = total_df[total_df['주차장별'] == selected_parking]
    
    if selected_data.empty:
        st.warning("선택한 주차장의 데이터가 없습니다.")
    else:
        st.markdown(f"### {selected_parking}의 주중 및 주말 이용시간과 요금")
        
        # 선택한 주차장의 주중 및 주말 이용시간과 요금 데이터를 표로 표시
       # st.write(selected_data[['주차장별', '주중 이용시간 시작', '주중 이용시간 종료', '주말 이용시간 시작', '주말 이용시간 종료', '기본요금', '정기금금액']])

        # 추가한 부분: 주차장의 이용시간과 요금 데이터를 표로 표시
        st.table(selected_data[['주중 이용시간 시작', '주중 이용시간 종료', '주말 이용시간 시작', '주말 이용시간 종료', '기본요금', '정기금금액']].reset_index(drop=True))

# 데이터 로드
parking_file_path = 'C:\\task\\한강공원주차장정보.csv'
parking_data = pd.read_csv(parking_file_path, encoding='cp949')

# Streamlit 앱 실행
parking_usage_and_fee(parking_data)


