# Changelog

## [0.2.0] — 2026-08-20

Revisão completa. Vigência legislativa verificada contra fontes oficiais em 20/08/2026.

### 🔴 Correções de fundamento legal (erros materiais da 0.1.0)

| # | O que estava errado | Correção | Fonte |
|---|---|---|---|
| 1 | `EIRELI/SLU` listada como tipo societário vigente na `description` e em `constituicao-societaria.md` | **EIRELI extinta** pelo art. 41 da Lei 14.195/2021, com transformação automática e de ofício em Ltda. desde 27/08/2021. A unipessoal vigente é a **SLU**, fundada no CC art. 1.052, §§ 1º-2º | Lei 14.195/2021; Ofício Circular SEI 4856/2022/ME — DREI |
| 2 | "3/4 do capital: modificação do contrato social, incorporação/fusão/dissolução" | A **Lei 14.451/2022 revogou o CC art. 1.076, I**. Hoje: **mais da metade do capital** (art. 1.076, II). Administrador não sócio (art. 1.061): 2/3 dos sócios se capital não integralizado, >1/2 do capital se integralizado | Lei 14.451/2022 |
| 3 | "Non-compete excessivo (jurisprudência TST limita a 2 anos)" — repetido em 3 arquivos | **Não há súmula nem OJ do TST**, e não há limite legal. O CC art. 1.147 prevê **5 anos**, só para trespasse. Fundamentação correta: CF art. 5º, XIII e art. 170; CC arts. 421-422; analogia ao art. 1.147; STJ exigindo limitação temporal **e** espacial cumulativas (REsp 1.203.109/MG, REsp 2.185.015/SC); compensação financeira em vínculo empregatício | CC art. 1.147; STJ |
| 4 | "Acordo de investidor-anjo (LC 182/21, arts. 2º-3º)" | Correto: **arts. 5º, 6º e 8º**. **O art. 7º foi vetado** — a citação original remetia a dispositivo inexistente | LC 182/2021 |
| 5 | "Dec. 13.609/43 para validade de documentos estrangeiros" | **Revogado** pela Lei 14.195/2021. Regime atual do Tradutor e Intérprete Público: **Lei 14.195/2021, arts. 18-28** + **IN DREI 52/2022**. Tradução juramentada e apostilamento (Decreto 8.660/2016) são exigências **distintas** — a skill as confundia | Planalto; IN DREI 52/2022 |
| 6 | "Assinatura eletrônica — válida pela Lei 14.063/20" para contratos privados | A **Lei 14.063/2020 não se aplica entre particulares** — regula interações com o poder público. Base para contrato privado: **MP 2.200-2/2001, art. 10, § 2º**. Registro em Junta: IN DREI 81/2020, alt. IN 112/2022 e 88/2022, admitindo gov.br | MP 2.200-2/2001 |
| 7 | ANPD tratada como "Autoridade Nacional", autarquia especial | Desde a **Lei 15.352, de 25/02/2026**, é **Agência** Nacional de Proteção de Dados — agência reguladora. A lei também alterou a Lei 13.709/2018, inclusive o art. 55-A e a definição de encarregado | Lei 15.352/2026 |
| 8 | Nenhuma menção a regulamento de transferência internacional de dados | **Resolução CD/ANPD 19/2024** — cláusulas-padrão exigíveis desde 23/08/2025. Ausência em contrato com fluxo internacional agora é classificada 🔴 CRÍTICO | Resolução CD/ANPD 19/2024 |
| 9 | Camada infralegal de anticorrupção incompleta | Confirmado **Decreto 11.129/2022** (arts. 56-57), que revogou o Decreto 8.420/2015. Acrescentada a **Portaria Normativa Interministerial CGU/AGU 1/2025**, que unificou as regras de leniência e revogou a IN CGU/AGU 2/2018, a Portaria Conjunta 4/2019 e a Portaria 36/2022 | Decreto 11.129/2022; PNI CGU/AGU 1/2025 |

### 🟠 Correções técnicas de skill

