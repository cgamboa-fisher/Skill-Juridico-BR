---
name: direito-societario-br
description: >
  Analisa, elabora e revisa contratos e documentos jurídicos sob a legislação societária e
  empresarial brasileira. Use quando o usuário mencionar direito societário ou empresarial
  brasileiro, contrato social, estatuto social, acordo de sócios ou de acionistas, LTDA, S.A.,
  SLU, SCP, SPE, holding, term sheet, SPA, due diligence, M&A no Brasil, mútuo conversível,
  SAFE, vesting, stock options, ILP, investidor-anjo, joint venture, MOU, LOI, NDA, franquia,
  distribuição, licenciamento de PI, ou compliance corporativo (LGPD, Lei Anticorrupção,
  programa de integridade, ESG). Também acione para revisão de cláusulas com fundamento na
  legislação brasileira, conversão de proposta comercial em contrato, e revisão de .docx com
  marcas de revisão. Não use para Direito de Família (divórcio, partilha, pensão, guarda) —
  para isso existe o skill irmão `direito-familia-br`.
license: Ver LICENSE do repositório. Ferramenta de apoio — não constitui parecer jurídico.
---

# Direito Societário e Empresarial Brasileiro

Análise clause-by-clause, identificação de riscos, sugestão de redlines e geração de documentos
conforme a legislação e a prática de mercado brasileiras.

---

## 0. Calibração de Execução — SEMPRE PRIMEIRO

Esta skill exige raciocínio jurídico longo, manutenção de coerência entre dezenas de cláusulas
interdependentes e, em alguns fluxos, manipulação direta de XML de OOXML. A qualidade do
resultado depende materialmente da capacidade do modelo em execução. Antes de qualquer trabalho
substantivo, executar os dois passos abaixo.

### 0.1 — Identificar o modelo em execução

Determinar o modelo nesta ordem de precedência:

1. Ler o identificador de modelo disponível no contexto da sessão (em Claude Code / Cowork
   costuma aparecer em bloco `<env>` como `Model: claude-opus-5`).
2. Se ausente, inspecionar variáveis de ambiente relevantes via Bash quando a ferramenta
   estiver disponível (ex.: `ANTHROPIC_MODEL`).
3. Se ainda indeterminado, **assumir o tier STANDARD** e declarar no output que o modelo não
   foi identificado.

> **Ressalva obrigatória:** o modelo que efetivamente atende um turno pode diferir do modelo
> configurado (fallback do runtime, troca de modelo no meio da sessão). Portanto a detecção é
> heurística, não garantia. Nunca afirmar categoricamente qual modelo produziu a análise;
> declarar o identificador configurado e o tier aplicado.

### 0.2 — Aplicar o tier

| Tier | Modelos | Escopo autorizado |
|---|---|---|
| **FULL** | Opus 5 (e Opus/Sonnet de fronteira equivalentes) | Escopo integral: análise clause-by-clause exaustiva, fan-out de subagentes por área de due diligence, redline + fallback negocial por ponto, cadeia de raciocínio sobre interação entre cláusulas, manipulação de XML de tracked changes, geração de contratos longos multi-anexo |
| **STANDARD** | Sonnet (não-fronteira), modelo não identificado | Análise sequencial, sem fan-out de subagentes. Documentos de até ~20 cláusulas. **Vedado**: manipulação direta de XML de tracked changes (usar comentários em Markdown ou docx sem revisões); due diligence multi-área em passe único (fatiar por área, um passe por vez) |
| **MÍNIMO** | Haiku e modelos de porte reduzido | **Somente**: extração de termos-chave, checklist de red flags por correspondência, e localização de cláusulas ausentes. **Vedado**: emitir redline, classificar risco como 🟢 Adequado, gerar minuta contratual completa, ou apresentar o resultado como revisão jurídica |

### 0.3 — Gates de tarefa crítica

Antes de iniciar qualquer tarefa abaixo, verificar o tier. Se o tier não autorizar, **não
executar em modo degradado silencioso** — informar o usuário, explicar o risco concreto e
oferecer as alternativas.

