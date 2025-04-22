import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Data Entry com Edição", layout="wide")

colunas = [
    "Data Mov", "Cod Cliente", "Cliente", 
    "Gestional Real", "Gestional Plan", 
    "Contable Real", "Contable Plan", 
    "Comentario", "desvio"
]

st.title("📝 Data Entry com Edição Livre")

# Inicializa os dados
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=colunas)

# 📂 Importação
st.sidebar.header("📂 Importar Arquivo")
arquivo = st.sidebar.file_uploader("Escolha um arquivo (.txt, .csv ou .xlsx)", type=["txt", "csv", "xlsx"])

if arquivo:
    try:
        if arquivo.name.endswith(".txt"):
            df_importado = pd.read_csv(arquivo, sep="|", encoding="latin1")
        elif arquivo.name.endswith(".csv"):
            df_importado = pd.read_csv(arquivo)
        elif arquivo.name.endswith(".xlsx"):
            df_importado = pd.read_excel(arquivo)
        else:
            st.sidebar.error("Formato de arquivo não suportado.")
            df_importado = None

        if df_importado is not None:
            if list(df_importado.columns) == colunas:
                st.session_state.dados = df_importado.copy()
                st.sidebar.success("Arquivo importado com sucesso!")
            else:
                st.sidebar.error("As colunas do arquivo não correspondem ao modelo esperado.")
    except Exception as e:
        st.sidebar.error(f"Erro ao importar: {str(e)}")

# ✏️ Editor de dados
st.subheader("📋 Editar Dados")
df_editado = st.data_editor(
    st.session_state.dados,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_dados"
)

# Salva as alterações no session_state
st.session_state.dados = df_editado

# ⬇️ Exportação
if not st.session_state.dados.empty:
    st.subheader("📤 Exportar Dados")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv = st.session_state.dados.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar CSV", data=csv, file_name="dados.csv", mime="text/csv")

    with col2:
        txt = st.session_state.dados.to_csv(index=False, sep="|").encode("utf-8")
        st.download_button("⬇️ Baixar TXT (pipe)", data=txt, file_name="dados.txt", mime="text/plain")

    with col3:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            st.session_state.dados.to_excel(writer, sheet_name="Dados", index=False)
        st.download_button("⬇️ Baixar Excel", data=buffer, file_name="dados.xlsx", mime="application/vnd.ms-excel")
