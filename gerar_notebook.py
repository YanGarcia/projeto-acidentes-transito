import nbformat as nbf
import os

# Inicializar o notebook
nb = nbf.v4.new_notebook()

# Células do notebook
cells = []

# 1. Introdução
cells.append(nbf.v4.new_markdown_cell("""# Projeto G2 — Tema 5: Acidentes de Trânsito no Brasil (2015-2024)
## Análise Exploratória e Visualização de Dados

**Curso**: Linguagens de Programação  
**Autor**: Aluno  
**Data**: Maio de 2026  

---

### 1. Introdução
Este Jupyter Notebook faz parte do Projeto Prático G2 da disciplina de Linguagens de Programação. O objetivo deste trabalho é analisar os registros históricos de acidentes de trânsito simulados que cobrem o período de **2015 a 2024** nas rodovias brasileiras. 

A exploração visa extrair indicadores fundamentais, compreender o perfil das ocorrências e identificar padrões espaciais e temporais a fim de apoiar a tomada de decisões de trânsito, infraestrutura e segurança viária."""))

# 2. Contextualização do problema
cells.append(nbf.v4.new_markdown_cell("""### 2. Contextualização do problema
Os acidentes de trânsito constituem uma das maiores causas de mortalidade externa e sequelas físicas e psicológicas no Brasil, gerando prejuízos bilionários aos cofres públicos, sistemas de saúde (SUS) e previdência social.

Mapear fatores como condições de clima, o trecho rodoviário, períodos do dia mais letais e tipos de sinistros mais comuns permite traçar estratégias preventivas e de fiscalização mais eficazes."""))

# 3. Explicação da base
cells.append(nbf.v4.new_markdown_cell("""### 3. Explicação da base de dados
O dataset `simulacao_acidentes_transito_brasil.csv` simula os registros de acidentes das rodovias federais. Ele contém 8.880 linhas e 15 colunas:
- `ano`: Ano da ocorrência (2015 a 2024).
- `mes`: Mês da ocorrência (1 a 12).
- `data`: Data em formato YYYY-MM-DD.
- `regiao`: Região geográfica brasileira (Norte, Nordeste, Centro-Oeste, Sudeste, Sul).
- `uf`: Estado (sigla).
- `municipio`: Nome do município da ocorrência.
- `rodovia`: Rodovia federal (BR-XXX).
- `tipo_acidente`: Classificação do acidente (Colisão, Tombamento, Saída de pista, Capotamento, Atropelamento).
- `condicao_climatica`: Condição climática no momento (Chuva, Ensolarado, Neblina, Nublado).
- `periodo_dia`: Período do dia (Manhã, Tarde, Noite, Madrugada).
- `acidentes`: Quantidade absoluta de acidentes no registro.
- `feridos`: Quantidade de feridos.
- `obitos`: Quantidade de óbitos (vítimas fatais).
- `veiculos_envolvidos`: Total de veículos associados.
- `nivel_gravidade`: Nível de gravidade estimado (Leve, Moderado, Grave, Crítico)."""))