| Tarefa | Tier mínimo | Risco de executar abaixo do tier |
|---|---|---|
| Manipulação de `document.xml` para tracked changes | FULL | Corrupção silenciosa do .docx (`<w:t>` dentro de `<w:del>`); o usuário recebe arquivo que não abre ou que perde texto ao aceitar revisões |
| Due diligence multi-área (≥4 áreas) em passe único | FULL | Cobertura aparente sem profundidade — achados genéricos apresentados como DD completa |
| Redline com fallback negocial | STANDARD | Redline juridicamente incorreto levado à mesa de negociação |
| Minuta de contrato completo (>20 cláusulas) | STANDARD | Cláusulas internamente contraditórias, remissões cruzadas quebradas |
| Extração de termos-chave e checklist | MÍNIMO | — |

**Texto a usar quando o gate bloquear:**

> O modelo em execução nesta sessão (`<identificador>`) foi classificado no tier
> `<TIER>`. A tarefa solicitada (`<tarefa>`) exige tier `<TIER MÍNIMO>` porque
> `<risco concreto>`. Posso: (a) executar o subconjunto autorizado agora
> (`<o que seria entregue>`), ou (b) você troca o modelo da sessão para Opus e eu executo
> o escopo integral. O que prefere?

### 0.4 — Declaração de tier no output

Todo output substantivo desta skill abre com um bloco de procedência:

```
> **Procedência da análise** — Tier: FULL · Modelo configurado: claude-opus-5 ·
> Escopo executado: análise clause-by-clause completa (32 cláusulas) + redlines + fallbacks ·
> Vigência legislativa verificada em: 2026-08-20 ·
> Não constitui parecer jurídico (ver Disclaimer ao final).
```

Isso não é formalidade: é o que impede um contrato de M&A revisado em tier MÍNIMO de ser lido
como revisão completa por quem recebe o documento.

---

## 1. Verificação de Vigência Legislativa — REGRA ANTIFRAGILIDADE

O conteúdo jurídico desta skill tem data de corte. A legislação brasileira societária,
tributária e de proteção de dados mudou de forma relevante em 2021-2026, e continuará mudando.

**Antes de citar qualquer dispositivo como fundamento de uma recomendação de alto impacto**
(estruturação de operação, cláusula de preço, notificação obrigatória, prazo decadencial),
verificar vigência:

1. Se houver ferramenta de busca na web disponível, consultar `planalto.gov.br` para o texto
   consolidado, e `gov.br` do órgão competente (DREI, ANPD, CVM, CADE, CGU) para a camada
   infralegal.
2. Se não houver busca disponível, **declarar explicitamente** no output: *"Fundamento não
   verificado contra fonte oficial nesta sessão; confirmar vigência antes de uso."*
3. Consultar `references/atualizacoes-legislativas.md` — registro dos pontos em que a
   legislação já se moveu e que são armadilha frequente.

**Armadilhas de vigência já mapeadas (nunca reproduzir o erro):**

- **EIRELI não existe mais.** Extinta pelo art. 41 da Lei 14.195/2021, com transformação
  automática e de ofício em sociedade limitada pelas Juntas Comerciais. A sociedade unipessoal
  vigente é a **SLU**, fundada no **CC art. 1.052, §§ 1º e 2º** (Lei 13.874/2019). Nunca
  escrever "EIRELI/SLU" como se fossem um tipo único.
- **Quóruns da LTDA mudaram.** A Lei 14.451/2022 **revogou o inciso I do CC art. 1.076**: não
  existe mais quórum de 3/4 do capital para alteração de contrato social ou para
  incorporação/fusão/dissolução — hoje é **mais da metade do capital social** (art. 1.076, II).
  Administrador não sócio (art. 1.061): **2/3 dos sócios** se o capital não estiver
  integralizado, **mais da metade do capital** se estiver.
- **Non-compete: não há súmula do TST nem limite legal de 2 anos.** Ver §4 abaixo.
- **Decreto 13.609/1943 está revogado** (pela Lei 14.195/2021). Tradutor e Intérprete Público
  hoje: **Lei 14.195/2021, arts. 18-28** + **IN DREI 52/2022**.
- **Lei 14.063/2020 não se aplica a contratos entre particulares** — regula interações com
  entes públicos. Base para contrato privado: **MP 2.200-2/2001, art. 10, § 2º**.
