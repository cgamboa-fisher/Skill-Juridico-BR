"""
ooxml_redline — marcas de revisão (tracked changes) em .docx, sem dependências externas.

Companheiro de `references/revisao-docx-tracked-changes.md`. Leia a referência antes de usar:
esta biblioteca resolve a *sintaxe* do OOXML, mas as decisões de *posicionamento* (onde inserir
um parágrafo novo, em que nível de numeração) continuam sendo suas, e são onde mora o risco.

Por que stdlib puro: `python-docx` não expõe tracked changes. Manipular `document.xml` como
árvore/string é o caminho, desde que com as travas abaixo.

Uso típico:

    import ooxml_redline as rl

    doc = rl.Document.open('contrato.docx', author='Investidor')
    doc.edit('âncora do parágrafo', 'texto antigo', 'texto novo', label='R1')
    doc.insert_after('âncora', ['Texto da nova cláusula.'], ilvl=2, label='nova 7.1.4')
    doc.save_marked('contrato - Comentado.docx')
    doc.save_clean('contrato - revisado.docx')

    rl.validate(doc, original_path='contrato.docx')   # escada de validação

Convenção de nomes de saída (ver a referência): `[Original] - Comentado.docx` e
`[Original] - revisado.docx`.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import xml.dom.minidom as minidom
import zipfile
from datetime import datetime, timezone

__all__ = [
    'Document', 'RedlineError', 'AnchorError',
    'outer_element', 'next_rev_id', 'visible_text',
    'unwrap', 'merge_mark_deleted', 'build_clean',
    'check_wellformed', 'check_text_nodes', 'check_ppr_order', 'check_dup_ids',
    'check_hex_ids', 'check_reject_restores_original', 'open_with_libreoffice', 'validate',
    'hex_id', 'CT_PPR_ORDER', 'HEX8_ATTRS',
]


class RedlineError(Exception):
    """Falha na aplicação de uma marca de revisão."""


class AnchorError(RedlineError):
    """Âncora não encontrada, ambígua, ou em posição que não pode ser editada."""


# ---------------------------------------------------------------------------
# Extração segura
# ---------------------------------------------------------------------------

# Elementos que se auto-aninham: um registro de revisão de formatação carrega
# dentro de si uma cópia do elemento que ele descreve. Regex não-guloso fecha no
# interno e corrompe o XML — sempre usar outer_element() para estes.
SELF_NESTING = {
    'w:pPr': 'w:pPrChange',   # <w:pPrChange> contém um <w:pPr>
    'w:rPr': 'w:rPrChange',   # <w:rPrChange> contém um <w:rPr>
    'w:tblPr': 'w:tblPrChange',
    'w:tcPr': 'w:tcPrChange',
    'w:trPr': 'w:trPrChange',
}


def outer_element(xml: str, tag: str, start: int = 0):
    """Localiza o primeiro `<tag>...</tag>` de primeiro nível a partir de `start`.

    Retorna `(inicio, fim)` ou None. Usa contagem de profundidade: é a única forma
    correta para os elementos de SELF_NESTING.
    """
    open_at = xml.find('<' + tag + '>', start)
    open_attr = re.search(r'<' + re.escape(tag) + r'\s[^>]*?>', xml[start:])
    if open_attr and (open_at < 0 or start + open_attr.start() < open_at):
        open_at = start + open_attr.start()
    if open_at < 0:
        return None
    pat = re.compile(r'<' + re.escape(tag) + r'(?:\s[^>]*?)?(/?)>|</' + re.escape(tag) + r'>')
    depth, j = 0, open_at
    while j < len(xml):
        m = pat.search(xml, j)
        if not m:
            return None
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                return (open_at, m.end())
        elif not m.group(1):
            depth += 1
        j = m.end()
    return None


def next_rev_id(xml: str) -> int:
    """Próximo `w:id` livre. Começa em max+10 para não encostar nos ids existentes.

    Nota: ids duplicados são comuns em documentos reais e o Word tolera. Não tente
    renumerar as revisões de outro autor — só garanta que as suas são novas.
    """
    ids = [int(i) for i in re.findall(r'w:id="(\d+)"', xml)]
    return (max(ids) + 10) if ids else 1


def visible_text(xml: str) -> str:
    """Texto visível: conteúdo de `<w:t>`. Exclui `<w:delText>` (texto já excluído)."""
    return ''.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', xml, re.S))


def _esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


_RUN_RE = re.compile(r'<w:r(?:\s[^>]*)?>(?:(?!</w:r>).)*?</w:r>', re.S)
_PARA_RE = re.compile(r'<w:p\b[^>]*>.*?</w:p>', re.S)


def _ins_spans(p: str):
    """Trechos cobertos por `<w:ins>` — editar dentro deles exige aninhar ins/del."""
    out = []
    for m in re.finditer(r'<w:ins\b[^>]*?[^/]>', p):
        span = outer_element(p, 'w:ins', m.start())
        if span:
            out.append(span)
    return out


# ---------------------------------------------------------------------------
# Ordem de elementos (schema)
# ---------------------------------------------------------------------------

# CT_PPr: a ordem é obrigatória. `rPr` (que carrega a marca de revisão do parágrafo)
# vem quase no fim — depois de pStyle/numPr/spacing/ind, antes de sectPr/pPrChange.
# Violar isso faz o Word recusar o arquivo com a mensagem enganosa
# "An incorrect text node was used", que aponta para nó de texto quando o problema é ordem.
CT_PPR_ORDER = [
    'w:pStyle', 'w:keepNext', 'w:keepLines', 'w:pageBreakBefore', 'w:framePr',
    'w:widowControl', 'w:numPr', 'w:suppressLineNumbers', 'w:pBdr', 'w:shd', 'w:tabs',
    'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap', 'w:overflowPunct',
    'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN', 'w:bidi', 'w:adjustRightInd',
    'w:snapToGrid', 'w:spacing', 'w:ind', 'w:contextualSpacing', 'w:mirrorIndents',
    'w:suppressOverlap', 'w:jc', 'w:textDirection', 'w:textAlignment',
    'w:textboxTightWrap', 'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr',
    'w:sectPr', 'w:pPrChange',
]


def set_para_mark(pPr: str, mark: str) -> str:
    """Insere a marca de revisão do parágrafo (`<w:ins/>` ou `<w:del/>`) no `pPr`.

    Respeita CT_PPR_ORDER e funde num `<w:rPr>` existente em vez de criar um segundo
    (dois `rPr` no mesmo `pPr` também invalidam o documento).
    """
    inner_start = pPr.index('>') + 1
    inner_end = pPr.rindex('</w:pPr>')
    inner = pPr[inner_start:inner_end]

    # o pPr aninhado dentro de pPrChange é de outro autor: não tocar
    cut = inner.find('<w:pPrChange')
    head, tail = (inner, '') if cut < 0 else (inner[:cut], inner[cut:])

    r = head.find('<w:rPr>')
    if r >= 0:
        # ins/del são os primeiros filhos de CT_ParaRPr
        at = r + len('<w:rPr>')
        head = head[:at] + mark + head[at:]
    else:
        sec = head.find('<w:sectPr')
        block = '<w:rPr>' + mark + '</w:rPr>'
        head = (head[:sec] + block + head[sec:]) if sec >= 0 else (head + block)
    return pPr[:inner_start] + head + tail + pPr[inner_end:]


# ---------------------------------------------------------------------------
# Simulação de revisões (aceitar / rejeitar)
# ---------------------------------------------------------------------------

def unwrap(xml: str, tag: str, author: str | None = None, keep: bool = True) -> str:
    """Resolve `<w:ins>`/`<w:del>`: `keep=True` mantém o conteúdo, `False` descarta.

    `author` restringe a um autor (para rejeitar só as suas revisões e conferir que o
    documento volta a ser o original). Tags auto-fechadas — marcas de parágrafo — são
    tratadas à parte: elas não envolvem conteúdo.
    """
    out, i = [], 0
    pat = re.compile(r'<' + tag + r'(?:\s[^>]*?)?(/?)>')
    while True:
        m = pat.search(xml, i)
        if not m:
            out.append(xml[i:])
            return ''.join(out)
        out.append(xml[i:m.start()])
        mine = author is None or f'w:author="{author}"' in m.group(0)
        if m.group(1) or m.group(0).rstrip().endswith('/>'):
            if not mine:
                out.append(m.group(0))
            i = m.end()
            continue
        span = outer_element(xml, tag, m.start())
        j = span[1]
        inner = xml[m.end():j - len('</' + tag + '>')]
        if not mine:
            out.append(m.group(0) + inner + '</' + tag + '>')
        elif keep:
            if tag == 'w:del':
                inner = (inner.replace('<w:delText xml:space="preserve">', '<w:t xml:space="preserve">')
                              .replace('<w:delText>', '<w:t>')
                              .replace('</w:delText>', '</w:t>'))
            out.append(inner)
        i = j


def merge_mark_deleted(xml: str) -> str:
    """Aplica a semântica de marca de fim de parágrafo excluída: FUNDIR com o seguinte.

    Um `<w:del>` dentro de `<w:pPr><w:rPr>` não quer dizer "apague este parágrafo" —
    quer dizer "junte-o ao próximo". O conteúdo é preservado e o parágrafo resultante
    herda o `pPr` do SEGUINTE (inclusive a numeração). Apagar em vez de fundir destrói
    texto em silêncio; foi o pior defeito da revisão que originou esta biblioteca.

    Cadeias são possíveis (A e B ambos marcados => A+B+C viram um só), por isso o laço.
    """
    while True:
        paras = list(_PARA_RE.finditer(xml))
        hit = None
        for k, m in enumerate(paras[:-1]):
            span = outer_element(m.group(0), 'w:pPr')
            if not span:
                continue
            head = m.group(0)[span[0]:span[1]]
            cut = head.find('<w:pPrChange')
            if cut >= 0:
                head = head[:cut]
                head += '</w:pPr>'
            rpr = outer_element(head, 'w:rPr')
            if rpr and re.search(r'<w:del[\s/]', head[rpr[0]:rpr[1]]):
                hit = (m, paras[k + 1])
                break
        if not hit:
            return xml

        cur, nxt = hit
        cur_body = cur.group(0)[cur.group(0).index('>') + 1:-len('</w:p>')]
        cs = outer_element(cur_body, 'w:pPr')
        if cs and cs[0] == 0:
            cur_body = cur_body[cs[1]:]

        nxt_xml = nxt.group(0)
        nb = nxt_xml[nxt_xml.index('>') + 1:-len('</w:p>')]
        ns = outer_element(nb, 'w:pPr')
        npr, nrest = (nb[:ns[1]], nb[ns[1]:]) if (ns and ns[0] == 0) else ('', nb)

        merged = nxt_xml[:nxt_xml.index('>') + 1] + npr + cur_body + nrest + '</w:p>'
        xml = xml[:cur.start()] + merged + xml[nxt.end():]


def build_clean(xml: str) -> str:
    """Aceita todas as revisões: fusão de parágrafos, ins/del, e limpa registros residuais."""
    xml = merge_mark_deleted(xml)
    xml = unwrap(xml, 'w:ins', keep=True)
    xml = unwrap(xml, 'w:del', keep=False)
    xml = re.sub(r'<w:pPrChange\b.*?</w:pPrChange>', '', xml, flags=re.S)
    xml = re.sub(r'<w:rPrChange\b.*?</w:rPrChange>', '', xml, flags=re.S)
    xml = re.sub(r'<w:commentRangeStart[^>]*/>|<w:commentRangeEnd[^>]*/>', '', xml)
    xml = re.sub(r'<w:r\b[^>]*>(?:(?!</w:r>).)*?<w:commentReference[^>]*/>.*?</w:r>', '',
                 xml, flags=re.S)
    return xml


# ---------------------------------------------------------------------------
# Documento
# ---------------------------------------------------------------------------

class Document:
    """Um .docx aberto para receber marcas de revisão."""

    def __init__(self, workdir: str, author: str, date: str, original_xml: str):
        self.dir = workdir
        self.author = author
        self.date = date
        self.original_xml = original_xml
        self.xml = original_xml
        self._id = next_rev_id(original_xml)
        self.applied: list[str] = []

    # -- ciclo de vida -----------------------------------------------------

    @classmethod
    def open(cls, path: str, author: str, date: str | None = None) -> 'Document':
        date = date or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        workdir = tempfile.mkdtemp(prefix='redline_')
        with zipfile.ZipFile(path) as z:
            z.extractall(workdir)
        xml = open(os.path.join(workdir, 'word', 'document.xml'), encoding='utf-8').read()
        return cls(workdir, author, date, xml)

    def _nid(self) -> int:
        self._id += 1
        return self._id

    def _write(self, root: str, xml: str, drop_comments: bool = False) -> None:
        with open(os.path.join(root, 'word', 'document.xml'), 'w', encoding='utf-8') as f:
            f.write(xml)
        if drop_comments:
            for name in ('comments.xml', 'commentsExtended.xml',
                         'commentsExtensible.xml', 'commentsIds.xml'):
                p = os.path.join(root, 'word', name)
                if os.path.exists(p):
                    os.remove(p)
            rels = os.path.join(root, 'word', '_rels', 'document.xml.rels')
            s = open(rels, encoding='utf-8').read()
            open(rels, 'w', encoding='utf-8').write(
                re.sub(r'<Relationship[^>]*comments[^>]*/>', '', s))
            ct = os.path.join(root, '[Content_Types].xml')
            s = open(ct, encoding='utf-8').read()
            open(ct, 'w', encoding='utf-8').write(
                re.sub(r'<Override[^>]*comments[^>]*/>', '', s))

    @staticmethod
    def _zip(root: str, out_path: str) -> None:
        if os.path.exists(out_path):
            os.remove(out_path)
        with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(os.path.join(root, '[Content_Types].xml'), '[Content_Types].xml')
            for base, _, files in os.walk(root):
                for f in files:
                    full = os.path.join(base, f)
                    arc = os.path.relpath(full, root)
                    if arc != '[Content_Types].xml':
                        z.write(full, arc)

    def save_marked(self, out_path: str) -> str:
        """Grava a versão com marcas de revisão (`- Comentado.docx`)."""
        self._write(self.dir, self.xml)
        self._zip(self.dir, out_path)
        return out_path

    def save_clean(self, out_path: str) -> str:
        """Grava a versão com as marcas aceitas (`- revisado.docx`)."""
        tmp = tempfile.mkdtemp(prefix='redline_clean_')
        shutil.rmtree(tmp)
        shutil.copytree(self.dir, tmp)
        self._write(tmp, build_clean(self.xml), drop_comments=True)
        self._zip(tmp, out_path)
        shutil.rmtree(tmp, ignore_errors=True)
        return out_path

    def baseline_clean(self, out_path: str) -> str:
        """Aceita SÓ as revisões pré-existentes (sem as suas). É o controle correto
        para diferenciar numeração — comparar contra o original cru gera falsos positivos."""
        tmp = tempfile.mkdtemp(prefix='redline_base_')
        shutil.rmtree(tmp)
        shutil.copytree(self.dir, tmp)
        self._write(tmp, build_clean(self.original_xml), drop_comments=True)
        self._zip(tmp, out_path)
        shutil.rmtree(tmp, ignore_errors=True)
        return out_path

    # -- localização -------------------------------------------------------

    def find_para(self, anchor: str, label: str = '') -> tuple[int, int]:
        """Span do único parágrafo cujo texto visível contém `anchor`.

        Falha se houver 0 ou 2+ — âncora ambígua é a origem clássica de patch no
        lugar errado.
        """
        hits = [(m.start(), m.end()) for m in _PARA_RE.finditer(self.xml)
                if anchor in visible_text(m.group(0))]
        if len(hits) != 1:
            raise AnchorError(f'[{label}] âncora com {len(hits)} ocorrências: {anchor[:70]!r}')
        return hits[0]

    # -- edições -----------------------------------------------------------

    def edit(self, anchor: str, find: str, repl: str, label: str = '') -> 'Document':
        """Substitui `find` por `repl` como marca de revisão (del + ins)."""
        s, e = self.find_para(anchor, label)
        self.xml = self.xml[:s] + self._edit_para(self.xml[s:e], find, repl, label) + self.xml[e:]
        self.applied.append(label or f'edit:{find[:30]}')
        return self

    def _edit_para(self, p: str, find: str, repl: str, label: str) -> str:
        runs = []
        for m in _RUN_RE.finditer(p):
            t = re.search(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', m.group(0), re.S)
            if not t:
                continue
            rpr = outer_element(m.group(0), 'w:rPr')
            runs.append({'span': (m.start(), m.end()), 'text': t.group(1),
                         'rpr': m.group(0)[rpr[0]:rpr[1]] if rpr else ''})
        if not runs:
            raise RedlineError(f'[{label}] parágrafo sem runs de texto')

        full = ''.join(r['text'] for r in runs)
        at = full.find(find)
        if at < 0:
            raise AnchorError(f'[{label}] não encontrado: {find[:70]!r}\n  no texto: {full[:200]!r}')
        if full.find(find, at + 1) >= 0:
            raise AnchorError(f'[{label}] ambíguo (2+ ocorrências no parágrafo): {find[:70]!r}')
        end = at + len(find)

        pos = first = last = None
        pos = 0
        for i, r in enumerate(runs):
            s, e = pos, pos + len(r['text'])
            if first is None and e > at:
                first, off_a = i, at - s
            if s < end:
                last, off_b = i, end - s
            pos = e

        protected = _ins_spans(p)
        for i in range(first, last + 1):
            if any(a <= runs[i]['span'][0] < b for a, b in protected):
                raise RedlineError(
                    f'[{label}] alvo dentro de <w:ins> de outro autor. '
                    f'Se for acréscimo ao fim, use append(); caso contrário aninhe ins/del à mão.')

        rpr = runs[first]['rpr']
        pre = runs[first]['text'][:off_a]
        post = runs[last]['text'][off_b:]

        out = []
        if pre:
            out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{pre}</w:t></w:r>')
        out.append(f'<w:del w:id="{self._nid()}" w:author="{self.author}" w:date="{self.date}">'
                   f'<w:r>{rpr}<w:delText xml:space="preserve">{find}</w:delText></w:r></w:del>')
        if repl:
            out.append(f'<w:ins w:id="{self._nid()}" w:author="{self.author}" w:date="{self.date}">'
                       f'<w:r>{rpr}<w:t xml:space="preserve">{repl}</w:t></w:r></w:ins>')
        if post:
            out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{post}</w:t></w:r>')
        return p[:runs[first]['span'][0]] + ''.join(out) + p[runs[last]['span'][1]:]

    def append(self, anchor: str, text: str, label: str = '') -> 'Document':
        """Acrescenta texto ao fim do parágrafo. Caminho seguro quando o parágrafo
        inteiro é `<w:ins>` de outro autor e edit() recusaria."""
        s, e = self.find_para(anchor, label)
        p = self.xml[s:e]
        body = (f'<w:ins w:id="{self._nid()}" w:author="{self.author}" w:date="{self.date}">'
                f'<w:r><w:t xml:space="preserve"> {_esc(text)}</w:t></w:r></w:ins>')
        i = p.rindex('</w:p>')
        self.xml = self.xml[:s] + p[:i] + body + p[i:] + self.xml[e:]
        self.applied.append(label or 'append')
        return self

    def new_para(self, model_p: str, text: str, ilvl: int | None = None) -> str:
        """Constrói um parágrafo inteiramente inserido, clonando o `pPr` do modelo.

        ATENÇÃO ao `ilvl`: clonar o modelo copia o nível dele. Criar uma subcláusula a
        partir do modelo da cláusula-pai a coloca no nível do pai, o que renumera todo o
        resto do documento e quebra remissões internas. Passe `ilvl` explicitamente.
        """
        span = outer_element(model_p, 'w:pPr')
        pPr = model_p[span[0]:span[1]] if span else '<w:pPr></w:pPr>'
        # registros de revisão do autor anterior não devem ser herdados
        pPr = re.sub(r'<w:pPrChange\b.*?</w:pPrChange>', '', pPr, flags=re.S)
        pPr = re.sub(r'<w:rPr>.*?</w:rPr>', '', pPr, flags=re.S)
        if ilvl is not None:
            pPr = re.sub(r'<w:ilvl w:val="\d+"/>', f'<w:ilvl w:val="{ilvl}"/>', pPr)
        pPr = set_para_mark(
            pPr, f'<w:ins w:id="{self._nid()}" w:author="{self.author}" w:date="{self.date}"/>')
        body = (f'<w:ins w:id="{self._nid()}" w:author="{self.author}" w:date="{self.date}">'
                f'<w:r><w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:ins>')
        return f'<w:p>{pPr}{body}</w:p>'

    def insert_after(self, anchor: str, texts: list[str], ilvl: int | None = None,
                     label: str = '') -> 'Document':
        """Insere parágrafos logo após o parágrafo-âncora.

        Duas armadilhas documentadas na referência:
        - Se a âncora tem a marca de fim excluída, o primeiro parágrafo novo será
          ABSORVIDO por ela ao aceitar. Ancore depois do fim da cadeia de fusão.
        - Várias chamadas na MESMA âncora se invertem: a última declarada fica primeira
          no documento. Declare na ordem inversa da desejada, ou use âncoras distintas.
        """
        s, e = self.find_para(anchor, label)
        model = self.xml[s:e]
        block = ''.join(self.new_para(model, t, ilvl) for t in texts)
        self.xml = self.xml[:e] + block + self.xml[e:]
        self.applied.append(label or 'insert_after')
        return self

    def insert_before(self, anchor: str, texts: list[str], ilvl: int | None = None,
                      model_anchor: str | None = None, label: str = '') -> 'Document':
        """Insere antes do parágrafo-âncora. `model_anchor` permite clonar a formatação
        de um parágrafo diferente daquele que define a posição — necessário quando a
        posição correta é antes de um título, mas a numeração deve vir de uma cláusula."""
        s, _ = self.find_para(anchor, label)
        if model_anchor:
            ms, me = self.find_para(model_anchor, label)
            model = self.xml[ms:me]
        else:
            model = self.xml[s:self.find_para(anchor, label)[1]]
        block = ''.join(self.new_para(model, t, ilvl) for t in texts)
        self.xml = self.xml[:s] + block + self.xml[s:]
        self.applied.append(label or 'insert_before')
        return self

    def delete_para(self, anchor: str, mark: bool = True, label: str = '') -> 'Document':
        """Exclui o conteúdo do parágrafo.

        `mark=True` exclui também a marca de fim: o parágrafo funde com o seguinte e
        desaparece. `mark=False` mantém a marca: use quando um parágrafo ANTERIOR já
        tem a marca excluída e vai absorver este — assim a cadeia termina aqui e a
        numeração do bloco é preservada.
        """
        s, e = self.find_para(anchor, label)
        p = self.xml[s:e]

        def conv(m):
            r = m.group(0)
            if '<w:delText' in r:
                return r
            r2 = re.sub(r'<w:t(\s[^>]*)?>', '<w:delText xml:space="preserve">', r)
            r2 = r2.replace('</w:t>', '</w:delText>')
            return (f'<w:del w:id="{self._nid()}" w:author="{self.author}" '
                    f'w:date="{self.date}">{r2}</w:del>')

        cut = p.index('>') + 1
        head, body = p[:cut], p[cut:]
        span = outer_element(body, 'w:pPr')
        if span and span[0] == 0:
            newp = (set_para_mark(body[:span[1]],
                    f'<w:del w:id="{self._nid()}" w:author="{self.author}" w:date="{self.date}"/>')
                    if mark else body[:span[1]])
            body = newp + _RUN_RE.sub(conv, body[span[1]:])
        else:
            body = _RUN_RE.sub(conv, body)
        self.xml = self.xml[:s] + head + body + self.xml[e:]
        self.applied.append(label or 'delete_para')
        return self


# ---------------------------------------------------------------------------
# Escada de validação
# ---------------------------------------------------------------------------

def check_wellformed(xml: str) -> list[str]:
    """Degrau 1 — XML bem-formado. Necessário, longe de suficiente."""
    try:
        minidom.parseString(xml)
        return []
    except Exception as exc:
        return [f'XML malformado: {exc}']


def check_text_nodes(xml: str) -> list[str]:
    """Degrau 2 — nós de texto na forma certa para o contexto de revisão.

    São DOIS pares, não um. Dentro de `w:del` o texto corrido vira `w:delText` **e** o
    código de campo vira `w:delInstrText`. Esquecer o segundo par é o defeito que o Word
    reporta como "An incorrect text node was used" e que passa despercebido: o degrau 4
    compara só texto visível, e código de campo não é visível.

    Faz varredura com pilha: contar com regex dá falso positivo em `<w:del/>`
    auto-fechado (marca de parágrafo), que é válido.
    """
    pares = {'w:t': 'w:delText', 'w:instrText': 'w:delInstrText'}
    dentro = {v: k for k, v in pares.items()}

    problems, stack = [], []
    for m in re.finditer(r'<(/?)(w:[A-Za-z0-9]+)([^>]*?)(/?)>', xml):
        closing, name, attrs, selfclose = m.groups()
        if selfclose or attrs.rstrip().endswith('/'):
            continue
        if closing:
            if stack and stack[-1] == name:
                stack.pop()
            continue
        em_del = 'w:del' in stack
        if name in pares and em_del:
            problems.append(f'<{name}> dentro de <w:del> na posição {m.start()} '
                            f'(use <{pares[name]}>)')
        if name in dentro and not em_del:
            problems.append(f'<{name}> fora de <w:del> na posição {m.start()} '
                            f'(use <{dentro[name]}>)')
        stack.append(name)
    return problems


def check_ppr_order(xml: str) -> list[str]:
    """Degrau 3 — ordem do CT_PPr e `rPr` não duplicado.

    É o degrau que o Word reporta como "An incorrect text node was used".
    """
    problems, i = [], 0
    while True:
        span = outer_element(xml, 'w:pPr', i)
        if not span:
            return problems
        inner = xml[span[0]:span[1]]
        cut = inner.find('<w:pPrChange')
        head = inner if cut < 0 else inner[:cut]
        if head.count('<w:rPr>') > 1:
            problems.append(f'<w:rPr> duplicado em <w:pPr> na posição {span[0]}')
        seen, last = [t for t in re.findall(r'<(w:[A-Za-z0-9]+)', head) if t in CT_PPR_ORDER], -1
        for t in seen:
            k = CT_PPR_ORDER.index(t)
            if k < last:
                problems.append(
                    f'<{t}> fora de ordem em <w:pPr> na posição {span[0]} '
                    f'(CT_PPr exige a ordem de CT_PPR_ORDER)')
                break
            last = k
        i = span[1]


# Atributo -> partes onde ele é ST_LongHexNumber. `None` = em qualquer parte.
# `w16cid:durableId` é a pegadinha: hex em `commentsIds.xml`, mas DECIMAL em
# `numbering.xml` — o próprio Word escreve `w16cid:durableId="790586536"` lá. Checar
# pelo nome do atributo, sem olhar a parte, dá 17 falsos positivos num .docx intocado.
HEX8_ATTRS = {
    'w14:paraId': None,
    'w14:textId': None,
    'w15:paraId': None,
    'w16cid:paraId': None,
    'w16cid:durableId': ('word/commentsIds.xml',),
}


def hex_id(n: int) -> str:
    """Id no formato `ST_LongHexNumber`: 8 dígitos hex. Use SEMPRE isto para gerar ids.

    Prefixo mnemônico é a armadilha: `ACME0384` parece um id e não é — `M` não é dígito
    hexadecimal. Prefixos que sobrevivem: `C0DE`, `DEAD`, `FADA`, `B0A`.
    """
    return f'{n & 0xFFFFFFFF:08X}'


def check_hex_ids(docx_path: str) -> list[str]:
    """Ids de parágrafo/comentário em `ST_LongHexNumber` — 8 dígitos hex, sem exceção.

    Vale para o PACOTE inteiro, não só o `document.xml`: `comments.xml`,
    `commentsExtended.xml` e `commentsIds.xml` carregam os mesmos ids e quebram igual.

    Um valor fora do padrão faz o Word recusar o arquivo inteiro; o LibreOffice abre sem
    reclamar, então o degrau 5 NÃO pega isto. Custou uma entrega em 01.09.2026.
    """
    problems = []
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if not name.endswith('.xml'):
                continue
            xml = z.read(name).decode('utf-8', errors='replace')
            for attr, partes in HEX8_ATTRS.items():
                if partes is not None and name not in partes:
                    continue
                for m in re.finditer(re.escape(attr) + r'="([^"]*)"', xml):
                    if not re.fullmatch(r'[0-9A-Fa-f]{8}', m.group(1)):
                        problems.append(
                            f'{name}: {attr}="{m.group(1)}" não é ST_LongHexNumber '
                            f'(8 dígitos hex) — o Word recusa o arquivo')
    return problems


def check_dup_ids(xml: str, original_xml: str) -> list[str]:
    """Ids duplicados INTRODUZIDOS por você. Duplicatas pré-existentes são comuns
    e o Word tolera — não são defeito seu e não devem ser 'corrigidas'."""
    def dups(s):
        seen, d = set(), set()
        for i in re.findall(r'w:id="(\d+)"', s):
            (d if i in seen else seen).add(i)
        return d
    novos = dups(xml) - dups(original_xml)
    return [f'ids de revisão duplicados introduzidos: {sorted(novos)}'] if novos else []


def check_reject_restores_original(xml: str, original_xml: str, author: str) -> list[str]:
    """Degrau 4 — rejeitar as SUAS revisões tem de reproduzir o original.

    É o teste que prova que você não destruiu conteúdo de outro autor.
    """
    rej = unwrap(xml, 'w:ins', author=author, keep=False)
    rej = unwrap(rej, 'w:del', author=author, keep=True)
    if visible_text(rej) == visible_text(original_xml):
        return []
    a, b = visible_text(original_xml), visible_text(rej)
    for k in range(min(len(a), len(b))):
        if a[k] != b[k]:
            return [f'rejeitar as revisões de {author} NÃO reproduz o original; '
                    f'primeira divergência em {k}:\n  original: {a[k-60:k+80]!r}\n'
                    f'  rejeitado: {b[k-60:k+80]!r}']
    return [f'rejeitar não reproduz o original (tamanhos {len(a)} vs {len(b)})']


SOFFICE_PATHS = [
    '/Applications/LibreOffice.app/Contents/MacOS/soffice',
    '/usr/bin/soffice', '/usr/local/bin/soffice', '/opt/homebrew/bin/soffice',
]


def open_with_libreoffice(docx_path: str, outdir: str | None = None) -> str | None:
    """Degrau 5 — abre o arquivo de verdade e devolve o texto renderizado.

    Retorna None se o LibreOffice não estiver instalado. Nesse caso o degrau 5 NÃO tem
    substituto por checagem de XML: declare no output que a abertura não foi verificada.
    """
    soffice = next((p for p in SOFFICE_PATHS if os.path.exists(p)), None)
    if not soffice:
        return None
    outdir = outdir or tempfile.mkdtemp(prefix='redline_lo_')
    profile = tempfile.mkdtemp(prefix='redline_profile_')
    subprocess.run([soffice, '--headless', '--norestore',
                    f'-env:UserInstallation=file://{profile}',
                    '--convert-to', 'txt:Text', '--outdir', outdir, docx_path],
                   capture_output=True, timeout=180)
    txt = os.path.join(outdir, os.path.splitext(os.path.basename(docx_path))[0] + '.txt')
    return open(txt, encoding='utf-8').read() if os.path.exists(txt) else None


def clause_numbers(rendered_text: str) -> dict:
    """Mapa {início do texto da cláusula: número} a partir do texto renderizado."""
    out = {}
    for line in rendered_text.splitlines():
        m = re.match(r'\s*(\d+(?:\.\d+)*)\.\s+(.{0,50})', line)
        if m and m.group(2).strip():
            out[m.group(2).strip()] = m.group(1)
    return out


def diff_numbering(baseline_text: str, marked_text: str) -> dict:
    """Compara a numeração contra o baseline `aceitar-tudo(original)`.

    Critério de aceite: `renumeradas` e `perdidas` vazias; `novas` = exatamente as
    cláusulas que você acrescentou.
    """
    b, n = clause_numbers(baseline_text), clause_numbers(marked_text)
    return {
        'renumeradas': [(k, b[k], n[k]) for k in b if k in n and b[k] != n[k]],
        'perdidas': [(b[k], k) for k in b if k not in n],
        'novas': sorted([(n[k], k) for k in n if k not in b]),
    }


def validate(doc: 'Document', clean_path: str | None = None,
             baseline_path: str | None = None,
             marked_path: str | None = None) -> dict:
    """Roda a escada completa. Retorna {degrau: [problemas]} — tudo vazio significa OK.

    Os degraus 1-4 rodam sempre. O degrau 5 depende do LibreOffice e dos dois .docx.

    `marked_path` habilita o degrau 2b (ids hex), que precisa do PACOTE, não só do
    `document.xml` — os ids de comentário vivem em outras partes. Passe sempre o caminho
    do `- Comentado.docx` recém-gravado; sem ele o degrau 2b não roda e o resultado avisa.
    """
    result = {
        '1_wellformed': check_wellformed(doc.xml),
        '2_text_nodes': check_text_nodes(doc.xml),
        '2b_hex_ids': (check_hex_ids(marked_path) if marked_path else
                       ['não executado — passe marked_path (o .docx gravado); '
                        'o LibreOffice não pega esta classe de defeito']),
        '3_ppr_order': check_ppr_order(doc.xml),
        '3b_dup_ids': check_dup_ids(doc.xml, doc.original_xml),
        '4_reject_restores': check_reject_restores_original(
            doc.xml, doc.original_xml, doc.author),
    }
    if clean_path and baseline_path:
        rendered = open_with_libreoffice(clean_path)
        base = open_with_libreoffice(baseline_path)
        if rendered is None or base is None:
            result['5_abertura'] = ['LibreOffice indisponível — abertura NÃO verificada. '
                                    'Declare isso no output; não há substituto por XML.']
        else:
            d = diff_numbering(base, rendered)
            problems = []
            if d['renumeradas']:
                problems.append(f'cláusulas renumeradas: {d["renumeradas"]}')
            if d['perdidas']:
                problems.append(f'cláusulas perdidas: {d["perdidas"]}')
            result['5_abertura'] = problems
            result['_novas'] = d['novas']
    else:
        result['5_abertura'] = ['não executado — passe clean_path e baseline_path']
    return result