| # | Problema | Correção |
|---|---|---|
| 10 | A skill instruía o modelo a chamar **`ask_user_input`** — ferramenta que **não existe** em nenhum ambiente Anthropic. Eram 10 ocorrências, incluindo 4 blocos de código completos. O modelo tentaria uma chamada inválida, falharia, e cairia em comportamento não especificado | Substituída por **`AskUserQuestion`**, com o schema correto (`header`, `question`, `multiSelect`, `options[].label`/`.description`), limite de 4 perguntas por chamada, labels ≤ 32 caracteres, e fallback documentado para ambientes sem a ferramenta |
| 11 | O workflow de tracked changes remetia a *"o `CLAUDE.md` do projeto"* para os detalhes técnicos — **arquivo inexistente no repositório**. O workflow mais arriscado da skill apontava para o vazio | Criado `references/revisao-docx-tracked-changes.md`, com fluxo completo, tabela de 7 erros de OOXML com a consequência de cada um, e checklist de entrega de 7 itens |
| 12 | `description` do frontmatter com ~1.400 caracteres, incluindo enumeração de 8 leis por número — verbosidade que dilui o sinal de acionamento | Reescrita em terceira pessoa, centrada em frases-gatilho que o usuário efetivamente diz, com a exclusão de Direito de Família mantida |
| 13 | Nenhuma instrução sobre o que fazer em sessão não assistida (agendada, headless), onde perguntar bloqueia indefinidamente | Regra explícita: adotar a interpretação conservadora, declarar a premissa no topo do output, prosseguir |
| 14 | Nenhum mecanismo contra decadência do conteúdo jurídico | Nova seção **§1 Verificação de Vigência** com regra de consulta a fonte oficial antes de fundamentar recomendação de alto impacto, marcação explícita de "não verificado", e o novo `references/atualizacoes-legislativas.md` como registro de armadilhas |

### ✨ Novo — calibração de execução por modelo

Nova **§0 do SKILL.md**, com quatro sub-rotinas:

- **§0.1 Detecção** — identificação do modelo por precedência (contexto `<env>` → variável de
  ambiente → assumir STANDARD), com ressalva explícita de que o modelo servindo um turno pode
  diferir do configurado. A skill declara o identificador configurado, não afirma certeza.
- **§0.2 Tiers** — FULL (Opus 5 e equivalentes de fronteira), STANDARD (Sonnet, ou modelo não
  identificado), MÍNIMO (Haiku e porte reduzido), cada um com escopo autorizado e vedações.
- **§0.3 Gates de tarefa crítica** — tabela tarefa × tier mínimo × risco concreto de executar
  abaixo do tier, com texto padronizado para bloquear e oferecer alternativas. Manipulação de
  `document.xml` e due diligence multi-área em passe único exigem FULL.
- **§0.4 Bloco de procedência** — todo output substantivo abre declarando tier, modelo
  configurado, escopo executado e data da verificação de vigência.

Efeitos correlatos: em tier MÍNIMO, a skill não preenche REDLINE, FALLBACK nem a classificação
🟢 Adequado; o formato de saída ganhou seção obrigatória **"Limitações desta Análise"**.

### ✨ Novo — conteúdo

- **`references/tributacao-contratos.md`** — reforma tributária do consumo em cláusulas
  contratuais: LC 214/2025, **LC 227/2026** (CGIBS, processo administrativo do IBS, ITCMD),
  **Decreto 12.955/2026** (regulamento da CBS), ano-teste de 2026 (0,9% CBS + 0,1% IBS, ADCT
  art. 125 e LC 214/2025 art. 348), e o marco de **03/08/2026** em que documento fiscal
  eletrônico passa a ser rejeitado sem os campos de IBS/CBS. Inclui checklist de 8 itens para
  cláusula de preço, modelo de núcleo de cláusula tributária, e a seção de operações societárias
  (ITBI e RE 796.376, ganho de capital, ágio, norma antielisiva, earn-out) com o **Tema
  Repetitivo 1.226 do STJ** sobre stock options (julgado 11/09/2024) corretamente enunciado.
- **`references/atualizacoes-legislativas.md`** — tabela de 11 afirmações erradas e comuns com a
  correção e a fonte, mais as novidades que precisam entrar nas minutas (reforma tributária,
  voto plural do art. 110-A, prazos de convocação do art. 124, Resolução CVM 168/2022, critérios
  do CADE com o alerta da proposta de elevação a R$ 2 bi / R$ 200 mi ainda não vigente,
  COF de 10 dias). Registra o único ponto **não verificado**: status da ADI no STF sobre os
  dispositivos da Lei 14.195/2021 relativos a tradutores públicos.
- **§4 do SKILL.md** — seção dedicada à fundamentação correta do non-compete, por ser o erro
  mais replicado da versão anterior.
- **Novos red flags** no Quick Scan: cláusula de preço silente quanto a IBS/CBS na transição;
  quórum contratual reproduzindo o revogado art. 1.076, I; ausência das cláusulas-padrão da ANPD
  em transferência internacional; cláusula arbitral sem destaque em contrato de adesão.
- **Nova pergunta de coleta** em `proposta-para-contrato.md` sobre tratamento de IBS/CBS em
  contratos com vigência superior a 12 meses.
- **Tabela de legislação** ampliada de 12 para 20 entradas, incluindo as normas de 2021-2026 que
  faltavam.

### 📦 Empacotamento

- Convertido em **plugin** instalável: `.claude-plugin/plugin.json` + `skills/`, compatível com
  Cowork, Claude.ai e Claude Code.
- `README.md` reescrito com instalação por ambiente, explicação dos tiers, tabela de referências
  e seção de manutenção.

---

## [0.1.0] — 2026-04

Versão inicial: SKILL.md e 7 arquivos de referência.
