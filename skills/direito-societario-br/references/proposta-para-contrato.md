# Geração de Contrato Comercial a partir de Proposta — Sub-Skill

## Quando Ativar

Ativar quando o usuário:
- Enviar uma proposta comercial e pedir para gerar o contrato correspondente
- Mencionar "transformar proposta em contrato", "minutar contrato da proposta",
  "formalizar esta proposta", "contrato baseado nesta proposta"
- Anexar PDF/documento de proposta comercial e pedir minuta contratual
- Descrever verbalmente os termos de um negócio e pedir a formalização

## Visão Geral

Uma proposta comercial contém os termos essenciais de um negócio (escopo, preço, prazo),
mas faltam-lhe as proteções jurídicas, cláusulas obrigatórias e boilerplate que um contrato
exige. Este sub-skill converte sistematicamente os elementos da proposta em um contrato
completo e juridicamente robusto.

## Fluxo de Trabalho — 5 Etapas

### Etapa 1: Extração e Mapeamento da Proposta

Ao receber a proposta (arquivo ou texto), extrair e mapear os seguintes campos:

| Campo da Proposta | Destino no Contrato | Obrigatório |
|---|---|---|
| Nome/razão social do ofertante | Qualificação da CONTRATADA | Sim |
| Nome/razão social do cliente | Qualificação da CONTRATANTE | Sim |
| CNPJ/CPF de ambas as partes | Qualificação das partes | Sim |
| Descrição dos serviços/produtos | Cláusula de Objeto (escopo) | Sim |
| Escopo detalhado / SOW | Anexo de Escopo ou Cláusula de Objeto | Sim |
| Entregáveis (deliverables) | Cláusula de Obrigações / Anexo | Sim |
| Preço / valor total | Cláusula de Remuneração | Sim |
| Forma de pagamento (parcelas, NF) | Cláusula de Condições de Pagamento | Sim |
| Prazo de execução | Cláusula de Vigência / Cronograma | Sim |
| Cronograma / milestones | Anexo de Cronograma | Se existir |
| SLA / níveis de serviço | Cláusula de SLA ou Anexo | Se existir |
| Equipe alocada | Cláusula de Recursos / Equipe-Chave | Se existir |
| Premissas e exclusões | Cláusula de Premissas e Limitações | Se existir |
| Validade da proposta | Não migra (informativo) | — |
| Condições especiais | Cláusulas específicas | Se existir |

### Etapa 2: Identificação de Lacunas — AskUserQuestion

> **Ferramenta:** em Cowork e Claude Code, usar `AskUserQuestion` (máx. 4 perguntas por chamada,
> 2-4 opções por pergunta, cada opção com `label` curto e `description`). Em ambiente sem a
> ferramenta, fazer as perguntas em texto numerado. **Não existe ferramenta `ask_user_input`.**
> Se a sessão for não assistida, adotar a opção mais conservadora e declarar a premissa no output.

Após o mapeamento, identificar quais informações estão faltando na proposta e que são
necessárias para o contrato. Usar `AskUserQuestion` para coletar.

**Coleta obrigatória — sempre perguntar se não constar na proposta:**

```
AskUserQuestion({
  questions: [
    {
      header: "Tipo de contrato",
      question: "Qual o tipo de contrato mais adequado?",
      multiSelect: false,
      options: [
        { label: "Prestação de serviços", description: "Obrigação de fazer — CC art. 593 e ss. Atenção ao risco de pejotização" },
        { label: "Fornecimento", description: "Compra e venda de produtos com entrega continuada ou parcelada" },
        { label: "Licenciamento", description: "Software ou tecnologia — Lei 9.609/98 e Lei 9.279/96" },
        { label: "Misto", description: "Serviço + fornecimento — exige separar escopo, preço e responsabilidade de cada parcela" }
      ]
    },
    {
      header: "Sua posição",
      question: "Qual a posição do seu cliente neste contrato?",
      multiSelect: false,
      options: [
        { label: "Contratante", description: "Quem paga — foco em SLA, garantias, propriedade dos entregáveis e saída" },
        { label: "Contratada", description: "Quem entrega — foco em limitação de responsabilidade, escopo fechado e reajuste" },
        { label: "Ambas as partes", description: "Minuta equilibrada, sem viés — declarar isso no documento" }
      ]
    }
  ]
})
```