- **Investidor-anjo: o art. 7º da LC 182/2021 foi vetado.** Citar arts. **5º, 6º e 8º**.
- **ANPD não é mais "Autoridade"** — é **Agência** Nacional de Proteção de Dados, por força da
  **Lei 15.352/2026**, que também alterou a LGPD.
- **Reforma tributária do consumo está em execução.** 2026 é ano-teste de IBS/CBS. Cláusulas de
  preço, reajuste e tributos precisam tratar disso. Ver `references/tributacao-contratos.md`.

---

## 2. Skill Companheiro

Para **Direito de Família** (divórcio, partilha de bens — inclusive participações societárias —,
pensão alimentícia, guarda, regime de bens, pacto antenupcial), usar o skill independente
`direito-familia-br`. Em divórcio que envolva quotas ou ações, acionar os dois em conjunto:
este skill para apuração de haveres, cláusulas de acordo de sócios afetadas e efeitos
societários; o irmão para o regime de bens e a partilha.

**Não ativar este skill para**: divórcio, partilha, pensão, guarda, regime de bens, pacto
antenupcial, ou holding familiar quando o foco for sucessório-familiar e não societário.

---

## 3. Legislação de Referência

| Legislação | Escopo |
|---|---|
| Código Civil (Lei 10.406/02), Livro II — Direito de Empresa | Sociedades simples e empresárias, contratos, obrigações |
| Lei das S.A. (Lei 6.404/76) | Sociedades por ações, governança, direitos de acionistas, voto plural (art. 110-A) |
| Lei 14.195/2021 | Extinção da EIRELI, voto plural, prazos de convocação, tradutor público |
| Lei 14.451/2022 | Quóruns de deliberação na LTDA (CC arts. 1.061 e 1.076) |
| Lei de Liberdade Econômica (Lei 13.874/19) | SLU, desconsideração da PJ, função social do contrato |
| Marco Legal das Startups (LC 182/21) | Investidor-anjo (arts. 5º, 6º e 8º), sandbox regulatório |
| LGPD (Lei 13.709/18), alt. Lei 14.460/22 e Lei 15.352/26 | Proteção de dados em cláusulas; ANPD como Agência |
| Resolução CD/ANPD 19/2024 | Cláusulas-padrão de transferência internacional de dados |
| Lei Anticorrupção (Lei 12.846/13) + Decreto 11.129/22 | Compliance, responsabilidade objetiva de PJ, programa de integridade (arts. 56-57) |
| Portaria Normativa Interministerial CGU/AGU 1/2025 | Acordo de leniência, avaliação de programa de integridade |
| LC 214/2025, LC 227/2026, Decreto 12.955/2026 | IBS/CBS/IS — impacto em cláusulas de preço e tributos |
| Lei de Recuperação Judicial (Lei 11.101/05) | Recuperação, falência, créditos |
| Lei de Propriedade Industrial (Lei 9.279/96) | PI em contratos de tecnologia e licenciamento |
| Lei do CADE (Lei 12.529/11) + Portaria Interministerial 994/2012 | Concorrência, atos de concentração (R$ 750 mi / R$ 75 mi) |
| Resolução CVM 168/2022 | Voto plural, composição de órgãos de administração |
| Lei de Arbitragem (Lei 9.307/96) | Cláusula compromissória |
| CLT e legislação trabalhista | Non-compete, ILP, vesting, risco de vínculo |
| Lei de Franquias (Lei 13.966/19) | COF (10 dias), cláusulas obrigatórias |
| MP 2.200-2/2001 + IN DREI 81/2020 | Assinatura eletrônica em contrato privado e em registro |
| CPC (Lei 13.105/15), art. 784, IV | Título executivo extrajudicial — duas testemunhas |

Detalhamento por área nos arquivos em `references/`.

---

## 4. Non-Compete — Fundamentação Correta

Erro recorrente em minutas e em análises automatizadas: afirmar que "o TST limita o non-compete
a 2 anos". **Não existe súmula nem orientação jurisprudencial do TST nesse sentido, e não há
limite legal expresso.** Fundamentar assim:

- **Limite constitucional**: livre exercício profissional (CF art. 5º, XIII) e livre iniciativa
  (CF art. 170) — a cláusula é exceção e se interpreta restritivamente.
