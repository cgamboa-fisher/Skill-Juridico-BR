---
name: direito-societario-br
description: >
  Análise, elaboração e revisão de contratos e documentos jurídicos sob a legislação societária
  e empresarial brasileira. Cobre contratos societários (acordo de acionistas, contrato social,
  estatuto social), operações de M&A (SPA, SHA, term sheets, due diligence), venture capital e
  startups (SAFE, mútuo conversível, vesting, stock options/ILP), direito empresarial (joint ventures,
  memorandos de entendimento, LOIs), e compliance corporativo (LGPD, Lei Anticorrupção, governança).
  Use este skill sempre que o usuário mencionar direito societário brasileiro, contratos empresariais,
  Código Civil brasileiro, Lei das S.A. (6.404/76), Lei de Liberdade Econômica (13.874/19),
  Marco Legal das Startups (LC 182/21), LGPD (13.709/18), Lei Anticorrupção (12.846/13),
  Lei de Recuperação Judicial (11.101/05), Código Comercial, CVM, CADE, acordo de acionistas,
  contrato social, estatuto, holding, EIRELI/SLU, LTDA, S.A., ou qualquer documento jurídico
  comercial no contexto brasileiro. Também acione quando o usuário pedir revisão de cláusulas
  com referências a legislação brasileira, análise de term sheets de investimento no Brasil,
  ou due diligence em operações brasileiras. Para questões de Direito de Família (divórcio,
  partilha, pensão alimentícia, guarda), instale o skill irmão `direito-familia-br`.
---

# Direito Societário e Empresarial Brasileiro

Skill especializado em análise, elaboração e revisão de documentos jurídicos no âmbito do
direito societário e empresarial brasileiro. Fornece análise clause-by-clause, identifica
riscos, sugere redlines e gera documentos seguindo a legislação e a prática de mercado do Brasil.

## Skill Companheiro

Para questões de **Direito de Família** (divórcio, partilha de bens — incluindo
participações societárias —, pensão alimentícia, guarda dos filhos, regimes de bens,
pacto antenupcial), o skill independente `direito-familia-br` cobre essa área. Os dois
skills são complementares e podem ser instalados juntos. Para casos onde divórcio envolve
quotas/ações de empresas, ambos podem ser acionados em conjunto.

## Quando Ativar

Ativar quando o usuário:
- Solicitar elaboração ou revisão de contratos societários ou empresariais brasileiros
- Mencionar legislação brasileira (CC, Lei 6.404/76, LGPD, etc.)
- Pedir análise de term sheets, acordos de acionistas, ou operações de M&A no Brasil
- Referir-se a tipos societários brasileiros (LTDA, S.A., SLU, SCP, SPE)
- Solicitar due diligence ou compliance em contexto brasileiro
- Pedir minutas de contrato social, estatuto, ata de assembleia, ou memorando

**Não ativar para** (usar `direito-familia-br`):
- Divórcio, partilha de bens, pensão alimentícia, guarda dos filhos
- Regimes de bens entre cônjuges
- Pacto antenupcial ou contrato de convivência
- Holdings familiares quando o foco for sucessório/familiar (não societário-puro)

## Legislação de Referência

Toda análise deve fundamentar-se na legislação vigente. As principais fontes são:

| Legislação | Escopo |
|---|---|
| Código Civil (Lei 10.406/02) — Livro II, Direito de Empresa | Sociedades simples e empresárias, contratos em geral |
| Lei das S.A. (Lei 6.404/76) | Sociedades por ações, governança, direitos de acionistas |
| Lei de Liberdade Econômica (Lei 13.874/19) | Simplificação, desconsideração da PJ, sociedade unipessoal |
| Marco Legal das Startups (LC 182/21) | Investidor-anjo, sandbox regulatório, insumos de inovação |
| LGPD (Lei 13.709/18) | Proteção de dados em cláusulas contratuais |
| Lei Anticorrupção (Lei 12.846/13) | Compliance, responsabilidade objetiva de PJ |
| Lei de Recuperação Judicial (Lei 11.101/05) | Recuperação, falência, créditos |
| Lei de Propriedade Industrial (Lei 9.279/96) | PI em contratos de tecnologia e licenciamento |
| Lei do CADE (Lei 12.529/11) | Concorrência, atos de concentração |
| Regulação CVM | Ofertas públicas, fundos, valores mobiliários |
| CLT e legislação trabalhista | Cláusulas de não-competição, ILP, vesting |
| Lei de Franquias (Lei 13.966/19) | Contratos de franquia, COF |

