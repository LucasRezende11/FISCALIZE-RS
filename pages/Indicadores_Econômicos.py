import streamlit as st
import sidrapy
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openpyxl


from utils import get_city, get_year, cities_df, water_sewer_solidwaste_df, page_title, prefeitos_data
from project import get_sidra_data, normalize, format_city_name

##### ------ IBGE variables ------ #####
variables1 = ["37", "513", "517", "6575", "525"]
variables2 = ["497"]
variables3 = ["2266"]
##### ------ Inflation index number data, treatment and deflation of GDP data ------ #####
def inflation_index(variables3, variables1, dfs_gdp, dfs_gdp_city):
    dfs_IPCA = {}
    dfs_IPCA = get_sidra_data("1737", variables3, "1", "1", 'all', 1, "dfs_IPCA", "IPCA_data")
    for key, df in dfs_IPCA.items():
        df_filtered = df[df.iloc[:, 0].astype(str).str.endswith("12")]
        dfs_IPCA[key] = df_filtered

    for key, df_ipca in dfs_IPCA.items():
        df_ipca.iloc[:, 0] = df_ipca.iloc[:, 0].str[:-2]
        df_ipca.iloc[:, 0] = df_ipca.iloc[:, 0].astype(str)

        for var in variables1:
            df_gdp = dfs_gdp[f"RS_gdp_data_{var}"]
            df_gdp_city = dfs_gdp_city[f"city_gdp_data_{var}"]

            df_gdp.iloc[:, 0] = df_gdp.iloc[:, 0].astype(str)
            df_gdp_city.iloc[:, 0] = df_gdp_city.iloc[:, 0].astype(str)

            ultimo_ano_gdp = df_gdp.iloc[:, 0].max()

            ipca_base_value = df_ipca[df_ipca.iloc[:, 0] == ultimo_ano_gdp].iloc[0, 1]

            df_gdp_merged = pd.merge(df_gdp, df_ipca, left_on=df_gdp.columns[0], right_on=df_ipca.columns[0], how='left')
            df_gdp_merged[df_gdp.columns[1]] = df_gdp_merged['Valor_x'] * (ipca_base_value / df_gdp_merged['Valor_y'])

            df_gdp_city_merged = pd.merge(df_gdp_city, df_ipca, left_on=df_gdp_city.columns[0], right_on=df_ipca.columns[0], how='left')
            df_gdp_city_merged[df_gdp_city.columns[1]] = df_gdp_city_merged['Valor_x'] * (ipca_base_value / df_gdp_city_merged['Valor_y'])

            dfs_gdp[f"RS_gdp_data_{var}"] = pd.DataFrame({
                df_gdp.columns[0]: df_gdp_merged[df_gdp.columns[0]],
                df_gdp.columns[1]: df_gdp_merged[df_gdp.columns[1]]})

            dfs_gdp_city[f"city_gdp_data_{var}"] = pd.DataFrame({
                df_gdp_city.columns[0]: df_gdp_city_merged[df_gdp_city.columns[0]],
                df_gdp_city.columns[1]: df_gdp_city_merged[df_gdp_city.columns[1]]})

    return dfs_gdp_city, dfs_gdp

dfs_gdp = get_sidra_data("5938", variables1, "3", "43", 'all', 1000, "dfs_gdp_RS", "RS_gdp_data")

@st.cache_data(show_spinner=False)
def load_gdp_data(city_code):
    dfs_gdp_city = get_sidra_data("5938", variables1, "6", city_code, 'all', 1000, "dfs_gdp_city", "city_gdp_data")
    dfs_gdp_city2 = get_sidra_data("5938", variables2, "6", city_code, 'all', 1, "dfs_gdp_city2", "city_gdp_data2")
    inflation_index(variables3, variables1, dfs_gdp, dfs_gdp_city)

    return dfs_gdp, dfs_gdp_city, dfs_gdp_city2

def calculate_vab_proportions(agro_df, industria_df, servicos_df, adm_publica_df, year):
    agro = agro_df.loc[agro_df['Ano'] == str(year), 'Valor'].values[0]
    industria = industria_df.loc[industria_df['Ano'] == str(year), 'Valor'].values[0]
    servicos = servicos_df.loc[servicos_df['Ano'] == str(year), 'Valor'].values[0]
    adm_publica = adm_publica_df.loc[adm_publica_df['Ano'] == str(year), 'Valor'].values[0]

    total_vab = agro + industria + servicos + adm_publica

    proportions = {
        "Agropecuária": agro / total_vab * 100,
        "Indústria": industria / total_vab * 100,
        "Serviços": servicos / total_vab * 100,
        "Administração Pública": adm_publica / total_vab * 100
    }
    return proportions

### --- aba inicial de indicadores econômicos --- ###
st.set_page_config(page_icon= "logo3.png",layout="wide")

