
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from prophet import Prophet
import numpy as np
from utils import load_data


def home(total_df) :
    st.markdown("### 한강공원 지천길 안내 \n"
                 "- 지천길 코스에 대한 설명\n"
                 "- 관련 코스와 코스에 대한 상세 설명 \n")
    
from millify import prettify

import streamlit as st
import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path, encoding='cp949')

def road(total_df):
    data = load_data('C:\\task\\한강지천길정리.csv')

    st.markdown("한강공원의 이용객, 주차장 마지막으로 둘레길을 소개해드리겠습니다.")

    gang_name = st.selectbox("강남/강북 구분", sorted(data['강남강북구분'].unique()))
    course_name = st.selectbox("코스 이름", sorted(data['코스명'].unique()))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{course_name} 코스 정보')
    st.markdown('코스와 강남/강북 구분을 선택하면 지천길의 정보를 확인할 수 있습니다.')

    filtered_data = data[(data['코스명'] == course_name) & (data['강남강북구분'] == gang_name)]

    if filtered_data.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        st.dataframe(filtered_data)

    if not filtered_data.empty:
        distance = filtered_data['거리'].iloc[0]
        duration = filtered_data['소요시간'].iloc[0]
        level = filtered_data['코스레벨'].iloc[0]
        detailed_course = filtered_data['상세코스'].iloc[0]
        description = filtered_data['설명'].iloc[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div style='font-size:20px;'>거리: <span style='color:red;'><b>{distance}</b></span></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='font-size:20px;'>소요시간: <span style='color:red;'><b>{duration}<b></span></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='font-size:20px;'>코스레벨: <span style='color:red;'><b>{level}<b></span></div>", unsafe_allow_html=True)
        
        st.markdown('')
        st.markdown(f"**상세코스:** {detailed_course}")
        st.markdown(f"**설명:** {description}")

if __name__ == "__main__":

    road()

def run_ml_home(total_df) :
    st.markdown("### 한강공원 지천길 알림 \n"
                "한강공원 지천길에 대한 길 안내입니다.")
    
    selected = option_menu(None, ['한강 지천길', '지천길 정보'],
                           icons=['person-walking', 'map'],
                           menu_icon='cast', default_index=0, orientation='horizontal',
                           styles={
                               'container' : {
                                           'padding' : '0!important',
                                           'background-color' : '#808080'},
                               'icon' :      {
                                           'color' : 'orange',
                                           'font-size' : '25px'},
                               'nav-link' :  {
                                           'font-size' : '15px',
                                           'text-align' : 'left',
                                           'margin' : '0px',
                                           '--hover-color' : '#eee'},
                               'nav-link-selected' : {
                                           'background-color' : 'green'}
                               })
    if selected == '한강 지천길' :
        home(total_df)
    elif selected == '지천길 정보' :
        total_df3 = load_data('C:\\task\\한강지천길정리.csv')
        road(total_df3)
    else:
        st.warning('Wrong')