Para detalhamento de cada área, consultar os arquivos em `references/`.

## Interação com o Usuário — ask_user_input

Este skill depende de contexto preciso para gerar análises e documentos corretos. Sempre que
informações essenciais estiverem faltando, usar a ferramenta `ask_user_input` para coletar
dados estruturados antes de prosseguir. Não adivinhar ou assumir — perguntar.

Princípios:
- Usar `ask_user_input` com opções tappable (single_select, multi_select) para facilitar resposta rápida
- Limitar a 1-3 perguntas por chamada, com 2-4 opções curtas e mutuamente exclusivas
- Se o usuário já forneceu a informação na conversa ou em arquivo anexo, não perguntar de novo
- Após receber respostas, prosseguir imediatamente com a tarefa — não fazer perguntas desnecessárias

## Fluxo de Trabalho

### 1. Identificação do Contexto

Antes de analisar ou redigir, é necessário ter clareza sobre 5 dimensões. Se o usuário não
fornecer todas elas na mensagem inicial, usar `ask_user_input` para coletar as faltantes.

**Dimensões obrigatórias:**
- **Tipo de documento**: contrato social, estatuto, SHA, SPA, term sheet, ata, procuração, etc.
- **Tipo societário**: LTDA, S.A. (aberta/fechada), SLU, SCP, SPE, consórcio
- **Posição do cliente**: sócio majoritário, minoritário, investidor, target, comprador, vendedor
- **Fase da operação**: constituição, rodada de investimento, M&A, reestruturação, dissolução
- **Porte e contexto**: startup early-stage, PME, empresa familiar, grupo econômico, multinacional

**Exemplo de coleta via ask_user_input:**

Quando o usuário pedir uma minuta de contrato ou análise sem contexto suficiente, usar:

```
ask_user_input({
  questions: [
    {
      question: "Qual o tipo societário envolvido?",
      options: ["LTDA", "S.A. Fechada", "S.A. Aberta", "SLU / Outro"],
      type: "single_select"
    },
    {
      question: "Qual a sua posição na operação?",
      options: ["Sócio majoritário", "Sócio minoritário", "Investidor", "Comprador / Vendedor"],
      type: "single_select"
    },
    {
      question: "Qual a fase da operação?",
      options: ["Constituição", "Investimento / Rodada", "M&A / Reestruturação", "Contrato comercial"],
      type: "single_select"
    }
  ]
})
```

**Quando coletar informações adicionais via ask_user_input durante a execução:**

- Ao encontrar cláusula ambígua em review: perguntar a intenção do usuário antes de sugerir redline
- Ao redigir contrato: se houver opções de estrutura (ex.: arbitragem vs. foro judicial), perguntar preferência
- Ao analisar term sheet: perguntar se há restrições de negociação (ex.: "investidor exige X")
- Ao identificar risco tributário: perguntar se o usuário já consultou assessor fiscal

**Exemplos de perguntas situacionais:**

Para resolução de disputas:
```
ask_user_input({
  questions: [{
    question: "Como prefere resolver disputas neste contrato?",
    options: ["Arbitragem (CAM-CCBC)", "Arbitragem (outra câmara)", "Foro judicial", "Ainda não decidi"],
    type: "single_select"
  }]
})
```

Para nível de proteção em acordo de sócios:
```
ask_user_input({
  questions: [{
    question: "Quais proteções são prioritárias para você?",
    options: ["Tag along", "Direito de preferência (ROFR)", "Matérias de veto", "Mecanismo de deadlock"],
    type: "multi_select"
  }]
})
```

Para definição de escopo em due diligence:
```
ask_user_input({
  questions: [{
    question: "Quais áreas a due diligence deve cobrir?",
    options: ["Societário + Contratos", "Trabalhista + Tributário", "Regulatório + Ambiental", "Todas as áreas"],
    type: "single_select"
  }]
})
```

### 2. Análise de Documentos (Review Mode)

Ao revisar um documento existente, seguir esta sequência:

**Quick Scan — Red Flags Iniciais**