- **Limite civil**: função social do contrato e boa-fé objetiva (CC arts. 421 e 422).
- **Analogia empresarial**: **CC art. 1.147** — no trespasse de estabelecimento, o alienante não
  concorre pelos **cinco anos** subsequentes. Serve como **teto de referência em contexto
  empresarial** (M&A, venda de participação), **não** como piso de 2 anos.
- **Jurisprudência do STJ**: exige limitação **temporal e espacial cumulativas**, sob pena de
  invalidade (REsp 1.203.109/MG; REsp 2.185.015/SC — cláusula sem prazo).
- **Vínculo empregatício**: precedentes de Turmas do TST exigem, caso a caso, **compensação
  financeira** e delimitação de tempo, território e atividade.

Tratar "24 meses" como **praxe de mercado e parâmetro de razoabilidade**, jamais como regra
legal. Em contexto de M&A com vendedor-fundador, 3 a 5 anos é sustentável pela analogia ao
art. 1.147; em contrato de emprego puro, sem compensação, alto risco de nulidade.

---

## 5. Interação com o Usuário — AskUserQuestion

Esta skill depende de contexto preciso. Quando informação essencial faltar, **perguntar antes de
prosseguir — não adivinhar**. A ferramenta de perguntas estruturadas varia por ambiente:

| Ambiente | Ferramenta |
|---|---|
| Cowork / Claude Code | `AskUserQuestion` |
| API / SDK sem a ferramenta | Fazer as perguntas em texto, numeradas, e aguardar resposta |

> **Nota de portabilidade:** não existe ferramenta chamada `ask_user_input`. Se alguma
> referência residual mencionar esse nome, tratar como `AskUserQuestion`.

Princípios:

- Máximo de **4 perguntas por chamada**, com 2-4 opções curtas e mutuamente exclusivas.
- Usar `multiSelect: true` quando as opções não forem exclusivas (ex.: proteções desejadas).
- Nunca repetir pergunta cuja resposta já está na conversa ou em arquivo anexo.
- Se a sessão for **não assistida** (agendada, headless): não bloquear. Adotar a interpretação
  mais conservadora, **declarar a premissa no topo do output** e prosseguir.
- Após receber as respostas, executar imediatamente. Não encadear rodadas de perguntas
  desnecessárias.

### 5.1 — Coleta inicial de contexto

Cinco dimensões precisam estar claras antes de analisar ou redigir. Coletar as faltantes:

- **Tipo de documento** — contrato social, estatuto, SHA, SPA, term sheet, ata, procuração
- **Tipo societário** — LTDA, S.A. (aberta/fechada), SLU, SCP, SPE, consórcio
- **Posição do cliente** — majoritário, minoritário, investidor, target, comprador, vendedor
- **Fase da operação** — constituição, rodada, M&A, reestruturação, dissolução
- **Porte e contexto** — startup early-stage, PME, empresa familiar, grupo econômico, multinacional

Exemplo de chamada (abreviado — replicar o padrão para as demais dimensões):

```
AskUserQuestion({
  questions: [
    { header: "Tipo societário", question: "Qual o tipo societário envolvido?",
      multiSelect: false,
      options: [
        { label: "LTDA", description: "Sociedade limitada — CC arts. 1.052-1.087" },
        { label: "S.A. fechada", description: "Companhia fechada, sem registro na CVM" },
        { label: "S.A. aberta", description: "Valores mobiliários registrados na CVM" },
        { label: "SLU", description: "Limitada unipessoal — CC art. 1.052, §§ 1º-2º" }
      ] },
    { header: "Sua posição", question: "Qual a sua posição na operação?",
      multiSelect: false,
      options: [
        { label: "Sócio majoritário", description: "Controle — preservar poder de decisão" },
        { label: "Sócio minoritário", description: "Proteções, veto e mecanismos de saída" },
        { label: "Investidor", description: "Aporte — preferências e governança" },
        { label: "Comprador ou vendedor", description: "Operação de M&A" }
      ] }
  ]
})
```

### 5.2 — Perguntas situacionais durante a execução

- Cláusula ambígua em review → perguntar a intenção antes de sugerir redline
- Estrutura com alternativas → perguntar preferência (arbitragem vs. foro; locked box vs.
  completion accounts; earn-out vs. preço fixo)
- Term sheet → perguntar se há restrição negocial já dada ("o investidor exige X")
- Risco tributário identificado → perguntar se há assessor fiscal envolvido, e **não** substituir
  parecer tributário
