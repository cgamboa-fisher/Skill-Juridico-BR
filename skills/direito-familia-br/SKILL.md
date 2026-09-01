---
name: direito-familia-br
description: >
  Análise, elaboração e revisão de documentos jurídicos de direito de família sob a legislação
  brasileira. Cobre divórcio (extrajudicial em cartório, judicial consensual e litigioso),
  partilha de bens (incluindo participações societárias, holdings familiares e bens no exterior),
  pensão alimentícia (filhos, ex-cônjuge, alimentos gravídicos, execução com prisão civil),
  guarda compartilhada e unilateral, plano parental, alienação parental, regimes de bens
  (comunhão parcial, universal, separação total/obrigatória, participação final, união estável),
  pacto antenupcial e contrato de convivência. Use este skill sempre que o usuário mencionar
  divórcio, separação, dissolução de união estável, partilha de bens, pensão alimentícia,
  guarda dos filhos, plano parental, regime de bens, comunhão parcial, comunhão universal,
  separação total, pacto antenupcial, contrato de convivência, alienação parental, escritura
  pública de divórcio, petição inicial de divórcio, alimentos gravídicos, holdings familiares,
  ou qualquer questão envolvendo Lei 11.441/07 (divórcio extrajudicial), Lei 5.478/68 (Lei de
  Alimentos), Lei 11.804/08 (alimentos gravídicos), Lei 12.318/10 (alienação parental),
  Lei 13.058/14 (guarda compartilhada), EC 66/2010, ou Livro IV do Código Civil. Para questões
  societárias e empresariais relacionadas (estruturação de holding, partilha envolvendo quotas
  de LTDA ou ações de S.A.), o skill se complementa com `direito-societario-br`.
---

# Direito de Família — Brasil

Skill especializado em análise, elaboração e revisão de documentos jurídicos no âmbito do
direito de família brasileiro. Foco em divórcio, partilha de bens, alimentos, guarda dos filhos,
e questões correlatas. Inclui templates de documentos prontos, checklists detalhados, e
conexões com direito societário para casos envolvendo empresários e investidores.

## Quando Ativar

Ativar quando o usuário:
- Mencionar divórcio, separação, dissolução de união estável, ou nulidade/anulação de casamento
- Solicitar elaboração de escritura pública de divórcio, petição inicial (consensual ou litigiosa),
  plano parental, acordo de partilha, ou acordo de pensão alimentícia
- Pedir checklist de partilha de bens ou de pensão alimentícia
- Mencionar regime de bens (comunhão parcial, universal, separação, participação final)
- Tratar de guarda compartilhada, guarda unilateral, alienação parental, ou convivência
- Solicitar análise patrimonial para fins de divórcio (especialmente envolvendo participações
  societárias, holdings familiares, ou empresas em operação)
- Elaborar pacto antenupcial ou contrato de convivência (planejamento preventivo)
- Tratar de alimentos gravídicos, execução de alimentos, ou prisão civil por inadimplemento

## Verificação de Vigência Legislativa — REGRA ANTIFRAGILIDADE

O conteúdo jurídico deste skill tem data de corte. Direito de família se move em três camadas, e a
que mais muda é justamente a que menos aparece em material didático: os **atos do CNJ** sobre
extrajudicialização.

**Antes de fundamentar qualquer recomendação de alto impacto** — escolha da via (judicial ou
extrajudicial), forma de fixação de alimentos, direito à meação, pedido de suspensão de poder
familiar —, verificar vigência:

1. Havendo busca na web, consultar `planalto.gov.br` para o texto consolidado, `atos.cnj.jus.br`
   para a camada infralegal notarial e registral, e `scon.stj.jus.br` / `portal.stf.jus.br` para a
   jurisprudência vinculante.
2. Não havendo busca, **declarar explicitamente** no output: *"Fundamento não verificado contra
   fonte oficial nesta sessão; confirmar vigência antes de uso."*
3. Consultar `references/atualizacoes-legislativas.md` — registro do que já mudou e das armadilhas
   frequentes.

**Armadilhas já mapeadas (nunca reproduzir o erro):**

- **Divórcio extrajudicial com filhos menores não é mais vedado.** A **Res. CNJ 571/2024** deu
  nova redação ao art. 34, § 2º da Res. CNJ 35/2007: é admitido desde que guarda, convivência e
  alimentos já estejam resolvidos por decisão judicial, o que deve constar da escritura.
