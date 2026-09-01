# Revisão de .docx com Marcas de Revisão (Tracked Changes)

> **Tier FULL obrigatório.** É a tarefa de maior risco desta skill, e o modo de falha não é erro visível.
> São três, todos silenciosos: (a) o arquivo não abre no Word; (b) texto do contrato desaparece ao aceitar
> as revisões; (c) a numeração automática se desloca e quebra as remissões cruzadas do próprio contrato.
> Em tier STANDARD ou MÍNIMO, não executar: entregar comentários em Markdown ou um .docx limpo com as
> alterações já aplicadas e um quadro comparativo, informando ao usuário por que as marcas não foram geradas.

Usar em conjunto com o skill `docx` e com **`scripts/ooxml_redline.py`**, que encapsula tudo que este
documento descreve como difícil de acertar. Use a biblioteca; este texto explica as decisões que ela
**não** pode tomar por você — sobretudo onde inserir um parágrafo e em que nível de numeração.

## Nomenclatura padrão de saída

| Saída | Nome |
|---|---|
| Com marcas de revisão | `[Nome Original] - Comentado.docx` |
| Versão limpa (marcas aceitas) | `[Nome Original] - revisado.docx` |

Exemplo: `Contrato Social 01.06.26.docx` → `Contrato Social 01.06.26 - Comentado.docx`

---

## 1. Semântica antes da sintaxe

O erro mais caro não é de XML malformado — é traduzir mal o que uma marca **significa**. Antes de escrever
qualquer patch, saiba o que cada construção vira ao ser aceita.

| Construção | O que significa ao aceitar |
|---|---|
| `<w:ins>` envolvendo runs | O conteúdo permanece; a marca some |
| `<w:del>` envolvendo runs (com `<w:delText>`) | O conteúdo desaparece |
| **`<w:del/>` dentro de `<w:pPr><w:rPr>`** | **A marca de fim do parágrafo é excluída: ele FUNDE com o seguinte** |
| `<w:ins/>` dentro de `<w:pPr><w:rPr>` | O parágrafo inteiro é novo |
| `<w:pPrChange>` / `<w:rPrChange>` | Registro de alteração de *formatação* feita por outro autor |

### A regra que destrói contratos

**Marca de fim de parágrafo excluída quer dizer "junte com o próximo", nunca "apague este".**

O conteúdo é preservado; some apenas a quebra. E o parágrafo resultante herda o `pPr` do **SEGUINTE** —
inclusive `numPr`, ou seja, **a numeração**. Duas consequências práticas:

- Apagar o parágrafo em vez de fundir **elimina texto do contrato em silêncio**. Nenhuma checagem de XML pega.
- Se o parágrafo seguinte não for numerado (um espaçador vazio, por exemplo), o texto fundido **perde o número
  da cláusula**.

Cadeias são comuns: se A e B têm a marca excluída, A+B+C viram um só parágrafo, com o `pPr` de C. Resolver
isso exige laço até estabilizar — `ooxml_redline.merge_mark_deleted()` faz isso.

---

## 2. Extração: profundidade sempre, nunca não-guloso

Alguns elementos **contêm uma cópia de si mesmos**, porque o registro de revisão de formatação carrega dentro
de si o elemento que descreve:

| Elemento | Aninha dentro de si |
|---|---|
| `w:pPr` | `w:pPrChange` → contém um `w:pPr` |
| `w:rPr` | `w:rPrChange` → contém um `w:rPr` |
| `w:tblPr`, `w:tcPr`, `w:trPr` | os respectivos `*Change` |

`<w:pPr>.*?</w:pPr>` fecha no **interno** e produz XML truncado. O sintoma é corrupção a centenas de
kilobytes de distância do ponto real. Usar `ooxml_redline.outer_element()`, que conta profundidade.

Corolário: `<w:t>` também casa com `<w:tbl>`, `<w:tc>`, `<w:tblPr>`. Ao extrair texto visível, o padrão é
`<w:t(?:\s[^>]*)?>` — nunca `<w:t[^>]*>`.

---

## 3. Ordem de elementos (schema)

Não basta o aninhamento estar certo: `CT_PPr` tem **ordem obrigatória**. O `<w:rPr>` que carrega a marca de
revisão do parágrafo vem quase no fim — depois de `pStyle`/`numPr`/`spacing`/`ind`, antes de
`sectPr`/`pPrChange`.

