# =============================================================================
# Projeto G2 — Tema 5: Acidentes de Trânsito no Brasil (2015-2024)
# Dashboard Interativo com Streamlit
# =============================================================================
# Tecnologias: Python, Pandas, Streamlit, Plotly, Matplotlib, Seaborn
# Descrição: Dashboard analítico para investigar padrões de acidentes de
#            trânsito no Brasil, com KPIs, filtros interativos, gráficos
#            e interpretação textual dos resultados.
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Acidentes de Trânsito no Brasil",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CSS CUSTOMIZADO — Visual Premium
# =============================================================================
st.markdown("""
<style>
    /* Importar fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Aplicar fonte global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Título principal */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        padding: 0.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 300;
    }

    /* Cards de KPI */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8ecff 100%);
        border: 1px solid #e0e4f5;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
    }

    div[data-testid="stMetric"] label {
        color: #5a5f7a;
        font-weight: 500;
        font-size: 0.85rem;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #1a1a2e;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e0e0e0;
    }

    /* Separadores */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 1.5rem 0;
    }

    /* Cabeçalhos de seção */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1a1a2e;
        border-left: 4px solid #667eea;
        padding-left: 12px;
        margin: 1.5rem 0 1rem 0;
    }

    /* Cards de interpretação */
    .insight-card {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%);
        border-left: 4px solid #667eea;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #2d3436;
    }

    /* Conclusão executiva */
    .conclusion-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 4px solid #ff9800;
        border-radius: 0 8px 8px 0;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #2d3436;
    }

    /* Tabs customizados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-weight: 500;
    }

    /* Esconder menu hamburger e footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CARREGAMENTO DE DADOS (com cache)
# =============================================================================
@st.cache_data
def carregar_dados():
    """Carrega e prepara o dataset de acidentes de trânsito."""
    df = pd.read_csv("dados/simulacao_acidentes_transito_brasil.csv", encoding="utf-8-sig")

    # Converter tipos
    df["data"] = pd.to_datetime(df["data"])
    df["ano"] = df["ano"].astype(int)
    df["mes"] = df["mes"].astype(int)

    # Engenharia de atributos
    df["taxa_letalidade"] = (df["obitos"] / df["acidentes"]).round(4)
    df["feridos_por_acidente"] = (df["feridos"] / df["acidentes"]).round(4)
    df["veiculos_por_acidente"] = (df["veiculos_envolvidos"] / df["acidentes"]).round(4)

    # Mapeamento ordinal de gravidade
    mapa_gravidade = {"Leve": 1, "Moderado": 2, "Grave": 3, "Crítico": 4}
    df["gravidade_num"] = df["nivel_gravidade"].map(mapa_gravidade)

    # Nomes dos meses em português
    meses_pt = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    df["mes_nome"] = df["mes"].map(meses_pt)

    # Ordenar dados
    df = df.sort_values(["ano", "mes", "regiao", "uf"]).reset_index(drop=True)

    return df


# Carregar dados
df = carregar_dados()

# =============================================================================
# SIDEBAR — FILTROS INTERATIVOS (7 filtros obrigatórios)
# =============================================================================
with st.sidebar:
    st.markdown("## 🔍 Filtros")
    st.markdown("---")

    # 1. Filtro por Ano
    anos_disponiveis = sorted(df["ano"].unique())
    anos_selecionados = st.multiselect(
        "📅 Ano",
        options=anos_disponiveis,
        default=anos_disponiveis,
        key="filtro_ano"
    )

    # 2. Filtro por Mês
    meses_disponiveis = sorted(df["mes"].unique())
    meses_nomes = {m: df[df["mes"] == m]["mes_nome"].iloc[0] for m in meses_disponiveis}
    meses_selecionados = st.multiselect(
        "🗓️ Mês",
        options=meses_disponiveis,
        default=meses_disponiveis,
        format_func=lambda x: meses_nomes[x],
        key="filtro_mes"
    )

    # 3. Filtro por Região
    regioes_disponiveis = sorted(df["regiao"].unique())
    regioes_selecionadas = st.multiselect(
        "🌎 Região",
        options=regioes_disponiveis,
        default=regioes_disponiveis,
        key="filtro_regiao"
    )

    # 4. Filtro por Estado (dinâmico conforme região)
    ufs_disponiveis = sorted(df[df["regiao"].isin(regioes_selecionadas)]["uf"].unique())
    ufs_selecionadas = st.multiselect(
        "🏛️ Estado (UF)",
        options=ufs_disponiveis,
        default=ufs_disponiveis,
        key="filtro_uf"
    )

    # 5. Filtro por Tipo de Acidente
    tipos_disponiveis = sorted(df["tipo_acidente"].unique())
    tipos_selecionados = st.multiselect(
        "💥 Tipo de Acidente",
        options=tipos_disponiveis,
        default=tipos_disponiveis,
        key="filtro_tipo"
    )

    # 6. Filtro por Período do Dia
    periodos_disponiveis = ["Madrugada", "Manhã", "Tarde", "Noite"]
    periodos_selecionados = st.multiselect(
        "🕐 Período do Dia",
        options=periodos_disponiveis,
        default=periodos_disponiveis,
        key="filtro_periodo"
    )

    # 7. Filtro por Nível de Gravidade
    gravidades_disponiveis = ["Leve", "Moderado", "Grave", "Crítico"]
    gravidades_selecionadas = st.multiselect(
        "⚠️ Nível de Gravidade",
        options=gravidades_disponiveis,
        default=gravidades_disponiveis,
        key="filtro_gravidade"
    )

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; font-size:0.75rem; color:#8a8a8a;'>"
        "Projeto G2 — Linguagens de Programação<br>2025</p>",
        unsafe_allow_html=True
    )

# =============================================================================
# APLICAR FILTROS
# =============================================================================
# Garantir que filtros não estejam vazios (fallback para todos)
if not anos_selecionados:
    anos_selecionados = anos_disponiveis
if not meses_selecionados:
    meses_selecionados = meses_disponiveis
if not regioes_selecionadas:
    regioes_selecionadas = regioes_disponiveis
if not ufs_selecionadas:
    ufs_selecionadas = ufs_disponiveis
if not tipos_selecionados:
    tipos_selecionados = tipos_disponiveis
if not periodos_selecionados:
    periodos_selecionados = periodos_disponiveis
if not gravidades_selecionadas:
    gravidades_selecionadas = gravidades_disponiveis

df_filtrado = df[
    (df["ano"].isin(anos_selecionados)) &
    (df["mes"].isin(meses_selecionados)) &
    (df["regiao"].isin(regioes_selecionadas)) &
    (df["uf"].isin(ufs_selecionadas)) &
    (df["tipo_acidente"].isin(tipos_selecionados)) &
    (df["periodo_dia"].isin(periodos_selecionados)) &
    (df["nivel_gravidade"].isin(gravidades_selecionadas))
]

# =============================================================================
# CABEÇALHO
# =============================================================================
st.markdown('<h1 class="main-title">🚗 Acidentes de Trânsito no Brasil</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Análise exploratória e visualização de dados — 2015 a 2024</p>',
    unsafe_allow_html=True
)

# Descrição do problema
with st.expander("ℹ️ Sobre este projeto", expanded=False):
    st.markdown("""
    Os acidentes de trânsito representam um dos principais problemas de segurança pública
    e saúde no Brasil, causando impactos sociais, econômicos e humanos significativos.

    Este dashboard permite investigar **padrões de acidentes de trânsito no Brasil**
    entre 2015 e 2024, identificando regiões críticas, horários de maior risco,
    tipos mais frequentes de ocorrência e fatores associados.

    **Utilize os filtros na barra lateral** para explorar os dados de forma interativa.
    """)

st.markdown("---")

# =============================================================================
# KPIs (6 obrigatórios)
# =============================================================================
st.markdown('<p class="section-header">📊 Indicadores-Chave (KPIs)</p>', unsafe_allow_html=True)

# Calcular KPIs
total_acidentes = int(df_filtrado["acidentes"].sum())
total_feridos = int(df_filtrado["feridos"].sum())
total_obitos = int(df_filtrado["obitos"].sum())

# Estado mais crítico
if not df_filtrado.empty:
    estado_critico = df_filtrado.groupby("uf")["acidentes"].sum().idxmax()
    estado_critico_valor = int(df_filtrado.groupby("uf")["acidentes"].sum().max())
else:
    estado_critico = "N/A"
    estado_critico_valor = 0

# Período mais perigoso
if not df_filtrado.empty:
    periodo_perigoso = df_filtrado.groupby("periodo_dia")["acidentes"].sum().idxmax()
    periodo_perigoso_valor = int(df_filtrado.groupby("periodo_dia")["acidentes"].sum().max())
else:
    periodo_perigoso = "N/A"
    periodo_perigoso_valor = 0

# Tipo de acidente mais frequente
if not df_filtrado.empty:
    tipo_frequente = df_filtrado.groupby("tipo_acidente")["acidentes"].sum().idxmax()
    tipo_frequente_valor = int(df_filtrado.groupby("tipo_acidente")["acidentes"].sum().max())
else:
    tipo_frequente = "N/A"
    tipo_frequente_valor = 0

# Exibir KPIs em 2 linhas de 3 colunas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🚨 Total de Acidentes", f"{total_acidentes:,}".replace(",", "."))
with col2:
    st.metric("🏥 Total de Feridos", f"{total_feridos:,}".replace(",", "."))
with col3:
    st.metric("⚰️ Total de Óbitos", f"{total_obitos:,}".replace(",", "."))

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("🏛️ Estado Mais Crítico", estado_critico, f"{estado_critico_valor:,}".replace(",", ".") + " acidentes")
with col5:
    st.metric("🕐 Período Mais Perigoso", periodo_perigoso, f"{periodo_perigoso_valor:,}".replace(",", ".") + " acidentes")
with col6:
    st.metric("💥 Tipo Mais Frequente", tipo_frequente, f"{tipo_frequente_valor:,}".replace(",", ".") + " acidentes")

st.markdown("---")

# =============================================================================
# GRÁFICOS — Usando Plotly para interatividade
# =============================================================================

# Paleta de cores consistente
CORES_PRIMARIAS = px.colors.qualitative.Set2
CORES_SEQUENCIAIS = "Blues"
CORES_DIVERGENTES = "RdYlGn_r"

# ---------- GRÁFICO 1: EVOLUÇÃO TEMPORAL ----------
st.markdown('<p class="section-header">📈 Evolução Temporal dos Acidentes</p>', unsafe_allow_html=True)

df_temporal = df_filtrado.groupby("ano").agg(
    acidentes=("acidentes", "sum"),
    feridos=("feridos", "sum"),
    obitos=("obitos", "sum")
).reset_index()

fig_temporal = go.Figure()
fig_temporal.add_trace(go.Scatter(
    x=df_temporal["ano"], y=df_temporal["acidentes"],
    mode="lines+markers", name="Acidentes",
    line=dict(color="#667eea", width=3),
    marker=dict(size=8, symbol="circle"),
    hovertemplate="Ano: %{x}<br>Acidentes: %{y:,.0f}<extra></extra>"
))
fig_temporal.add_trace(go.Scatter(
    x=df_temporal["ano"], y=df_temporal["feridos"],
    mode="lines+markers", name="Feridos",
    line=dict(color="#f093fb", width=2, dash="dash"),
    marker=dict(size=6),
    hovertemplate="Ano: %{x}<br>Feridos: %{y:,.0f}<extra></extra>"
))
fig_temporal.add_trace(go.Scatter(
    x=df_temporal["ano"], y=df_temporal["obitos"],
    mode="lines+markers", name="Óbitos",
    line=dict(color="#e74c3c", width=2, dash="dot"),
    marker=dict(size=6),
    yaxis="y2",
    hovertemplate="Ano: %{x}<br>Óbitos: %{y:,.0f}<extra></extra>"
))
fig_temporal.update_layout(
    title="",
    xaxis=dict(title="Ano", dtick=1),
    yaxis=dict(title="Acidentes / Feridos", gridcolor="#f0f0f0"),
    yaxis2=dict(title="Óbitos", overlaying="y", side="right", gridcolor="#f0f0f0"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    height=400,
    margin=dict(l=60, r=60, t=30, b=40),
    hovermode="x unified"
)
st.plotly_chart(fig_temporal, use_container_width=True, key="chart_temporal")

st.markdown("---")

# ---------- GRÁFICOS 2 e 3: BARRAS POR ESTADO + COMPARAÇÃO REGIONAL ----------
st.markdown('<p class="section-header">🗺️ Comparação Geográfica</p>', unsafe_allow_html=True)

col_geo1, col_geo2 = st.columns([3, 2])

with col_geo1:
    # Barras por estado (horizontal, ordenado)
    df_estado = df_filtrado.groupby("uf")["acidentes"].sum().sort_values(ascending=True).reset_index()
    fig_estado = px.bar(
        df_estado, x="acidentes", y="uf",
        orientation="h",
        color="acidentes",
        color_continuous_scale="Blues",
        labels={"acidentes": "Total de Acidentes", "uf": "Estado"},
        title="Acidentes por Estado"
    )
    fig_estado.update_layout(
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(l=40, r=20, t=40, b=40),
        yaxis=dict(tickfont=dict(size=11))
    )
    st.plotly_chart(fig_estado, use_container_width=True, key="chart_estado")

with col_geo2:
    # Comparação por região
    df_regiao = df_filtrado.groupby("regiao").agg(
        acidentes=("acidentes", "sum"),
        obitos=("obitos", "sum")
    ).reset_index().sort_values("acidentes", ascending=False)

    fig_regiao = px.bar(
        df_regiao, x="regiao", y="acidentes",
        color="regiao",
        color_discrete_sequence=CORES_PRIMARIAS,
        labels={"acidentes": "Total de Acidentes", "regiao": "Região"},
        title="Acidentes por Região"
    )
    fig_regiao.update_layout(
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_regiao, use_container_width=True, key="chart_regiao")

st.markdown("---")

# ---------- GRÁFICOS 4 e 5: TIPO DE ACIDENTE + PIZZA CLIMA ----------
st.markdown('<p class="section-header">🔍 Análise por Tipo e Clima</p>', unsafe_allow_html=True)

col_tipo1, col_tipo2 = st.columns(2)

with col_tipo1:
    # Barras por tipo de acidente
    df_tipo = df_filtrado.groupby("tipo_acidente")["acidentes"].sum().sort_values(ascending=False).reset_index()
    fig_tipo = px.bar(
        df_tipo, x="tipo_acidente", y="acidentes",
        color="tipo_acidente",
        color_discrete_sequence=["#667eea", "#764ba2", "#f093fb", "#5dade2", "#48dbfb"],
        labels={"acidentes": "Total de Acidentes", "tipo_acidente": "Tipo de Acidente"},
        title="Acidentes por Tipo"
    )
    fig_tipo.update_layout(
        height=420,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_tipo, use_container_width=True, key="chart_tipo")

with col_tipo2:
    # Pizza por condição climática
    df_clima = df_filtrado.groupby("condicao_climatica")["acidentes"].sum().reset_index()
    fig_clima = px.pie(
        df_clima, values="acidentes", names="condicao_climatica",
        color_discrete_sequence=["#667eea", "#f9ca24", "#a0a0a0", "#5dade2"],
        title="Distribuição por Condição Climática",
        hole=0.35
    )
    fig_clima.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="%{label}: %{value:,.0f} acidentes (%{percent})<extra></extra>"
    )
    fig_clima.update_layout(
        height=420,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_clima, use_container_width=True, key="chart_clima")

st.markdown("---")

# ---------- GRÁFICO 6: HEATMAP POR HORÁRIO ----------
st.markdown('<p class="section-header">🔥 Heatmap — Período do Dia × Mês</p>', unsafe_allow_html=True)

# Criar tabela pivot para o heatmap
meses_ordem = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
periodos_ordem = ["Madrugada", "Manhã", "Tarde", "Noite"]

df_heatmap = df_filtrado.groupby(["periodo_dia", "mes_nome"])["acidentes"].sum().reset_index()
df_heatmap_pivot = df_heatmap.pivot_table(
    index="periodo_dia", columns="mes_nome", values="acidentes", fill_value=0
)

# Reordenar
meses_presentes = [m for m in meses_ordem if m in df_heatmap_pivot.columns]
periodos_presentes = [p for p in periodos_ordem if p in df_heatmap_pivot.index]
df_heatmap_pivot = df_heatmap_pivot.reindex(index=periodos_presentes, columns=meses_presentes, fill_value=0)

fig_heatmap = px.imshow(
    df_heatmap_pivot.values,
    labels=dict(x="Mês", y="Período do Dia", color="Acidentes"),
    x=meses_presentes,
    y=periodos_presentes,
    color_continuous_scale="YlOrRd",
    aspect="auto"
)
fig_heatmap.update_layout(
    height=350,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=100, r=20, t=20, b=60),
    xaxis=dict(tickangle=45)
)
fig_heatmap.update_traces(
    hovertemplate="Mês: %{x}<br>Período: %{y}<br>Acidentes: %{z:,.0f}<extra></extra>"
)
st.plotly_chart(fig_heatmap, use_container_width=True, key="chart_heatmap")

st.markdown("---")

# ---------- GRÁFICOS EXTRAS: RANKING MUNICÍPIOS + GRAVIDADE ----------
st.markdown('<p class="section-header">🏙️ Ranking de Municípios e Análise de Gravidade</p>', unsafe_allow_html=True)

col_extra1, col_extra2 = st.columns(2)

with col_extra1:
    # Ranking de municípios
    df_municipio = df_filtrado.groupby("municipio").agg(
        acidentes=("acidentes", "sum"),
        obitos=("obitos", "sum")
    ).sort_values("acidentes", ascending=False).head(15).reset_index()

    fig_muni = px.bar(
        df_municipio.sort_values("acidentes", ascending=True),
        x="acidentes", y="municipio",
        orientation="h",
        color="obitos",
        color_continuous_scale="OrRd",
        labels={"acidentes": "Total de Acidentes", "municipio": "Município", "obitos": "Óbitos"},
        title="Top 15 Municípios Mais Críticos"
    )
    fig_muni.update_layout(
        height=480,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=120, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_muni, use_container_width=True, key="chart_municipio")

with col_extra2:
    # Análise de gravidade
    df_gravidade = df_filtrado.groupby("nivel_gravidade").agg(
        acidentes=("acidentes", "sum"),
        feridos=("feridos", "sum"),
        obitos=("obitos", "sum")
    ).reset_index()

    # Garantir ordem correta
    ordem_grav = ["Leve", "Moderado", "Grave", "Crítico"]
    df_gravidade["nivel_gravidade"] = pd.Categorical(
        df_gravidade["nivel_gravidade"], categories=ordem_grav, ordered=True
    )
    df_gravidade = df_gravidade.sort_values("nivel_gravidade")

    fig_grav = go.Figure()
    fig_grav.add_trace(go.Bar(
        x=df_gravidade["nivel_gravidade"], y=df_gravidade["acidentes"],
        name="Acidentes", marker_color="#667eea"
    ))
    fig_grav.add_trace(go.Bar(
        x=df_gravidade["nivel_gravidade"], y=df_gravidade["feridos"],
        name="Feridos", marker_color="#f093fb"
    ))
    fig_grav.add_trace(go.Bar(
        x=df_gravidade["nivel_gravidade"], y=df_gravidade["obitos"],
        name="Óbitos", marker_color="#e74c3c"
    ))
    fig_grav.update_layout(
        title="Distribuição por Nível de Gravidade",
        barmode="group",
        height=480,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis_title="Nível de Gravidade",
        yaxis_title="Quantidade"
    )
    st.plotly_chart(fig_grav, use_container_width=True, key="chart_gravidade")

st.markdown("---")

# ---------- TABELA DINÂMICA ----------
st.markdown('<p class="section-header">📋 Tabela Dinâmica — Exploração Detalhada</p>', unsafe_allow_html=True)

# Agrupar para a tabela dinâmica
df_tabela = df_filtrado.groupby(["ano", "regiao", "uf", "tipo_acidente", "condicao_climatica", "periodo_dia", "nivel_gravidade"]).agg(
    total_acidentes=("acidentes", "sum"),
    total_feridos=("feridos", "sum"),
    total_obitos=("obitos", "sum"),
    total_veiculos=("veiculos_envolvidos", "sum"),
    taxa_letalidade_media=("taxa_letalidade", "mean")
).reset_index()

df_tabela["taxa_letalidade_media"] = (df_tabela["taxa_letalidade_media"] * 100).round(2)
df_tabela = df_tabela.rename(columns={
    "ano": "Ano",
    "regiao": "Região",
    "uf": "UF",
    "tipo_acidente": "Tipo de Acidente",
    "condicao_climatica": "Condição Climática",
    "periodo_dia": "Período",
    "nivel_gravidade": "Gravidade",
    "total_acidentes": "Acidentes",
    "total_feridos": "Feridos",
    "total_obitos": "Óbitos",
    "total_veiculos": "Veículos",
    "taxa_letalidade_media": "Taxa Letalidade (%)"
})

st.dataframe(
    df_tabela.sort_values("Acidentes", ascending=False),
    use_container_width=True,
    height=400,
    hide_index=True
)

st.markdown("---")

# =============================================================================
# INTERPRETAÇÃO TEXTUAL (dinâmica baseada nos filtros)
# =============================================================================
st.markdown('<p class="section-header">📝 Interpretação dos Resultados</p>', unsafe_allow_html=True)

if not df_filtrado.empty:
    # Evolução temporal
    if len(df_temporal) > 1:
        primeiro_ano = df_temporal.iloc[0]
        ultimo_ano = df_temporal.iloc[-1]
        variacao = ((ultimo_ano["acidentes"] - primeiro_ano["acidentes"]) / primeiro_ano["acidentes"] * 100)
        tendencia = "aumento" if variacao > 0 else "redução"
        st.markdown(
            f'<div class="insight-card">'
            f'<strong>📈 Evolução Temporal:</strong> Entre {int(primeiro_ano["ano"])} e {int(ultimo_ano["ano"])}, '
            f'houve uma <strong>{tendencia} de {abs(variacao):.1f}%</strong> no total de acidentes. '
            f'O ano com maior registro foi <strong>{int(df_temporal.loc[df_temporal["acidentes"].idxmax(), "ano"])}</strong> '
            f'com {int(df_temporal["acidentes"].max()):,} acidentes.'
            f'</div>'.replace(",", "."),
            unsafe_allow_html=True
        )

    # Estado mais crítico
    st.markdown(
        f'<div class="insight-card">'
        f'<strong>🏛️ Estado Mais Crítico:</strong> <strong>{estado_critico}</strong> lidera o ranking estadual '
        f'com {estado_critico_valor:,} acidentes no período filtrado. '
        f'Isso representa <strong>{(estado_critico_valor / total_acidentes * 100):.1f}%</strong> do total.'
        f'</div>'.replace(",", "."),
        unsafe_allow_html=True
    )

    # Período mais perigoso
    st.markdown(
        f'<div class="insight-card">'
        f'<strong>🕐 Período Mais Perigoso:</strong> O período da <strong>{periodo_perigoso}</strong> concentra '
        f'a maior parte dos acidentes ({periodo_perigoso_valor:,}), representando '
        f'<strong>{(periodo_perigoso_valor / total_acidentes * 100):.1f}%</strong> do total filtrado.'
        f'</div>'.replace(",", "."),
        unsafe_allow_html=True
    )

    # Condição climática
    clima_top = df_filtrado.groupby("condicao_climatica")["acidentes"].sum()
    clima_mais = clima_top.idxmax()
    clima_mais_pct = (clima_top.max() / clima_top.sum() * 100)
    st.markdown(
        f'<div class="insight-card">'
        f'<strong>🌦️ Relação com Clima:</strong> A condição climática <strong>"{clima_mais}"</strong> '
        f'está associada ao maior número de acidentes, representando <strong>{clima_mais_pct:.1f}%</strong> '
        f'do total. Isso sugere que as condições de {clima_mais.lower()} podem ser um fator de risco significativo.'
        f'</div>',
        unsafe_allow_html=True
    )

    # Gravidade
    grav_critico = df_filtrado[df_filtrado["nivel_gravidade"] == "Crítico"]["acidentes"].sum()
    grav_grave = df_filtrado[df_filtrado["nivel_gravidade"] == "Grave"]["acidentes"].sum()
    pct_graves = ((grav_critico + grav_grave) / total_acidentes * 100) if total_acidentes > 0 else 0
    st.markdown(
        f'<div class="insight-card">'
        f'<strong>⚠️ Gravidade:</strong> Os acidentes classificados como <strong>Grave</strong> ou '
        f'<strong>Crítico</strong> representam <strong>{pct_graves:.1f}%</strong> do total filtrado. '
        f'A taxa média de letalidade (óbitos/acidentes) é de '
        f'<strong>{(total_obitos / total_acidentes * 100):.2f}%</strong>.'
        f'</div>',
        unsafe_allow_html=True
    )

    # Região com mais óbitos
    regiao_obitos = df_filtrado.groupby("regiao")["obitos"].sum()
    regiao_mais_obitos = regiao_obitos.idxmax()
    regiao_mais_obitos_val = int(regiao_obitos.max())
    st.markdown(
        f'<div class="insight-card">'
        f'<strong>💀 Vítimas Fatais por Região:</strong> A região <strong>{regiao_mais_obitos}</strong> '
        f'apresenta o maior número de vítimas fatais, com <strong>{regiao_mais_obitos_val:,}</strong> óbitos '
        f'no período filtrado, representando <strong>{(regiao_mais_obitos_val / total_obitos * 100):.1f}%</strong> '
        f'do total de óbitos.'
        f'</div>'.replace(",", "."),
        unsafe_allow_html=True
    )

else:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste os filtros na barra lateral.")

st.markdown("---")

# =============================================================================
# CONCLUSÃO EXECUTIVA
# =============================================================================
st.markdown('<p class="section-header">📌 Conclusão Executiva</p>', unsafe_allow_html=True)

if not df_filtrado.empty:
    # Top 3 estados
    top3_estados = df_filtrado.groupby("uf")["acidentes"].sum().nlargest(3)
    top3_str = ", ".join([f"{uf} ({val:,})" for uf, val in top3_estados.items()]).replace(",", ".")

    # Top 3 municípios
    top3_munis = df_filtrado.groupby("municipio")["acidentes"].sum().nlargest(3)
    top3_munis_str = ", ".join([f"{m} ({v:,})" for m, v in top3_munis.items()]).replace(",", ".")

    st.markdown(
        f'<div class="conclusion-card">'
        f'<strong>📌 Síntese da Análise</strong><br><br>'
        f'A análise dos dados de acidentes de trânsito no Brasil para o período filtrado revela um cenário '
        f'que demanda atenção das autoridades de segurança viária. No total, foram registrados '
        f'<strong>{total_acidentes:,}</strong> acidentes, resultando em <strong>{total_feridos:,}</strong> '
        f'feridos e <strong>{total_obitos:,}</strong> óbitos.<br><br>'
        f'Os estados mais críticos são: <strong>{top3_str}</strong>. '
        f'Os municípios com maior concentração de ocorrências são: <strong>{top3_munis_str}</strong>.<br><br>'
        f'O período da <strong>{periodo_perigoso}</strong> se destaca como o mais perigoso, '
        f'enquanto o tipo de acidente mais recorrente é <strong>{tipo_frequente}</strong>. '
        f'A condição climática <strong>{clima_mais}</strong> está associada ao maior volume de ocorrências.<br><br>'
        f'<strong>Recomendações:</strong> intensificar a fiscalização nos estados e municípios mais críticos, '
        f'implementar campanhas de conscientização focadas no período da {periodo_perigoso.lower()}, '
        f'e investir em infraestrutura viária para reduzir acidentes do tipo {tipo_frequente.lower()}.'
        f'</div>'.replace(",", "."),
        unsafe_allow_html=True
    )
else:
    st.info("Selecione filtros para visualizar a conclusão executiva.")