- **Pensão pode ser fixada em salários mínimos.** STF, **ARE 842.157 (Tema 821)**: não viola a CF.
  A vedação do art. 7º, IV alcança obrigações sem caráter alimentar.
- **Súmula 377/STF não gera meação automática.** STJ, **EREsp 1.623.858/MG**: a comunicação dos
  aquestos na separação obrigatória exige **prova do esforço comum**.
- **Alienação parental**: a **Lei 14.340/2022** revogou o art. 6º, VII da Lei 12.318/2010 — a
  suspensão do poder familiar exige ação própria — e tornou obrigatória a oitiva da criança
  (Lei 13.431/2017), sob pena de nulidade.
- **Guarda compartilhada** é afastada havendo elementos de risco de violência doméstica
  (**Lei 14.713/2023**, CC art. 1.584, § 2º).
- **PL 4/2025 (reforma do Código Civil) NÃO está em vigor** — segue em comissão no Senado.
  Circulam artigos de "nova lei 2026" que apresentam o projeto como direito posto. Projeto não
  é lei: conferir número, sanção e publicação antes de acolher.

## Legislação de Referência

> Vigência verificada contra fonte oficial em **2026-09-01**. Ao usar depois de meses, reconferir
> conforme a seção acima.

| Norma | Escopo |
|---|---|
| CF art. 226, §6º | Divórcio direto (após EC 66/2010 — sem prazo, sem culpa) |
| CC arts. 1.511-1.590 | Direito de família — casamento, divórcio, união estável |
| CC arts. 1.639-1.688 | Regime de bens entre cônjuges |
| CC arts. 1.694-1.710 | Alimentos |
| CC arts. 1.723-1.727 | União estável |
| Lei 5.478/68 | Lei de Alimentos |
| Lei 11.441/07 | Divórcio extrajudicial em cartório |
| Lei 11.804/08 | Alimentos gravídicos |
| Lei 12.318/10, alt. Lei 14.340/22 | Alienação parental — rito, visitação assistida, oitiva da criança |
| Lei 13.058/14 | Guarda compartilhada como regra |
| Lei 14.713/23 | Risco de violência doméstica afasta a guarda compartilhada (CC art. 1.584, § 2º) |
| Lei Maria da Penha (Lei 11.340/06) | Violência doméstica — implicações em guarda |
| CPC arts. 528-533 | Execução de alimentos (incluindo prisão civil) |
| CPC arts. 693-699 | Procedimento das ações de família |
| Res. CNJ 35/2007, alt. Res. CNJ 571/2024 | Divórcio extrajudicial — admite filhos menores ou incapazes se guarda, convivência e alimentos já resolvidos judicialmente |
| STF, ARE 842.157 (Tema 821) | Pensão em salários mínimos não viola a CF |
| STJ, EREsp 1.623.858/MG | Súmula 377/STF exige prova do esforço comum |

Para detalhamento de cada área, consultar os arquivos em `references/`.

## Interação com o Usuário — AskUserQuestion

Direito de família é uma área onde o contexto pessoal é determinante para a análise correta.
Coletar as informações essenciais antes de redigir documentos ou emitir análises. Não assumir —
perguntar.

> **Nota de portabilidade:** a ferramenta chama-se **`AskUserQuestion`**. Não existe ferramenta
> chamada `ask_user_input`; se alguma referência residual mencionar esse nome, tratar como
> `AskUserQuestion`. Em ambiente sem a ferramenta (API/SDK), fazer as perguntas em texto,
> numeradas, e aguardar resposta.

Regras do schema:

- Máximo de **4 perguntas por chamada**; cada pergunta com **2 a 4 opções** mutuamente exclusivas.
- Cada opção tem `label` curto (1-5 palavras) e `description` explicando a consequência.
- `header` é o rótulo curto da pergunta (até 12 caracteres).
- `multiSelect: true` quando as opções não forem exclusivas.
- Não incluir opção "Outro" — a ferramenta já oferece.
- Nunca repetir pergunta cuja resposta já está na conversa ou em documento anexo.
- **Sessão não assistida** (agendada, headless): não bloquear. Adotar a interpretação mais
  protetiva ao vulnerável (menor, alimentando), declarar a premissa no topo do output e prosseguir.

