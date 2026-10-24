window.DADOS = {
  "geradoEm": "2026-10-23T23:31:04",
  "kpis": [
    {
      "rotulo": "IPCA acumulado em 12 meses",
      "valor": 4.58,
      "detalhe": "variação de preços em %, até 09/2026"
    },
    {
      "rotulo": "Selic no último mês",
      "valor": 1.08,
      "detalhe": "juros em % ao mês, em 09/2026"
    },
    {
      "rotulo": "Meses consolidados",
      "valor": 141,
      "detalhe": "presentes nas duas fontes desde 01/2015"
    }
  ],
  "series": {
    "rotulos": [
      "10/2024",
      "11/2024",
      "12/2024",
      "01/2025",
      "02/2025",
      "03/2025",
      "04/2025",
      "05/2025",
      "06/2025",
      "07/2025",
      "08/2025",
      "09/2025",
      "10/2025",
      "11/2025",
      "12/2025",
      "01/2026",
      "02/2026",
      "03/2026",
      "04/2026",
      "05/2026",
      "06/2026",
      "07/2026",
      "08/2026",
      "09/2026"
    ],
    "conjuntos": [
      {
        "nome": "IPCA (% ao mês)",
        "valores": [
          0.56,
          0.39,
          0.52,
          0.16,
          1.31,
          0.56,
          0.43,
          0.26,
          0.24,
          0.26,
          -0.11,
          0.48,
          0.09,
          0.18,
          0.33,
          0.33,
          0.7,
          0.88,
          0.67,
          0.58,
          0.16,
          0.07,
          -0.32,
          0.82
        ]
      },
      {
        "nome": "Selic (% ao mês)",
        "valores": [
          0.93,
          0.79,
          0.93,
          1.01,
          0.99,
          0.96,
          1.06,
          1.14,
          1.1,
          1.28,
          1.16,
          1.22,
          1.28,
          1.05,
          1.22,
          1.16,
          1.0,
          1.21,
          1.09,
          1.07,
          1.12,
          1.22,
          1.09,
          1.08
        ]
      }
    ]
  },
  "categorias": {
    "titulo": "IPCA acumulado por ano, em % (último ano até 09/2026)",
    "rotulos": [
      "2015",
      "2016",
      "2017",
      "2018",
      "2019",
      "2020",
      "2021",
      "2022",
      "2023",
      "2024",
      "2025",
      "2026"
    ],
    "valores": [
      10.67,
      6.29,
      2.95,
      3.75,
      4.31,
      4.52,
      10.06,
      5.78,
      4.62,
      4.83,
      4.26,
      3.95
    ]
  },
  "fontes": [
    {
      "nome": "IPCA, variação mensal em % (Banco Central, série SGS 433)",
      "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv&dataInicial=01/01/2015&dataFinal=30/09/2026"
    },
    {
      "nome": "Selic acumulada no mês em % (Banco Central, série SGS 4390)",
      "url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=csv&dataInicial=01/01/2015&dataFinal=30/09/2026"
    }
  ]
};