Verificar imediatamente:
- Cláusulas que conflitem com normas de ordem pública (CC art. 421-A, art. 1.010 e ss.)
- Ausência de cláusulas obrigatórias por lei (ex.: objeto, sede, capital social em contrato social)
- Limitações de responsabilidade que violem o CDC ou a LGPD
- Cláusulas abusivas em contratos de adesão (CC art. 423-424)
- Penalidades desproporcionais (CC art. 413 — redução equitativa da cláusula penal)
- Cláusulas de non-compete sem limitação temporal/geográfica razoável
- Ausência de cláusula LGPD quando há tratamento de dados pessoais
- Cláusula de arbitragem sem observar Lei 9.307/96

**Análise Clause-by-Clause**

Para cada cláusula relevante, registrar:

```
CLÁUSULA: [Identificação — ex.: "Cláusula 5.2 — Direito de Preferência"]
CLASSIFICAÇÃO: 🔴 Crítico | 🟡 Atenção | 🟢 Adequado
FUNDAMENTAÇÃO: [Artigo de lei aplicável]
PROBLEMA: [Descrição do risco ou inadequação]
IMPACTO: [Consequência prática para o cliente]
MERCADO: [Como o mercado brasileiro tipicamente trata essa questão]
REDLINE SUGERIDO: [Texto alternativo proposto]
FALLBACK: [Posição intermediária caso o redline principal seja rejeitado]
```

**Tabela de Termos-Chave**

Sempre gerar tabela resumo:

| Termo | Valor | Localização | Observação |
|---|---|---|---|
| Capital Social | R$ X | Cláusula 4 | Verificar integralização |
| Objeto Social | Descrição | Cláusula 2 | Verificar amplitude |
| Prazo | Determinado/Indeterminado | Cláusula 12 | — |
| Foro | Comarca X | Cláusula 15 | Considerar arbitragem |

### 3. Elaboração de Documentos (Draft Mode)

Ao redigir documentos novos:

**Estrutura-base para Contratos Societários**

Seguir a estrutura padrão do mercado brasileiro:
1. Qualificação completa das partes (CNPJ/CPF, endereço, representante legal)
2. Considerandos (recitals) — contexto factual da operação
3. Definições — termos definidos em ordem alfabética
4. Objeto e escopo
5. Cláusulas substantivas (direitos, obrigações, preço, prazo)
6. Declarações e garantias (reps & warranties)
7. Obrigações de fazer e não-fazer (covenants)
8. Condições precedentes e subsequentes
9. Indenização e limitação de responsabilidade
10. Confidencialidade e LGPD
11. Vigência e rescisão
12. Penalidades
13. Resolução de disputas (foro ou arbitragem)
14. Disposições gerais (cessão, novação, integralidade, tolerância)
15. Assinaturas e testemunhas (2 testemunhas — requisito CC art. 784, IV, CPC para título executivo extrajudicial)

**Linguagem**

- Redigir em português jurídico formal brasileiro
- Usar termos técnicos consagrados na prática brasileira (e não traduções literais do inglês)
- Terminologia: "contrato social" (não "operating agreement"), "quotas" (não "shares" para LTDA),
  "integralização" (não "capital contribution"), "direito de preferência" (não "right of first refusal"),
  "tag along" e "drag along" são aceitos como termos de mercado
- Referenciar artigos de lei entre parênteses: (art. X da Lei Y)

### 4. Categorias de Documentos

#### 4.1 — Constituição Societária
Consultar `references/constituicao-societaria.md` para:
- Contrato social de LTDA (CC arts. 1.052-1.087)
- Estatuto social de S.A. (Lei 6.404/76, arts. 2º-4º, 11-18)
- Sociedade unipessoal de responsabilidade limitada — SLU (CC art. 1.052, §1º)
- Sociedade em conta de participação — SCP (CC arts. 991-996)
- SPE — Sociedade de propósito específico
- Consórcio (Lei 6.404/76, arts. 278-279)

#### 4.2 — Acordo de Sócios / Acionistas
Consultar `references/acordo-socios.md` para:
- Acordo de quotistas (LTDA)
- Acordo de acionistas (S.A. — Lei 6.404/76, art. 118)
- Tag along, drag along, lock-up
- Direito de preferência e primeira oferta
- Cláusulas de saída (put/call options)
- Deadlock resolution (shotgun, Russian roulette, mediação/arbitragem)
- Governança: quóruns, matérias reservadas, voto afirmativo