> **Armadilha de diagnóstico.** Violação de ordem faz o Word recusar o arquivo com
> **"An incorrect text node was used"**. A mensagem aponta para nó de texto quando o problema é ordem de
> elementos — e leva a procurar por horas no lugar errado. Se essa mensagem aparecer e os nós de texto
> estiverem corretos, **suspeite da ordem antes de qualquer outra coisa**.

Dois `<w:rPr>` no mesmo `<w:pPr>` também invalidam o documento: funda no existente em vez de acrescentar.
`ooxml_redline.set_para_mark()` cuida dos dois casos; a lista completa de ordem está em `CT_PPR_ORDER`.

---

## 4. Posicionamento de inserções

Aqui a biblioteca não decide por você. Três armadilhas, todas descobertas na prática:

**a) Cadeia de fusão.** Inserir um parágrafo logo após um parágrafo com marca de fim excluída faz o **novo
parágrafo absorver o anterior** ao aceitar. Antes de escolher a âncora, verifique se ela (ou os parágrafos
seguintes) têm marca excluída, e ancore **depois do fim da cadeia**. Quando a posição correta é antes de um
título mas a numeração deve vir de uma cláusula, use `insert_before(..., model_anchor=...)`: posição e modelo
podem ser parágrafos diferentes.

**b) Inversão na mesma âncora.** Várias inserções ancoradas no **mesmo** parágrafo se invertem — a última
declarada fica primeira no documento, porque cada uma empurra a anterior para baixo. Declare na ordem inversa
da desejada, ou use âncoras distintas. Ignorar isso já produziu uma cláusula que se autorreferenciava.

**c) Herança de `ilvl`.** Clonar o `pPr` de um modelo copia o **nível de numeração** dele. Criar uma
subcláusula a partir do modelo da cláusula-pai a coloca no nível do pai, o que **renumera todo o resto do
documento** e quebra as remissões internas do contrato. Sempre passe `ilvl` explicitamente ao criar
subcláusula.

**Ordem das operações.** Inserir antes de excluir quando a âncora é a mesma: depois de `delete_para()` o
texto vira `<w:delText>` e some do texto visível, tornando a âncora inencontrável.

---

## 5. Escada de validação

Cada degrau pega uma classe de defeito que o anterior **não** pega. Parar no degrau 1 ou 2 é como não validar.
`ooxml_redline.validate()` roda a escada inteira.

| # | Verificação | Pega | Deixa passar |
|---|---|---|---|
| 1 | XML bem-formado (`minidom.parseString`) | Malformação | Tudo o mais |
| 2 | `w:t` nunca dentro de `w:del`; `w:delText` sempre dentro | Corrupção clássica de nó de texto | Ordem, semântica, numeração |
| 3 | Ordem do `CT_PPr` + `rPr` não duplicado | **Arquivo que o Word recusa** | Perda de texto, renumeração |
| 4 | **Rejeitar as suas revisões reproduz o original**, caractere a caractere | Destruição de conteúdo alheio | Renumeração |
| 5 | **Abrir o arquivo** + diferenciar a numeração contra o baseline | Renumeração, remissões quebradas, parágrafo perdido | — |

Comprovado empiricamente: um `rPr` fora de ordem passa nos degraus 1 e 2; uma exclusão sem fusão passa em 1,
2 e 3; uma subcláusula com `ilvl` errado passa em 1, 2, 3 **e 4**, e só aparece no 5.

### Degrau 5 — abrir de verdade

XML bem-formado **não** é evidência de que o Word aceita o arquivo. O único teste válido é abrir:

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --norestore \
  -env:UserInstallation=file:///tmp/lo_val --convert-to txt:Text --outdir out arquivo.docx