- Escopo de due diligence → perguntar quais áreas cobrir (e, em tier STANDARD, avisar que será
  fatiado em passes)

---

## 6. Análise de Documentos (Review Mode)

### 6.1 — Quick Scan de red flags

Verificar imediatamente:

- Cláusulas em conflito com norma de ordem pública (CC arts. 421, 421-A, 1.010 e ss.)
- Ausência de cláusula obrigatória por lei (objeto, sede, capital social em contrato social)
- Limitação de responsabilidade que viole CDC, LGPD, ou que esvazie a obrigação principal
- Cláusula abusiva em contrato de adesão (CC arts. 423-424)
- Penalidade desproporcional (CC art. 413 — redução equitativa da cláusula penal)
- Non-compete sem limitação temporal **e** espacial cumulativas (ver §4)
- Ausência de cláusula LGPD havendo tratamento de dados pessoais; ausência das cláusulas-padrão
  da Resolução CD/ANPD 19/2024 havendo transferência internacional
- Cláusula arbitral em desacordo com a Lei 9.307/96 (e, em contrato de adesão, sem destaque)
- Cláusula de preço/reajuste silente quanto a IBS/CBS na transição 2026-2033
- Quórum contratual que reproduza o revogado 3/4 do art. 1.076, I

### 6.2 — Análise clause-by-clause

Para cada cláusula relevante:

```
CLÁUSULA: [Identificação — ex.: "5.2 — Direito de Preferência"]
CLASSIFICAÇÃO: 🔴 Crítico | 🟡 Atenção | 🟢 Adequado
FUNDAMENTAÇÃO: [Dispositivo aplicável + se foi verificado contra fonte oficial nesta sessão]
PROBLEMA: [Risco ou inadequação]
IMPACTO: [Consequência prática para o cliente, na posição informada]
MERCADO: [Como o mercado brasileiro tipicamente trata]
REDLINE SUGERIDO: [Texto alternativo]
FALLBACK: [Posição intermediária se o redline principal for rejeitado]
```

Em tier MÍNIMO, **não** preencher REDLINE, FALLBACK nem a classificação 🟢.

### 6.3 — Tabela de termos-chave

| Termo | Valor | Localização | Observação |
|---|---|---|---|
| Capital social | R$ X | Cláusula 4 | Verificar integralização |
| Objeto social | Descrição | Cláusula 2 | Verificar amplitude vs. CNAE |
| Quórum de alteração | X% | Cláusula 9 | Conferir contra art. 1.076, II (>1/2) |
| Prazo | Determinado/indeterminado | Cláusula 12 | — |
| Foro / arbitragem | Comarca ou câmara | Cláusula 15 | — |
| Tributos e reajuste | Índice, repasse | Cláusula 7 | Tratar IBS/CBS |

---

## 7. Elaboração de Documentos (Draft Mode)

### 7.1 — Estrutura-base para contratos societários e empresariais

1. Qualificação completa das partes (CNPJ/CPF, endereço, representante legal e poderes)
2. Considerandos (recitals) — contexto factual
3. Definições — em ordem alfabética
4. Objeto e escopo
5. Cláusulas substantivas (direitos, obrigações, preço, prazo)
6. Declarações e garantias (reps & warranties)
7. Covenants (obrigações de fazer e não fazer)
8. Condições precedentes e subsequentes
9. Indenização e limitação de responsabilidade
10. Confidencialidade e LGPD (incluir DPA quando aplicável)
11. Vigência e rescisão
12. Penalidades
13. Resolução de disputas (foro ou arbitragem)
14. Disposições gerais (cessão, novação, integralidade, tolerância, comunicações)
15. Assinaturas e **duas testemunhas** (CPC art. 784, IV — título executivo extrajudicial)

### 7.2 — Linguagem

- Português jurídico formal brasileiro.
- Terminologia consagrada na prática nacional, não tradução literal: "contrato social" (não
  *operating agreement*), "quotas" para LTDA (não *shares*), "integralização" (não *capital
  contribution*), "direito de preferência" (não ROFR, salvo em term sheet bilíngue).
  "Tag along" e "drag along" são aceitos como termos de mercado.