#### 4.3 — Operações de M&A
Consultar `references/ma-operations.md` para:
- Term sheet / LOI (vinculante vs. não-vinculante)
- Memorando de entendimentos (MOU)
- Share Purchase Agreement (SPA) / Contrato de compra e venda de quotas/ações
- Asset Purchase Agreement
- Due diligence — checklist por área (societário, trabalhista, tributário, regulatório, ambiental, PI)
- Declarações e garantias (reps & warranties) — padrões brasileiros
- Escrow, earn-out, holdback
- Condições precedentes (CADE, anuência regulatória)
- Cláusula MAC (Material Adverse Change)

#### 4.4 — Venture Capital e Startups
Consultar `references/vc-startups.md` para:
- Mútuo conversível (instrumento mais usado no Brasil pré-Marco Legal)
- SAFE adaptado ao Brasil (nota: SAFE americano não é diretamente aplicável — adaptar)
- Contrato de opção de compra de participação societária
- Contrato de vesting / ILP (Incentivo de Longo Prazo)
- Stock option plan (plano de opção de compra de ações — Lei 6.404/76, art. 168, §3º)
- Phantom stock / SAR (Stock Appreciation Rights)
- Term sheet de rodada (Seed, Series A, B) — padrões LAVCA/ABVCAP
- Acordo de investidor-anjo (LC 182/21, arts. 2º-3º)
- Cláusula de antidiluição (full ratchet vs. weighted average)
- Liquidation preference (participante vs. não-participante)

#### 4.5 — Compliance e Governança
Consultar `references/compliance-governanca.md` para:
- Cláusulas LGPD em contratos (controlador/operador, bases legais, DPA)
- Cláusulas anticorrupção (Lei 12.846/13, FCPA, UK Bribery Act se aplicável)
- Programa de integridade (Decreto 11.129/22)
- Governança para LTDA e S.A. fechada
- Conselho de administração, comitê de auditoria, conselho fiscal
- Código de ética e canal de denúncia
- ESG em cláusulas contratuais

#### 4.6 — Contratos Empresariais Diversos
Consultar `references/contratos-empresariais.md` para:
- Joint venture (contratual e societária)
- Franchising (Lei 13.966/19 — COF, prazo, território)
- Licenciamento de tecnologia e PI (INPI — averbação)
- Distribuição e representação comercial (Lei 4.886/65)
- Prestação de serviços (CC art. 593 e ss.)
- Fornecimento / Supply agreement
- SLA — Service Level Agreement
- NDA / Confidencialidade
- Cessão de direitos autorais (Lei 9.610/98)

#### 4.7 — Geração de Contrato a partir de Proposta Comercial
Consultar `references/proposta-para-contrato.md` para:
- Workflow completo de conversão proposta → contrato
- Mapeamento automático de campos da proposta para cláusulas contratuais
- Coleta interativa de informações faltantes via ask_user_input
- Templates por tipo de serviço/produto
- Checklist de validação pré-geração

Este sub-skill é acionado quando o usuário fornecer uma proposta comercial (PDF, texto,
planilha, ou descrição verbal) e solicitar a geração do contrato correspondente. Usar
`ask_user_input` para coletar todas as informações que a proposta não cubra antes de redigir.

## Padrões de Risco — Classificação

Ao revisar cláusulas, aplicar esta matriz de risco:

**🔴 CRÍTICO — Risco elevado, ação imediata necessária**
- Violação de norma de ordem pública
- Ausência de cláusula obrigatória por lei
- Cláusula que pode ser declarada nula judicialmente
- Exposição a responsabilidade ilimitada ou solidária inesperada
- Risco de desconsideração da personalidade jurídica (CC art. 50)
- Ausência de autorização societária necessária (ex.: alienação de imóvel sem anuência de cônjuge)

**🟡 ATENÇÃO — Risco moderado, negociável**
- Cláusula abaixo do padrão de mercado (desfavorável ao cliente)
- Limitação de responsabilidade inferior à prática usual
- Prazo ou condição inadequados
- Omissão de proteção disponível mas não obrigatória
- Non-compete excessivo (jurisprudência TST limita a 2 anos)
- Earn-out sem mecanismos de proteção (auditoria, gestão operacional)

