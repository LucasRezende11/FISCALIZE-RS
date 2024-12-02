import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


from utils import get_city, cities_df, mde_index_df, create_tooltip, education_data, ideb_data, ranking_ideb_data, page_title
from project import format_city_name

### --- aba de indicadores de educação --- ###
st.set_page_config(page_icon= "logo3.png",layout="wide")

def education_indicators():
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

    page_title("Indicadores de Educação")

    city = get_city(cities_df)

    if city:

        city = city.upper()

        if f'PM DE {city}' in mde_index_df['Município'].values:
            mde_value = mde_index_df[mde_index_df['Município'] == f'PM DE {city}'].iloc[:, -1].values[0]
            city_rank = mde_index_df[mde_index_df['Município'] == f'PM DE {city}'].index[0] + 1
            col1, col2 = st.columns([30, 1])

            with col1:
                city = format_city_name(city)
                st.markdown(f"""
                    <div style='text-align: center; font-size: 22px; margin-top: 10px; margin-bottom: 10px'>
                        Índice MDE de {city}: <strong>{mde_value:.2f}</strong>
                        <span style="font-size: 18px;">({int(city_rank)}º posição no ranking estadual em 2022)</span>
                    </div>
                    <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 10px;">
                    """, unsafe_allow_html=True)
            with col2:
                st.markdown(create_tooltip("O índice MDE mínimo é de <bold>25%</bold> - O índice mostra o percentual de impostos destinado para Manutenção e Desenvolvimento do Ensino"),
                    unsafe_allow_html=True)

            place = format_city_name(city)

            city_ideb_rank_initial = ranking_ideb_data[ranking_ideb_data['Município'] == place].iloc[0, 1]
            city_ideb_rank_final = ranking_ideb_data[ranking_ideb_data['Município'] == place].iloc[0, 2]

            col3, col4 = st.columns([30, 1])

            with col3:
                st.markdown(
                        f"""
                        <div style='text-align: center; font-size: 22px; margin-top: 0px; margin-bottom: 10px'>
                            Posição de {city} no Ranking de IDEB estadual (2021):
                            <br>Anos Iniciais: <strong>{city_ideb_rank_initial}</strong> | Anos Finais: <strong>{city_ideb_rank_final}</strong>
                        </div>
                        <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 10px;">
                        """, unsafe_allow_html=True)

            with col4:
                st.markdown(create_tooltip("O Índice IDEB reflete a qualidade da educação básica a partir de avaliações e taxas de aprovação."),unsafe_allow_html=True)

        else:
            st.warning(f"Dados do Índice MDE para {city} não estão disponíveis.")