```

`ooxml_redline.open_with_libreoffice()` procura o binário nos caminhos usuais. **Sem LibreOffice, o degrau 5
não tem substituto por checagem de XML** — declare no output que a abertura não foi verificada, em vez de
apresentar os degraus 1-4 como validação completa.

### Metodologia de baseline

Para comparar numeração, o controle correto é **`aceitar-tudo(original)`**, não o original cru. O documento
recebido normalmente já traz revisões pendentes de outro autor; aceitá-las desloca a numeração por conta
delas, e comparar contra o original cru atribui esse deslocamento a você. Numa revisão real isso produziu
**13 falsas renumerações**.

`Document.baseline_clean()` gera esse controle. Critério de aceite:

> **0 cláusulas renumeradas · 0 cláusulas perdidas · N cláusulas novas**, sendo N exatamente as que você
> acrescentou, com os números esperados.

---

## 6. Validar o validador

Um validador que passa não prova nada se você não sabe o que ele **não** cobre. Dois erros reais:

- Um verificador de `<w:t>` em `<w:del>` acusou 3 falsos positivos (por tratar `<w:del/>` auto-fechado como
  tag de abertura). Ao confirmar que eram falsos, concluiu-se que o arquivo estava bom — quando na verdade o
  verificador simplesmente não cobria ordem de elementos, e o arquivo não abria.
- Um script de baseline leu o diretório errado por um `replace` que não casou, e produziu um controle sem
  sentido que quase virou conclusão.

Práticas:

1. **Rodar o validador contra o original intocado primeiro.** Se acusar erro ali, o bug é do validador.
2. **Teste negativo:** injetar de propósito cada defeito que o validador deveria pegar e confirmar que ele
   acusa. Sem isso, "passou" é indistinguível de "não olhou".
3. Varredura com pilha, não contagem por regex, para verificar aninhamento.
4. Conferir que o script leu o arquivo que você acha que ele leu.

---

## 7. Erros recorrentes — causa e correção

| Erro | Correto | Consequência de errar |
|---|---|---|
| `<w:t>` dentro de `<w:del>` | `<w:delText>` dentro de `<w:del>` | Texto excluído reaparece ou some de forma inconsistente |
| Apagar parágrafo com marca de fim excluída | **Fundir com o seguinte** | **Texto do contrato desaparece em silêncio** |
| `<w:rPr>` no início do `<w:pPr>` | Depois de `pStyle`/`numPr`/`spacing`/`ind` | Word recusa: *"An incorrect text node was used"* |
| Dois `<w:rPr>` no mesmo `<w:pPr>` | Fundir no existente | Documento inválido |
| `<w:pPr>.*?</w:pPr>` não-guloso | `outer_element()` com profundidade | XML truncado por causa do `pPrChange` aninhado |
| Subcláusula herdando o `ilvl` do pai | `ilvl` explícito | Renumera o documento; quebra remissões internas |
| Inserir logo após parágrafo com marca excluída | Ancorar após o fim da cadeia | O parágrafo novo absorve o anterior |
| Várias inserções na mesma âncora | Declarar em ordem inversa | Ordem trocada; remissões podem se autorreferenciar |
| Excluir e depois procurar pela mesma âncora | Inserir antes de excluir | Âncora vira `delText` e some do texto visível |
| `<w:commentRangeStart/>` dentro de `<w:r>` | Filhos diretos de `<w:p>` | Comentário não ancora |
| String original reconstruída de memória | Extrair do `document.xml` via grep/parse | Patch falha em silêncio ou acerta o trecho errado |
| Renumerar ids de revisão de outro autor | Só garantir que os **seus** são novos (`next_rev_id`) | Duplicatas pré-existentes são comuns e o Word tolera |
| Editar `unpacked/` e `unpacked2/` em paralelo | `pack → unpack` entre passes | Perda de alterações do passe anterior |
| Autor da revisão vazio ou genérico | Autor explícito + `w:date` ISO 8601 | Revisões não agrupam; auditoria impossível |
| Reescrever o `<w:p>` inteiro para mudar uma palavra | Cirurgia no `<w:r>` específico | Perda de formatação, numeração e estilos |

---

## 8. Checklist de entrega

- [ ] Escada de validação completa, degraus 1 a 5, sem pendências
- [ ] **Rejeitar todas as suas revisões reproduz o original** caractere a caractere
- [ ] **Arquivo aberto de verdade** (LibreOffice ou Word) — ou declarado como não verificado
- [ ] Diff de numeração contra `aceitar-tudo(original)`: 0 renumeradas, 0 perdidas, N novas conforme esperado
- [ ] Remissões cruzadas citadas nas cláusulas novas apontam para os números corretos **após** a inserção
- [ ] Aba **Revisão** mostra as alterações com o autor esperado
- [ ] Revisões e comentários de outros autores preservados intactos
- [ ] Comentários de assessoria (`[Nota a ...]`) removidos antes de circular com a outra parte
- [ ] Ambos os arquivos entregues (`- Comentado` e `- revisado`), quando solicitado
- [ ] Teste negativo executado quando o validador for novo ou alterado
