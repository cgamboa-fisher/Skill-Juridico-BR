# 🇧🇷 Direito Societário BR — Claude Code Skill

**AI-powered legal analysis, drafting, and review for Brazilian corporate and business law.**

Skill especializado em análise, elaboração e revisão de contratos e documentos jurídicos
sob a legislação societária e empresarial brasileira. Desenvolvido para advogados, assessores
jurídicos, venture builders, e profissionais que lidam com contratos comerciais no Brasil.

> ⚠️ **Disclaimer**: Este skill é uma ferramenta de apoio. Não constitui parecer jurídico
> e não substitui a consulta a advogado habilitado na OAB. Toda análise gerada deve ser
> revisada por profissional qualificado antes de uso em operações reais.

---

## Instalação

### Claude Code (Terminal / Bash)

```bash
# Clonar ou copiar a pasta do skill para o diretório de skills do Claude Code
# Opção 1 — Copiar diretamente para o diretório global de skills
cp -r direito-societario-br ~/.claude/skills/direito-societario-br

# Opção 2 — Clonar em local de sua preferência e criar symlink
cp -r direito-societario-br ~/Developer/direito-societario-br
ln -s ~/Developer/direito-societario-br ~/.claude/skills/direito-societario-br

# Verificar instalação
ls ~/.claude/skills/direito-societario-br/SKILL.md
```

### Claude Code (Desktop App)

1. Abra o Claude Code Desktop
2. Vá em **Settings** (ícone de engrenagem)
3. Navegue até **Skills**
4. Clique em **"Add Skill"** ou **"Import"**
5. Selecione a pasta `direito-societario-br` ou o arquivo `direito-societario-br.skill`
6. O skill será ativado automaticamente quando relevante

### Claude.ai (Web / App)

