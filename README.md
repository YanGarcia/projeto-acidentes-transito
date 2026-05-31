<p align="center">
  <h1 align="center">🚗 Projeto G2 — Acidentes de Trânsito no Brasil (2015-2024)</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/>
</p>

---

## 📋 Descrição

Projeto acadêmico de **análise e visualização de dados de acidentes de trânsito no Brasil**, desenvolvido como trabalho da disciplina de Linguagens de Programação. O projeto utiliza **Python**, **Pandas**, **Matplotlib**, **Seaborn** e **Streamlit** para construir um **dashboard interativo** com KPIs, filtros dinâmicos e gráficos analíticos, permitindo explorar padrões e tendências nos dados de acidentes no período de 2015 a 2024.

> 💡 O dashboard oferece uma visão completa dos dados, com indicadores-chave de desempenho (KPIs), filtros interativos por múltiplas dimensões e interpretações textuais automáticas dos resultados.

---

## 📸 Screenshots

| Tela | Descrição |
|------|-----------|
| **Dashboard Principal** | Visão geral com KPIs, gráficos de tendência temporal e distribuição por estado |
| **Filtros Interativos** | Painel lateral com filtros por ano, estado, tipo de acidente, condição climática e mais |
| **Gráficos Analíticos** | Gráficos de barras, linhas, pizza e heatmaps para análise aprofundada |
| **Tabela Dinâmica** | Tabela interativa com os dados filtrados e opção de download |
| **Conclusão Executiva** | Seção com interpretação textual e principais insights extraídos dos dados |

> 📌 *Substitua esta seção por capturas de tela reais do dashboard após a implantação.*

---

## 🔧 Tecnologias

| Tecnologia | Versão | Descrição |
|:----------:|:------:|-----------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.10+ | Linguagem principal do projeto |
| ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white) | 2.0+ | Manipulação e análise de dados |
| ![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white) | 1.24+ | Computação numérica |
| ![Matplotlib](https://img.shields.io/badge/-Matplotlib-11557C?logo=matplotlib&logoColor=white) | 3.7+ | Visualização de dados estática |
| ![Seaborn](https://img.shields.io/badge/-Seaborn-444876?logo=python&logoColor=white) | 0.12+ | Visualização estatística |
| ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit&logoColor=white) | 1.30+ | Framework para dashboard interativo |
| ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?logo=plotly&logoColor=white) | 5.18+ | Gráficos interativos |

---

## 📁 Estrutura do Projeto

```
projeto-acidentes-transito/
├── app.py                    # Dashboard Streamlit
├── requirements.txt          # Dependências do projeto
├── README.md                 # Documentação
├── index.html                # GitHub Pages
├── dados/
│   └── simulacao_acidentes_transito_brasil.csv
├── notebooks/
│   └── analise_acidentes.ipynb
├── database/
└── imagens/
```

| Arquivo / Pasta | Descrição |
|-----------------|-----------|
| `app.py` | Arquivo principal do dashboard Streamlit |
| `requirements.txt` | Lista de dependências Python |
| `index.html` | Página estática para GitHub Pages |
| `dados/` | Diretório com a base de dados CSV |
| `notebooks/` | Jupyter Notebooks com análises exploratórias |
| `database/` | Diretório para armazenamento de dados processados |
| `imagens/` | Capturas de tela e recursos visuais |

---

## 🚀 Instalação e Execução

### Pré-requisitos

- **Python 3.10+** instalado
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

### Passo a Passo

**1. Clone o repositório:**

```bash
git clone https://github.com/YanGarcia/projeto-acidentes-transito.git
```

**2. Acesse o diretório do projeto:**

```bash
cd projeto-acidentes-transito
```

**3. (Opcional) Crie e ative um ambiente virtual:**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

**4. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**5. Execute o dashboard:**

```bash
streamlit run app.py
```

> ✅ O dashboard será aberto automaticamente no navegador em `http://localhost:8501`

---

## ✨ Funcionalidades

### 📊 KPIs (Indicadores-Chave)

| # | KPI | Descrição |
|:-:|-----|-----------|
| 1 | **Total de Acidentes** | Número total de acidentes no período selecionado |
| 2 | **Total de Vítimas Fatais** | Contagem de óbitos registrados |
| 3 | **Total de Feridos** | Número total de pessoas feridas |
| 4 | **Média de Acidentes/Ano** | Média anual de ocorrências |
| 5 | **Estado com Mais Acidentes** | Unidade federativa com maior incidência |
| 6 | **Tipo Mais Frequente** | Categoria de acidente mais recorrente |

### 🎛️ Filtros Interativos

