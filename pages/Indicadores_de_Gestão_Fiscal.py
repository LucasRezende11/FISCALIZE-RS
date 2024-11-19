import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import get_city, cities_df, net_consolidated_debt, personnel_expenses, remains_to_be_paid, credit_operations, page_title, election_years
from project import format_city_name

years = list(range(2000, 2041))

### --- aba de indicadores de gestão fiscal --- ###
st.set_page_config(page_icon= "logo3.png",layout="wide")

def fiscal_management_indicators():
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

    page_title("Indicadores de Gestão Fiscal")

    city = get_city(cities_df)

    if city:
        city = format_city_name(city)

        rcl_data_city = net_consolidated_debt[net_consolidated_debt.iloc[:, 0].str.strip().str.lower() == city.lower()]

        if not rcl_data_city.empty:
            rcl_years = rcl_data_city.iloc[:, 1]
            rcl_values = rcl_data_city.iloc[:, 2]

            fig_rcl = px.line(x=rcl_years, y=rcl_values, title=f"Evolução da Receita Corrente Líquida - {city}",
                              labels={'x': 'Ano', 'y': 'RCL (R$)'}, markers=True, color_discrete_sequence=['#191e2c'])

            fig_rcl.update_layout(title=dict(text="Evolução da Receita Corrente Líquida", font=dict(size=20)), yaxis=dict(range=[0, None], title='RCL (R$)', titlefont=dict(size=14)),
            xaxis_title=None, dragmode=False, legend=dict(title=None, font=dict(size=12), orientation="h", y=-0.2, x=0.5, xanchor='center'), margin=dict(l=10, r=10, t=40, b=5))

            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            st.plotly_chart(fig_rcl, config={'scrollZoom': False, 'displayModeBar': False})
            st.markdown("""
            <p style="font-size:14px;text-align: justify;">
            <strong>Receita Corrente Líquida Municipal:</strong> Somatório das receitas tributárias, de contribuições patrimoniais, industriais, agropecuárias e de serviços e outras receitas correntes, com as transferências correntes, destas excluídas as transferências intragovernamentais.
            </p>
            """, unsafe_allow_html=True)
