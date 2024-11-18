import streamlit as st
import sidrapy
import unidecode
import pandas as pd

def main():
    run_app()

def run_app():
    # --- PAGE SETUP ---
    about_page = st.Page("pages/fiscalize_rs.py",
        title="FISCALIZE RS",
        icon=":material/search:",
        default=True)

    revenue_page = st.Page("pages/Indicadores_de_Receita_Municipal.py",
        title="Indicadores de Receita Municipal",
        icon=":material/currency_exchange:")

    economic_page = st.Page(
        "pages/Indicadores_Econômicos.py",
        title="Indicadores Econômicos",
        icon=":material/query_stats:")

    health_page = st.Page("pages/Indicadores_de_Saúde.py",
        title="Indicadores de Saúde",
        icon=":material/local_hospital:")

    education_page = st.Page("pages/Indicadores_de_Educação.py",
        title="Indicadores de Educação",
        icon=":material/school:")

    administration_page = st.Page("pages/Indicadores_de_Gestão_Fiscal.py",
        title="Indicadores de Gestão Fiscal",
        icon=":material/admin_panel_settings:")

    sanitation_page = st.Page("pages/Indicadores_de_Saneamento.py",
        title="Indicadores de Saneamento",
        icon=":material/valve:")

    references_page = st.Page("pages/Referências.py",
        title="Referências",
        icon=":material/menu_book:")

    # --- NAVIGATION  ---
    pg = st.navigation(pages=[about_page, revenue_page, economic_page, health_page, education_page, administration_page, sanitation_page, references_page])

    pg.run()


# --- NORMALIZE function ---
def normalize(nome):
    return unidecode.unidecode(nome)


# --- FORMAT CITY NAME function ---
def format_city_name(name):
    if not name or not isinstance(name, str):
        return ""
    exceptions = ['de', 'do', 'da', 'dos', 'das']
    words = name.split()
    formatted_words = [words[0].title()]
    for word in words[1:]:
        if word.lower() in exceptions:
            formatted_words.append(word.lower())
        else:
            formatted_words.append(word.title())
    formatted_name = ' '.join(formatted_words)
    return formatted_name


# --- SIDRA data collection function ---
def get_sidra_data(table_code, variables, territorial_level, ibge_territorial_code, period = 'all', unity = 1, dfs_name="dfs", df_name_prefix="df"):
    dfs = {}
    for var in variables:
        df = sidrapy.get_table(
        table_code=table_code,
        variable=var,
        territorial_level=territorial_level,
        ibge_territorial_code=ibge_territorial_code,
        period=period,
        timeout=90)

        df_filtered = df.iloc[:, [7, 4]].copy()
        df_filtered.columns = ['Ano', 'Valor']
        df_filtered.iloc[:, 1] = pd.to_numeric(df_filtered.iloc[:, 1], errors='coerce') * unity
        df_filtered = df_filtered.dropna().reset_index(drop=True)

        df_name = f"{df_name_prefix}_{var}"
        dfs[df_name] = df_filtered

    globals()[dfs_name] = dfs
    return dfs


if __name__ == "__main__":
    main()


