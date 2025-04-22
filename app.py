import streamlit as st
import pandas as pd
import io
import os

# 🔽 Apenas se rodando localmente
import tkinter as tk
from tkinter import filedialog

def salvar_com_dialogo(df, tipo):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tk
    tipos = {
        "csv": ("CSV Files", "*.csv"),
        "txt": ("Text Files", "*.txt"),
        "xlsx": ("Excel Files", "*.xlsx")
    }
    extensao = tipo.lower()
    filepath = filedialog.asksaveasfilename(
        defaultextension=f".{extensao}",
        filetypes=[tipos[extensao]],
        title="Salvar como..."
    )
    if filepath:
        if extensao == "csv":
            df.to_csv(filepath, index=False)
        elif extensao == "txt":
            df.to_csv(filepath, sep="|", index=False)
        elif extensao == "xlsx":
            with pd.ExcelWriter(filepath, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Dados", index=False)
        st.success(f"Arquivo salvo em:\n{filepath}")
    else:
        st.warning("Salvamento cancelado.")

# 🔧 Exemplo com DataFrame qualquer
st.title("💾 Exportação Local com Diálogo (Tkinter)")

# Simula dados carregados
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame({
        "Data Mov": ["20250425"],
        "Cod Cliente": ["B21"],
        "Cliente": ["Redução"],
        "Gestional Real": [1325.03],
        "Gestional Plan": [1325.03],
        "Contable Real": [1325.03],
        "Contable Plan": [1325.03],
        "Comentario": ["OK"],
        "desvio": [-0.0021]
    })

df = st.session_state.dados
st.dataframe(df, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 Salvar CSV"):
        salvar_com_dialogo(df, "csv")

with col2:
    if st.button("💾 Salvar TXT"):
        salvar_com_dialogo(df, "txt")

with col3:
    if st.button("💾 Salvar Excel"):
        salvar_com_dialogo(df, "xlsx")
