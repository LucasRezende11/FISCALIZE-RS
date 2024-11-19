import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


from utils import get_city, get_year, cities_df, revenue_data, page_title
from project import format_city_name

### --- aba de receitas municipais  --- ###
st.set_page_config(page_icon= "logo3.png",layout="wide")

def municipal_revenues():
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

    st.markdown("""
    <style>
        .metric-box {
            background-color: #DDDDDD; padding: 10px; border-radius: 5px;text-align: center; margin-bottom: 10px;
        }
        .metric-box-success {
            background-color: rgba(144, 238, 144, 0.5);
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        .metric-box-failure {
            background-color: rgba(255, 99, 71, 0.5);
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.image("logo.png", width=150)

    page_title("Indicadores de Receitas Municipais")

    city = get_city(cities_df)
    year = get_year(2016, 2024)

    if city:
        city = city.lower().strip().title()
        revenue_filtered = revenue_data[(revenue_data['Município'].str.strip().str.lower() == city.lower()) & (revenue_data['Ano'].astype(str) == str(year))]

        if not revenue_filtered.empty:
            receita_prevista = revenue_filtered['Receita Prevista'].values[0]
            total_revenue = revenue_filtered['Receita Arrecadada'].values[0]
            receita_impostos = revenue_filtered['Receita de impostos e taxas'].values[0]
            receita_transferencias = revenue_filtered['Receita de transferências'].values[0]

            participacao_receita_impostos = (receita_impostos / total_revenue) * 100
            participacao_receita_transferencias = (receita_transferencias / total_revenue) * 100

            if total_revenue >= receita_prevista:
                frustracao = "Não"
                diferenca = total_revenue - receita_prevista
            else:
                frustracao = "Sim"
                diferenca = receita_prevista - total_revenue

            receita_prevista_formatada = f"R$ {format(round((receita_prevista / 1_000_000), 2), ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')} milhões"
            receita_arrecadada_formatada = f"R$ {format(round((total_revenue / 1_000_000), 2), ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')} milhões"
            receita_impostos_formatada = f"R$ {format(round((receita_impostos / 1_000_000), 2), ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')} milhões"
            receita_transferencias_formatada = f"R$ {format(round((receita_transferencias / 1_000_000), 2), ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')} milhões"
            diferenca_formatada = f"R$ {format(round((diferenca / 1_000_000), 2), ',.2f').replace(',', 'X').replace('.', ',').replace('X', '.')} milhões"


            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f'<div class="metric-box"><h3 style="font-size: 24px;">Receita Arrecadada</h3><p style="font-size: 20px;">{receita_arrecadada_formatada} ({year})</p></div>', unsafe_allow_html=True)

            with col2:
                st.markdown(f'<div class="metric-box"><h3 style="font-size: 24px;">Receita Prevista</h3><p style="font-size: 20px;">{receita_prevista_formatada} ({year})</p></div>', unsafe_allow_html=True)

            with col3:
                if frustracao == "Sim":
                    st.markdown(f'<div class="metric-box-failure"><h3 style="font-size: 24px;">Frustração de Receitas</h3><p style="font-size: 20px;">{diferenca_formatada}</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="metric-box-success"><h3 style="font-size: 23px; text-align: center">Não frustração de Receitas</h3><p style="font-size: 20px;">{diferenca_formatada}</p></div>', unsafe_allow_html=True)
        else:
            st.warning("Dados não disponíveis para o município e ano selecionados.")
###################################################################################################################################
        revenue_city_all_years = revenue_data[revenue_data['Município'].str.strip().str.lower() == city.lower()].sort_values(by='Ano')

        fig = px.line(revenue_city_all_years, x='Ano', y=['Receita Prevista', 'Receita Arrecadada'], hover_data={'variable': False},
                        title=f"Evolução da Receita Prevista e Arrecadada - {city}", labels={'value': 'Receita (R$)', 'Ano': 'Ano'},markers=True, color_discrete_map={'Receita Prevista': '#ec8900',
        'Receita Arrecadada': '#191e2c'})

        max_revenue_value = revenue_city_all_years[['Receita Prevista', 'Receita Arrecadada']].max().max() * 1.15

        city = format_city_name(city)
        fig.update_layout(title=dict(text=f"Evolução da Receita Prevista e Arrecadada - {city}", font=dict(size=20)), yaxis=dict(range=[0, max_revenue_value], title='Receita (R$)', titlefont=dict(size=14)),
        xaxis_title= None, xaxis_title_font=dict(size=14), yaxis_title='Receita (R$)', dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2,x=0.5, xanchor='center'), margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        col4, col5 = st.columns(2)
        participacao_receita_impostos_formatada = f"{participacao_receita_impostos:.2f}%"
        participacao_receita_transferencias_formatada = f"{participacao_receita_transferencias:.2f}%"

        with col4:
            st.markdown("""
                <div style="background-color: #DDDDDD; padding: 10px; border-radius: 5px; text-align: center;margin-bottom: 10px">
                    <h3 style="margin: 0;">Receita de Impostos e Taxas</h3>
                    <p style="font-size: 24px; font-weight: bold;">{}</p>
                    <p style="font-size: 20px;">Participação na Receita Total: <strong>{}</strong></p>
                </div>
            """.format(receita_impostos_formatada, participacao_receita_impostos_formatada), unsafe_allow_html=True)

        with col5:
            st.markdown("""
                <div style="background-color: #DDDDDD; padding: 10px; border-radius: 5px; text-align: center;">
                    <h3 style="margin: 0;">Receita de Transferências</h3>
                    <p style="font-size: 24px; font-weight: bold;">{}</p>
                    <p style="font-size: 20px;">Participação na Receita Total: <strong>{}</strong> </p>
                </div>
            """.format(receita_transferencias_formatada, participacao_receita_transferencias_formatada), unsafe_allow_html=True)

        st.markdown("""
            <p style="font-size:14px;text-align: justify;">
            *Considere para as seguintes análises que as transferências representam, em certa medida, o grau de dependência do município para com outros entes federativos.
            </p>
            """, unsafe_allow_html=True)
###################################################################################################################################
        col6, col7 = st.columns(2)
        max_impostos = revenue_city_all_years['Receita de impostos e taxas'].max()*1.15
        max_transferencias = revenue_city_all_years['Receita de transferências'].max()*1.15

        with col6:
            fig2 = px.line(revenue_city_all_years, x='Ano', y='Receita de impostos e taxas',  title=f"Evolução da Receita de Impostos e Taxas - {city}",
                        labels={'Receita de impostos e taxas': 'Receita (R$)', 'Ano': 'Ano'},  markers=True, color_discrete_sequence=['#191e2c'])

            fig2.update_layout(title=dict(text=f"Evolução da Receita de Impostos e Taxas - {city}", font=dict(size=20)), yaxis=dict(range=[0, max_impostos], title='Receita (R$)', titlefont=dict(size=14)),
            xaxis_title= None, xaxis_title_font=dict(size=14),legend=dict(font=dict(size=12), title=None),dragmode=False, margin=dict(l=10, r=10, t=40, b=5))
            st.plotly_chart(fig2, config={'scrollZoom': False, 'displayModeBar': False})

        with col7:
            fig3 = px.line(revenue_city_all_years, x='Ano', y='Receita de transferências', title=f"Evolução da Receita de transferências - {city}",
                        labels={'Receita de transferências': 'Receita (R$)', 'Ano': 'Ano'}, markers=True, color_discrete_sequence=['#ec8900'])

            fig3.update_layout(title=dict(text=f"Evolução da Receita de Transferências - {city}", font=dict(size=20)),yaxis=dict(range=[0, max_transferencias], title='Receita (R$)', titlefont=dict(size=14)),
            xaxis_title= None, xaxis_title_font=dict(size=14),legend=dict(font=dict(size=12), title=None),dragmode=False, margin=dict(l=10, r=10, t=40, b=5))
            st.plotly_chart(fig3, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        transferencias_federais = revenue_city_all_years.groupby('Ano')['Transferências da União'].sum()
        transferencias_estaduais = revenue_city_all_years.groupby('Ano')['Transferências do estado'].sum()

        participacao_transferencias_federais = (transferencias_federais / total_revenue) * 100
        participacao_transferencias_estaduais = (transferencias_estaduais / total_revenue) * 100

        participacao_federal_formatada = f"{participacao_transferencias_federais.iloc[-1]:.2f}%"
        participacao_estadual_formatada = f"{participacao_transferencias_estaduais.iloc[-1]:.2f}%"

        col8, col9 = st.columns(2)

        with col8:
            st.markdown(f"""
                <div style="background-color: #DDDDDD; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px">
                    <h3 style="margin: 0;"font-size: 24px;">Participação das Transferências Federais na Receita Total</h3>
                    <p style="font-size: 20px;"><strong>{participacao_federal_formatada}</strong> <span style="font-size: 20px;">({year})</span></p>
                </div>
            """, unsafe_allow_html=True)

        with col9:
            st.markdown(f"""
                <div style="background-color: #DDDDDD; padding: 10px; border-radius: 5px; text-align: center;margin-bottom: 10px">
                    <h3 style="margin: 0;">Participação das Transferências Estaduais na Receita Total</h3>
                    <p style="font-size: 20px;"><strong>{participacao_estadual_formatada}</strong> <span style="font-size: 20px;">({year})</span></p>
                </div>
            """, unsafe_allow_html=True)
###################################################################################################################################
        max_y_value = max(transferencias_federais.max(), transferencias_estaduais.max())*1.15

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=transferencias_federais.index, y=transferencias_federais, name='Transferências da União e de suas Entidades', marker_color='#191e2c'))
        fig4.add_trace(go.Bar(x=transferencias_estaduais.index, y=transferencias_estaduais, name='Transferências dos Estados e do Distrito Federal e de suas Entidades', marker_color='#ec8900'))

        fig4.update_layout(barmode='stack',title=dict(text=f"Evolução das Transferências - {city}",font=dict(size=20)),xaxis_title= None,xaxis=dict(title_font=dict(size=14)),
        yaxis_title='Valor (R$)', yaxis=dict(range=[0, max_y_value], title_font=dict(size=14)),legend=dict(title=None, font=dict(size=12),orientation="h", y=-0.2,x=0.5, xanchor='center'), margin=dict(l=10, r=10, t=40, b=5))

        st.plotly_chart(fig4, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
        revenue_city_all_years['Percentual Impostos e Taxas'] = ((revenue_city_all_years['Receita de impostos e taxas'] / revenue_city_all_years['Receita Arrecadada']) * 100).round(2)
        revenue_city_all_years['Percentual Transferências União'] = ((revenue_city_all_years['Transferências da União'] / revenue_city_all_years['Receita Arrecadada']) * 100).round(2)
        revenue_city_all_years['Percentual Transferências Estado'] = ((revenue_city_all_years['Transferências do estado'] / revenue_city_all_years['Receita Arrecadada']) * 100).round(2)
        revenue_city_all_years['Percentual Outros'] = (100 - (revenue_city_all_years['Percentual Impostos e Taxas'] + revenue_city_all_years['Percentual Transferências União'] +
                                                            revenue_city_all_years['Percentual Transferências Estado'])).round(2)

        def plot_revenue_composition(revenue_city_all_years, city):
            revenue_totals = {'Impostos e Taxas': revenue_city_all_years['Percentual Impostos e Taxas'].sum(),
                'Transferências da União': revenue_city_all_years['Percentual Transferências União'].sum(),
                'Transferências Estaduais': revenue_city_all_years['Percentual Transferências Estado'].sum(),
                'Outros': revenue_city_all_years['Percentual Outros'].sum()}

            ordered_sectors = sorted(revenue_totals, key=revenue_totals.get, reverse=True)

            fig5 = go.Figure()

            for sector in ordered_sectors:
                if sector == 'Impostos e Taxas':
                    fig5.add_trace(go.Bar( x=revenue_city_all_years['Ano'],
                        y=revenue_city_all_years['Percentual Impostos e Taxas'],
                        name='Impostos e Taxas',
                        marker_color='#191e2c',
                        text=revenue_city_all_years['Percentual Impostos e Taxas'].astype(str) + '%',
                        textposition='inside',
                        hovertemplate='Impostos e Taxas: %{y}%<extra></extra>'))
                elif sector == 'Transferências da União':
                    fig5.add_trace(go.Bar(x=revenue_city_all_years['Ano'],
                        y=revenue_city_all_years['Percentual Transferências União'],
                        name='Transferências da União',
                        marker_color='#394555',
                        text=revenue_city_all_years['Percentual Transferências União'].astype(str) + '%',
                        textposition='inside',
                        hovertemplate='Transferências da União: %{y}%<extra></extra>'))
                elif sector == 'Transferências Estaduais':
                    fig5.add_trace(go.Bar(x=revenue_city_all_years['Ano'],
                        y=revenue_city_all_years['Percentual Transferências Estado'],
                        name='Transferências Estaduais',
                        marker_color='#647081',
                        text=revenue_city_all_years['Percentual Transferências Estado'].astype(str) + '%',
                        textposition='inside',
                        hovertemplate='Transferências Estaduais: %{y}%<extra></extra>'))
                elif sector == 'Outros':
                    fig5.add_trace(go.Bar(x=revenue_city_all_years['Ano'],
                        y=revenue_city_all_years['Percentual Outros'],
                        name='Outros',
                        marker_color='#ec8900',
                        text=revenue_city_all_years['Percentual Outros'].astype(str) + '%',
                        textposition='inside',
                        hovertemplate='Outros: %{y}%<extra></extra>'))

            fig5.update_layout(barmode='stack', title=dict(text=f"Composição Percentual da Receita Arrecadada - {city}", font=dict(size=20)),
                xaxis_title=None, yaxis_title='Percentual (%)', yaxis=dict(range=[0, 100], title_font=dict(size=14)),
                xaxis=dict(type='category', title_font=dict(size=14)), legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center', title=None, font=dict(size=12)),
                margin=dict(l=10, r=10, t=40, b=5))

            return fig5

        st.plotly_chart(plot_revenue_composition(revenue_city_all_years, city), config={'scrollZoom': False, 'displayModeBar': False})

        st.markdown("""
            <p style="font-size:14px;text-align: justify;">
            *Como existe falta de padronização no lançamento dos dados, há cidades que não possuem dados para transferências do estado e da União. Em alguns casos, quando haviam dados, foram usados os códigos 1710 e 1720, ou 1721 e 1722.
            </p>
            """, unsafe_allow_html=True)

municipal_revenues()