**Coleta situacional — perguntar conforme o tipo de contrato:**

Para contratos de prestação de serviços:
```
AskUserQuestion({
  questions: [
    {
      header: "Rescisão",
      question: "Como deve funcionar a rescisão imotivada?",
      multiSelect: false,
      options: [
        { label: "Bilateral, aviso de 30 dias", description: "Padrão de mercado para serviços recorrentes" },
        { label: "Bilateral, aviso de 60 dias", description: "Adequado quando há equipe alocada ou investimento inicial" },
        { label: "Só por justa causa", description: "Vigência rígida — combinar com multa compensatória" },
        { label: "Assimétrica", description: "Só uma das partes pode denunciar — dizer qual e prever compensação" }
      ]
    },
    {
      header: "Limite de resp.",
      question: "Qual o limite de responsabilidade desejado?",
      multiSelect: false,
      options: [
        { label: "Valor do contrato", description: "Teto no valor total pago ou a pagar" },
        { label: "12 meses de remuneração", description: "Comum em contratos de prazo indeterminado" },
        { label: "Sem teto para danos diretos", description: "Posição de contratante — exclui lucros cessantes" },
        { label: "Preciso de orientação", description: "Apresentar as opções com prós e contras antes de decidir" }
      ]
    },
    {
      header: "Disputas",
      question: "Como resolver disputas?",
      multiSelect: false,
      options: [
        { label: "Foro da sede da contratante", description: "Judicial — mais barato, mais lento, público" },
        { label: "Foro da sede da contratada", description: "Judicial — vantagem logística para quem entrega" },
        { label: "Arbitragem", description: "Lei 9.307/96. Sigilosa e rápida, mas custo alto — inviável em contrato de baixo valor" },
        { label: "Mediação e depois arbitragem", description: "Escalonada — tentativa de composição antes do procedimento" }
      ]
    }
  ]
})
```

Para contratos com componente de tecnologia/software:
```
AskUserQuestion({
  questions: [
    {
      header: "Titularidade da PI",
      question: "Quem detém a propriedade intelectual do que será desenvolvido?",
      multiSelect: false,
      options: [
        { label: "Contratante", description: "Cessão total e definitiva — exige cláusula expressa de cessão (Lei 9.610/98, art. 49)" },
        { label: "Contratada, com licença", description: "Titularidade fica com quem desenvolve; contratante recebe licença de uso — definir escopo, prazo e exclusividade" },
        { label: "Compartilhada", description: "Cotitularidade — definir regras de exploração, sublicenciamento e receita" },
        { label: "Depende do entregável", description: "Separar background IP (preexistente) de foreground IP (desenvolvido no projeto)" }
      ]
    },
    {
      header: "Dados pessoais",
      question: "Haverá tratamento de dados pessoais?",
      multiSelect: false,
      options: [
        { label: "Sim, incluir DPA completo", description: "Definir controlador/operador, bases legais, incidentes, suboperadores, eliminação" },
        { label: "Sim, com transf. internacional", description: "Obrigatório adotar as cláusulas-padrão da Resolução CD/ANPD 19/2024" },
        { label: "Possivelmente", description: "Incluir cláusula LGPD de contingência e obrigação de comunicar se passar a haver tratamento" },
        { label: "Não", description: "Apenas dados de pessoa jurídica — manter cláusula mínima de confidencialidade" }
      ]
    }
  ]
})
```

Para contratos de fornecimento:
```
AskUserQuestion({
  questions: [
    {
      header: "Aceite",
      question: "Como funciona o aceite dos produtos ou entregas?",
      multiSelect: false,
      options: [
        { label: "Automático na entrega", description: "Favorece a contratada — sem janela de recusa" },
        { label: "Inspeção em 7 dias", description: "Aceite tácito se não houver recusa fundamentada no prazo" },
        { label: "Inspeção em 30 dias", description: "Adequado a entregáveis complexos ou que exijam homologação" },
        { label: "Aceite formal por escrito", description: "Termo de aceite assinado — favorece a contratante, mas travar prazo para evitar aceite indefinido" }
      ]
    },
    {
      header: "Garantia",
      question: "Qual o regime de garantia?",
      multiSelect: false,
      options: [
        { label: "Legal apenas", description: "Vício redibitório do CC arts. 441-446; CDC só se houver relação de consumo" },
        { label: "Estendida — 6 meses", description: "Correção de defeitos sem custo no período" },
        { label: "Estendida — 12 meses", description: "Padrão em software e equipamentos" },
        { label: "Sem garantia adicional", description: "Só a legal — sinalizar como ponto de risco para a contratante" }
      ]
    }
  ]
})
```

