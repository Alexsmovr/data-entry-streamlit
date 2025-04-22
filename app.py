import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Data Entry com Exportação", layout="wide")

# Definindo as colunas fixas
colunas = [
    "Data Mov", "Cod Cliente", "Cliente", 
    "Gestional Real", "Gestional Plan", 
    "Contable Real", "Contable Plan", 
    "Comentario", "desvio"
]

st.title("📝 Data Entry com Exportação")

# Session state para armazenar os dados
if 'dados' not in st.session_state:
    st.session_state.dados = []

# Formulário de entrada
with st.form("formulario"):
    inputs = []
    cols = st.columns(len(colunas))
    for i, coluna in enumerate(colunas):
        if "Real" in coluna or "Plan" in coluna or coluna == "desvio":
            valor = cols[i].number_input(coluna, format="%.6f", key=coluna)
        else:
            valor = cols[i].text_input(coluna, key=coluna)
        inputs.append(valor)

    submit = st.form_submit_button("➕ Adicionar Linha")
    if submit:
        st.session_state.dados.append(inputs)
        st.success("Linha adicionada com sucesso!")

# Mostrar tabela atual
if st.session_state.dados:
    df = pd.DataFrame(st.session_state.dados, columns=colunas)
    st.subheader("📋 Dados Inseridos")
    st.dataframe(df, use_container_width=True)

    # Botões de exportação
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
            writer.save()
        st.download_button("⬇️ Baixar Excel", data=buffer, file_name="dados.xlsx", mime="application/vnd.ms-excel")
