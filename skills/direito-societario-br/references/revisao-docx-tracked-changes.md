# Revisão de .docx com Marcas de Revisão (Tracked Changes)

> **Tier FULL obrigatório.** Manipulação direta de OOXML é a tarefa de maior risco desta skill:
> o modo de falha não é erro visível, é **corrupção silenciosa** — o usuário recebe um arquivo
> que abre, mas perde texto ao aceitar as revisões. Em tier STANDARD ou MÍNIMO, não executar:
> entregar comentários em Markdown ou um .docx limpo com as alterações já aplicadas e um quadro
> comparativo, informando ao usuário por que as marcas de revisão não foram geradas.

Usar em conjunto com o skill `docx`.

## Nomenclatura padrão de saída

| Saída | Nome |
|---|---|
| Com marcas de revisão | `[Nome Original] - Comentado.docx` |
| Versão limpa (marcas aceitas) | `[Nome Original] - revisado.docx` |

Exemplo: `Contrato Social 01.06.26.docx` → `Contrato Social 01.06.26 - Comentado.docx`

## Fluxo

1. **Unpack** — descompactar o `.docx` (é um zip) em diretório de trabalho.
2. **Inspecionar antes de editar** — localizar o trecho exato em `word/document.xml` com `grep`.
   Nunca reconstruir a string original de memória: a formatação intercala `<w:r>`/`<w:rPr>` de
   forma que não é previsível a partir do texto visível.
3. **Descobrir o próximo ID de revisão** — buscar o maior `w:id` existente no XML e iniciar em
   `max_id + 10`. IDs duplicados quebram o painel de revisões.
4. **Aplicar as edições** — inserções em `<w:ins>`, exclusões em `<w:del>`, comentários em
   `word/comments.xml` com os marcadores correspondentes em `document.xml`.
5. **Pack** — recompactar. Entre passes sucessivos, **sempre** `pack → unpack`; nunca manter dois
   diretórios descompactados em paralelo.
6. **Validar** — abrir o arquivo programaticamente, aceitar todas as revisões e conferir se o
   texto resultante é o esperado.

## Erros recorrentes — tabela de causa e correção

| Erro frequente | Correto | Consequência de errar |
|---|---|---|
| `<w:t>` dentro de `<w:del>` | Usar **`<w:delText>`** dentro de `<w:del>` | Corrupção silenciosa: o Word abre o arquivo mas o texto excluído reaparece ou desaparece de forma inconsistente |
| `<w:commentRangeStart/>` ou `<w:commentRangeEnd/>` dentro de `<w:r>` | São **filhos diretos de `<w:p>`** | Comentário não ancora; painel de revisão vazio ou deslocado |
| String original reconstruída de memória | Extrair o trecho exato do `document.xml` via `grep` antes de escrever o script | O replace não encontra o alvo e falha em silêncio, ou acerta o trecho errado |
| IDs de revisão hardcoded sem checar os existentes | Buscar o `max` no XML e iniciar em `max_id + 10` | Revisões se sobrepõem ou não aparecem |
| Editar `unpacked/` e `unpacked2/` em paralelo | `pack → unpack` entre passes | Perda de alterações do passe anterior |
| Autor da revisão vazio ou genérico | Definir autor explícito (ex.: `Claude`) e `w:date` em ISO 8601 | Revisões não agrupam por autor; auditoria impossível |
| Reescrever o `<w:p>` inteiro para mudar uma palavra | Cirurgia no `<w:r>` específico | Perda de formatação, numeração e estilos do parágrafo |

## Checklist de entrega

- [ ] Arquivo abre sem aviso de reparo no Word
- [ ] Aba **Revisão** mostra as alterações com o autor esperado
- [ ] Aceitar todas as alterações produz o texto correto, sem duplicação nem lacuna
- [ ] Rejeitar todas as alterações restaura exatamente o documento original
- [ ] Numeração de cláusulas e sumário permanecem íntegros
- [ ] Comentários ancorados no trecho correto
- [ ] Ambos os arquivos entregues (`- Comentado` e `- revisado`), quando solicitado