**Coleta inicial obrigatória:**

```
AskUserQuestion({
  questions: [
    { header: "Modalidade", question: "Qual a modalidade de divórcio pretendida?",
      multiSelect: false,
      options: [
        { label: "Extrajudicial", description: "Cartório — consensual; com filhos menores ou incapazes exige guarda, convivência e alimentos já resolvidos judicialmente (Res. CNJ 571/2024)" },
        { label: "Judicial consensual", description: "Há filhos menores ou disputa pontual, mas há acordo" },
        { label: "Judicial litigioso", description: "Disputa significativa sobre partilha, guarda ou alimentos" },
        { label: "Ainda a definir", description: "Preciso de orientação sobre qual via cabe ao caso" }
      ] },
    { header: "Regime", question: "Qual o regime de bens do casamento ou da união?",
      multiSelect: false,
      options: [
        { label: "Comunhão parcial", description: "Regime legal supletivo desde 1977 (CC art. 1.658)" },
        { label: "Comunhão universal", description: "Exige pacto antenupcial (CC art. 1.667)" },
        { label: "Separação", description: "Convencional por pacto, ou obrigatória (CC art. 1.641)" },
        { label: "União estável", description: "Sem contrato escrito — presume-se comunhão parcial (CC art. 1.725)" }
      ] },
    { header: "Filhos", question: "Há filhos menores ou incapazes?",
      multiSelect: false,
      options: [
        { label: "Menores de 18", description: "Extrajudicial só se guarda, convivência e alimentos já estiverem resolvidos judicialmente" },
        { label: "Maiores incapazes", description: "Mesma condição dos menores; pode exigir curatela" },
        { label: "Ambos", description: "Menores e maiores incapazes" },
        { label: "Não há", description: "Sem filhos, ou todos maiores e capazes" }
      ] }
  ]
})
```

**Coleta complementar quando houver patrimônio empresarial:**

```
AskUserQuestion({
  questions: [
    { header: "Participação", question: "Que participações societárias entram na partilha?",
      multiSelect: true,
      options: [
        { label: "Quotas de LTDA", description: "Apuração de haveres e eventual acordo de sócios aplicável" },
        { label: "Ações de S.A.", description: "Companhia aberta ou fechada" },
        { label: "Holding familiar", description: "Pode envolver doação com reserva de usufruto e cláusulas restritivas" },
        { label: "Empresa no exterior", description: "Exige análise de lei aplicável e eventual carta rogatória" }
      ] },
    { header: "Sua posição", question: "Qual a sua posição na operação?",
      multiSelect: false,
      options: [
        { label: "Titular das quotas", description: "Sócio ou acionista cuja participação será partilhada" },
        { label: "Cônjuge não sócio", description: "Com direito à meação sobre o valor da participação" },
        { label: "Orientando ambos", description: "Atuação consensual para as duas partes" }
      ] }
  ]
})
```

**Coleta para definição de pensão alimentícia:**

```
AskUserQuestion({
  questions: [
    { header: "Renda", question: "Qual a fonte de renda do alimentante?",
      multiSelect: false,
      options: [
        { label: "CLT", description: "Folha definida — permite desconto direto em folha" },
        { label: "Autônomo", description: "Renda variável — dificulta percentual; considerar valor fixo" },
        { label: "Sócio", description: "Pró-labore mais dividendos — atenção à base de cálculo" },
        { label: "Misto", description: "CLT somado a outras fontes" }
      ] },
    { header: "Fixação", question: "Como a pensão deve ser fixada?",
      multiSelect: false,
      options: [
        { label: "Percentual", description: "Sobre rendimentos líquidos — acompanha a variação da renda" },
        { label: "Valor fixo", description: "Em reais, com índice de reajuste definido" },
        { label: "Misto", description: "Parte percentual, parte fixa" },
        { label: "Preciso orientação", description: "Recomendar com base na fonte de renda informada" }
      ] }
  ]
})
```

**Coleta situacional durante a execução:**

