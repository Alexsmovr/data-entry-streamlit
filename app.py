# Exportação se houver dados
if not st.session_state.dados.empty:
    st.subheader("📤 Exportar Dados")

    # Campo para nome personalizado do arquivo
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