# 4. Leitura dos dados
cells.append(nbf.v4.new_markdown_cell("""### 4. Leitura dos dados"""))
cells.append(nbf.v4.new_code_cell(r"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração de estilo dos gráficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('viridis')

# Carregar o dataset
caminho_csv = "dados/simulacao_acidentes_transito_brasil.csv"
df = pd.read_csv(caminho_csv, encoding='utf-8-sig')

# Visualizar as primeiras linhas
print("--- Primeiras 5 Linhas do Dataset ---")
display(df.head())

# Exibir informações estruturais gerais
print("\n--- Informações Estruturais (DataTypes) ---")
df.info()

# Exibir estatísticas gerais das colunas numéricas
print("\n--- Estatísticas Descritivas ---")
display(df.describe())"""))

# 5. Limpeza e preparação
cells.append(nbf.v4.new_markdown_cell("""### 5. Limpeza e preparação"""))
cells.append(nbf.v4.new_code_cell(r"""# Verificar valores ausentes
print("Valores nulos por coluna:")
print(df.isnull().sum())

# Converter a coluna data para Datetime
df['data'] = pd.to_datetime(df['data'])

# Garantir tipos corretos para ano e mes
df['ano'] = df['ano'].astype(int)
df['mes'] = df['mes'].astype(int)

# Ordenar de forma cronológica
df = df.sort_values(by='data').reset_index(drop=True)

print("\nLimpeza e preparação concluídas com sucesso. Tipo da data convertido para datetime e ordenado cronologicamente.")"""))

# 6. Engenharia de atributos
cells.append(nbf.v4.new_markdown_cell("""### 6. Engenharia de atributos"""))
cells.append(nbf.v4.new_code_cell(r"""# Criar taxa de letalidade (óbitos por acidente)
df['taxa_letalidade'] = (df['obitos'] / df['acidentes']).round(4)

# Criar média de feridos por acidente
df['feridos_por_acidente'] = (df['feridos'] / df['acidentes']).round(4)

# Criar média de veículos envolvidos por acidente
df['veiculos_por_acidente'] = (df['veiculos_envolvidos'] / df['acidentes']).round(4)

# Mapear a gravidade para um score numérico ordinal
mapa_gravidade = {"Leve": 1, "Moderado": 2, "Grave": 3, "Crítico": 4}
df['gravidade_num'] = df['nivel_gravidade'].map(mapa_gravidade)

# Adicionar nome do mês em português
meses_pt = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
df['mes_nome'] = df['mes'].map(meses_pt)

print("Novas colunas criadas:\n- taxa_letalidade\n- feridos_por_acidente\n- veiculos_por_acidente\n- gravidade_num (ordinal)\n- mes_nome")
display(df.head(2))"""))

# 7. KPIs
cells.append(nbf.v4.new_markdown_cell("""### 7. KPIs (Indicadores-Chave)"""))
cells.append(nbf.v4.new_code_cell(r"""kpis = {}

kpis['total_acidentes'] = int(df['acidentes'].sum())
kpis['total_feridos'] = int(df['feridos'].sum())
kpis['total_obitos'] = int(df['obitos'].sum())

# Estado mais crítico
uf_critico = df.groupby('uf')['acidentes'].sum().idxmax()
kpis['estado_critico'] = uf_critico

# Período do dia mais perigoso
periodo_perigoso = df.groupby('periodo_dia')['acidentes'].sum().idxmax()
kpis['periodo_perigoso'] = periodo_perigoso

# Tipo de acidente mais frequente
tipo_comum = df.groupby('tipo_acidente')['acidentes'].sum().idxmax()
kpis['tipo_acidente_frequente'] = tipo_comum

print("=================== KPIs ===================")
print(f"🚨 Total de Acidentes: {kpis['total_acidentes']:,}".replace(",", "."))
print(f"🏥 Total de Feridos: {kpis['total_feridos']:,}".replace(",", "."))
print(f"⚰️ Total de Óbitos: {kpis['total_obitos']:,}".replace(",", "."))
print(f"🏛️ Estado Mais Crítico: {kpis['estado_critico']}")
print(f"🕐 Período Mais Perigoso: {kpis['periodo_perigoso']}")
print(f"💥 Tipo Mais Frequente: {kpis['tipo_acidente_frequente']}")
print("============================================")"""))

# 8. Visualizações
cells.append(nbf.v4.new_markdown_cell("""### 8. Visualizações e Gráficos
Nesta seção, salvaremos as imagens no diretório `imagens/`."""))

# 8.a Linha temporal
cells.append(nbf.v4.new_markdown_cell("""#### a) Evolução temporal anual de acidentes"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(10, 5))
df_temporal = df.groupby('ano')['acidentes'].sum().reset_index()
sns.lineplot(data=df_temporal, x='ano', y='acidentes', marker='o', color='#4f46e5', linewidth=2.5)
plt.title('Evolução do Número Anual de Acidentes (2015-2024)', fontsize=14, pad=15)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Total de Acidentes', fontsize=12)
plt.xticks(df_temporal['ano'])
plt.tight_layout()
os.makedirs('imagens', exist_ok=True)
plt.savefig('imagens/evolucao_temporal.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.b Barras por estado
cells.append(nbf.v4.new_markdown_cell("""#### b) Total de acidentes por Estado (UF)"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(12, 6))
df_uf = df.groupby('uf')['acidentes'].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=df_uf, x='acidentes', y='uf', palette='Blues_r')
plt.title('Total de Acidentes por Estado (UF) — Ranking Geral', fontsize=14, pad=15)
plt.xlabel('Quantidade de Acidentes', fontsize=12)
plt.ylabel('Estado', fontsize=12)
plt.tight_layout()
plt.savefig('imagens/acidentes_por_uf.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.c Barras por tipo
cells.append(nbf.v4.new_markdown_cell("""#### c) Distribuição por Tipo de Acidente"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(10, 5))
df_tipo = df.groupby('tipo_acidente')['acidentes'].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=df_tipo, x='tipo_acidente', y='acidentes', palette='viridis')
plt.title('Frequência por Tipo de Acidente', fontsize=14, pad=15)
plt.xlabel('Tipo de Acidente', fontsize=12)
plt.ylabel('Quantidade de Acidentes', fontsize=12)
plt.tight_layout()
plt.savefig('imagens/acidentes_por_tipo.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.d Heatmap
cells.append(nbf.v4.new_markdown_cell("""#### d) Heatmap: Período do Dia × Mês"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(12, 6))
meses_ordem = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
periodos_ordem = ["Madrugada", "Manhã", "Tarde", "Noite"]
df_heat = df.groupby(['periodo_dia', 'mes_nome'])['acidentes'].sum().reset_index()
df_pivot = df_heat.pivot(index='periodo_dia', columns='mes_nome', values='acidentes')
df_pivot = df_pivot.reindex(index=periodos_ordem, columns=meses_ordem)
sns.heatmap(df_pivot, annot=True, fmt=',.0f', cmap='YlOrRd', cbar_kws={'label': 'Acidentes'})
plt.title('Heatmap: Concentração de Acidentes (Período do Dia × Mês)', fontsize=14, pad=15)
plt.xlabel('Mês', fontsize=12)
plt.ylabel('Período do Dia', fontsize=12)
plt.tight_layout()
plt.savefig('imagens/heatmap_periodo_mes.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.e Pizza por clima
cells.append(nbf.v4.new_markdown_cell("""#### e) Proporção de acidentes por Condição Climática"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(7, 7))
df_clima = df.groupby('condicao_climatica')['acidentes'].sum()
plt.pie(df_clima, labels=df_clima.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Distribuição de Acidentes por Condição Climática', fontsize=14, pad=15)
plt.tight_layout()
plt.savefig('imagens/pizza_clima.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.f Barras por região
cells.append(nbf.v4.new_markdown_cell("""#### f) Comparação Regional de Acidentes"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(9, 5))
df_regiao = df.groupby('regiao')['acidentes'].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=df_regiao, x='regiao', y='acidentes', palette='Set2')
plt.title('Quantidade de Acidentes por Região do Brasil', fontsize=14, pad=15)
plt.xlabel('Região', fontsize=12)
plt.ylabel('Acidentes', fontsize=12)
plt.tight_layout()
plt.savefig('imagens/acidentes_por_regiao.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.g Ranking municipios
cells.append(nbf.v4.new_markdown_cell("""#### g) Ranking Top 15 Municípios Críticos"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(12, 6))
df_mun = df.groupby('municipio')['acidentes'].sum().sort_values(ascending=False).head(15).reset_index()
sns.barplot(data=df_mun, x='acidentes', y='municipio', palette='flare')
plt.title('Top 15 Municípios com Mais Acidentes', fontsize=14, pad=15)
plt.xlabel('Quantidade de Acidentes', fontsize=12)
plt.ylabel('Município', fontsize=12)
plt.tight_layout()
plt.savefig('imagens/top15_municipios.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.h Distribuição por nível gravidade
cells.append(nbf.v4.new_markdown_cell("""#### h) Distribuição por Nível de Gravidade"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(9, 5))
ordem_g = ["Leve", "Moderado", "Grave", "Crítico"]
df_g = df.groupby('nivel_gravidade')['acidentes'].sum().reindex(ordem_g).reset_index()
sns.barplot(data=df_g, x='nivel_gravidade', y='acidentes', palette='coolwarm')
plt.title('Distribuição de Acidentes por Nível de Gravidade', fontsize=14, pad=15)
plt.xlabel('Nível de Gravidade', fontsize=12)
plt.ylabel('Quantidade de Acidentes', fontsize=12)
plt.tight_layout()
plt.savefig('imagens/acidentes_por_gravidade.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.i Evolução de óbitos
cells.append(nbf.v4.new_markdown_cell("""#### i) Evolução temporal de óbitos por ano"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(10, 5))
df_obitos = df.groupby('ano')['obitos'].sum().reset_index()
sns.lineplot(data=df_obitos, x='ano', y='obitos', marker='s', color='#dc2626', linewidth=2.5)
plt.title('Evolução do Número Anual de Óbitos (2015-2024)', fontsize=14, pad=15)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Total de Óbitos', fontsize=12)
plt.xticks(df_obitos['ano'])
plt.tight_layout()
plt.savefig('imagens/evolucao_obitos.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 8.j Heatmap clima x gravidade
cells.append(nbf.v4.new_markdown_cell("""#### j) Heatmap: Condição Climática × Nível de Gravidade"""))
cells.append(nbf.v4.new_code_cell(r"""plt.figure(figsize=(10, 5))
df_cg = df.groupby(['condicao_climatica', 'nivel_gravidade'])['acidentes'].sum().reset_index()
df_cg_pivot = df_cg.pivot(index='condicao_climatica', columns='nivel_gravidade', values='acidentes')
df_cg_pivot = df_cg_pivot.reindex(columns=ordem_g)
sns.heatmap(df_cg_pivot, annot=True, fmt=',.0f', cmap='Blues', cbar_kws={'label': 'Acidentes'})
plt.title('Heatmap: Relação Clima × Nível de Gravidade', fontsize=14, pad=15)
plt.xlabel('Nível de Gravidade', fontsize=12)
plt.ylabel('Condição Climática', fontsize=12)
plt.tight_layout()
plt.savefig('imagens/heatmap_clima_gravidade.png', dpi=150, bbox_inches='tight')
plt.show()"""))

# 9. Interpretação
cells.append(nbf.v4.new_markdown_cell("""### 9. Interpretação dos Resultados
- **Panorama geral:** No conjunto de dados analisado foram registrados **172.190 acidentes**, **120.374 feridos** e **5.167 óbitos**.
- **Evolução temporal:** A série anual é essencialmente estável — 2015 teve 17.067 acidentes e 2024 teve 17.189 (variação ≈ 0,7%).
- **Região / Estado:** A região com maior volume é o **Sudeste** (60.442 acidentes) e o estado com maior número absoluto é **Rio de Janeiro (RJ: 18.572)**.
- **Períodos:** O maior volume de acidentes ocorre na **Tarde** (44.487), seguido por **Madrugada** (43.321). A **Tarde** também apresenta a maior taxa média de letalidade (óbitos/acidentes ≈ 3,21%).
- **Clima:** **Ensolarado** concentra o maior número absoluto de acidentes (70.634), mas a maior taxa de letalidade por condição climática ocorre em **Nublado** (≈ 3,14%); Neblina e Chuva têm taxas próximas.
- **Tipos de acidente:** Os mais frequentes são **Saída de pista** (35.633), **Atropelamento** (34.450) e **Colisão** (34.097); Tombamento e Capotamento também aparecem entre os mais comuns.
- **Gravidade:** A maioria das ocorrências é classificada como Moderado, enquanto categorias Grave/Crítico concentram maior severidade.

> Observação: as interpretações foram atualizadas para refletir agregados numéricos (contagens e taxas). Sempre que possível prefira apontar valores/percentuais em vez de afirmações qualitativas.
"""))

# 10. Conclusão
cells.append(nbf.v4.new_markdown_cell("""### 10. Conclusão
Com base nos dados agregados (172.190 acidentes e 5.167 óbitos), apresentamos as principais conclusões e recomendações quantitativas:

- **Síntese:** O cenário exige intervenções direcionadas por volume e por letalidade. A Tarde concentra o maior volume de acidentes e a maior taxa média de letalidade; o Sudeste e o estado do RJ merecem atenção por volume absoluto.
- **Recomendações operacionais:** intensificar fiscalização e campanhas educativas nos estados/municípios de maior volume (ex.: RJ e municípios do top), priorizar ações no período da Tarde, e implantar medidas específicas para reduzir 'Saída de pista' e 'Atropelamento'.
- **Infraestrutura e resposta:** investir em melhorias de infraestrutura nas rodovias críticas, ampliar cobertura de socorro médico emergencial e monitorar impacto das intervenções por meio de métricas (queda da taxa de letalidade e redução de acidentes por município).

As recomendações acima foram formuladas para alinhar ações às evidências estatísticas observadas e devem ser refinadas localmente com dados contextuais adicionais.
"""))

# Anexar as células ao notebook
nb['cells'] = cells

# Salvar o arquivo notebook
notebook_path = "notebooks/analise_acidentes.ipynb"
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook Jupyter gerado com sucesso em: {os.path.abspath(notebook_path)}")