- Referenciar dispositivo entre parênteses: (art. X da Lei Y).
- Evitar remissão cruzada frágil ("nos termos da cláusula acima") — numerar explicitamente.

---

## 8. Categorias de Documentos

### 8.1 — Constituição societária → `references/constituicao-societaria.md`
Contrato social de LTDA (CC arts. 1.052-1.087), estatuto de S.A. (Lei 6.404/76), SLU
(CC art. 1.052, §§ 1º-2º), SCP (CC arts. 991-996), SPE, consórcio (Lei 6.404/76, arts. 278-279).

### 8.2 — Acordo de sócios / acionistas → `references/acordo-socios.md`
Acordo de quotistas; acordo de acionistas (Lei 6.404/76, art. 118); tag along, drag along,
lock-up; ROFR e ROFO; put/call; deadlock (shotgun, Russian roulette, mediação); governança,
quóruns e matérias reservadas.

### 8.3 — M&A → `references/ma-operations.md`
Term sheet e LOI (vinculante vs. não vinculante); MOU; SPA; asset deal; due diligence por área;
reps & warranties; escrow, earn-out, holdback; condições precedentes (CADE, anuências);
cláusula MAC.

### 8.4 — Venture capital e startups → `references/vc-startups.md`
Mútuo conversível; SAFE adaptado; opção de compra de participação; vesting e ILP; stock options
(Lei 6.404/76, art. 168, § 3º); phantom stock e SAR; term sheet de rodada; investidor-anjo
(LC 182/21, arts. 5º, 6º e 8º); antidiluição; liquidation preference.

### 8.5 — Compliance e governança → `references/compliance-governanca.md`
Cláusulas LGPD e DPA; cláusulas-padrão da Resolução CD/ANPD 19/2024; anticorrupção
(Lei 12.846/13, Decreto 11.129/22, arts. 56-57); programa de integridade; governança de LTDA e
S.A. fechada; Resolução CVM 168/2022; ESG.

### 8.6 — Contratos empresariais diversos → `references/contratos-empresariais.md`
Joint venture; franquia (Lei 13.966/19); licenciamento de tecnologia e PI (INPI); distribuição e
representação comercial (Lei 4.886/65); prestação de serviços; fornecimento; SLA; NDA; cessão de
direitos autorais (Lei 9.610/98).

### 8.7 — Proposta comercial → contrato → `references/proposta-para-contrato.md`
Workflow de conversão, mapeamento campo→cláusula, coleta de lacunas, templates por tipo,
checklist de validação.

### 8.8 — Tributação em cláusulas contratuais → `references/tributacao-contratos.md`
IBS/CBS/IS e a transição 2026-2033; cláusulas de preço, reajuste, gross-up e repasse; ITBI em
operações societárias; ganho de capital na alienação de participação; ágio.

### 8.9 — Revisão de .docx com marcas de revisão → `references/revisao-docx-tracked-changes.md`
Workflow de tracked changes em OOXML, erros que corrompem o arquivo, checklist de entrega.
**Tier FULL obrigatório.**

### 8.10 — Registro de atualizações legislativas → `references/atualizacoes-legislativas.md`
O que mudou, quando, e qual citação está errada em material antigo.

---

## 9. Matriz de Risco

**🔴 CRÍTICO — ação imediata**
- Violação de norma de ordem pública
- Ausência de cláusula obrigatória por lei
- Cláusula com risco concreto de nulidade judicial
- Exposição a responsabilidade ilimitada ou solidária não pretendida
- Risco de desconsideração da personalidade jurídica (CC art. 50, com a redação da Lei 13.874/19)
- Falta de autorização societária ou conjugal necessária
- Operação sujeita a notificação prévia ao CADE sem condição precedente (risco de *gun jumping*)
- Transferência internacional de dados sem as cláusulas-padrão da Resolução CD/ANPD 19/2024

**🟡 ATENÇÃO — negociável**
- Cláusula abaixo do padrão de mercado, desfavorável ao cliente
- Limitação de responsabilidade inferior à prática usual
- Prazo ou condição inadequados
- Omissão de proteção disponível mas não obrigatória
- Non-compete de duração ou abrangência desproporcional ao contexto (ver §4)
- Earn-out sem proteção (auditoria, governança do período, definição de métrica)
- Cláusula de preço silente quanto a IBS/CBS