Para qualquer contrato com preço e vigência superior a 12 meses (reforma tributária):
```
AskUserQuestion({
  questions: [
    {
      header: "Preço e tributos",
      question: "Como o preço deve tratar os tributos sobre o consumo (IBS/CBS) na transição até 2033?",
      multiSelect: false,
      options: [
        { label: "Preço líquido de tributos", description: "Tributos destacados em nota e acrescidos ao preço — repasse integral à contratante" },
        { label: "Preço com tributos inclusos", description: "Contratada absorve; prever renegociação se a carga variar acima de um gatilho" },
        { label: "Repasse com gatilho", description: "Ajuste automático quando a variação de carga exceder percentual definido" },
        { label: "Preciso de orientação", description: "Explicar o risco da transição 2026-2033 antes de decidir — ver references/tributacao-contratos.md" }
      ]
    }
  ]
})
```

### Etapa 3: Geração do Contrato

Com todas as informações coletadas, gerar o contrato seguindo esta estrutura:

```
CONTRATO DE [TIPO] Nº [●]/[ANO]

Pelo presente instrumento particular, as partes abaixo qualificadas:

CONTRATANTE: [razão social], [tipo societário], inscrita no CNPJ/MF sob
nº [●], com sede em [endereço completo], neste ato representada por
[nome], [cargo], portador(a) do RG nº [●] e CPF/MF nº [●];

CONTRATADA: [razão social], [tipo societário], inscrita no CNPJ/MF sob
nº [●], com sede em [endereço completo], neste ato representada por
[nome], [cargo], portador(a) do RG nº [●] e CPF/MF nº [●];

doravante denominadas, individualmente, "Parte" e, em conjunto, "Partes",

CONSIDERANDO QUE:
(a) [contexto extraído da proposta — natureza do negócio]
(b) [motivação — por que as partes estão contratando]
(c) [referência à proposta comercial nº X, de [data], se aplicável]

Resolvem celebrar o presente Contrato, que se regerá pelas cláusulas
e condições a seguir:

CLÁUSULA 1ª — DEFINIÇÕES
[Termos definidos em ordem alfabética]

CLÁUSULA 2ª — OBJETO
[Extraído do escopo da proposta — expandir e detalhar]

CLÁUSULA 3ª — OBRIGAÇÕES DA CONTRATADA
[Converter deliverables da proposta em obrigações formais]

CLÁUSULA 4ª — OBRIGAÇÕES DA CONTRATANTE
[Aprovações, acesso, informações, pagamento]

CLÁUSULA 5ª — REMUNERAÇÃO E CONDIÇÕES DE PAGAMENTO
[Converter preço/parcelas da proposta]
5.1. Valor total: R$ [●] ([extenso])
5.2. Forma de pagamento: [parcelas conforme proposta]
5.3. Nota fiscal: emitida em até [5] dias úteis antes do vencimento
5.4. Reajuste: [IPCA/IGP-M/sem reajuste — conforme prazo do contrato]
5.5. Multa por atraso: [2% + juros de 1% a.m. — padrão CC art. 406]
5.6. Impostos: [retenções na fonte — ISS, IR, CSLL, PIS, COFINS conforme IN RFB]

CLÁUSULA 6ª — PRAZO E VIGÊNCIA
[Converter prazo de execução da proposta]
6.1. Vigência: [●] meses a contar da assinatura
6.2. Renovação: [automática por períodos iguais / mediante aditivo]

CLÁUSULA 7ª — CONFIDENCIALIDADE
[Cláusula padrão — CC art. 422, boa-fé objetiva]

CLÁUSULA 8ª — PROPRIEDADE INTELECTUAL
[Conforme resposta do AskUserQuestion]

CLÁUSULA 9ª — PROTEÇÃO DE DADOS — LGPD
[Se aplicável — conforme references/compliance-governanca.md]

CLÁUSULA 10ª — LIMITAÇÃO DE RESPONSABILIDADE
[Conforme resposta do AskUserQuestion]
10.1. Exclusão de danos indiretos, lucros cessantes e danos morais
10.2. Cap: [valor do contrato / 12 meses de remuneração]
10.3. Exceções ao cap: dolo, fraude, violação de confidencialidade, PI, LGPD

CLÁUSULA 11ª — RESCISÃO
[Conforme resposta do AskUserQuestion]
11.1. Rescisão imotivada: mediante aviso prévio de [30/60] dias
11.2. Rescisão por justa causa: inadimplemento não sanado em [15] dias após notificação
11.3. Efeitos: pagamento dos serviços prestados até a data, devolução de materiais

CLÁUSULA 12ª — ANTICORRUPÇÃO
[Cláusula padrão — Lei 12.846/13]

CLÁUSULA 13ª — DISPOSIÇÕES GERAIS
13.1. Cessão: vedada sem anuência prévia por escrito
13.2. Integralidade: este Contrato substitui todos os entendimentos anteriores
13.3. Tolerância: não implica renúncia a direitos
13.4. Independência das cláusulas: nulidade parcial não afeta o todo
13.5. Alterações: somente mediante aditivo escrito assinado pelas Partes
13.6. Comunicações: por escrito, aos endereços das Partes

CLÁUSULA 14ª — RESOLUÇÃO DE DISPUTAS
[Conforme resposta do AskUserQuestion — foro ou arbitragem]

E, por estarem justas e contratadas, as Partes assinam o presente
instrumento em 2 (duas) vias de igual teor e forma, na presença de
2 (duas) testemunhas.

[Local], [data]

_________________________          _________________________
CONTRATANTE                        CONTRATADA

Testemunhas:
1. Nome: _________________ CPF: _________________
2. Nome: _________________ CPF: _________________
```