###################################################################################################################################
            fiscal_option = st.sidebar.selectbox("Escolha o indicador fiscal", ["Dívida Consolidada Líquida", "Operações de Crédito", "Restos a Pagar", "Despesas com Pessoal"])

            if fiscal_option == "Dívida Consolidada Líquida":
                debt_values = rcl_data_city.iloc[:, 4]

                max_rcl = debt_values.max() * 1.15

                fig_debt = px.line(x=rcl_years, y=debt_values,title=f"Evolução da Dívida Consolidada Líquida - {city}", labels={'x': 'Ano', 'y': 'Dívida Consolidada Líquida (R$)'}, markers=True, color_discrete_sequence=['#191e2c'])

                fig_debt.update_layout(title=dict(text=f"Evolução da Dívida Consolidada Líquida - {city}", font=dict(size=20)), yaxis=dict(range=[0, max_rcl], title='Dívida Consolidada Líquida (R$)', titlefont=dict(size=14)),
                xaxis_title=None, xaxis=dict(type='category', titlefont=dict(size=14)), dragmode=False, legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center', title=None, font=dict(size=12)),
                margin=dict(l=10, r=10, t=40, b=5))

                st.plotly_chart(fig_debt, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                debt_percent = (debt_values / rcl_values) * 100

                limit_alert = 108.00
                limit_legal = 120.00

                debt_status = ['Em conformidade' if val < limit_alert
                               else 'Em alerta' if val < limit_legal
                               else 'Fora de conformidade' for val in debt_percent]

                existing_categories = set(debt_status)

                fig_debt_percent = px.bar(x=rcl_years, y=debt_percent, title=f"Percentual da Dívida Consolidada Líquida em relação à RCL - {city}",
                          labels={'x': 'Ano', 'y': 'Percentual (%)'}, color=debt_status, color_discrete_map={
                              "Em conformidade": "green",
                              "Em alerta": "yellow",
                              "Fora de conformidade": "red"})

                fig_debt_percent.update_traces(hovertemplate='%{y:.2f}%<br>Ano: %{x}')

                for status, color in {"Em conformidade": "green", "Em alerta": "yellow", "Fora de conformidade": "red"}.items():
                    if status not in existing_categories:
                        fig_debt_percent.add_trace(go.Bar(x=[None], y=[None], marker_color=color, name=status, showlegend=True))

                max_debt = max(debt_percent)*1.3
                fig_debt_percent.update_layout(barmode='stack', title=dict(text=f"Percentual da Dívida Consolidada Líquida em relação à RCL - {city}", font=dict(size=20)),
                yaxis=dict(range=[0, max_debt], title='Percentual (%)', titlefont=dict(size=14)),
                legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center', title=None, font=dict(size=12)), margin=dict(l=10, r=10, t=40, b=10))

                st.plotly_chart(fig_debt_percent, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                st.markdown(
                    """
                    <table style="width:100%; border-collapse: collapse;">
                        <tr style="background-color: #BBBBBB;">
                            <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Limites</th>
                            <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Percentual da RCL</th>
                        </tr>
                        <tr>
                        <tr style="background-color: #FFFFFF;">
                            <td style="padding: 8px; border: 1px solid #ddd;">
                                a) Limite para Emissão de Alerta - LRF, inciso III do § 1º do art. 59
                            </td>
                            <td style="padding: 8px; border: 1px solid #ddd;text-align: center;">108,00%</td>
                        </tr>
                        <tr>
                        <tr style="background-color: #FFFFFF;">
                            <td style="padding: 8px; border: 1px solid #ddd;">
                                b) Limite Legal - Resolução do Senado Federal nº 40/2001, Inciso II do art. 3º
                            </td>
                            <td style="padding: 8px; border: 1px solid #ddd;text-align: center;">120,00%</td>
                        </tr>
                    </table>
                    """, unsafe_allow_html=True)
###################################################################################################################################
            if fiscal_option == "Despesas com Pessoal":
                personnel_expenses_city = personnel_expenses[personnel_expenses['Município'].str.strip().str.lower() == city.lower()]

                if not personnel_expenses_city.empty:
                    expenses_years = personnel_expenses_city['Ano']
                    personal_expenses_values = personnel_expenses_city.iloc[:, 4]

                    fig_personal_expenses = px.line(x=expenses_years, y=personal_expenses_values, title=f"Evolução das Despesas com Pessoal - {city}",
                        labels={'x': 'Ano', 'y': 'Despesas com Pessoal (R$)'}, markers=True, color_discrete_sequence=['#191e2c'])

                    max_personnel = max(personal_expenses_values)*1.15

                    fig_personal_expenses.update_layout(title=dict(text=f"Evolução das Despesas com Pessoal - {city}", font=dict(size=20)), yaxis=dict(range=[0, max_personnel], title='Despesas com Pessoal (R$)',
                        titlefont=dict(size=14)), xaxis_title=None, xaxis=dict(type='category', titlefont=dict(size=14)), dragmode=False, legend=dict(orientation="h", y=-0.2, x=0.5,
                        xanchor='center',title=None,font=dict(size=12)), margin=dict(l=10, r=10, t=40, b=5))

                    st.plotly_chart(fig_personal_expenses, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                    rcl_data_city = net_consolidated_debt[net_consolidated_debt.iloc[:, 0].str.strip().str.lower() == city.lower()]

                    if not rcl_data_city.empty:
                        rcl_years = rcl_data_city.iloc[:, 1]
                        rcl_values = rcl_data_city.iloc[:, 2]

                        common_years = expenses_years[expenses_years.isin(rcl_years)]
                        personal_expenses_values_common = personal_expenses_values[expenses_years.isin(common_years)]
                        rcl_values_common = rcl_values[rcl_years.isin(common_years)]

                        expenses_percent = (personal_expenses_values_common.values / rcl_values_common.values) * 100

                        limit_alert = 48.60
                        limit_prudencial = 51.30
                        limit_legal = 54.00

                        expenses_status = ['Em conformidade' if val < limit_alert
                                        else 'Em alerta' if val < limit_prudencial
                                        else 'Fora de conformidade - prudencial' if val < limit_legal
                                        else 'Fora de conformidade - legal' for val in expenses_percent]

                        fig_expenses_percent = px.bar( x=expenses_years, y=expenses_percent, title=f"Percentual das Despesas com Pessoal em relação à RCL - {city}",
                            labels={'x': 'Ano', 'y': 'Percentual (%)'}, color=expenses_status, color_discrete_map={
                                "Em conformidade": "green",
                                "Em alerta": "yellow",
                                "Fora de conformidade - prudencial": "#ec8900",
                                "Fora de conformidade - legal": "red"})

                        fig_expenses_percent.update_traces(hovertemplate='%{y:.2f}%<br>Ano: %{x}')

                        existing_categories = set(expenses_status)
                        for status, color in {"Em conformidade": "green", "Em alerta": "yellow", "Fora de conformidade - prudencial": "#ec8900",  "Fora de conformidade - legal": "red"}.items():
                            if status not in existing_categories:
                                fig_expenses_percent.add_trace(go.Bar(x=[None], y=[None], marker_color=color, name=status, showlegend=True))

                        max_expenses = max(expenses_percent)*1.3

                        fig_expenses_percent.update_layout( barmode='stack',title=dict(text=f"Percentual das Despesas com Pessoal em relação à RCL - {city}", font=dict(size=20)),
                                    yaxis=dict(range=[0, max_expenses], title='Percentual (%)', titlefont=dict(size=14)), xaxis_title=None,
                                    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center', title=None,
                                    font=dict(size=12)), margin=dict(l=10, r=10, t=40, b=10))

                        st.plotly_chart(fig_expenses_percent, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                        st.markdown(
                            """
                            <table style="width:100%; border-collapse: collapse;">
                                <tr style="background-color: #BBBBBB;">
                                    <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Limites</th>
                                    <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Percentual da RCL</th>
                                </tr>
                                <tr style="background-color: #FFFFFF;">
                                    <td style="padding: 8px; border: 1px solid #ddd;">
                                        a) Limite para Emissão de Alerta - LRF, Inciso II do § 1º do art. 59
                                    </td>
                                    <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">48,60%</td>
                                </tr>
                                <tr style="background-color: #FFFFFF;">
                                    <td style="padding: 8px; border: 1px solid #ddd;">
                                        b) Limite Prudencial - LRF, Parágrafo Único do art. 22
                                    </td>
                                    <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">51,30%</td>
                                </tr>
                                <tr style="background-color: #FFFFFF;">
                                    <td style="padding: 8px; border: 1px solid #ddd;">
                                        c) Limite Legal - LRF, alínea "b" do Inciso III do art. 20
                                    </td>
                                    <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">54,00%</td>
                                </tr>
                            </table>
                            """,
                            unsafe_allow_html=True
                        )
###################################################################################################################################
            if fiscal_option == "Operações de Crédito":
                credit_operations_city = credit_operations[credit_operations['Município'].str.strip().str.lower() == city.lower()]

                if not credit_operations_city.empty:
                    credit_years = credit_operations_city[0]
                    credit_values = credit_operations_city.iloc[:, 4]

                    rcl_data_city = net_consolidated_debt[net_consolidated_debt.iloc[:, 0].str.strip().str.lower() == city.lower()]

                    if not rcl_data_city.empty:
                        rcl_years = rcl_data_city.iloc[:, 1]
                        rcl_values = rcl_data_city.iloc[:, 2]

                        fig_credit_evolution = px.line(x=credit_years, y=credit_values, title=f"Evolução das Operações de Crédito - {city}",
                            labels={'x': 'Ano', 'y': 'Operações de Crédito (R$)'}, markers=True, color_discrete_sequence=['#191e2c'])

                        max_credit = max(credit_values)*1.15

                        fig_credit_evolution.update_layout(title=dict(text=f"Evolução das Operações de Crédito - {city}", font=dict(size=20)),
                        yaxis=dict(range=[0, max_credit], title='Operações de Crédito (R$)', titlefont=dict(size=14)), xaxis=dict(type='category', titlefont=dict(size=14)),
                        dragmode=False, legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center', title=None, font=dict(size=12)), margin=dict(l=10, r=10, t=40, b=5))

                        st.plotly_chart(fig_credit_evolution, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                        common_years = credit_years[credit_years.isin(rcl_years)]
                        credit_values_common = credit_values[credit_years.isin(common_years)]
                        rcl_values_common = rcl_values[rcl_years.isin(common_years)]

                        credit_percent = (credit_values_common.values / rcl_values_common.values) * 100

                        limit_alert_credit = 14.40
                        limit_legal_credit = 16.00

                        credit_status = ['Em conformidade' if val < limit_alert_credit
                                        else 'Em alerta' if val < limit_legal_credit
                                        else 'Fora de conformidade' for val in credit_percent]

                        fig_credit_percent = px.bar( x=common_years, y=credit_percent, title=f"Percentual das Operações de Crédito em relação à RCL - {city}",
                            labels={'x': 'Ano', 'y': 'Percentual (%)'}, color=credit_status,color_discrete_map={
                                "Em conformidade": "green",
                                "Em alerta": "yellow",
                                "Fora de conformidade": "red"})

                        fig_credit_percent.update_traces(hovertemplate='%{y:.2f}%<br>Ano: %{x}')

                        existing_categories = set(credit_status)
                        for status, color in {"Em conformidade": "green", "Em alerta": "yellow", "Fora de conformidade": "red"}.items():
                            if status not in existing_categories:
                                fig_credit_percent.add_trace(go.Bar(x=[None], y=[None], marker_color=color, name=status, showlegend=True))

                        max_credit = max(credit_percent)*1.3
                        fig_credit_percent.update_layout(title=dict(text=f"Percentual das Operações de Crédito em relação à RCL - {city}",font=dict(size=20)),
                        yaxis=dict(range=[0, max_credit], title='Percentual (%)',titlefont=dict(size=14)),legend=dict(orientation="h",
                        y=-0.2, x=0.5, xanchor='center', title=None, font=dict(size=12)), margin=dict(l=10, r=10, t=40, b=10))

                        st.plotly_chart(fig_credit_percent, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                        st.markdown(
                            """
                            <table style="width:100%; border-collapse: collapse;">
                                <tr style="background-color: #BBBBBB;">
                                    <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Descrição</th>
                                    <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Percentual da RCL</th>
                                </tr>
                                <tr style="background-color: #FFFFFF;">
                                    <td style="padding: 8px; border: 1px solid #ddd;">
                                        a) Operações de Crédito - Internas e Externas - Limite para Emissão de Alerta s/Limite Legal - LRF, Inciso III do § 1º do art. 59
                                    </td>
                                    <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">14,40%</td>
                                </tr>
                                <tr style="background-color: #FFFFFF;">
                                    <td style="padding: 8px; border: 1px solid #ddd;">
                                        b) Operações de Crédito - Internas e Externas - Limite Legal - Resolução do Senado Federal nº 43/2001, art. 7º
                                    </td>
                                    <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">16,00%</td>
                                </tr>
                            </table>
                            """,unsafe_allow_html=True)
                        st.markdown("""
                        <p style="font-size:12px;text-align: justify;">
                        *Nesta aba foram utilizadas as "OPERAÇÕES DE CRÉDITO - INTERNAS E EXTERNAS" como medida, sendo desconsideradas as "OPERAÇÕES DE CRÉDITO - ANTECIPAÇÃO DA RECEITA(ARO)"
                        </p>
                        """, unsafe_allow_html=True)
###################################################################################################################################
            if fiscal_option == "Restos a Pagar":
                remains_to_be_paid_city = remains_to_be_paid[remains_to_be_paid['Município'].str.strip().str.lower() == city.lower()]

                if not remains_to_be_paid_city.empty:
                    remains_years = remains_to_be_paid_city['Ano']
                    remains_values = remains_to_be_paid_city.iloc[:, 2]
                    insuficiency_values = remains_to_be_paid_city.iloc[:, 4]

                    df_election_years = pd.DataFrame({
                        'Year': remains_years.values,
                        'Election_year': [election_years(year) for year in remains_years]
                    })

                    non_election_years = df_election_years[df_election_years['Election_year'] == False]['Year'].values

                    colors = ['Ano Eleitoral' if remains_years.iloc[i] in non_election_years else 'Ano não-eleitoral' for i in range(len(remains_years))]

                    fig_remains_evolution = px.bar(x=remains_years, y=remains_values, title=f"Evolução de Restos a Pagar - {city}",
                        labels={'x': '', 'y': 'Valor de Restos a Pagar (R$)'}, color=colors, color_discrete_map={'Ano Eleitoral': 'black', 'Ano não-eleitoral': 'gray'})

                    fig_remains_evolution.update_traces(hovertemplate='%{y:.2f}%<br>Ano: %{x}')

                    fig_remains_evolution.update_layout(title=dict(text=f"Evolução de Restos a Pagar - {city}", font=dict(size=20)),
                    yaxis=dict(range=[0, None], title='Valor de Restos a Pagar (R$)', titlefont=dict(size=14)),
                    dragmode=False, legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center', title=None, font=dict(size=12)), margin=dict(l=10, r=10, t=40, b=5))

                    st.plotly_chart(fig_remains_evolution, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                    fig_remains_bar = px.bar(x=remains_years, y=insuficiency_values, title=f"Insuficiência Financeira - {city}",
                        labels={'x': '', 'y': 'Valor de Insuficiência Financeira (R$)'}, color=colors,
                        color_discrete_map={'Ano Eleitoral': 'black', 'Ano não-eleitoral': 'gray'})

                    fig_remains_bar.update_traces(hovertemplate='%{y:.2f}%<br>Ano: %{x}')

                    fig_remains_bar.update_layout(title=dict(text=f"Insuficiência Financeira - {city}", font=dict(size=20)),xaxis_title=None, yaxis_title='Valor de Insuficiência Financeira (R$)',
                    yaxis=dict(range=[0, None], titlefont=dict(size=14)), dragmode=False,legend=dict(orientation="h", y=-0.2,x=0.5, xanchor='center', title= None, font=dict(size=12)), margin=dict(l=10, r=10, t=40, b=5))

                    st.plotly_chart(fig_remains_bar, config={'scrollZoom': False, 'displayModeBar': False})
###################################################################################################################################
                    st.markdown(
                        """
                        <table style="width:100%; border-collapse: collapse;">
                            <tr style="background-color: #BBBBBB;">
                                <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Regra</th>
                                <th style="text-align: center; padding: 8px; border: 1px solid #ddd;">Descrição</th>
                            </tr>
                            <tr style="background-color: #FFFFFF;">
                                <td style="padding: 8px; border: 1px solid #ddd; text-align: left;">
                                    Equilíbrio Financeiro
                                </td>
                                <td style="padding: 8px; border: 1px solid #ddd;">
                                    § 1º do art. 1º da LRF: Garante o equilíbrio das contas públicas, prevenindo déficits excessivos e promovendo responsabilidade fiscal.
                                </td>
                            </tr>
                            <tr style="background-color: #FFFFFF;">
                                <td style="padding: 8px; border: 1px solid #ddd; text-align: left;">
                                    Restos a Pagar
                                </td>
                                <td style="padding: 8px; border: 1px solid #ddd;">
                                    Art. 42 da LRF: Define restrições ao empenho de despesas que não possam ser pagas no mesmo exercício financeiro, especialmente no último ano de mandato.
                                </td>
                            </tr>
                        </table>
                        """, unsafe_allow_html=True)
                    st.markdown("""
                        <p style="font-size:14px;text-align: justify;">
                        *As prefeituras não podem assinalar depesas como "Restos a pagar" nos dois últimos quadrimestres do último ano de mandato. Assim,
                        a existência de gastos com essa marcação nos anos eleitorais nos gráficos acima é um indicativo de possibilidade de haver inconformidade, necessitanto maior investigação.
                        </p>
                        """, unsafe_allow_html=True)

fiscal_management_indicators()