- Ao gerar plano parental: perguntar sobre rotina escolar, distância entre residências, viagens
- Ao redigir partilha: perguntar se há acordo prévio sobre destinação de imóveis específicos
- Ao tratar de alienação parental: perguntar se há indicadores objetivos ou apenas suspeita
- Ao envolver violência doméstica: NÃO insistir em mediação consensual — direcionar para assistência especializada

## Fluxo de Trabalho

### 1. Identificação do Contexto

Antes de qualquer análise ou redação, ter clareza sobre 5 dimensões:

- **Modalidade**: extrajudicial, judicial consensual, judicial litigioso
- **Regime de bens**: define o que se comunica e o que não se comunica
- **Composição familiar**: filhos (menores, maiores, incapazes), gravidez em curso
- **Patrimônio**: imóveis, financeiro, empresarial, exterior
- **Posição do cliente**: cônjuge titular de patrimônio, cônjuge não-titular, ambos (consensual)

### 2. Análise de Documentos (Review Mode)

Ao revisar acordo, escritura ou petição existente:

**Quick Scan — Red Flags Iniciais:**
- Divórcio extrajudicial com filhos menores ou incapazes SEM prévia resolução judicial de guarda, convivência e alimentos (Res. CNJ 571/2024)
- Pensão **reajustada por índice inexistente ou não pactuado**, deixando o valor sem critério de
  correção. (Fixar em número de salários mínimos NÃO é vício: o STF assentou a constitucionalidade
  no ARE 842.157, Tema 821 de repercussão geral)
- Pensão sem cláusula de reajuste em acordo de longo prazo
- Renúncia ampla a alimentos sem assistência jurídica documentada
- Partilha desigual sem recolhimento de ITCMD
- Acordo sem plano parental detalhado (em casos com filhos)
- Bens no exterior não declarados (risco de ocultação patrimonial)
- Ausência de cláusula sobre mudança de domicílio com filhos

**Análise Cláusula a Cláusula:**

```
CLÁUSULA: [Identificação — ex.: "Cláusula 5ª — Pensão Alimentícia"]
CLASSIFICAÇÃO: 🔴 Crítico | 🟡 Atenção | 🟢 Adequado
FUNDAMENTAÇÃO: [Artigo de lei aplicável]
PROBLEMA: [Descrição]
IMPACTO: [Consequência prática]
JURISPRUDÊNCIA: [STJ/TJ relevante quando aplicável]
SUGESTÃO: [Texto alternativo]
FALLBACK: [Posição intermediária]
```

### 3. Elaboração de Documentos (Draft Mode)

Estrutura padrão por tipo de documento:

**Escritura pública de divórcio consensual** — consultar `references/divorcio-procedimento-documentos.md`

**Petição inicial de divórcio** — consultar `references/divorcio-procedimento-documentos.md`

**Plano parental** — consultar `references/guarda-protecao-criancas.md`

**Acordo de partilha de bens** — consultar `references/regimes-bens-partilha.md`

**Acordo de pensão alimentícia** — consultar `references/pensao-alimenticia.md`

### 4. Categorias de Documentos

#### 4.1 — Procedimento e Documentos do Divórcio
Consultar `references/divorcio-procedimento-documentos.md` para:
- 3 modalidades de divórcio (extrajudicial, consensual judicial, litigioso)
- Templates: escritura pública, petição inicial consensual, petição inicial litigiosa
- Procedimento das ações de família (CPC arts. 693-699)
- Mediação e conciliação obrigatórias
- Tutela de urgência para alimentos provisórios

#### 4.2 — Regimes de Bens e Partilha
Consultar `references/regimes-bens-partilha.md` para:
- 6 regimes de bens com regras de comunicabilidade
- Súmula 377 STF (separação obrigatória)
- Checklist completo de partilha (5 dimensões)
- Aspectos tributários (ITBI, ITCMD, IR, ganho de capital)
- Atenção especial à reforma do ITCMD 2026-2027
- Pacto antenupcial e contrato de convivência (prevenção)

#### 4.3 — Pensão Alimentícia
Consultar `references/pensao-alimenticia.md` para:
- Alimentos para filhos (binômio necessidade × possibilidade)
- Alimentos para ex-cônjuge (caráter transitório)
- Alimentos gravídicos (Lei 11.804/08)
- Critérios usuais de fixação (CLT, autônomo, empresário)
- Execução com prisão civil (CPC art. 528) e penhora (CPC art. 528, §8º)
- Checklist de pensão (5 dimensões)
- Revisão, exoneração, cessação

