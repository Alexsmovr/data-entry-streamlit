import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Data Entry com Exportação", layout="wide")

colunas = [
    "Data Mov", "Cod Cliente", "Cliente", 
    "Gestional Real", "Gestional Plan", 
    "Contable Real", "Contable Plan", 
    "Comentario", "desvio"
]

st.title("📝 Data Entry com Exportação")

# Inicializa os dados
if 'dados' not in st.session_state:
    st.session_state.dados = []

if 'linhas_importadas' not in st.session_state:
    st.session_state.linhas_importadas = []

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
                st.session_state.linhas_importadas = df_importado.values.tolist()
                st.sidebar.success("Arquivo carregado. Edite e insira linha por linha.")
            else:
                st.sidebar.error("As colunas do arquivo não correspondem ao modelo esperado.")
    except Exception as e:
        st.sidebar.error(f"Erro ao importar: {str(e)}")

# 🔄 Carrega uma linha do arquivo importado (se houver)
valores_iniciais = {}
if st.session_state.linhas_importadas:
    linha_atual = st.session_state.linhas_importadas[0]
    for i, coluna in enumerate(colunas):
        valores_iniciais[coluna] = linha_atual[i]
else:
    for coluna in colunas:
        valores_iniciais[coluna] = ""

# Formulário com dados pré-preenchidos (se houver)
with st.form("formulario"):
    inputs = []
    cols = st.columns(len(colunas))
    for i, coluna in enumerate(colunas):
        valor_padrao = valores_iniciais[coluna]
        if "Real" in coluna or "Plan" in coluna or coluna == "desvio":
            valor = cols[i].number_input(coluna, format="%.6f", key=f"{coluna}_input", value=float(valor_padrao) if valor_padrao != "" else 0.0)
        else:
            valor = cols[i].text_input(coluna, key=f"{coluna}_input", value=str(valor_padrao))
        inputs.append(valor)

    submit = st.form_submit_button("➕ Adicionar Linha")
    if submit:
        st.session_state.dados.append(inputs)
        if st.session_state.linhas_importadas:
            st.session_state.linhas_importadas.pop(0)  # Remove a linha já inserida
        st.success("Linha adicionada com sucesso!")

# 📋 Mostra os dados já inseridos
if st.session_state.dados:
    df = pd.DataFrame(st.session_state.dados, columns=colunas)
    st.subheader("📋 Dados Inseridos")
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar CSV", data=csv, file_name="dados.csv", mime="text/csv")

    with col2:
        txt = df.to_csv(index=False, sep="|").encode("utf-8")
        st.download_button("⬇️ Baixar TXT (pipe)", data=txt, file_name="dados.txt", mime="text/plain")

    with col3:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Dados", index=False)
        st.download_button("⬇️ Baixar Excel", data=buffer, file_name="dados.xlsx", mime="application/vnd.ms-excel")