###################################################################################################################################
        st.markdown(
            f"""
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px; margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Investimento em Educação</strong></h2>
            </div>
            """,unsafe_allow_html=True)

        city = city.upper()
        education_data_city = education_data[education_data['Município'] == city].sort_values(by='Ano')
        max_gasto = education_data_city['Gasto total com educação'].max() * 1.15

        fig = px.line(education_data_city, x='Ano', y='Gasto total com educação', title=f"Evolução do Gasto Total com Educação",
                          labels={'Gasto total com educação': f'Gasto com educação (R$)', 'Ano': 'Ano'},markers=True, color_discrete_sequence=['#191e2c'])
        
        city = format_city_name(city)
        fig.update_layout(title=dict(text=f"Evolução do Gasto Total com Educação - {city}", font=dict(size=20)),
                yaxis=dict(range=[0, max_gasto], title=f'Gasto com educação (R$)', titlefont=dict(size=14)),xaxis_title=None,
                dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'), margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px; margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Investimento destinado à Educação Fundamental</strong></h2>
            </div>
            """,unsafe_allow_html=True)

        education_data_city = education_data[education_data['Município'] == city.upper()].sort_values(by='Ano')
        education_data_city['Participação Educação fundamental'] = (education_data_city['Gasto com educação fundamental'] / education_data_city['Gasto total com educação']) * 100
        max_participation = education_data_city['Participação Educação fundamental'].max() * 1.05

        fig = px.bar(education_data_city,x='Ano',y='Participação Educação fundamental',title=f"Participação do Gasto com Educação Fundamental no Total de Educação - {city}",
            labels={'Participação Educação fundamental': 'Participação (%)', 'Ano': 'Ano'}, color_discrete_sequence=['#394555'], text='Participação Educação fundamental')

        fig.update_layout(title=dict(text="Participação do Gasto com Educação Fundamental no Total de Educação", font=dict(size=20)),
            yaxis=dict(range=[0, max_participation], title='Participação (%)', titlefont=dict(size=14)),xaxis_title=None,
            dragmode=False,legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=10, r=10, t=40, b=5))
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px; margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Evolução do IDEB</strong></h2>
            </div>
            """,unsafe_allow_html=True)

        place = format_city_name(city)

        municipio_iniciais = ideb_data[ideb_data['Município'] == place][['Ano', 'Anos Iniciais Municipal']]
        estado_iniciais = ideb_data[ideb_data['Município'] == place][['Ano', 'Anos Iniciais Estadual']]

        municipio_iniciais = municipio_iniciais.rename(columns={'Anos Iniciais Municipal': f'IDEB - Anos Iniciais - {place}'})
        estado_iniciais = estado_iniciais.rename(columns={'Anos Iniciais Estadual': 'IDEB - Anos Iniciais - Rio Grande do Sul'})

        iniciais_data = pd.merge(municipio_iniciais, estado_iniciais, on='Ano', how='inner')

        max_ideb = iniciais_data[[f'IDEB - Anos Iniciais - {place}', 'IDEB - Anos Iniciais - Rio Grande do Sul']].max().max() * 1.15

        fig_iniciais = px.line(iniciais_data.melt(id_vars='Ano', var_name='Local', value_name='IDEB'), x='Ano', y='IDEB', color='Local',
            title=f"Comparação do IDEB - Anos Iniciais: {place} vs Rio Grande do Sul", labels={'IDEB': 'IDEB', 'Ano': 'Ano'}, markers=True, hover_data={'Local': False}, color_discrete_map={f'IDEB - Anos Iniciais - {place}' : '#ec8900', 'IDEB - Anos Iniciais - Rio Grande do Sul': '#191e2c'})

        fig_iniciais.update_layout(title=dict(text="Comparação do IDEB - Anos Iniciais", font=dict(size=20)),yaxis=dict(range=[0, max_ideb], title='IDEB', titlefont=dict(size=14)),
            xaxis_title=None, dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'), margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig_iniciais, config={'scrollZoom': False, 'displayModeBar': False})

        municipio_finais = ideb_data[ideb_data['Município'] == place][['Ano', 'Anos Finais Municipal']]
        estado_finais = ideb_data[ideb_data['Município'] == place][['Ano', 'Anos Finais Estadual']]

        municipio_finais = municipio_finais.rename(columns={'Anos Finais Municipal': f'IDEB - Anos Finais - {place}'})
        estado_finais = estado_finais.rename(columns={'Anos Finais Estadual': 'IDEB - Anos Finais - Rio Grande do Sul'})

        finais_data = pd.merge(municipio_finais, estado_finais, on='Ano', how='inner')

        max_ideb2 = finais_data[[f'IDEB - Anos Finais - {place}', 'IDEB - Anos Finais - Rio Grande do Sul']].max().max() * 1.15

        fig_finais = px.line(finais_data.melt(id_vars='Ano', var_name='Local', value_name='IDEB'), x='Ano', y='IDEB', color='Local', markers=True, hover_data={'Local': False},
            title=f"Comparação do IDEB - Anos Finais: {place} vs Rio Grande do Sul", labels={'IDEB': 'IDEB', 'Ano': 'Ano'}, color_discrete_map={f'IDEB - Anos Finais - {place}' : '#ec8900', 'IDEB - Anos Finais - Rio Grande do Sul': '#191e2c'})

        fig_finais.update_layout(title=dict(text="Comparação do IDEB - Anos Finais", font=dict(size=20)),
            yaxis=dict(range=[0, max_ideb2],title='IDEB', titlefont=dict(size=14)), xaxis_title=None,dragmode=False,
            legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'), margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig_finais, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px;margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Evolução do Índice MDE</strong></h2>
            </div>
            """, unsafe_allow_html=True)

        municipio_selecionado = f'PM DE {city.upper()}'

        estado_df = mde_index_df[mde_index_df['Município'] == 'Rio Grande do Sul'].iloc[:, 1:].transpose().reset_index()
        estado_df.columns = ['Ano', 'Média do índice MDE dos municípios do RS']

        municipio_df = mde_index_df[mde_index_df['Município'] == municipio_selecionado].iloc[:, 1:].transpose().reset_index()
        municipio_df.columns = ['Ano', f'Índice MDE {city.title()}']

        mde_plot_data = pd.merge(municipio_df, estado_df, on='Ano')

        max_mde = mde_plot_data[['Média do índice MDE dos municípios do RS', f'Índice MDE {city.title()}']].max().max() * 1.15

        fig_mde = px.line(mde_plot_data, x='Ano', y=[f'Índice MDE {city.title()}', 'Média do índice MDE dos municípios do RS'],
                        hover_data={'variable': False}, title=f"Evolução do Índice MDE - {municipio_selecionado} vs média dos municípios do RS",
                        labels={'value': 'Índice MDE', 'Ano': 'Ano'}, markers=True, color_discrete_map={f'Índice MDE {city.title()}' : '#ec8900', 'Média do índice MDE dos municípios do RS': '#191e2c'})

        fig_mde.add_hline(y=25, line=dict(color='red', dash='dash', width=2), annotation_text="Mínimo 25%", annotation_position="bottom right")

        fig_mde.update_layout(title=dict(text=f"Índice MDE - {format_city_name(city)} vs média dos municípios do RS", font=dict(size=20)), yaxis=dict(range=[0, max_mde], title='Índice MDE (%)', titlefont=dict(size=14)),
            xaxis_title=None, xaxis_title_font=dict(size=14), dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig_mde, config={'scrollZoom': False, 'displayModeBar': False})

        st.markdown("""
            <p style="font-size:14px;text-align: justify;">
            *O índice mínimo de 25(%) se refere apenas ao MDE municipal, e a linha de média dos municípios não se refere aos valores repassados pelo estado, que possui valor mínimo menor.
            </p>
            """, unsafe_allow_html=True)

education_indicators()
