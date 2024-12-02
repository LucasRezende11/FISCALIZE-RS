import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


from utils import get_city, cities_df, asps_index_df, create_tooltip, imunization_bcg, imunization_polio, health_data, mortality_data, page_title
from project import format_city_name

### --- aba de indicadores de Saúde --- ###
st.set_page_config(page_icon= "logo3.png",layout="wide")

def health_indicators():
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

    page_title("Indicadores de Saúde")

    city = get_city(cities_df)

    if city:
        city = city.upper()
        if f'PM DE {city}' in asps_index_df['Município'].values:
            asps_value = asps_index_df[asps_index_df['Município'] == f'PM DE {city}'].iloc[:, -1].values[0]
            city_rank = asps_index_df[asps_index_df['Município'] == f'PM DE {city}'].index[0] + 1
            city = city.title()
            col1, col2 = st.columns([30, 1])

            with col1:
                city = format_city_name(city)
                st.markdown(
                    f"""
                    <div style='text-align: center; font-size: 22px; margin-top: 10px;margin-bottom: 10px'>
                        Índice ASPS de {city}: <strong>{asps_value:.2f}</strong>
                        <span style="font-size: 18px;">({int(city_rank)}º posição no ranking estadual em 2023)</span>
                    </div>
                    <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 20px;">
                    """, unsafe_allow_html=True)

            with col2:
                st.markdown(create_tooltip("O índice ASPS mínimo é de 15% - O índice mostra o percentual de impostos destinado para Ações e Serviços Públicos em Saúde"), unsafe_allow_html=True)

        else:
            st.warning(f"Dados do Índice ASPS para {city} não estão disponíveis.")
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px;margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Investimento em Saúde</strong></h2>
            </div>
            """,
            unsafe_allow_html=True)
        city = city.upper()
        health_data_city = health_data[health_data['Município'] == city].sort_values(by='Ano')
        max_health = health_data_city['Gasto total com saúde'].max()*1.15
        fig = px.line( health_data_city, x='Ano', y='Gasto total com saúde', title=f"Evolução do Gasto Total com Saúde",
                      labels={'Gasto Total Saúde': 'Gasto com Saúde (R$)', 'Ano': 'Ano'}, markers=True, color_discrete_sequence=['#191e2c'])

        city = format_city_name(city)
        fig.update_layout(title=dict(text=f"Evolução do Gasto Total com Saúde - {city}", font=dict(size=20)),
            yaxis=dict(range=[0, max_health], title='Gasto com Saúde (R$)', titlefont=dict(size=14)),
            xaxis_title=None,xaxis_title_font=dict(size=14),yaxis_title='Gasto com Saúde (R$)',
            dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px;margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Investimento destinado à Atenção Básica</strong></h2>
            </div>
            """,
            unsafe_allow_html=True)

        health_data_city['Participação Saúde Básica'] = (health_data_city['Gasto com saúde básica'] / health_data_city['Gasto total com saúde']) * 100
        max_participation = health_data_city['Participação Saúde Básica'].max() * 1.05

        fig = px.bar(health_data_city, x='Ano', y='Participação Saúde Básica', title=f"Participação do Gasto com Atenção Básica no Total de Saúde - {city}",
            labels={'Participação Saúde Básica': 'Participação (%)', 'Ano': 'Ano'}, color_discrete_sequence=['#394555'], text='Participação Saúde Básica')

        fig.update_layout(title=dict(text=f"Participação do Gasto com Atenção Básica no Total de Saúde", font=dict(size=20)),
            yaxis=dict(range=[0, max_participation], title='Participação (%)', titlefont=dict(size=14)), xaxis_title=None,
            xaxis_title_font=dict(size=14), dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=10, r=10, t=40, b=5))
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px;margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Evolução da Imunização</strong></h2>
            </div>
            """,unsafe_allow_html=True)

        place = format_city_name(city)

        municipio_polio = imunization_polio[imunization_polio['Município'] == place].iloc[:, 1:]
        estado_polio = imunization_polio[imunization_polio['Município'] == 'Rio Grande do Sul'].iloc[:, 1:]

        municipio_polio = municipio_polio.melt(var_name='Ano', value_name=f'Cobertura {place}')

        estado_polio = estado_polio.melt(var_name='Ano', value_name='Cobertura Rio Grande do Sul')

        polio_data = pd.merge(municipio_polio, estado_polio, on='Ano')

        max_polio = polio_data[[f'Cobertura {place}', 'Cobertura Rio Grande do Sul']].max().max() * 1.15

        fig_polio = px.line( polio_data, x='Ano', y=[f'Cobertura {place}', 'Cobertura Rio Grande do Sul'], hover_data={'variable': False},
            title=f"Comparação da Cobertura de Imunização contra Poliomielite - {place} vs Rio Grande do Sul",
            labels={'value': 'Cobertura (%)', 'Ano': 'Ano'}, markers=True, color_discrete_map={f'Cobertura {place}': '#ec8900', 'Cobertura Rio Grande do Sul': '#191e2c'})

        fig_polio.update_layout(title=dict(text="Comparação da Cobertura de Imunização contra Poliomielite", font=dict(size=20)),
            yaxis=dict(range=[0, max_polio], title='Cobertura (%)', titlefont=dict(size=14)), xaxis_title=None,
            xaxis_title_font=dict(size=14), dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig_polio, config={'scrollZoom': False, 'displayModeBar': False})

        municipio_bcg = imunization_bcg[imunization_bcg['Município'] == place].iloc[:, 1:]
        estado_bcg = imunization_bcg[imunization_bcg['Município'] == 'Rio Grande do Sul'].iloc[:, 1:]

        municipio_bcg = municipio_bcg.melt(var_name='Ano', value_name=f'Cobertura {place}')
        estado_bcg = estado_bcg.melt(var_name='Ano', value_name='Cobertura Rio Grande do Sul')

        bcg_data = pd.merge(municipio_bcg, estado_bcg, on='Ano')

        max_bcg = bcg_data[[f'Cobertura {place}', 'Cobertura Rio Grande do Sul']].max().max() * 1.15

        fig_bcg = px.line( bcg_data, x='Ano', y=[f'Cobertura {place}', 'Cobertura Rio Grande do Sul'], hover_data={'variable': False},
            title=f"Comparação da Cobertura de Imunização contra BCG - {place} vs Rio Grande do Sul", labels={'value': 'Cobertura (%)', 'Ano': 'Ano'}, markers=True, color_discrete_map={f'Cobertura {place}': '#ec8900', 'Cobertura Rio Grande do Sul': '#191e2c'} )

        fig_bcg.update_layout(title=dict(text="Comparação da Cobertura de Imunização BCG", font=dict(size=20)), yaxis=dict(range=[0, max_bcg], title='Cobertura (%)', titlefont=dict(size=14)),
            xaxis_title=None, xaxis_title_font=dict(size=14), dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig_bcg, config={'scrollZoom': False, 'displayModeBar': False})

###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px;margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Evolução da Mortalidade Infantil</strong></h2>
            </div>
            """, unsafe_allow_html=True)

        mortality_data['Taxa de Mortalidade Município'] = (mortality_data.iloc[:, 6].astype(str).replace('-', np.nan).str.replace(',', '.').astype(float))
        mortality_data['Taxa de Mortalidade Estado'] = (mortality_data.iloc[:, 7].astype(str).replace('-', np.nan).str.replace(',', '.').astype(float))

        city_data = mortality_data[mortality_data['Município'] == place]

        mortality_plot_data = pd.DataFrame({'Ano': city_data['Ano'],f'Taxa de Mortalidade {place}': city_data['Taxa de Mortalidade Município'],
            'Taxa de Mortalidade Estado': city_data['Taxa de Mortalidade Estado']})

        max_mortality = city_data[['Taxa de Mortalidade Município', 'Taxa de Mortalidade Estado']].max().max() * 1.15

        fig_mortality = px.line(mortality_plot_data, x='Ano', y=[f'Taxa de Mortalidade {place}', 'Taxa de Mortalidade Estado'], hover_data={'variable': False},
            title=f"Evolução da Taxa de Mortalidade - {place} vs Estado",labels={'value': 'Taxa de Mortalidade (%)', 'Ano': 'Ano'}, markers=True, color_discrete_map={f'Taxa de Mortalidade {place}': '#ec8900', 'Taxa de Mortalidade Estado': '#191e2c'})

        fig_mortality.update_layout( title=dict(text="Evolução da Taxa de Mortalidade Infantil", font=dict(size=20)),
            yaxis=dict(range=[0, max_mortality], title='Taxa de Mortalidade (%)', titlefont=dict(size=14)), xaxis_title=None, xaxis_title_font=dict(size=14),
            dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig_mortality, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        st.markdown(
            """
            <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px;margin-bottom: 10px">
                <h2 style="text-align: center; margin-top: 0; font-size: 30px; color: #333;"><strong>Evolução do Índice ASPS</strong></h2>
            </div>
            """, unsafe_allow_html=True)

        municipio_selecionado = (f'PM DE {city.upper()}')

        estado_df = asps_index_df[asps_index_df['Município'] == 'Rio Grande do Sul'].iloc[:, 1:].transpose().reset_index()
        estado_df.columns = ['Ano', 'Média do índice ASPS dos municípios do RS']

        municipio_df = asps_index_df[asps_index_df['Município'] == municipio_selecionado].iloc[:, 1:].transpose().reset_index()
        municipio_df.columns = ['Ano', f'Índice ASPS {city.title()}']

        asps_plot_data = pd.merge(municipio_df, estado_df, on='Ano')

        max_asps = asps_plot_data[['Média do índice ASPS dos municípios do RS', f'Índice ASPS {city.title()}']].max().max() * 1.15

        fig_asps = px.line(asps_plot_data, x='Ano', y=[f'Índice ASPS {city.title()}', 'Média do índice ASPS dos municípios do RS'],
                        hover_data={'variable': False}, title=f"Evolução do Índice ASPS - {municipio_selecionado} vs média dos municípios do RS",
                        labels={'value': 'Índice ASPS', 'Ano': 'Ano'}, markers=True, color_discrete_map={f'Índice ASPS {city.title()}': '#ec8900', 'Média do índice ASPS dos municípios do RS': '#191e2c'})

        fig_asps.add_hline(y=15, line=dict(color='red', dash='dash', width=2), annotation_text="Mínimo 15%", annotation_position="bottom right")

        fig_asps.update_layout(title=dict(text=f"Índice ASPS - {format_city_name(city)} vs média dos municípios do RS", font=dict(size=20)),
            yaxis=dict(range=[0, max_asps], title='Índice ASPS (%)', titlefont=dict(size=14)), xaxis_title=None,
            xaxis_title_font=dict(size=14), dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'),
            margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig_asps, config={'scrollZoom': False, 'displayModeBar': False})

        st.markdown("""
            <p style="font-size:14px;text-align: justify;">
            *O índice mínimo de 15(%) se refere apenas ao ASPS municipal, e a linha de média dos municípios não se refere aos valores repassados pelo estado, que possui valor mínimo menor.
            </p>
            """, unsafe_allow_html=True)

health_indicators()
