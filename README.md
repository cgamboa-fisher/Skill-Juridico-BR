# 🇧🇷 Direito Societário BR — Plugin para Cowork, Claude.ai e Claude Code

Skill especializado em análise, elaboração e revisão de contratos e documentos jurídicos sob a
legislação societária e empresarial brasileira. Para advogados, assessores jurídicos, venture
builders e profissionais que lidam com contratos comerciais no Brasil.

> ⚠️ **Disclaimer** — Ferramenta de apoio. Não constitui parecer jurídico e não substitui a
> consulta a advogado habilitado na OAB. Toda análise gerada deve ser revisada por profissional
> qualificado antes de uso em operação real.

**Versão 0.2.0** · Legislação verificada contra fontes oficiais em **20/08/2026**.

---

## O que mudou na 0.2.0

Esta versão corrige erros jurídicos materiais da 0.1.0 e adiciona calibração por modelo.
Ver `CHANGELOG.md` para a lista completa. Em resumo:

- **Calibração de execução por tier de modelo** (FULL / STANDARD / MÍNIMO), com gates que
  bloqueiam tarefas de alto risco em modelos que não as sustentam, e declaração de procedência
  em todo output.
- **Nove correções de fundamento legal** — EIRELI extinta, quóruns de LTDA pós-Lei 14.451/2022,
  fundamentação real do non-compete, artigos do investidor-anjo, Decreto 13.609/43 revogado,
  escopo da Lei 14.063/2020, ANPD como Agência, cláusulas-padrão de transferência internacional,
  Decreto 8.420/2015 revogado.
- **Reforma tributária do consumo** — nova referência sobre IBS/CBS em cláusulas de preço.
- **Correção da ferramenta de interação** — a 0.1.0 instruía o modelo a chamar `ask_user_input`,
  que não existe. Agora usa `AskUserQuestion`, com formato correto e fallback em texto.
- **Link morto corrigido** — o workflow de tracked changes remetia a um `CLAUDE.md` inexistente
  no repositório; agora é uma referência própria.

---

## Instalação

### Cowork (Claude desktop app)

1. Baixe o arquivo `direito-societario-br.plugin`.
2. Arraste-o para a conversa no Cowork, ou abra **Configurações → Plugins → Instalar**.
3. Confirme a instalação no card que aparece na conversa.

### Claude.ai (web e app)

1. Acesse **Configurações → Capacidades** e ative *Code execution and file creation*.
2. Em **Skills**, clique em **+ Add** e faça upload do `.plugin` (ou do `.skill` da pasta
   `skills/direito-societario-br/`).

### Claude Code

```bash
# Como plugin
claude plugin install ./direito-societario-br

# Ou apenas a skill, no diretório global
cp -r skills/direito-societario-br ~/.claude/skills/direito-societario-br
ls ~/.claude/skills/direito-societario-br/SKILL.md
```

### Desinstalar

Cowork e Claude.ai: remover em **Configurações → Plugins**.
Claude Code: `rm -rf ~/.claude/skills/direito-societario-br`

---

## Calibração por modelo

Esta skill declara um modelo mínimo recomendado e ajusta o escopo do que entrega conforme a
capacidade do modelo em execução. O objetivo é impedir o pior cenário: um contrato revisado por
um modelo de porte reduzido, devolvendo observações genéricas, e sendo lido como revisão completa.

| Tier | Modelos | Escopo |
|---|---|---|
| **FULL** | Opus 5 e equivalentes de fronteira | Escopo integral: clause-by-clause exaustiva, subagentes por área de due diligence, redline + fallback, XML de tracked changes, contratos multi-anexo |
| **STANDARD** | Sonnet não-fronteira, modelo não identificado | Análise sequencial, até ~20 cláusulas. Vedado: XML de tracked changes e DD multi-área em passe único |
| **MÍNIMO** | Haiku e modelos de porte reduzido | Somente extração de termos-chave e checklist de red flags. Vedado emitir redline ou apresentar como revisão jurídica |

Todo output abre com um bloco de procedência declarando tier, modelo configurado, escopo
executado e data da verificação de vigência legislativa. A detecção é **heurística**: o modelo
que atende um turno pode diferir do configurado, e a skill diz isso em vez de afirmar certeza.

**Recomendação:** rode em **Opus 5** para qualquer trabalho de review ou minuta destinado a uso
real. Os tiers inferiores existem para degradar com honestidade, não como equivalentes.

---

## Estrutura