### Etapa 4: Validação — Checklist Pós-Geração

Após gerar o contrato, verificar automaticamente:

- [ ] Todas as informações da proposta foram incorporadas ao contrato
- [ ] Campos [●] estão marcados onde dados ainda faltam
- [ ] Escopo do contrato é consistente com a proposta (sem omissões ou adições indevidas)
- [ ] Preço e condições de pagamento conferem com a proposta
- [ ] Prazo e cronograma conferem com a proposta
- [ ] Cláusulas obrigatórias estão presentes (LGPD, anticorrupção, confidencialidade)
- [ ] Limitação de responsabilidade está equilibrada
- [ ] Rescisão tem mecanismo funcional com aviso prévio
- [ ] Penalidade por mora está dentro dos limites legais (CC art. 412 — penalidade ≤ valor da obrigação)
- [ ] Duas testemunhas previstas (CPC art. 784, IV)
- [ ] Foro ou arbitragem definidos
- [ ] Reajuste previsto se prazo > 12 meses
- [ ] Retenções tributárias mencionadas (ISS, IR, CSLL, PIS/COFINS)
- [ ] Não há contradições entre cláusulas do contrato e termos da proposta

### Etapa 5: Apresentação e Iteração

Ao apresentar o contrato ao usuário:
1. Entregar o contrato completo em formato .docx (quando possível) ou markdown
2. Destacar os campos [●] que precisam ser preenchidos pelo usuário
3. Listar as decisões tomadas (ex.: "Incluí limitação de responsabilidade ao valor do contrato conforme sua escolha")
4. Indicar cláusulas que podem precisar de ajuste conforme negociação
5. Oferecer: "Quer que eu ajuste alguma cláusula, adicione SLA, ou inclua um Anexo de Escopo mais detalhado?"

## Mapeamento Proposta → Contrato — Por Tipo

### Proposta de Prestação de Serviços

