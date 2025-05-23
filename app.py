
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Data Entry Web", layout="wide")

# Logo da Ternium
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Ternium_logo.svg/2560px-Ternium_logo.svg.png", width=200)

 

# Define colunas padrão
colunas = [
    "Data Mov", "Cod Cliente", "Cliente", 
    "Gestional Real", "Gestional Plan", 
    "Contable Real", "Contable Plan", 
    "Comentario", "desvio"
]

# Inicializa session_state
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=colunas)

st.title("📝 Data Entry com Edição e Exportação Web")

# 📂 Importação de arquivo
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

# ✏️ Edição interativa dos dados
st.subheader("📋 Editar Dados")
df_editado = st.data_editor(
    st.session_state.dados,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_dados"
)
st.session_state.dados = df_editado

# Exportação se houver dados
if not st.session_state.dados.empty:
    st.subheader("📤 Exportar Dados")

    # Nome personalizado do arquivo
    nome_arquivo = st.text_input("📁 Nome do arquivo para exportação (sem extensão)", value="dados_exportados")
    st.caption("💡 O navegador pode sobrescrever ou renomear esse arquivo automaticamente se ele já existir na sua pasta de downloads.")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv = st.session_state.dados.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Baixar CSV",
            data=csv,
            file_name=f"{nome_arquivo}.csv",
            mime="text/csv"
        )

    with col2:
        txt = st.session_state.dados.to_csv(index=False, sep="|").encode("latin1")
        st.download_button(
            "⬇️ Baixar TXT",
            data=txt,
            file_name=f"{nome_arquivo}.txt",
            mime="text/plain"
        )

    with col3:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            st.session_state.dados.to_excel(writer, sheet_name="Dados", index=False)
        st.download_button(
            "⬇️ Baixar Excel",
            data=buffer,
            file_name=f"{nome_arquivo}.xlsx",
            mime="application/vnd.ms-excel"
        )
