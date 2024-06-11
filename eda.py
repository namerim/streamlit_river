import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from edaplus import parking_usage_chart
from mlml import parking_create_chart, parking_usage_and_fee

from utils import load_data
from viz import showViz
from statistic import showStat
from map import display_parking_map

def home() :
    st.markdown("### 한강공원 주차장 알림 \n"
                "- 한강공원 주차장 이용현황 \n"
                "- 한강공원 주차장 이용 추세\n")
    st.markdown("### 한강공원 주차장 예측현황 \n"
                "- 한강공원 주차장 예측 그래프")
    st.markdown("### 한강공원 주차장 위치 \n"
                "- 한강공원 주차장 위치 지도 \n")
    st.markdown("### 한강공원 주차장 정보 \n"
                "- 한강공원 주차장 이용 시간 \n"
                "- 한강공원 주차장 이용 금액 \n")
    

def run_eda_home(total_df) :

    data = load_data('한강공원 주차장 월별 이용 현황.csv')

    st.markdown("### 한강공원 주차장 알림 \n"
                "한강공원 주차장 이용 현황, 예측 현황, 위치, 요금을 나타내는 페이지입니다.")
    
    selected = option_menu(None, ['주차장', '이용현황', '예측현황', '위치', '요금'],
                           icons=['car-front', 'car-front-fill', 'bar-chart', 'pin-map', 'coin'],
                           menu_icon='cast', default_index=0, orientation='horizontal',
                           styles={
                               'container' : {
                                               'padding' : '0!important',
                                               'background-color' : '#808080'},
                               'icon' : {
                                               'color' : 'orange',
                                               'font-size' : '25px'},
                               'nav-link' : {
                                               'font-size' : '15px',
                                               'text-align' : 'left',
                                               'margin' : '0px',
                                               '--hover-color' : '#eee'},
                               'nav-link-selected' : {
                                               'background-color' : 'green'}
                               })
    if selected == '주차장' :
        home()
    elif selected == '이용현황' :
        parking_usage_chart(total_df)
    elif selected == '예측현황' :
        parking_create_chart(total_df)
    elif selected == '위치' :
        total_df2 = load_data('C:\\task\\한강공원주차장정보.csv')
        display_parking_map(total_df2)
    elif selected == '요금' :
        total_df2 = load_data('C:\\task\\한강공원주차장정보.csv')
        parking_usage_and_fee(total_df2)
    else:
        st.warning('Wrong')