```
direito-societario-br/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── direito-societario-br/
│       ├── SKILL.md
│       └── references/
│           ├── atualizacoes-legislativas.md      # ⭐ novo — registro de vigência
│           ├── tributacao-contratos.md           # ⭐ novo — IBS/CBS em cláusulas
│           ├── revisao-docx-tracked-changes.md   # ⭐ novo — corrige link morto
│           ├── constituicao-societaria.md
│           ├── acordo-socios.md
│           ├── ma-operations.md
│           ├── vc-startups.md
│           ├── compliance-governanca.md
│           ├── contratos-empresariais.md
│           └── proposta-para-contrato.md
├── CHANGELOG.md
└── README.md
```

### Referências

| Arquivo | Conteúdo |
|---|---|
| `atualizacoes-legislativas.md` | Tabela de correções obrigatórias: o que material antigo afirma de errado e qual é a citação correta, com fonte. Consultar antes de fundamentar recomendação de alto impacto |
| `tributacao-contratos.md` | IBS/CBS/IS e a transição 2026-2033. Checklist de cláusula de preço, modelo de núcleo de cláusula tributária, ITBI, ganho de capital, ágio, Tema 1.226 do STJ sobre stock options |
| `revisao-docx-tracked-changes.md` | Workflow de OOXML, tabela de erros que corrompem o `.docx` silenciosamente, checklist de entrega. Tier FULL obrigatório |
| `constituicao-societaria.md` | LTDA, S.A., SLU, SCP, SPE, consórcio. Quóruns atualizados pela Lei 14.451/2022 |
| `acordo-socios.md` | Governança, matérias reservadas, ROFR/ROFO, tag e drag along, deadlock, apuração de haveres |
| `ma-operations.md` | Share vs. asset deal, cinco fases, DD em 8 áreas, reps & warranties, mecanismos de preço, MAC |
| `vc-startups.md` | Mútuo conversível, SAFE adaptado, investidor-anjo, term sheet, vesting e ILP, antidiluição |
| `compliance-governanca.md` | LGPD e DPA, Resolução CD/ANPD 19/2024, anticorrupção, programa de integridade, ESG |
| `contratos-empresariais.md` | Joint venture, franquia, licenciamento, representação comercial, serviços, SLA, NDA |
| `proposta-para-contrato.md` | Conversão proposta → contrato em 5 etapas, mapeamento campo→cláusula, templates |

---

## Exemplos de uso

```
Revise este contrato social de LTDA e identifique cláusulas problemáticas.
Sou o sócio minoritário com 30% das quotas.
```

```
Preciso de um acordo de quotistas para uma LTDA com 3 sócios (60/25/15),
com tag along, drag along, matérias de veto e shotgun para deadlock.
```

```
Analise este term sheet de Series A. Estou no lado da startup (founder).
O investidor propõe liquidation preference de 1,5x participante com full ratchet.
```

```
Transforme esta proposta comercial em contrato de prestação de serviços.
[anexar proposta.pdf]
```

```
Monte um checklist de due diligence para aquisição de uma empresa de tecnologia
(LTDA, SaaS B2B, 50 funcionários, faturamento R$ 10M/ano).
```

---

## Skill companheiro

Para **Direito de Família** (divórcio, partilha — inclusive de participações societárias —,
pensão, guarda, regime de bens, pacto antenupcial), use o skill independente
`direito-familia-br`. Em divórcio que envolva quotas ou ações, os dois trabalham juntos.

---

## Manutenção

O maior risco desta skill não é omitir — é citar com confiança um dispositivo revogado. A
legislação societária, tributária e de proteção de dados brasileira se moveu de forma
significativa entre 2021 e 2026 e continuará se movendo.

Ao atualizar:

1. Verifique contra `planalto.gov.br` (texto consolidado) e o `gov.br` do órgão competente
   (DREI, ANPD, CVM, CADE, CGU) para a camada infralegal.
2. Registre a mudança em `references/atualizacoes-legislativas.md`, inclusive a afirmação
   errada que passa a ser armadilha.
3. Atualize a data de verificação no topo daquele arquivo, no `README.md` e no `CHANGELOG.md`.

Pull requests bem-vindos para atualização legislativa, novos templates, correção de citações e
novos sub-skills (tributário, trabalhista, regulatório).

---

## Licença

Fornecido "as-is" para uso pessoal e profissional. Não constitui assessoria jurídica. O autor
não se responsabiliza pelo uso inadequado ou por decisões tomadas com base exclusiva nas
análises geradas.

## Créditos

Desenvolvido para uso com Claude (Anthropic) e ferramentas compatíveis com o padrão Agent
Skills. Inspirado em:

- [lawvable/awesome-legal-skills](https://github.com/lawvable/awesome-legal-skills)
- [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)
- [anthropics/knowledge-work-plugins/legal](https://github.com/anthropics/knowledge-work-plugins/blob/main/legal/README.md)