| # | Filtro | Tipo |
|:-:|--------|------|
| 1 | **Ano** | Seleção múltipla |
| 2 | **Mês** | Seleção múltipla |
| 3 | **Região** | Seleção múltipla |
| 4 | **Estado (UF)** | Seleção múltipla |
| 5 | **Tipo de Acidente** | Seleção múltipla |
| 6 | **Período do Dia** | Seleção múltipla |
| 7 | **Nível de Gravidade** | Seleção múltipla |


### 📈 Gráficos e Visualizações

- 📉 **Evolução Temporal** — Acidentes por ano (gráfico de linhas)
- 📊 **Distribuição por Estado** — Top estados com mais acidentes (gráfico de barras)
- 🍕 **Tipo de Acidente** — Proporção por categoria (gráfico de pizza)
- 🌡️ **Heatmap** — Correlação entre variáveis numéricas
- 🕐 **Acidentes por Turno** — Distribuição por período do dia
- 🌧️ **Condição Climática** — Impacto do clima nos acidentes

### 📋 Recursos Adicionais

- 📄 **Tabela Dinâmica** — Visualização e download dos dados filtrados
- 💬 **Interpretação Textual** — Análise automática dos padrões identificados
- 📝 **Conclusão Executiva** — Resumo dos principais insights e recomendações

---

## 🗄️ Base de Dados

| Característica | Detalhe |
|----------------|---------|
| **Registros** | 8.880 |
| **Colunas** | 15 |
| **Período** | 2015 – 2024 |
| **Tipo** | Dados simulados |
| **Formato** | CSV |

### Colunas da Base de Dados

| # | Coluna | Tipo | Descrição |
|:-:|--------|------|-----------|
| 1 | `ano` | int | Ano do acidente |
| 2 | `mes` | int | Mês do acidente |
| 3 | `data` | date | Data da ocorrência |
| 4 | `regiao` | str | Região do Brasil |
| 5 | `uf` | str | Estado (Unidade Federativa) |
| 6 | `municipio` | str | Município da ocorrência |
| 7 | `rodovia` | str | Rodovia ou via |
| 8 | `tipo_acidente` | str | Tipo do acidente |
| 9 | `condicao_climatica` | str | Clima no momento |
| 10 | `periodo_dia` | str | Manhã, tarde, noite ou madrugada |
| 11 | `acidentes` | int | Quantidade de acidentes |
| 12 | `feridos` | int | Quantidade de feridos |
| 13 | `obitos` | int | Quantidade de óbitos |
| 14 | `veiculos_envolvidos` | int | Quantidade de veículos |
| 15 | `nivel_gravidade` | str | Baixo, Médio, Alto, Crítico / Leve, Moderado, Grave, Crítico |

> ⚠️ **Nota:** Os dados são **simulados** para fins acadêmicos e não representam estatísticas oficiais.

---

## 🌐 Deploy

### 📄 GitHub Pages

1. Acesse as **Settings** do repositório no GitHub
2. Navegue até **Pages** no menu lateral
3. Em **Source**, selecione a branch `main`
4. Em **Folder**, selecione `/ (root)`
5. Clique em **Save**
6. Aguarde alguns minutos e acesse a URL gerada

> O arquivo `index.html` na raiz do projeto será exibido como página inicial.

### ☁️ Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta **GitHub**
3. Clique em **"New app"**
4. Conecte ao seu **repositório GitHub**
5. Selecione `app.py` como **arquivo principal**
6. Clique em **"Deploy!"**

> O deploy é automático e a aplicação será atualizada a cada push na branch principal.

---

## 🔗 Links

| Recurso | URL |
|---------|-----|
| 🌐 **GitHub Pages** | `https://YanGarcia.github.io/projeto-acidentes-transito/` |
| 🚀 **Streamlit Cloud** | `https://YanGarcia-projeto-acidentes-transito.streamlit.app/` |
| 📦 **Repositório** | `https://github.com/YanGarcia/projeto-acidentes-transito` |

> 📌 *Substitua `YanGarcia` pelo seu nome de usuário do GitHub.*

---

## 📜 Licença

Este projeto está licenciado sob a **Licença MIT** — consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2024-2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Autor

| | |
|---|---|
| **Nome** | *Seu Nome Completo* |
| **Curso** | Linguagens de Programação |
| **Instituição** | *Nome da Instituição* |
| **Contato** | *seu.email@exemplo.com* |
| **GitHub** | [@YanGarcia](https://github.com/YanGarcia) |

---

<p align="center">
  Feito com ❤️ para a disciplina de Linguagens de Programação
</p>

<p align="center">
  <a href="#-projeto-g2--acidentes-de-trânsito-no-brasil-2015-2024">⬆️ Voltar ao topo</a>
</p>