1. Acesse [claude.ai/settings/capabilities](https://claude.ai/settings/capabilities)
2. Ative **"Code execution and file creation"**
3. Role até a seção **Skills** e clique em **"+ Add"**
4. Faça upload do arquivo `direito-societario-br.skill`
5. Pronto — Claude ativará o skill automaticamente quando detectar contexto jurídico brasileiro

### Desinstalar

```bash
rm -rf ~/.claude/skills/direito-societario-br
```

---

## Estrutura do Skill

```
direito-societario-br/
├── SKILL.md                                   # Skill principal (382 linhas)
└── references/                                # Referências carregadas on-demand
    ├── constituicao-societaria.md             # Tipos societários (LTDA, S.A., SLU, SCP, SPE)
    ├── acordo-socios.md                       # Acordo de sócios/acionistas
    ├── ma-operations.md                       # Operações de M&A
    ├── vc-startups.md                         # Venture capital e startups
    ├── compliance-governanca.md               # LGPD, anticorrupção, ESG, governança
    ├── contratos-empresariais.md              # Contratos comerciais diversos
    └── proposta-para-contrato.md              # Sub-skill: proposta → contrato
```

---

## Descrição dos Componentes

### SKILL.md — Arquivo Principal

O arquivo raiz que o Claude carrega ao ativar o skill. Contém:

- **Legislação de referência**: tabela com 12 leis/regulamentos mapeados (CC, Lei 6.404/76, LGPD, Lei Anticorrupção, Marco Legal das Startups, etc.)
- **Interação via ask_user_input**: instruções explícitas para o Claude coletar informações faltantes via perguntas interativas com opções tappable, evitando suposições
- **Fluxo de trabalho em 4 etapas**: identificação de contexto → análise (review mode) → elaboração (draft mode) → categorização
- **Template de análise clause-by-clause**: classificação 🔴🟡🟢 com fundamentação legal, redline sugerido e fallback
- **Matriz de risco**: critérios objetivos para classificar cláusulas como críticas, atenção ou adequadas
- **10 Regras de Ouro**: princípios invioláveis (citar fundamento legal, alertar questões tributárias, 2 testemunhas, LGPD sempre, etc.)
- **Formatos de saída padronizados**: templates para análise/review e para minutas/elaboração

### references/constituicao-societaria.md
Referência completa sobre **tipos societários brasileiros**:
- LTDA (CC arts. 1.052-1.087): cláusulas obrigatórias, quóruns, integralização, cessão de quotas, exclusão de sócio
- S.A. (Lei 6.404/76): aberta vs. fechada, órgãos societários, acordo de acionistas (art. 118), direito de retirada, tag along
- SLU, SCP, SPE, Consórcio
- Checklist completo para contrato social de LTDA (19 itens)

### references/acordo-socios.md
Referência sobre **acordos de quotistas e acionistas**:
- Estrutura padrão em 6 seções (governança, transferência, deadlock, saída, acessórias)
- Matérias reservadas (lista de 15+ matérias típicas com veto rights)
- ROFR, ROFO, tag along, drag along, lock-up — mecânicas e armadilhas
- Mecanismos de deadlock (shotgun, Russian roulette, leilão reverso, mediação)
- Apuração de haveres (valor patrimonial, EBITDA, DCF, perito)
- Tabela de 9 red flags com severidade

### references/ma-operations.md
Referência sobre **fusões e aquisições no Brasil**:
- Estruturas (share deal vs. asset deal vs. incorporação/fusão/cisão)
- 5 fases da operação: preliminar → due diligence → SPA → condições precedentes → closing
- Checklist de due diligence em 8 áreas (societário, trabalhista, tributário, contratual, regulatório, PI, imobiliário, LGPD)
- Reps & warranties — padrões brasileiros, knowledge qualifiers, disclosure schedules
- Mecanismos de preço (locked box vs. completion accounts vs. earn-out)
- Escrow/holdback — percentuais e prazos de mercado
- Cláusula MAC com carve-outs típicos
- Aspectos tributários (ganho de capital PF/PJ, ITBI, ágio)
- Tabela de 9 red flags

### references/vc-startups.md
Referência sobre **venture capital e startups**:
- Mútuo conversível (instrumento brasileiro — diferenças do SAFE americano)
- Contrato de opção de compra de participação
- Investidor-anjo (LC 182/21)
- Term sheet de rodada — termos econômicos (liquidation preference, antidiluição) e de controle (board, veto, drag/tag)
- Vesting/ILP: stock options (Lei 6.404/76, art. 168 §3º), vesting de quotas (LTDA), phantom stock/SAR
- Good leaver / bad leaver
- Checklist de rodada de investimento (12 itens)
- Tabela de 9 red flags

### references/compliance-governanca.md
Referência sobre **compliance corporativo**:
- LGPD em contratos: quando incluir, definições-chave, 12 cláusulas obrigatórias/recomendadas, modelo completo de DPA
- Lei Anticorrupção: aplicação em contratos, modelo de cláusula anticorrupção, programa de integridade
- Governança corporativa: LTDA e S.A. fechada, referências IBGC
- ESG em cláusulas contratuais: modelo de cláusula
- Checklist de compliance em contratos (11 itens)

### references/contratos-empresariais.md
Referência sobre **contratos comerciais diversos**:
- Joint venture (contratual e societária)
- Franquia (Lei 13.966/19 — COF, cláusulas obrigatórias)
- Licenciamento de tecnologia/PI (INPI, tipos de licença, royalties, dedutibilidade)
- Representação comercial (Lei 4.886/65 — indenização mínima obrigatória)
- Prestação de serviços (risco de pejotização)
- NDA/Confidencialidade
- Cessão de direitos autorais (Lei 9.610/98)
- SLA — Service Level Agreement
- Boilerplate brasileiro (12 cláusulas gerais padrão)

### references/proposta-para-contrato.md — Sub-Skill
**Workflow de conversão de proposta comercial em contrato**, com:
- Etapa 1: extração e mapeamento automático (tabela campo→cláusula)
- Etapa 2: coleta interativa de lacunas via `ask_user_input` (4 blocos de perguntas por tipo de contrato)
- Etapa 3: geração do contrato completo (template com 14 cláusulas)
- Etapa 4: checklist de validação pós-geração (14 verificações automáticas)
- Etapa 5: apresentação e iteração com o usuário
- 3 tabelas de mapeamento por tipo (serviços, fornecimento, software)
- Lista de 13 cláusulas que propostas nunca contêm mas contratos sempre precisam
- Red flags de propostas comerciais

---

## Exemplos de Uso

### Revisão de Contrato
```
Revise este contrato social de LTDA e identifique cláusulas problemáticas.
Sou o sócio minoritário com 30% das quotas.
```

### Elaboração de Acordo de Sócios
```
Preciso de um acordo de quotistas para uma LTDA com 3 sócios (60/25/15).
Quero incluir tag along, drag along, matérias de veto, e cláusula shotgun para deadlock.
```

### Análise de Term Sheet
```
Analise este term sheet de Series A. Estou no lado da startup (founder).
O investidor propõe liquidation preference de 1.5x participante com full ratchet.
```

### Conversão de Proposta em Contrato
```
Transforme esta proposta comercial em contrato formal de prestação de serviços.
[anexar proposta.pdf]
```

### Due Diligence
```
Monte um checklist de due diligence para aquisição de uma empresa de tecnologia
(LTDA, SaaS B2B, 50 funcionários, faturamento R$10M/ano).
```

---

## Legislação Coberta

| Lei | Escopo no Skill |
|---|---|
| Código Civil (Lei 10.406/02) | Sociedades, contratos, obrigações |
| Lei das S.A. (Lei 6.404/76) | Sociedades por ações, governança |
| Lei de Liberdade Econômica (Lei 13.874/19) | SLU, simplificação |
| Marco Legal das Startups (LC 182/21) | Investidor-anjo, sandbox |
| LGPD (Lei 13.709/18) | Proteção de dados em contratos |
| Lei Anticorrupção (Lei 12.846/13) | Compliance, responsabilidade PJ |
| Lei de Recuperação Judicial (Lei 11.101/05) | Recuperação e falência |
| Lei de PI (Lei 9.279/96) | Licenciamento, patentes, marcas |
| Lei do CADE (Lei 12.529/11) | Atos de concentração |
| Lei de Arbitragem (Lei 9.307/96) | Cláusula arbitral |
| Lei de Franquias (Lei 13.966/19) | COF, contrato de franquia |
| CLT | Non-compete, vesting, vínculo |
| Lei de Direitos Autorais (Lei 9.610/98) | Cessão, software |
| Lei de Software (Lei 9.609/98) | Titularidade, licenciamento |
| CPC (Lei 13.105/15) | Título executivo (art. 784) |

---

## Compatibilidade

| Ferramenta | Suporte |
|---|---|
| Claude Code | ✅ Nativo |
| Claude.ai (Pro/Max/Team/Enterprise) | ✅ Via upload de .skill |
| Claude Desktop | ✅ Via import |
| OpenAI Codex | ✅ Copiar para diretório de skills |
| Cursor | ✅ Copiar para diretório de skills |
| Gemini CLI | ✅ Via conversão (scripts disponíveis em repos como alirezarezvani/claude-skills) |

---

## Licença

Este skill é fornecido "as-is" para uso pessoal e profissional. Não constitui assessoria
jurídica. O autor não se responsabiliza pelo uso inadequado ou por decisões tomadas com
base exclusiva nas análises geradas por este skill.

O conteúdo jurídico reflete a legislação brasileira vigente até abril de 2026. Alterações
legislativas posteriores podem tornar partes deste skill desatualizadas.

## Contribuições

Pull requests são bem-vindos para:
- Atualização de referências legislativas
- Novos templates de documentos
- Correção de referências a artigos de lei
- Novos sub-skills para áreas específicas (tributário, trabalhista, regulatório)

## Créditos

Desenvolvido com auxílio de Claude (Anthropic) para uso com Claude Code e ferramentas
compatíveis com o padrão Agent Skills. Inspirado nos projetos:
- [lawvable/awesome-legal-skills](https://github.com/lawvable/awesome-legal-skills)
- [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)
- [anthropics/knowledge-work-plugins/legal](https://github.com/anthropics/knowledge-work-plugins/blob/main/legal/README.md)