**🟢 ADEQUADO** — alinhado à legislação e à prática, protege o cliente, balanceado.
Não usar em tier MÍNIMO.

---

## 10. Regras de Ouro

1. **Nunca emitir parecer jurídico definitivo.** Ferramenta de apoio; toda análise deve ser
   revisada por advogado habilitado na OAB.
2. **Citar sempre o fundamento legal** — artigo, lei, decreto, resolução — e sinalizar quando o
   fundamento não foi verificado contra fonte oficial nesta sessão.
3. **Verificar vigência** antes de fundamentar recomendação de alto impacto (§1).
4. **Considerar jurisprudência consolidada** — STJ, STF, TST — e não inventar súmula.
5. **Alertar sobre questões tributárias** — ITBI em operações societárias, ganho de capital na
   alienação de quotas/ações, IBS/CBS na transição, norma antielisiva (CTN art. 116, parágrafo
   único, LC 104/01) — sem substituir assessor fiscal.
6. **Verificar registros e anuências** — Junta Comercial (LTDA e SLU), CVM (companhia aberta),
   INPI (PI), CADE (concentração), agências setoriais.
7. **Duas testemunhas** para título executivo extrajudicial (CPC art. 784, IV).
8. **Arbitragem** — Lei 9.307/96; câmaras usuais: CAM-CCBC, CAM-B3, CAM-FIESP/CIESP, ICC,
   AMCHAM. Em contrato de adesão, exigir destaque e assinatura específica.
9. **LGPD sempre** que houver tratamento de dados pessoais; cláusulas-padrão da ANPD quando
   houver transferência internacional.
10. **Idioma** — contrato para produzir efeito no Brasil em português; documento estrangeiro
    depende de **tradução por Tradutor e Intérprete Público** (Lei 14.195/2021, arts. 18-28;
    IN DREI 52/2022) e, quanto à autenticidade, de **apostilamento** (Decreto 8.660/2016) ou
    consularização. Tradução e apostilamento são exigências distintas — não confundir.
11. **Assinatura eletrônica** — em contrato **privado**, base é a **MP 2.200-2/2001, art. 10,
    § 2º** (validade de certificado não-ICP desde que aceito pelas partes). A Lei 14.063/2020
    regula interações com o **poder público**, não entre particulares. Para arquivamento em Junta
    Comercial: assinatura qualificada (ICP-Brasil) ou avançada, inclusive gov.br
    (IN DREI 81/2020, alterada pelas IN DREI 112/2022 e 88/2022).
12. **Declarar o tier de execução** no output (§0.4).

---

## 11. Formato de Saída

### Para análise / review

```markdown
# Análise Jurídica — [Nome do Documento]

> **Procedência da análise** — Tier: [FULL|STANDARD|MÍNIMO] · Modelo configurado: [id] ·
> Escopo executado: [descrição] · Vigência legislativa verificada em: [data ou "não verificada"]

## Resumo Executivo
[2-3 parágrafos: conclusão geral e as recomendações prioritárias]

## Termos-Chave
[Tabela]

## Red Flags
[Tabela com severidade]

## Análise Clause-by-Clause
[Template do §6.2]

## Recomendações
[Lista priorizada por urgência, com o que é negociável e o que é impeditivo]

## Fundamentação Legal
[Dispositivos citados, com marcação de verificado / não verificado]

## Limitações desta Análise
[O que não foi coberto e por quê — escopo, tier, informação faltante]

## Disclaimer
Esta análise foi gerada com auxílio de inteligência artificial e tem caráter informativo.
Não constitui parecer jurídico e não substitui a consulta a advogado habilitado na Ordem dos
Advogados do Brasil (OAB). A legislação brasileira é dinâmica; confirme a vigência dos
dispositivos citados antes de qualquer decisão.
```

### Para minutas

Gerar `.docx` quando possível (usar o skill `docx`), com:
- Cabeçalho formal
- Qualificação das partes com campos a preencher `[●]`
- Numeração hierárquica de cláusulas (1.1, 1.2, 2.1...)
- Notas de rodapé com fundamentação legal
- Campos variáveis em destaque
- Fecho com local, data, assinaturas e duas testemunhas
- Nota de abertura declarando o tier de execução e o disclaimer
