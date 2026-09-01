# Interface com Direito Societário — Referência

Conexões críticas entre Direito de Família e Direito Societário em casos de divórcio
envolvendo empresários, investidores e famílias com patrimônio estruturado em sociedades.

Este arquivo é a "ponte" entre o skill `direito-familia-br` e o skill complementar
`direito-societario-br`. Para análise societária aprofundada (avaliação de empresas,
governança em LTDA/S.A., acordos de sócios), consultar o skill irmão.

## 8. Conexões com Direito Societário e Empresarial

### 8.1 — Holdings Familiares e Planejamento Sucessório

Holdings patrimoniais e familiares têm dupla função em direito de família:
- **Estruturação**: organizar o patrimônio para sucessão e proteção
- **Risco em divórcio**: dependendo da estrutura, quotas da holding podem ser comuns
  ao casal e sujeitas a partilha

**Pontos de atenção:**
- Quem é sócio da holding? (cônjuge incluído ou não?)
- Quotas/ações da holding integram ou não a partilha?
- Acordo de sócios prevê regras para divórcio? (lock-up, exclusão)
- Bens incluídos na holding adquiridos antes ou durante o casamento?

### 8.2 — Partilha Envolvendo Quotas/Ações de Empresa Operacional

**Cenário típico**: cônjuge é sócio em LTDA ou S.A. e o outro tem direito à meação.

**Caminhos possíveis:**
- **Cônjuge não-sócio recebe quotas/ações**: complica governança da empresa
  (novo sócio pode não ser desejado pelos demais; verificar acordo de sócios)
- **Cônjuge não-sócio recebe equivalente em dinheiro**: avaliação da participação
- **Cônjuge não-sócio recebe outros bens em compensação**: torna patrimonial

**Avaliação da participação** (mesmo que não vá ser transferida):
- Valor patrimonial contábil (geralmente subavaliado)
- Valor patrimonial ajustado a mercado
- Múltiplo de EBITDA do setor
- Fluxo de caixa descontado (DCF)
- Avaliação por perito independente (quando litigioso)

**Risco de ocultação patrimonial:**
- Aumento súbito de despesas operacionais antes do divórcio
- Diminuição de pró-labore e dividendos
- Distribuição de lucros para outros sócios (laranjas)
- Operações com partes relacionadas (vendas a preços não-mercado)
- Investigação contábil pode ser necessária

### 8.3 — Acordo Antenupcial e Pacto de Convivência (Prevenção)

Para empresários e investidores, fortemente recomendável:
- **Pacto antenupcial** (casamento) com regime de separação total
- **Contrato de convivência** (união estável) com regime de separação total
- Cláusulas que excluem expressamente: bens da empresa, holding familiar,
  participações societárias atuais e futuras
- Definir tratamento de aquestos derivados de bens particulares
- Cláusula de renúncia a alimentos pós-divórcio entre cônjuges (controvertido,
  mas possível para ex-cônjuge — não para filhos, que são irrenunciáveis)

## Quando Acionar o Skill Companheiro (`direito-societario-br`)

O skill companheiro deve ser referenciado (ou suas referências consultadas) em situações como:

| Situação | Skill a Consultar | Referência específica |
|---|---|---|
| Avaliação de empresa para fins de meação | direito-societario-br | `references/ma-operations.md` (métodos de valuation) |
| Acordo de sócios com cláusula de divórcio | direito-societario-br | `references/acordo-socios.md` |
| Estruturação de holding familiar | direito-societario-br | `references/constituicao-societaria.md` |
| Stock options/ILP do cônjuge na partilha | direito-societario-br | `references/vc-startups.md` (vesting) |
| Empresa em rodada de investimento durante divórcio | direito-societario-br | `references/vc-startups.md` |

## Workflow Combinado — Divórcio com Empresa

Quando o usuário traz caso envolvendo empresa significativa:

### Etapa 1 — Triagem (este skill)
- Confirmar regime de bens
- Confirmar data de aquisição da participação (antes/durante o casamento)
- Confirmar tipo de participação (LTDA, S.A., holding)
- Identificar se há acordo de sócios

### Etapa 2 — Análise Societária (skill companheiro)
- Verificar contrato social/estatuto/acordo
- Identificar restrições à transferência (lock-up, ROFR, drag along)
- Avaliar a participação (método adequado: VPL, EBITDA múltiplo, DCF)
- Verificar passivos ocultos da empresa que afetariam o valor

### Etapa 3 — Definição da Solução (este skill)
- Cônjuge não-sócio recebe quotas/ações? (geralmente indesejável)
- Cônjuge não-sócio recebe equivalente em dinheiro?
- Cônjuge não-sócio recebe outros bens em compensação?
- Pagamento parcelado ou à vista?

### Etapa 4 — Documentação (ambos os skills)
- Acordo de partilha (este skill)
- Alteração contratual da empresa (skill companheiro)
- Cessão de quotas/ações se aplicável (skill companheiro)

## Sinais de Ocultação Patrimonial em Empresas

Atenção redobrada quando o cônjuge sócio apresenta:
- Queda súbita de pró-labore nos 12 meses anteriores ao divórcio
- Aumento de despesas operacionais ou "consultorias" pagas a terceiros
- Distribuição desproporcional de lucros para outros sócios
- Operações com partes relacionadas a preços não-mercado
- Aumento de capital ou emissão de novas quotas/ações com diluição do cônjuge
- Reorganização societária recente (cisão, transferência para holding)
- Empresa "parada" ou "sem movimento" mas com indicadores de atividade

Em qualquer destes casos, recomendar:
- Investigação contábil por perito independente
- Quebra de sigilo bancário judicial (CPC art. 396)
- Tutela de urgência para indisponibilidade de bens (CPC art. 300)
- Investigação da rede de sócios e empresas vinculadas (CADE, JUCESP, etc.)
