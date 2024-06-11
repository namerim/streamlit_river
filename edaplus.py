import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def parking_usage_chart(total_df):

    # 사용자 선택에 따라 데이터 필터링
    parking_lot = st.sidebar.selectbox("주차장명", sorted(total_df['주차장명'].unique()))
    filtered_data = total_df[total_df['주차장명'] == parking_lot]
    
    if filtered_data.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        st.markdown(f"## {parking_lot} 주차장의 월별 이용 현황")

        acc_year = st.sidebar.selectbox("년도", sorted(filtered_data['날짜'].str[:4].unique()))
        
        # 날짜를 datetime 형식으로 변환
        filtered_data['날짜'] = pd.to_datetime(filtered_data['날짜'], format='%Y/%m')
        
        # 선택한 년도 데이터만 필터링
        filtered_data = filtered_data[filtered_data['날짜'].dt.year == int(acc_year)]
        
        # 월별 주차대수 및 이용시간 합계 계산
        monthly_usage = filtered_data.groupby(filtered_data['날짜'].dt.strftime('%Y-%m'))[['주차대수', '이용시간']].sum().reset_index()
        
        # 두 개의 y축을 가진 그래프 생성
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # 주차대수 선 그래프 추가
        fig.add_trace(
            go.Scatter(x=monthly_usage['날짜'], y=monthly_usage['주차대수'], name='주차대수', mode='lines+markers'),
            secondary_y=False,
        )
        
        # 이용시간 선 그래프 추가
        fig.add_trace(
            go.Scatter(x=monthly_usage['날짜'], y=monthly_usage['이용시간'], name='이용시간', mode='lines+markers', marker=dict(color='orange')),
            secondary_y=True,
        )
        
        # y축 레이블 설정
        fig.update_yaxes(title_text="주차대수 (대)", secondary_y=False)
        fig.update_yaxes(title_text="이용시간 (분)", secondary_y=True)
        
        # 레이아웃 업데이트
        fig.update_layout(
            title=f'{parking_lot} 주차장의 {acc_year}년 월별 주차대수 및 이용시간',
            xaxis_title='날짜',
            width=800, height=600,
            template='plotly_white'
        )
        
        st.plotly_chart(fig)

# 데이터 로드
parking_file_path = 'C:\\task\\한강공원 주차장 월별 이용 현황.csv'
parking_data = pd.read_csv(parking_file_path, encoding='cp949')

# Streamlit 앱 실행
parking_usage_chart(parking_data)
