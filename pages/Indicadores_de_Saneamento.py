import streamlit as st
import pandas as pd


from utils import get_city, cities_df, water_sewer_solidwaste_df, page_title, create_tooltip

### --- aba de indicadores do SNIS --- ###
st.set_page_config(page_icon= "logo3.png",layout="wide")

def snis_indicators():
    st.markdown("""
    <style>
        /* Altera a cor de fundo da página principal */
        [data-testid="stAppViewContainer"] {
            background-color: #f0f0f0;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #BBBBBB;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.image("logo.png", width=150)

    page_title("Indicadores de Saneamento")

    city = get_city(cities_df)

    if city:
        city_data = water_sewer_solidwaste_df[water_sewer_solidwaste_df['Município'] == city]

        if not city_data.empty:
            ano_base = city_data['Ano Base'].values[0]

            def format_percentage(value):
                if pd.notnull(value) and isinstance(value, (int, float)):
                    return f"{value * 100:.2f}%"
                else:
                    return "Dados indisponíveis"

            def indicators(colx, coly, indicador, info, emoji):
                colx, coly = st.columns([30, 1])

                with colx:
                    st.markdown(
                        f"""
                        <div style='text-align: left; font-size: 30px; margin-top: 10px;margin-bottom: 10px'>
                            <strong>Atendimento de {indicador}</strong> {emoji}
                            </div>
                            <div style="font-size: 18px;text-align: center; margin-bottom: 5px;">
                            <span><strong>Atendimento em {city}:</strong> {format_percentage(city_data[f'Atendimento de {indicador} municipal'].values[0])}</span>
                            </div>
                            <div style="font-size: 18px; text-align: center; margin-bottom: 5px;">
                            <span><strong>Atendimento Estadual:</strong> {format_percentage(city_data[f'Atendimento de {indicador} estadual'].values[0])}</span>
                        </div>
                        <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 20px;">
                        """, unsafe_allow_html=True)

                with coly:
                    st.markdown(create_tooltip(info), unsafe_allow_html=True)

            indicators("col1", "col2", "água", "Razão entre População total atendida com abastecimento de água e População total do município", "🚰")

            indicators("col3", "col4", "esgoto", "Razão entre População total atendida com esgotamento sanitário e População total do município", "🚽")

            indicators("col1", "col2", "resíduos sólidos", "Razão entre População total atendida no município com coleta regular de pelo menos uma vez por semana e População total do município", "🗑️")

            st.markdown(f"<small>(Ano Base: {ano_base})</small>", unsafe_allow_html=True)

snis_indicators()