def economic_indicators():
    st.markdown("""
    <style>
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

    page_title("Indicadores Econômicos")

    city = get_city(cities_df)
    year = get_year(2002, 2022)

    if city:
        population = water_sewer_solidwaste_df.loc[water_sewer_solidwaste_df['Município'] == city, 'População'].values[0]
        st.markdown(
            f"""
            <div style='text-align: center; font-size: 22px; margin-top:10px;margin-bottom: 10px;'>
                    População de {city}: <strong>{population}</strong>
                    <span style="font-size: 16px;">(Censo 2022)</span>
            </div>
            <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 10px;">
            """,unsafe_allow_html=True)
###################################################################################################################################
        st.markdown(
            f"""
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px; margin-bottom: 10px;">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Últimos prefeitos de {city}</strong></h2>
            </div>
            """,unsafe_allow_html=True)

        place = normalize(city).upper()
        prefeitos_data['Município'] = prefeitos_data['Município'].apply(normalize)
        df_cidade = prefeitos_data[prefeitos_data['Município'] == place]

        df_cidade = df_cidade.sort_values(by='Ano')

        fig = go.Figure()

        for i, row in df_cidade.iterrows():
            fig.add_trace(go.Bar(x=[row['Ano']], y=[0.6], name=row['Ano'], text=f"<b>{row['Partido']}</b>",textposition='inside', insidetextanchor='middle', textfont=dict(size=18, color='white'), hoverinfo="text", marker=dict(color='rgb(55, 83, 109)'),  customdata=[row['Candidato']],
            hovertemplate=f"Candidato: {row['Candidato']}"))

        city = city.title()

        city = format_city_name(city)
        fig.update_layout(barmode='stack', title=dict(text=f'Prefeitos de {city} ao Longo dos Anos', font=dict(size=20)), xaxis_title="Ano da Eleição", showlegend=False, xaxis=dict(tickmode='array', tickvals=df_cidade['Ano']),
        yaxis=dict(showticklabels=False,showgrid=False, range=[0, 1]), height=200, margin=dict(l=10, r=10, t=40, b=20), dragmode=False )

        st.plotly_chart(fig, config={'scrollZoom': False, 'displayModeBar': False}, use_container_width=True)
###################################################################################################################################
        loading_message = st.empty()

        loading_message.markdown('<p style="font-size:16px;"><bold>Carregando o restante dos dados ...<bold></p>', unsafe_allow_html=True)

        city = format_city_name(city)
        city_code = str(cities_df.loc[cities_df.iloc[:, 1] == city, cities_df.columns[2]].values[0])

        dfs_gdp, dfs_gdp_city, dfs_gdp_city2 = load_gdp_data(city_code)

        loading_message.empty()

        GDP_value = dfs_gdp_city['city_gdp_data_37'].loc[dfs_gdp_city['city_gdp_data_37']['Ano'] == str(year), 'Valor'].values[0]
        GDP_value = f"R$ {round((GDP_value / 1_000_000), 2):,.2f} milhões"
        ratio_state_gdp = dfs_gdp_city2['city_gdp_data2_497'].loc[dfs_gdp_city2['city_gdp_data2_497']['Ano'] == str(year), 'Valor'].values[0]

        st.markdown(
            f"""
            <div style='text-align: center; font-size: 22px; margin-top: 10px;'>
                PIB deflacionado de {city}: <strong>{GDP_value}</strong>
                <span style="font-size: 16px;">(em {year})</span>
            </div>
            <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 10px;">

            <div style='text-align: center; font-size: 22px; margin-top: 5px;'>
                O município representa <strong>{ratio_state_gdp}%</strong> do PIB do RS
                <span style="font-size: 16px;">(em {year})</span>
            </div>
            <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 10px;">
            """,
            unsafe_allow_html=True)
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px; margin-bottom: 10px;">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Evolução do PIB</strong></h2>
            </div>
            """,unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        max_gdp_value = dfs_gdp_city['city_gdp_data_37']['Valor'].max()*1.15
        max_ratio_value = dfs_gdp_city2['city_gdp_data2_497']['Valor'].max()*1.15

        fig_gdp = px.line(dfs_gdp_city['city_gdp_data_37'], x='Ano', y='Valor', title=f'Evolução do PIB deflacionado de {city}', markers=True, color_discrete_sequence=['#191e2c'])
        fig_gdp.update_layout(title=dict(text=f'Evolução do PIB deflacionado de {city}', font=dict(size=20)), yaxis_range=[0, max_gdp_value],xaxis_title= None, yaxis_title='PIB (R$)', dragmode=False, margin=dict(l=10, r=10, t=40, b=20))
        col1.plotly_chart(fig_gdp, config={'scrollZoom': False, 'displayModeBar': False})

        fig_ratio = px.line(dfs_gdp_city2['city_gdp_data2_497'], x='Ano', y='Valor', title=f'Proporção do PIB de {city} no PIB do RS',  markers=True, color_discrete_sequence=['#ec8900'])
        fig_ratio.update_layout(title=dict(text=f'Proporção do PIB de {city} no PIB do RS', font=dict(size=20)),yaxis_range=[0, max_ratio_value],xaxis_title= None,yaxis_title='Proporção (%)',dragmode=False, margin=dict(l=10, r=10, t=40, b=20))
        col2.plotly_chart(fig_ratio, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px;margin-bottom: 10px;">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Distribuição do Valor Adicionado Bruto (VAB)</strong></h2>
            </div>
            """, unsafe_allow_html=True)

        agro_df_city = dfs_gdp_city['city_gdp_data_513']
        industria_df_city = dfs_gdp_city['city_gdp_data_517']
        servicos_df_city = dfs_gdp_city['city_gdp_data_6575']
        adm_publica_df_city = dfs_gdp_city['city_gdp_data_525']

        agro_df_state = dfs_gdp['RS_gdp_data_513']
        industria_df_state = dfs_gdp['RS_gdp_data_517']
        servicos_df_state = dfs_gdp['RS_gdp_data_6575']
        adm_publica_df_state = dfs_gdp['RS_gdp_data_525']

        color_map = {"Agropecuária": "#ec8900", "Indústria": "#394555", "Serviços": "#191e2c", "Administração Pública": "#bcbcbc"}

        proportions_city = calculate_vab_proportions(agro_df_city, industria_df_city, servicos_df_city, adm_publica_df_city, year)
        proportions_state = calculate_vab_proportions(agro_df_state, industria_df_state, servicos_df_state, adm_publica_df_state, year)

        df_vab_city = pd.DataFrame(list(proportions_city.items()), columns=['Setor', 'Proporção'])
        df_vab_state = pd.DataFrame(list(proportions_state.items()), columns=['Setor', 'Proporção'])

        fig_vab_city = px.pie(df_vab_city, values='Proporção', names='Setor', title=f"Distribuição do VAB por Setor - {city} ({year})",color=df_vab_city['Setor'], color_discrete_map=color_map)
        fig_vab_city.update_layout(title=dict(text=f"Distribuição do VAB por Setor - {city} ({year})", font=dict(size=20)), margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.2,x=0.5, xanchor='center'))
        fig_vab_state = px.pie(df_vab_state, values='Proporção', names='Setor', title=f"Distribuição do VAB por Setor - RS ({year})",color=df_vab_state['Setor'], color_discrete_map=color_map)
        fig_vab_state.update_layout(title=dict(text=f"Distribuição do VAB por Setor - RS ({year})", font=dict(size=20)), margin=dict(l=10, r=10, t=40, b=10),legend=dict(orientation="h", y=-0.2,x=0.5, xanchor='center'))

        col3, col4 = st.columns(2)
        col3.plotly_chart(fig_vab_city, config={'scrollZoom': False, 'displayModeBar': False})
        col4.plotly_chart(fig_vab_state, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px; margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Evolução dos Setores ao Longo do Tempo</strong></h2>
            </div>
            """,
            unsafe_allow_html=True)

        def plot_sector_evolution(dfs_gdp_city):
            agro = dfs_gdp_city['city_gdp_data_513'][['Ano', 'Valor']]
            agro['Setor'] = 'Agropecuária'

            industria = dfs_gdp_city['city_gdp_data_517'][['Ano', 'Valor']]
            industria['Setor'] = 'Indústria'

            servicos = dfs_gdp_city['city_gdp_data_6575'][['Ano', 'Valor']]
            servicos['Setor'] = 'Serviços'

            adm_publica = dfs_gdp_city['city_gdp_data_525'][['Ano', 'Valor']]
            adm_publica['Setor'] = 'Administração Pública'

            df_sectors = pd.concat([agro, industria, servicos, adm_publica])

            sector_totals = df_sectors.groupby('Setor')['Valor'].sum().sort_values(ascending=False)
            ordered_sectors = sector_totals.index.tolist()

            df_sectors['Setor'] = pd.Categorical(df_sectors['Setor'], categories=ordered_sectors, ordered=True)

            df_sectors = df_sectors.sort_values(by=['Setor', 'Ano'])

            fig_evolution = px.bar(df_sectors,x='Ano',y='Valor',color='Setor',title=f"Evolução do VAB dos Setores {city}",labels={'Valor': 'Valor (R$)', 'Ano': 'Ano'},
            color_discrete_map=color_map)

            fig_evolution.update_layout(barmode='stack', xaxis_title= None, yaxis_title='Valor (R$)', dragmode=False, title=dict(text=f"Evolução do VAB dos Setores {city}", font=dict(size=20)),
            margin=dict(l=10, r=10, t=40, b=5), legend=dict(orientation="h", y=-0.2,x=0.5, xanchor='center'), legend_title_text='')

            return fig_evolution

        st.plotly_chart(plot_sector_evolution(dfs_gdp_city), config={'scrollZoom': False, 'displayModeBar': False})

economic_indicators()