| Elemento da Proposta | Cláusula Contratual | Notas |
|---|---|---|
| Descrição dos serviços | Cláusula de Objeto | Expandir com obrigações de meio vs. resultado |
| Escopo / SOW | Anexo I — Escopo de Serviços | Detalhar deliverables, aceite, critérios |
| Equipe proposta | Cláusula de Equipe-Chave | Incluir restrição de substituição sem aprovação |
| Preço por hora / projeto | Cláusula de Remuneração | Definir: fixo, variável, teto (cap) |
| Cronograma | Anexo II — Cronograma | Vincular a milestones de pagamento |
| Premissas | Cláusula de Premissas | Converter em obrigações do contratante |
| Exclusões | Cláusula de Escopo Negativo | "Não estão incluídos no objeto..." |
| SLA proposto | Anexo III — SLA | Converter em obrigações com penalidades |

### Proposta de Fornecimento de Produtos

| Elemento da Proposta | Cláusula Contratual | Notas |
|---|---|---|
| Descrição dos produtos | Cláusula de Objeto | Especificações técnicas em anexo |
| Quantidade | Cláusula de Objeto | Definir tolerância (±X%) |
| Preço unitário / total | Cláusula de Remuneração | CIF, FOB, ou entrega na sede? |
| Prazo de entrega | Cláusula de Entrega | Penalidade por atraso |
| Garantia | Cláusula de Garantia | Mínimo legal CDC ou contratual |
| Condições de pagamento | Cláusula de Pagamento | Vincular a entrega/aceite |
| Especificações técnicas | Anexo I — Especificações | Critério de conformidade |

### Proposta de Licenciamento de Software

| Elemento da Proposta | Cláusula Contratual | Notas |
|---|---|---|
| Software / módulos | Cláusula de Objeto — Licença | Escopo da licença (uso, nº de usuários) |
| Implementação | Cláusula de Implantação / SOW | Cronograma, responsabilidades |
| Treinamento | Cláusula de Treinamento | Horas, formato, materiais |
| Suporte / manutenção | Anexo de SLA | Níveis, horário, canal |
| Fee de licença | Cláusula de Remuneração — Setup | One-time ou recorrente |
| Fee mensal / anual | Cláusula de Remuneração — Recorrente | Reajuste, período mínimo |
| Customizações | Cláusula de Desenvolvimentos Adicionais | PI das customizações |
| Dados | Cláusula LGPD + DPA | Controlador/operador, subprocessadores |

## Cláusulas que a Proposta Nunca Contém (sempre adicionar)

Estas cláusulas quase nunca aparecem em propostas comerciais mas são essenciais no contrato:

1. **Definições** — termos técnicos e comerciais definidos com precisão
2. **Declarações e garantias** — ao menos declaração de poderes para contratar
3. **Confidencialidade** — obrigação recíproca, prazo de sobrevivência
4. **Propriedade intelectual** — titularidade de trabalhos desenvolvidos
5. **LGPD** — se houver qualquer tratamento de dados pessoais
6. **Anticorrupção** — declaração de conformidade (Lei 12.846/13)
7. **Limitação de responsabilidade** — cap e exclusões
8. **Força maior** — definição e consequências (CC art. 393)
9. **Cessão** — regras de transferência do contrato
10. **Rescisão** — hipóteses, aviso prévio, consequências
11. **Disposições gerais** — boilerplate (tolerância, integralidade, novação)
12. **Resolução de disputas** — foro ou arbitragem
13. **Testemunhas** — 2 testemunhas para título executivo

## Red Flags — Propostas Comerciais

Ao analisar a proposta antes de converter em contrato, alertar o usuário sobre:

| Situação na Proposta | Risco | Ação |
|---|---|---|
| Escopo vago ("serviços de consultoria em geral") | Disputas sobre o que está incluído | Detalhar no contrato com escopo positivo e negativo |
| Sem prazo definido | Obrigação perpétua | Definir vigência e renovação |
| Preço sem condições de reajuste (contrato >12 meses) | Erosão inflacionária | Incluir cláusula de reajuste (IPCA, IGP-M) |
| "Preço a combinar" para itens adicionais | Sem teto, sem controle | Definir tabela de preços unitários ou teto |
| Premissas irrealistas | Risco de atraso e culpa recíproca | Converter em CPs ou obrigações do contratante |
| SLA sem penalidade | Sem enforcement | Vincular a créditos de serviço ou rescisão |
| Sem menção a PI | Disputa futura sobre titularidade | Definir expressamente no contrato |
| Proposta unilateral (sem aceitação formal) | Prova frágil de acordo | Contrato bilateral assinado resolve |