#### 4.4 — Guarda dos Filhos e Proteção
Consultar `references/guarda-protecao-criancas.md` para:
- Guarda compartilhada (regra — Lei 13.058/14, alterações Lei 14.713/23)
- Guarda unilateral (excepcional)
- Plano parental detalhado (template)
- Convivência, mudança de domicílio, viagens
- Alienação parental (Lei 12.318/10)
- Lei Maria da Penha em contexto familiar (Lei 11.340/06)

#### 4.5 — Interface com Direito Societário
Consultar `references/interface-societario.md` para:
- Holdings familiares e risco de partilha
- Partilha envolvendo quotas de LTDA ou ações de S.A.
- Avaliação de participações societárias (valor patrimonial, EBITDA, DCF)
- Risco de ocultação patrimonial em empresas operacionais
- Pacto antenupcial e contrato de convivência para empresários
- Acordo de sócios — cláusulas que afetam cônjuge em divórcio
- Quando complementar com o skill `direito-societario-br`

#### 4.6 — Revisão de .docx com marcas de revisão
Consultar **`../../shared/revisao-docx-tracked-changes.md`** e usar a biblioteca
**`../../shared/ooxml_redline.py`**. Ambos ficam em `shared/`, na raiz do plugin, compartilhados
com o skill `direito-societario-br` — não duplicar; corrigir sempre no compartilhado.

Aplica-se a **qualquer** `.docx` jurídico editado aqui: minuta de divórcio consensual, escritura
pública, pacto antenupcial, contrato de convivência, plano parental, acordo de alimentos. Alterar
o texto direto, sem marcas, impede a outra parte e o cartório de verem o que mudou.

**Tarefa de tier FULL.** Os três modos de falha são silenciosos: arquivo que o Word recusa; perda
de texto por tratar marca de fim de parágrafo como exclusão em vez de fusão; e renumeração
automática que quebra remissões internas. Abaixo do tier FULL, não gerar marcas — entregar `.docx`
limpo com as alterações aplicadas mais um quadro comparativo, dizendo por que as marcas não foram
geradas.

Especificidades de família que a referência genérica não cobre:

- **Escritura pública de divórcio** (Lei 11.441/07) é minutada pelo cartório. O papel aqui é
  revisar a minuta recebida com marcas, para o tabelião ver as alterações propostas — nunca
  devolver texto reescrito em silêncio.
- **Nomenclatura**: `[Nome Original] - Comentado.docx` (com marcas) e `- revisado.docx` (limpa),
  igual ao skill irmão.
- **Dados sensíveis.** Minutas de família carregam CPF, endereço, dados de menores e, às vezes,
  relato de violência. Antes de entregar, conferir que os comentários e as marcas não expõem
  informação que a outra parte não deveria receber: o painel de revisões preserva **autor e data**
  de cada alteração, e comentários internos de estratégia ficam visíveis para quem abrir o arquivo.
  Remover notas internas antes de circular.
- **Valores e datas** alterados em cláusula de alimentos exigem conferência dupla após aceitar as
  marcas: um número trocado numa fusão de parágrafo é o defeito mais caro possível aqui.

#### 4.7 — Registro de atualizações legislativas
Consultar `references/atualizacoes-legislativas.md` antes de fundamentar recomendação de alto
impacto: registra o que já mudou (Res. CNJ 571/2024, Tema 821 do STF, EREsp 1.623.858/MG,
Lei 14.340/2022, Lei 14.713/2023), o que está apenas em tramitação (PL 4/2025) e a rotina de
reverificação.

## Regras de Ouro

1. **Nunca fornecer parecer jurídico definitivo** — esta é uma ferramenta de apoio; toda
   análise deve ser revisada por advogado(a) especializado(a) em direito de família
2. **Sempre sugerir mediação prévia** em casos consensuais e em desacordos não-violentos
3. **Em indícios de violência doméstica** — NÃO insistir em mediação; direcionar para
   delegacia especializada e/ou assistência jurídica gratuita (Lei Maria da Penha)
4. **Citar fundamento legal** — artigo, lei, jurisprudência STJ/STF — e **sinalizar quando o
   fundamento não foi verificado** contra fonte oficial nesta sessão