**🟢 ADEQUADO — Em conformidade**
- Alinhado com legislação e prática de mercado
- Protege adequadamente os interesses do cliente
- Balanceado entre as partes

## Regras de Ouro

1. **Nunca fornecer parecer jurídico definitivo** — esta é uma ferramenta de apoio; toda análise
   deve ser revisada por advogado habilitado na OAB
2. **Citar sempre o fundamento legal** — artigo, lei, decreto
3. **Considerar jurisprudência consolidada** — STJ, STF, TST quando relevante
4. **Alertar sobre questões tributárias** — ITBI em operações societárias, ganho de capital em
   alienação de quotas/ações, planejamento tributário (LC 104/01, art. 116 CTN)
5. **Verificar registros** — Junta Comercial (LTDA), CVM (S.A. aberta), INPI (PI), CADE (concentração)
6. **Duas testemunhas** — para que o contrato seja título executivo extrajudicial (CPC art. 784, IV)
7. **Considerar Lei de Arbitragem** — Lei 9.307/96, câmaras: CAM-CCBC, CAM-B3, FIESP/CIESP, ICC
8. **LGPD sempre** — incluir cláusulas de proteção de dados quando houver tratamento de dados pessoais
9. **Idioma** — contratos no Brasil devem ser redigidos ou traduzidos para português
   (Dec. 13.609/43 para validade de documentos estrangeiros)
10. **Assinatura eletrônica** — válida pela Lei 14.063/20, MP 2.200-2/01 (ICP-Brasil e outras formas)

## Workflow de Revisão de Documentos .docx com Marcas de Revisão

Ao revisar documentos Word com tracked changes, usar o skill `/docx` e seguir este processo:

### Nomenclatura Padrão de Arquivos de Saída
- Arquivo com marcas de revisão: `[Nome Original] - Comentado.docx`
- Versão limpa (marcas aceitas): `[Nome Original] - revisado.docx`
- Exemplo: `Contrato Social 01.06.26.docx` → `Contrato Social 01.06.26 - Comentado.docx`

### Regras Críticas (erros recorrentes a evitar)

| Erro frequente | Correto |
|----------------|---------|
| `<w:t>` dentro de `<w:del>` | Usar `<w:delText>` dentro de `<w:del>` — `<w:t>` corrompe silenciosamente |
| `<w:commentRangeStart/End>` dentro de `<w:r>` | Marcadores de comentário são filhos diretos de `<w:p>` |
| `OLD_string` reconstruída de memória | Extrair o trecho exato do `document.xml` via `grep` antes de escrever o script |
| IDs de revisão hardcoded sem verificar existentes | Buscar max ID no XML; iniciar em `max_id + 10` |
| Editar `unpacked/` e `unpacked2/` em paralelo | Sempre `pack → unpack` entre passes sucessivos |

### Checklist de Entrega
- [ ] Arquivo abre sem erros no Word
- [ ] Aba Revisão mostra alterações do autor "Claude"
- [ ] Aceitar todas as mudanças produz texto correto e sem corrupção

> Para detalhes técnicos completos sobre o workflow XML, consultar o `CLAUDE.md` do projeto.

## Formato de Saída

### Para análise/review:
```markdown
# Análise Jurídica — [Nome do Documento]

## Resumo Executivo
[2-3 parágrafos com conclusão geral e recomendações prioritárias]

## Termos-Chave
[Tabela com termos essenciais extraídos]

## Red Flags
[Tabela com flags críticos encontrados]

## Análise Clause-by-Clause
[Análise detalhada seguindo o template acima]

## Recomendações
[Lista priorizada de ações — classificada por urgência]

## Fundamentação Legal
[Artigos de lei citados na análise]

## Disclaimer
Esta análise foi gerada com auxílio de inteligência artificial e tem caráter
informativo. Não constitui parecer jurídico e não substitui a consulta a
advogado habilitado na Ordem dos Advogados do Brasil (OAB).
```

### Para minutas/elaboração:
Gerar o documento completo em formato .docx quando possível, com:
- Cabeçalho formal
- Qualificação das partes com campos a preencher [●]
- Numeração de cláusulas (1.1, 1.2, 2.1...)
- Notas de rodapé com fundamentação legal
- Campos em destaque para dados variáveis
- Fecho com local, data, assinaturas e testemunhas
