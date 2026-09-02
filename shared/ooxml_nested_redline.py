# -*- coding: utf-8 -*-
"""Excluir texto que está DENTRO de uma <w:ins> de outro autor.

A ooxml_redline recusa esse caso de propósito (`edit()` levanta RedlineError) porque
substituir o intervalo destruiria a marca alheia. A construção correta é aninhar:

    <w:ins autor=CONTRAPARTE> … <w:del autor=INVESTIDORA><w:r><w:delText>…</w:delText></w:r></w:del> … </w:ins>

Semântica: a contraparte inseriu, a INVESTIDORA excluiu. Aceitar tudo → some. Rejeitar só as
marcas da INVESTIDORA → volta como inserção dela. O degrau 4 compara texto visível, e partir um
run em três preserva a concatenação.
"""
import re

RUN_RE = re.compile(r'<w:r(?:\s[^>]*)?>.*?</w:r>', re.S)


def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def delete_inside_foreign_ins(doc, anchor, find, label=''):
    """Marca `find` como excluído por `doc.author`, preservando a <w:ins> alheia.

    `find` precisa caber inteiro em um único run — é o caso comum, e exigir isso evita
    reconstruir intervalos que atravessam runs (onde mora a armadilha dos campos).
    """
    s, e = doc.find_para(anchor, label)
    p = doc.xml[s:e]

    if re.search(r'<w:(?:instrText|fldChar)\b', p):
        raise ValueError(
            f'[{label}] o paragrafo contem campo (fldChar/instrText): excluir por aqui '
            f'quebraria o campo e exigiria <w:delInstrText>. Ancore fora do campo.')

    alvo = None
    for m in RUN_RE.finditer(p):
        t = re.search(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', m.group(0), re.S)
        if t and find in t.group(1):
            if alvo is not None:
                raise ValueError(f'[{label}] {find!r} aparece em mais de um run')
            alvo = (m, t)
    if alvo is None:
        raise ValueError(f'[{label}] {find!r} não encontrado em nenhum run isolado')

    m, t = alvo
    run = m.group(0)
    abertura = run[:run.index('>') + 1]
    rpr_m = re.match(r'<w:rPr>.*?</w:rPr>', run[len(abertura):], re.S)
    rpr = rpr_m.group(0) if rpr_m else ''

    texto = t.group(1)
    i = texto.index(find)
    pre, post = texto[:i], texto[i + len(find):]

    def r_normal(txt):
        return f'{abertura}{rpr}<w:t xml:space="preserve">{_esc(txt)}</w:t></w:r>'

    peças = []
    if pre:
        peças.append(r_normal(pre))
    peças.append(
        f'<w:del w:id="{doc._nid()}" w:author="{doc.author}" w:date="{doc.date}">'
        f'{abertura}{rpr}<w:delText xml:space="preserve">{_esc(find)}</w:delText></w:r>'
        f'</w:del>')
    if post:
        peças.append(r_normal(post))

    novo_p = p[:m.start()] + ''.join(peças) + p[m.end():]
    doc.xml = doc.xml[:s] + novo_p + doc.xml[e:]
    doc.applied.append(label or f'del-aninhado:{find[:30]}')
    return doc
