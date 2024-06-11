
# 지도 작성해서 만들기 위도 경도 껴서 만들어보기 못 만들면 리스트만 작성

import pandas as pd
import streamlit as st
import geopandas as gpd

import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.font_manager as fm

import streamlit as st
import pandas as pd
import plotly.express as px

def display_parking_map(total_df):
    st.markdown("## 주차장 위치 지도")
    
    # 위도와 경도를 사용하여 지도에 주차장의 위치를 표시
    fig = px.scatter_mapbox(total_df, lat='위치정보(위도)', lon='위치정보(경도)', hover_name='주차장별', hover_data=['주차장별', '위치정보(위도)', '위치정보(경도)'],
                            zoom=10, height=600, color_discrete_sequence=["red"], custom_data=['주차장별'])
    
    # 점의 크기 조절
    fig.update_traces(marker=dict(size=10))
    
    # 지도 스타일 설정
    fig.update_layout(mapbox_style="open-street-map")
    
    # 지도 출력
    selected_parking = st.sidebar.selectbox("주차장 선택", total_df['주차장별'].unique())
    filtered_data = total_df[total_df['주차장별'] == selected_parking]
    if not filtered_data.empty:
        center_lat = filtered_data['위치정보(위도)'].iloc[0]
        center_lon = filtered_data['위치정보(경도)'].iloc[0]
        fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon}, margin={"r":30,"t":30,"l":30,"b":30})

    
    st.plotly_chart(fig)

def main():
    # 데이터 로드
    total_df = pd.read_csv('C:\\task\\한강공원주차장정보.csv')  # 데이터 파일 경로를 적절히 지정해주세요.

    # 지도에 주차장 위치 표시
    display_parking_map(total_df)

if __name__ == "__main__":
    main()

    
    
    
    
    
    
    
    
    
