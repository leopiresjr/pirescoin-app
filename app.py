import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PIL import Image

# ====== Configuração da página ======
st.set_page_config(page_title="PIREScoin – Caça Tesouros",
                   page_icon="💰", layout="centered")

# ====== CSS para responsividade e centralização ======
st.markdown("""
    <style>
        .main {
            max-width: 800px;
            margin: auto;
            padding-top: 20px;
        }
        h1, h2, h3, p {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ====== Logo e título ======
logo = Image.open("logo.png")
st.image(logo, width=120)

st.markdown("<h1 style='color:#f4c430;'>PIREScoin</h1>",
            unsafe_allow_html=True)
st.markdown("<p>Análise diária de criptomoedas com inteligência estratégica</p>",
            unsafe_allow_html=True)
st.markdown("---")

# ====== Criptomoedas analisadas ======
ativos = {
    'Bitcoin (BTC)': 'BTC-USD',
    'Ethereum (ETH)': 'ETH-USD',
    'Cardano (ADA)': 'ADA-USD'
}

hoje = datetime.now().date()
ontem = hoje - timedelta(days=1)

retornos = {}
for nome, ticker in ativos.items():
    try:
        dados = yf.download(ticker, start=str(
            ontem), end=str(hoje), progress=False)
        if not dados.empty:
            preco_inicio = dados['Close'].iloc[0]
            preco_fim = dados['Close'].iloc[-1]
            retorno = (preco_fim - preco_inicio) / preco_inicio
            retornos[nome] = retorno
    except Exception:
        pass

# ====== Exibição de resultados com gráfico e botão funcional ======
if retornos:
    df = pd.DataFrame.from_dict(
        retornos, orient='index', columns=['Retorno 24h'])
    df = df.sort_values('Retorno 24h', ascending=False)

    if not df.empty:
        melhor = df.index[0]
        melhor_valor = df.iloc[0, 0]

        st.subheader("📊 Última análise")
        st.success(
            f"Melhor cripto hoje: **{melhor}** com retorno de **{melhor_valor:.2%}**")

        # ====== Gráfico de barras horizontal ======
        st.markdown("### 📉 Comparativo de Retorno")
        fig, ax = plt.subplots(figsize=(6, 3))
        cores = ['#FFD700' if i == melhor else '#87CEEB' for i in df.index]

        df['Retorno 24h'].plot(kind='barh', ax=ax, color=cores)
        ax.set_xlabel("Retorno (%)")
        ax.set_ylabel("Criptomoeda")
        ax.set_title("Retorno das criptomoedas nas últimas 24h")
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        st.pyplot(fig)

        # ====== Expansão de detalhes ======
        with st.expander("🔍 Ver mais detalhes (em breve)"):
            st.info(
                "Simulação de gráfico, risco e tendências futuras (a ser implementado).")

        # ====== Botão funcional com lógica de decisão ======
        if st.button("🚀 Sugerir entrada estratégica"):
            st.markdown("### 📌 Recomendação Estratégica")

            if melhor_valor > 0.02:
                st.success(
                    f"A tendência de **{melhor}** está positiva. Entrada recomendada com cautela.")
            elif melhor_valor > 0:
                st.info(
                    f"**{melhor}** apresenta leve valorização. Aguarde confirmação de tendência.")
            else:
                st.warning(
                    f"**{melhor}** está em queda nas últimas 24h. Não recomendado entrar agora.")

    else:
        st.warning(
            "⚠️ Nenhum retorno disponível. Os dados não puderam ser carregados.")
else:
    st.warning("⚠️ Nenhuma criptomoeda teve dados disponíveis nas últimas 24h.")