5. **Considerar variação regional** — TJSP, TJRJ, TJMG e demais Tribunais podem divergir
6. **Pensão pode ser fixada em salários mínimos** — o STF firmou, no ARE 842.157 (Tema 821 de
   repercussão geral), que "a utilização do salário mínimo como base de cálculo do valor de pensão
   alimentícia não viola a Constituição Federal". A vedação do CF art. 7º, IV alcança obrigações
   **sem** caráter alimentar. O que não pode é ficar sem critério de reajuste algum
7. **Filhos menores ou incapazes: extrajudicial é possível desde 2024** — desde que guarda,
   convivência e alimentos já estejam resolvidos por decisão judicial, o que deve constar do corpo
   da escritura (Res. CNJ 571/2024, que deu nova redação ao art. 34, § 2º da Res. CNJ 35/2007).
   Sem essa prévia resolução judicial, a via continua sendo a judicial
8. **MP obrigatório quando há menores** em divórcio judicial
9. **Plano parental detalhado** — minimiza conflitos futuros
10. **ITCMD em partilha desigual** — alertar sobre risco fiscal
11. **Bens no exterior** — declaração CBE/BACEN; ocultação é crime
12. **Holdings familiares** — sempre avaliar comunicabilidade no regime aplicável
13. **Nunca entregar um `.docx` gerado sem tê-lo aberto** — XML bem-formado não é evidência de
    que o Word aceita o arquivo, nem de que o conteúdo sobreviveu às marcas de revisão. Ver §4.6

## Padrões de Risco — Classificação

**🔴 CRÍTICO — Risco elevado, ação imediata**
- Violação de norma de ordem pública (renúncia a alimentos de filho menor)
- Divórcio extrajudicial com filhos menores sem prévia resolução judicial de guarda e alimentos
- Indícios de violência doméstica não tratados adequadamente
- Pensão sem qualquer critério de reajuste definido
- Ocultação patrimonial detectada
- Acordo sem plano parental em casos com menores
- Partilha desigual sem ITCMD recolhido

**🟡 ATENÇÃO — Risco moderado, negociável**
- Cláusula de reajuste de pensão ausente
- Plano parental genérico (sem detalhamento de feriados, viagens)
- Avaliação patrimonial desatualizada
- Acordo de sócios sem cláusula de divórcio
- Renúncia entre cônjuges sem assistência jurídica documentada

**🟢 ADEQUADO — Em conformidade**
- Documentação completa e atualizada
- Plano parental detalhado e factível
- Pensão com critério objetivo e reajuste
- Partilha com avaliação atualizada e tributos calculados

## Disclaimer

Direito de família envolve aspectos pessoais sensíveis. As referências aqui são gerais —
TJSP, TJRJ, TJMG, TJRS e demais Tribunais podem ter entendimentos divergentes em pontos
específicos. Toda análise deve considerar a jurisprudência local atualizada e ser revisada
por advogado(a) especializado(a) antes de qualquer ato com efeitos jurídicos definitivos.

Atenção redobrada em casos envolvendo:
- Patrimônio em múltiplas jurisdições
- Empresas em operação ou em processos de M&A
- Holding familiar e estruturas de planejamento sucessório
- Filhos com necessidades especiais
- Indícios de violência doméstica (encaminhar a serviços especializados)
- Histórico de alienação parental

## Formato de Saída

### Para análise/review:
```markdown
# Análise Jurídica — [Documento]

## Resumo Executivo
[Conclusão geral e recomendações prioritárias]

## Contexto Identificado
[Modalidade, regime de bens, composição familiar, patrimônio]

## Red Flags
[Tabela com flags críticos]

## Análise Detalhada
[Cláusula a cláusula]

## Recomendações
[Lista priorizada]

## Fundamentação Legal
[Artigos e leis citados]

## Disclaimer
[aviso sobre revisão por advogado especializado]
```

### Para minutas/elaboração:
Gerar documento completo em formato .docx (quando disponível) ou markdown, com:
- Cabeçalho formal
- Qualificação completa das partes
- Campos [●] para preenchimento de dados específicos
- Numeração de cláusulas
- Notas com fundamentação legal
- Fecho com local, data, assinaturas (e testemunhas se aplicável)
