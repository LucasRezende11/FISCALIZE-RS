import streamlit as st

st.set_page_config(page_icon= "logo3.png", layout="wide")

def about_function():
    st.sidebar.image("logo.png", width=150)
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

    st.markdown(
        """
        <div style="background-color: #DDDDDD; padding: 2px; border-radius: 5px; text-align: center;">
            <h1 style="font-size: 60px; margin: 0;">
                <span style="color: red;">FISCA</span><span style="color: #FFFF10;">LIZE</span>
                <span style="color: green;">RS</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True)

    st.markdown(
        """
        ## **Objetivo**

        <p style="font-size:20px;text-align: justify;">
        O <strong>FISCALIZE RS</strong> é uma iniciativa que busca <strong><u>democratizar o acesso às informações de gestão municipal</u></strong>, e que almeja trazer uma visão geral dos municípios, permitindo aos indivíduos exercerem sua cidadania de maneira mais ativa e fiscalizar se as municipalidades estão cumprindo as suas funções básicas e constitucionais.
        A partir da ferramenta, o usuário consegue obter informações socioeconômicas, das contas públicas municipais e de indicadores de setores basilares, como saúde e educação.
        </p>

        <p style="font-size:20px;text-align: justify;">
        Além disso, busca-se mostrar a importância da gestão adequada dos recursos públicos e dos investimentos em saúde, educação e saneamento, com o objetivo de promover o desenvolvimento de maneira ampla.
        </p>

        ## **Como pesquisar**

        <p style="font-size:20px;">
        O <strong>FISCALIZE RS</strong> é focado nos municípios gaúchos, e para realizar a consulta é muito simples:
        </p>

        <p style="font-size:20px;text-align: justify;">
        - 🗂️ <strong>Acesse as abas de interesse no menu lateral</strong><br>
        - 📍 <strong>Selecione o município desejado</strong> (algumas abas requerem também a escolha de um ano ou outra opção de visualização)<br>
        - ⏳ <strong>Aguarde alguns segundos</strong> até que os dados sejam carregados<br>
        - 📊 <strong>Pronto!</strong> Agora, você pode fazer uma análise consciente sobre a situação do município.
        </p>

        <p style="font-size:18px;text-align: justify;background-color: #CCCCCC; padding: 10px;">
        <strong>Formato dos dados:</strong> Em geral, os dados são apresentados em sua forma nominal, ou seja, sem considerar o efeito da inflação sobre os valores. Isso não acontece apenas na página de "Indicadores Econômicos", onde os dados estão deflacionados.<br>
        A decisão para esse formato foi tomada levando em conta o caráter fiscalizatório propostosto para a ferramenta, então, dados nominais são mais fáceis de serem encontrados e checados nas referências utilizadas.
        </p>

        <p style="font-size:18px;text-align: justify;">
        <strong>Dica:</strong> Acesse os cards informativos &#9432;</span> <!-- Ícone de informação --> para compreender melhor os indicadores, e também consulte as referências, na aba com mesmo nome, para aprofundar seus conhecimentos sobre gestão pública.
        </p>

        <h3 style="text-align: center;"><strong>Tem alguma dúvida ou sugestão?</strong></h3>

        <p style="font-size:18px;text-align: center;">
        Por favor, <a href="https://forms.gle/Yb73ubje8mSXkWBN9" target="_blank" style="text-decoration: underline; color: blue;">entre em contato</a>. Esta é uma plataforma que visa o acesso à informação básica de qualidade.<br>
        Qualquer sugestão ou informe de inconsistências será bem-vindo.
        </p>
        """, unsafe_allow_html=True)

about_function()
