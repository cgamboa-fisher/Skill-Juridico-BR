# Changelog

## [0.3.0] — 2026-08-31

Endurecimento do workflow de tracked changes, a partir de uma revisão real de acordo de investimento em que
a geração do `.docx` marcado exigiu sete rodadas de correção. Os defeitos encontrados não eram cobertos pela
0.2.0, e nenhum deles era pego pelas checagens que a skill recomendava.

### 🔴 Correções de conteúdo

| # | O que faltava | Correção |
|---|---|---|
| 1 | A skill tratava marca de fim de parágrafo excluída como exclusão do parágrafo | **`<w:del/>` em `<w:pPr><w:rPr>` significa FUNDIR com o seguinte**, e o parágrafo resultante herda o `pPr` do seguinte — inclusive a numeração. Tratar como exclusão apaga texto do contrato em silêncio. Documentado em §1 da referência e implementado em `merge_mark_deleted()` |
| 2 | Nada sobre ordem de elementos — só sobre aninhamento | `CT_PPr` tem ordem obrigatória; `<w:rPr>` vem depois de `pStyle`/`numPr`/`spacing`/`ind`. Violar isso faz o Word recusar o arquivo com a mensagem enganosa **"An incorrect text node was used"**, que aponta para nó de texto quando o problema é ordem. Nova §3 e `CT_PPR_ORDER` |
| 3 | Regra "usar parser real" sem dizer onde o regex quebra | `w:pPr` e `w:rPr` **se auto-aninham** (via `pPrChange`/`rPrChange`): regex não-guloso fecha no interno e corrompe o XML. Nova §2 e `outer_element()` com contagem de profundidade |
| 4 | Nada sobre posicionamento de inserções | Três armadilhas documentadas em §4: inserir dentro de cadeia de fusão faz o parágrafo novo absorver o anterior; inserções na mesma âncora se invertem; clonar `pPr` herda o `ilvl` e renumera o documento, quebrando remissões internas |
| 5 | Checklist parava em "arquivo abre sem aviso de reparo" | **Escada de validação de 5 degraus** (§5), com o que cada degrau pega e o que deixa passar. Comprovado por teste negativo: `ilvl` errado passa nos degraus 1 a 4 e só aparece no 5 |
| 6 | Nenhuma metodologia de comparação | O baseline correto é **`aceitar-tudo(original)`**, não o original cru: o documento recebido já traz revisões pendentes de outro autor, e compará-lo cru atribui esse deslocamento a você. Num caso real gerou 13 falsas renumerações. `Document.baseline_clean()` |

### 🟠 Novo

- **`scripts/ooxml_redline.py`** — biblioteca em stdlib puro para marcas de revisão. `Document` com
  `edit/append/insert_after/insert_before/delete_para/new_para`, simulação de aceitar/rejeitar
  (`unwrap`, `merge_mark_deleted`, `build_clean`), e os validadores da escada (`validate`,
  `check_ppr_order`, `check_reject_restores_original`, `open_with_libreoffice`).
  Testada contra o caso real: reproduz o resultado correto em uma execução, com 0 cláusulas renumeradas,
  0 perdidas e exatamente as 6 novas esperadas.
- **§6 "Validar o validador"** — um validador que passa não prova nada se você não sabe o que ele não cobre.
  Inclui a exigência de teste negativo quando o validador for novo ou alterado.
- **Regra de Ouro 13** — nunca entregar `.docx` gerado sem tê-lo aberto. XML bem-formado não é evidência de
  que o Word aceita o arquivo. Sem LibreOffice disponível, declarar que a abertura não foi verificada.

### 🟢 `direito-familia-br` incorporado ao plugin

O skill irmão vivia solto em `~/.claude/skills/`, sem versionamento e sem backup, parado no estado
pré-0.2.0. Passa a ser o segundo skill deste plugin, com o material de tracked changes compartilhado.

| # | Problema | Correção |
|---|---|---|
| 7 | Chamava **`ask_user_input`** — ferramenta inexistente — em 5 pontos, com schema errado (`type: "single_select"`, `options` como strings) e blocos com até 6 opções | Reescrito para **`AskUserQuestion`** com o schema correto (`header`, `multiSelect`, `options[].label`/`.description`), respeitando o limite de 4 opções por pergunta, mais as regras de uso e o comportamento em sessão não assistida |
| 8 | **Nenhuma orientação sobre tracked changes**, embora minutas de divórcio, pactos antenupciais e planos parentais exijam marcas de revisão | Novo §4.6 apontando para o material compartilhado, com o gate de tier FULL e as especificidades de família: escritura pública minutada pelo cartório, dados sensíveis expostos no painel de revisões, conferência dupla de valores em cláusula de alimentos |
| 9 | Sem regra sobre validação de `.docx` gerado | Regra de Ouro 13, espelhando a 13 do skill irmão |

