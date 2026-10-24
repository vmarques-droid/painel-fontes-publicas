# ============================================================================
# coletor.py : baixa planilhas de fontes publicas e gera os dados do painel
# Versao em miniatura do sistema Ecoa (Internacionaliza UFG), em 3 passos:
#   PASSO 1, BAIXAR:    cada fonte publica vira uma tabela (DataFrame)
#   PASSO 2, ORGANIZAR: cruzamos as series por mes e resumimos por ano
#   PASSO 3, SALVAR:    gravamos dados/consolidado.json e dados/dados.js
#
# Para trocar de fonte: edite a lista FONTES e ajuste o PASSO 2 (ORGANIZAR).
# ============================================================================
import io
import json
import os
from datetime import datetime

import pandas as pd
import requests

# Cada fonte e um dicionario de configuracao: endereco, formato e dicas de
# leitura (sep, decimal, encoding). Troque pelas fontes do seu projeto!
FONTES = [
    {
        "apelido": "ipca",
        "nome": "IPCA, variação mensal em % (Banco Central, série SGS 433)",
        "url": ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
                "?formato=csv&dataInicial=01/01/2015&dataFinal=30/09/2026"),
        "formato": "csv", "sep": ";", "decimal": ",", "encoding": "utf-8",
    },
    {
        "apelido": "selic",
        "nome": "Selic acumulada no mês em % (Banco Central, série SGS 4390)",
        "url": ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados"
                "?formato=csv&dataInicial=01/01/2015&dataFinal=30/09/2026"),
        "formato": "csv", "sep": ";", "decimal": ",", "encoding": "utf-8",
    },
]

PASTA = os.path.dirname(os.path.abspath(__file__))  # pasta deste script

def baixar(url):
    # Download com identificacao (portais publicos recusam robos anonimos),
    # timeout (rede lenta nao congela a aula) e ate 3 tentativas.
    cabecalhos = {"User-Agent": "Mozilla/5.0 (painel-aula-ufg)"}
    for tentativa in (1, 2, 3):
        try:
            resposta = requests.get(url, headers=cabecalhos, timeout=60)
            resposta.raise_for_status()  # para tudo se o site respondeu erro
            print(f"   ok: {len(resposta.content) / 1024:.0f} KB recebidos")
            return io.BytesIO(resposta.content)
        except requests.exceptions.RequestException:
            if tentativa == 3:
                raise  # 3 falhas seguidas: desiste e mostra o erro
            print(f"   tentativa {tentativa} falhou, tentando de novo...")

def acumular(variacoes):
    # Compoe variacoes mensais em % num acumulado (juros sobre juros).
    fator = (1 + variacoes / 100).prod()
    return round(float((fator - 1) * 100), 2)

# ============================= PASSO 1: BAIXAR ==============================
print("PASSO 1: baixando as fontes publicas...")
tabelas = {}
for fonte in FONTES:
    print(f" - {fonte['apelido']} ({fonte['formato']})")
    conteudo = baixar(fonte["url"])
    if fonte["formato"] == "csv":
        tabelas[fonte["apelido"]] = pd.read_csv(
            conteudo, sep=fonte["sep"], decimal=fonte["decimal"],
            encoding=fonte["encoding"])
    elif fonte["formato"] == "xlsx":  # ja pronto para o desafio com Excel
        tabelas[fonte["apelido"]] = pd.read_excel(
            conteudo, sheet_name=fonte["aba"])
    print(f"   {len(tabelas[fonte['apelido']])} linhas na tabela")

# =========================== PASSO 2: ORGANIZAR =============================
print("PASSO 2: organizando e cruzando as tabelas...")

# As duas fontes chegam no mesmo formato (data; valor). Renomeamos a coluna
# valor de cada uma e cruzamos as tabelas pela data: este merge por mes
# e o coracao da consolidacao.
ipca = tabelas["ipca"].rename(columns={"valor": "ipca"})
selic = tabelas["selic"].rename(columns={"valor": "selic"})
mensal = pd.merge(ipca, selic, on="data")  # fica so o mes presente nas duas
mensal["quando"] = pd.to_datetime(mensal["data"], format="%d/%m/%Y")
mensal = mensal.sort_values("quando")

recorte = mensal.tail(24)  # o grafico de linhas mostra os ultimos 24 meses
rotulos_meses = recorte["quando"].dt.strftime("%m/%Y").tolist()
valores_ipca = [round(float(v), 2) for v in recorte["ipca"]]
valores_selic = [round(float(v), 2) for v in recorte["selic"]]
ultimo_mes = rotulos_meses[-1]

ipca_12m = acumular(mensal["ipca"].tail(12))  # KPI: inflacao de 12 meses

# Resumo por categoria: o IPCA acumulado dentro de cada ano.
mensal["ano"] = mensal["quando"].dt.year
por_ano = mensal.groupby("ano")["ipca"].apply(acumular)

print(f" - series cruzadas: {len(mensal)} meses, ultimo mes {ultimo_mes}")
print(f" - acumulado por ano: {len(por_ano)} anos")

# ============================= PASSO 3: SALVAR ==============================
print("PASSO 3: salvando a pasta dados/ ...")
consolidado = {
    "geradoEm": datetime.now().isoformat(timespec="seconds"),
    "kpis": [  # cartoes do painel: valor sempre como numero, nunca texto
        {"rotulo": "IPCA acumulado em 12 meses", "valor": ipca_12m,
         "detalhe": f"variação de preços em %, até {ultimo_mes}"},
        {"rotulo": "Selic no último mês", "valor": valores_selic[-1],
         "detalhe": f"juros em % ao mês, em {ultimo_mes}"},
        {"rotulo": "Meses consolidados", "valor": int(len(mensal)),
         "detalhe": "presentes nas duas fontes desde 01/2015"},
    ],
    "series": {
        "rotulos": rotulos_meses,
        "conjuntos": [
            {"nome": "IPCA (% ao mês)", "valores": valores_ipca},
            {"nome": "Selic (% ao mês)", "valores": valores_selic},
        ],
    },
    "categorias": {
        "titulo": f"IPCA acumulado por ano, em % (último ano até {ultimo_mes})",
        "rotulos": [str(ano) for ano in por_ano.index],
        "valores": [float(v) for v in por_ano],  # numero do Python, nao do pandas
    },
    "fontes": [{"nome": fonte["nome"], "url": fonte["url"]} for fonte in FONTES],
}

pasta_dados = os.path.join(PASTA, "dados")
os.makedirs(pasta_dados, exist_ok=True)

# consolidado.json guarda os dados puros; dados.js e o MESMO objeto numa
# atribuicao, para o index.html abrir com clique duplo (sem erro de CORS).
with open(os.path.join(pasta_dados, "consolidado.json"), "w", encoding="utf-8") as arq:
    json.dump(consolidado, arq, ensure_ascii=False, indent=2)
with open(os.path.join(pasta_dados, "dados.js"), "w", encoding="utf-8") as arq:
    arq.write("window.DADOS = ")
    json.dump(consolidado, arq, ensure_ascii=False, indent=2)
    arq.write(";\n")

print("Pronto! Abra o index.html com dois cliques para ver o painel.")
