import pandas as pd
import streamlit as st

from project import format_city_name

##### ------ sheets ------ #####
cities_df = pd.read_excel('data_tables/cities_data.xlsx', header=None)
cities_df.columns = ['State', 'Município', 'IBGE Code']

asps_index_df = pd.read_excel('data_tables/ASPS_index_data.xlsx')

mde_index_df = pd.read_excel('data_tables/MDE_index_data.xlsx')

water_sewer_solidwaste_df = pd.read_excel('data_tables/water_sewer_solidwaste_data.xlsx')

revenue_data = pd.read_excel('data_tables/revenue_data.xlsx')

net_consolidated_debt = pd.read_excel('data_tables/net_consolidated_debt.xlsx')

remains_to_be_paid = pd.read_excel('data_tables/remains_to_be_paid.xlsx')

personnel_expenses = pd.read_excel('data_tables/personnel_expenses.xlsx')

credit_operations = pd.read_excel('data_tables/credit_operations.xlsx')

imunization_polio = pd.read_excel('data_tables/imunization_polio.xlsx')

imunization_bcg = pd.read_excel('data_tables/imunization_bcg.xlsx')

health_data = pd.read_excel('data_tables/health_data.xlsx')

education_data = pd.read_excel('data_tables/education_data.xlsx')

mortality_data = pd.read_excel('data_tables/mortality_data.xlsx')

ideb_data = pd.read_excel('data_tables/ideb_data.xlsx')

ranking_ideb_data = pd.read_excel('data_tables/ranking_ideb.xlsx')

prefeitos_data = pd.read_excel('data_tables/prefeitos_rs.xlsx')


def get_city(cities_df):
    if "city" not in st.session_state:
        st.session_state.city = ""
    city = st.sidebar.text_input("Município", st.session_state.city).strip()
    city = format_city_name(city)

    if city:
        if city in cities_df['Município'].values:
            st.session_state.city = city
        else:
            st.sidebar.warning("A cidade deve ser do Rio Grande do Sul. Verifique a ortografia e tente novamente.")
            return None

    return st.session_state.city

def get_year(first_year, last_year):
    year = st.sidebar.selectbox("Ano", list(range(first_year, last_year)))
    return year

def create_tooltip(info_text):
    tooltip_html = f"""
    <style>
        .info-icon {{
            display: inline-block;
            width: 18px;
            height: 18px;
            background-color: #BBBBBB;
            color: #555;
            text-align: center;
            border-radius: 50%;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            vertical-align: baseline;
            margin-top: 8px;
        }}
        .tooltip {{
            position: relative;
            display: inline-block;
            margin-left: -10px;
        }}
        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 200px;
            background-color: #f9f9f9;
            color: #000;
            text-align: justify;
            font-size: 10px
            border-radius: 5px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
            box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
        }}
        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
    </style>
    <div class="tooltip">
        <span class="info-icon">i</span>
        <div class="tooltiptext">{info_text}</div>
    </div>
    """
    return tooltip_html


def page_title(name):
    st.markdown(
        f"""
        <div style="background-color: #DDDDDD; padding: 0px; border-radius: 5px; text-align: center;margin-bottom: 10px">
            <h1 style="font-size: 50px; margin: 0;"><strong>{name}</strong></h1>
        </div>
        """, unsafe_allow_html=True)