### 🔴 Verificação de vigência em `direito-familia-br` (fontes oficiais, 01/09/2026)

O skill não tinha seção de vigência e carregava **dois erros materiais** — afirmações que levariam
a orientação jurídica errada, não apenas imprecisa.

| # | O que estava errado | Correção | Fonte |
|---|---|---|---|
| 10 | "Filhos menores: divórcio extrajudicial é **nulo** — sempre via judicial" (Regra de Ouro 7, mais 🔴 CRÍTICO, mais um reference) | A **Res. CNJ 571/2024** (DOU 02/09/2024) deu nova redação ao **art. 34, § 2º da Res. CNJ 35/2007**: havendo filhos menores ou incapazes, a escritura é permitida **desde que comprovada a prévia resolução judicial** de guarda, visitação e alimentos, o que deve constar do corpo da escritura | Res. CNJ 571/2024 |
| 11 | "Pensão **jamais** indexada ao salário mínimo (inconstitucional — CF art. 7º, IV)" (Regra de Ouro 6, mais 🔴 CRÍTICO, mais um reference) | **Errado.** STF, **ARE 842.157, Tema 821** de repercussão geral: "a utilização do salário mínimo como base de cálculo do valor de pensão alimentícia não viola a Constituição Federal". A vedação do art. 7º, IV alcança obrigações **sem** caráter alimentar | STF, Tema 821 |
| 12 | Súmula 377/STF citada como "muito relevante na prática", sem ressalva, sugerindo meação automática | **Releitura pelo STJ**: a Segunda Seção, no **EREsp 1.623.858/MG**, exige **prova do esforço comum**. Não há presunção — em separação obrigatória o cônjuge não tem direito automático à metade dos aquestos | STJ, EREsp 1.623.858/MG |
| 13 | "Lei 12.318/10 — Alienação parental", sem as alterações | **Lei 14.340/2022**: revogou o art. 6º, VII (suspensão do poder familiar exige ação própria, não cabe nos autos da alienação); visitação assistida no fórum ou entidade conveniada; oitiva da criança obrigatória na forma da Lei 13.431/2017, sob pena de nulidade | Lei 14.340/2022 |
| 14 | "Lei 14.713/23 — Critérios para guarda compartilhada (alterações ao CC)", vago | Precisado: alterou o **CC art. 1.584, § 2º** — a compartilhada é afastada havendo elementos que evidenciem probabilidade de risco de violência doméstica ou familiar | Lei 14.713/2023 |

**Novo:** seção **"Verificação de Vigência Legislativa — REGRA ANTIFRAGILIDADE"** e
`references/atualizacoes-legislativas.md`, com as armadilhas acima, a rotina de reverificação
(CNJ primeiro — é a camada que mais se move) e o registro do **PL 4/2025** como *em tramitação*,
com alerta explícito contra os artigos de "Nova Lei do Divórcio 2026" / "Nova Lei da Pensão 2026"
que apresentam o projeto como direito posto. Tabela de legislação passou a trazer a data da
verificação e as três referências jurisprudenciais.

### Estrutura

Material comum movido para **`shared/`** na raiz do plugin — `ooxml_redline.py` e
`revisao-docx-tracked-changes.md` —, referenciado por ambos os skills como `../../shared/`.
Corrigir sempre no compartilhado; não duplicar.

`plugin.json` mantém `name: direito-societario-br` para preservar a identidade no marketplace
"My Uploads" (renomear criaria um plugin novo no reenvio); `description` e `keywords` atualizados
para refletir os dois skills.

> **Ação necessária:** este plugin é instalado por upload. As mudanças só entram em vigor após
> reenviar o pacote. Enquanto isso, `~/.claude/skills/direito-familia-br` é um symlink para
> `skills/direito-familia-br` deste repo, para o skill continuar disponível e atualizado.
> Remover o symlink depois do reenvio.

### Arquivos

`shared/revisao-docx-tracked-changes.md` reescrito (3,6 KB → ~13 KB) e movido de
`skills/direito-societario-br/references/`; `shared/ooxml_redline.py` criado;
`skills/direito-societario-br/SKILL.md` §0.3, §8.9 e §10 atualizados;
`skills/direito-familia-br/` incorporado, com §"Interação com o Usuário", §4.6 e Regra de Ouro 13.

---

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
