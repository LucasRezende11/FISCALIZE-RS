import streamlit as st

from utils import page_title

### --- aba de referências --- ###
st.set_page_config(page_icon= "logo3.png", layout="wide")

def references():
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
    st.markdown(
            """
            <div style='text-align: center; font-size: 22px; margin-top:10px;margin-bottom: 10px;'>
                    <strong>Autor:</strong> Lucas Alexandre Rezende - Graduando em Ciências Econômicas pela UFRGS
            </div>
            <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 10px;">
            """,unsafe_allow_html=True)


    st.markdown(
        """
        <p style="font-size:40px;text-align: left;">
        <strong><bold>Indicadores de Receita Municipal</bold></strong>
        </p>

        <p style="font-size:17px;text-align: justify;">
        <strong>-Portal do TCE-RS (dados de receita):</strong> https://portal.tce.rs.gov.br/aplicprod/f?p=20001:23:::NO:::<br>
        <strong>-Por que e como inflacionar/deflacionar valores? (o que é e para que serve deflacionar os dados):</strong> https://terracoeconomico.com.br/por-que-e-como-inflacionar-deflacionar-valores/
        </p>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style="font-size:40px;text-align: left;">
        <strong><bold>Indicadores Econômicos</bold></strong>
        </p>

        <p style="font-size:17px;text-align: justify;">
        <strong>-Censo Demográfico do IBGE de 2022 (população):</strong> https://censo2022.ibge.gov.br/<br>
        <strong>-Tabela 1737 do SIDRA-IBGE (dados do IPCA):</strong> https://sidra.ibge.gov.br/tabela/1737<br>
        <strong>-Tabela 5938 do SIDRA-IBGE (dados do PIB):</strong> https://sidra.ibge.gov.br/tabela/5938<br>
        <strong>-Portal do TSE (informações dos prefeitos eleitos):</strong> https://dadosabertos.tse.jus.br/dataset/?q=candidatos&sort=score+desc%2C+metadata_modified+desc
        </p>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style="font-size:40px;text-align: left;">
        <strong><bold>Indicadores de Saúde</bold></strong>
        </p>

        <p style="font-size:17px;text-align: justify;">
        <strong>-Portal do TCE-RS (dados de investimento em saúde e índice ASPS):</strong> https://portal.tce.rs.gov.br/aplicprod/f?p=20001:23:::NO:::<br>
        <strong>-DATASUS - tabnet (dados de imunização):</strong> https://datasus.saude.gov.br/informacoes-de-saude-tabnet/<br>
        <strong>-Lei complementar nº 141 (estabelece o investimento mínimo em Ações e Serviço Público de Saúde - ASPS):</strong> https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp141.htm<br>
        <strong>-Manual de Demonstrativos Fiscais (expõe sobre o que são consideradas Ações e Serviço Público de Saúde):</strong> https://conteudo.tesouro.gov.br/manuais/index.php?option=com_content&view=article&id=1308:03-12-02-01-acoes-e-servicos-publicos-de-saude-asps&catid=661&Itemid=675<br>
        <strong>-Epidemiol. Serv. Saúde (explicação sobre cálculo da cobertura vacinal):</strong> https://bvsms.saude.gov.br/bvs/publicacoes/denominadores_calculo_coberturas_vacinais.pdf<br>
        <strong>-Portal CIDADES - IBGE (dados de mortalidade infantil):</strong> https://cidades.ibge.gov.br/brasil/rs/pesquisa/17/15752
        </p>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style="font-size:40px;text-align: left;">
        <strong><bold>Indicadores de Educação</bold></strong>
        </p>

        <p style="font-size:17px;text-align: justify;">
        <strong>-Portal do TCE-RS (dados de investimento em educação e índice MDE):</strong> https://portal.tce.rs.gov.br/aplicprod/f?p=20001:23:::NO:::<br>
        <strong>-Portal CIDADES - IBGE (dados do Índice de Desenvolviemnto da Educação Básica - IDEB):</strong> https://cidades.ibge.gov.br/brasil/rs/pesquisa/40/30277<br>
        <strong>-Artigo 212 da Constituição Federal de 1988 (estabelece o investimento mínimo em Manutenção e Desenvolvimento da Educação - MDE):</strong> https://portal.stf.jus.br/constituicao-supremo/artigo.asp?abrirBase=CF&abrirArtigo=212<br>
        <strong>-INEP (conceituação do índice IDEB):</strong> https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb
        </p>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style="font-size:40px;text-align: left;">
        <strong><bold>Indicadores de Gestão Fiscal</bold></strong>
        </p>

        <p style="font-size:17px;text-align: justify;">
        <strong>-Portal do TCE-RS (dados de Receita Corrente Líquida e dos 4 indicadores analisados):</strong> https://portal.tce.rs.gov.br/aplicprod/f?p=20001:23:::NO:::<br>
        <strong>-Congresso Nacional (conceituação de Receita Corrente Líquida):</strong> https://www.congressonacional.leg.br/legislacao-e-publicacoes/glossario-orcamentario/-/orcamentario/termo/receita_corrente_liquida_rcl<br>
        <strong>-Artigo 169 da Constituição Federal de 1988 (conceituação dos limites ligados à Receita Corrente Líquida):</strong> https://www.planalto.gov.br/ccivil_03/leis/lcp/Lcp96impressao.htm
        <strong>-Confederação Nacional de Municípios (conceituação e normas para "Restos à pagar"):</strong> https://cnm.org.br/storage/biblioteca/RestosaPagar(2011).pdf
        </p>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <p style="font-size:40px;text-align: left;">
        <strong><bold>Indicadores de Saneamento</bold></strong>
        </p>

        <p style="font-size:17px;text-align: justify;">
        <strong>-Glossário de Indicadores (explicação dos indicadores de água, esgoto e resíduos sólidos):</strong> https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/snis/produtos-do-snis/diagnosticos/Glossario_Indicadores_AE2022.pdf<br>
        <strong>-Painel de Indicadores - SNIS (dados dos indicadores de água, esgoto e resíduos sólidos):</strong> http://appsnis.mdr.gov.br/indicadores-hmg/web/agua_esgoto/mapa-agua
        </p>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <hr style="border: 1px solid #ccc; width: 100%; margin: 0; margin-top: 10px; margin-bottom: 10px;">
        <div style='text-align: center; font-size: 40px; margin-top:10px;margin-bottom: 10px;'>
        <strong>Agradecimentos</strong><br>
        <div style='text-align: left; font-size: 20px; margin-top:10px;margin-bottom: 10px;'>
        <strong>Revisão de indicadores de saúde:</strong> Ana Paula Bernardi - Graduanda em Biomedicina pela UFCSPA
        </div>
        """,unsafe_allow_html=True)

    st.sidebar.image("logo.png", width=150)

references()
