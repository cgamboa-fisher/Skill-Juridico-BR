"""Inserção de comentários do Word — o que a ooxml_redline não cobre.

A biblioteca só sabe REMOVER comentários (em save_clean). Aqui só se acrescenta:
os comentários pré-existentes de outros autores nunca são tocados.
"""
import os
import re

REF_RUN = ('<w:r><w:rPr><w:rStyle w:val="Refdecomentrio"/></w:rPr>'
           '<w:commentReference w:id="{cid}"/></w:r>')


def _esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


class Commenter:
    """Acrescenta comentários a um Document já aberto pela ooxml_redline."""

    def __init__(self, doc, author, date, initials='CB', first_id=900):
        self.doc = doc
        self.author = author
        self.date = date
        self.initials = initials
        self.next_id = first_id
        self.pending = []          # (cid, para_id, texto)

    def add(self, anchor, text, label=''):
        """Ancora o comentário no parágrafo inteiro que contém `anchor`."""
        cid = self.next_id
        self.next_id += 1
        # ST_LongHexNumber: EXATAMENTE 8 dígitos hexadecimais. Prefixo mnemônico com
        # letra fora de 0-9A-F (o 'M' de 'ACME') faz o Word recusar o arquivo inteiro,
        # enquanto o LibreOffice abre sem reclamar. Ver hex_id() na ooxml_redline.
        para_id = f'{(0xC0DE0000 + cid) & 0xFFFFFFFF:08X}'

        s, e = self.doc.find_para(anchor, label or f'comment:{cid}')
        p = self.doc.xml[s:e]

        span = re.search(r'</w:pPr>', p)
        at = span.end() if span else p.index('>') + 1
        start = f'<w:commentRangeStart w:id="{cid}"/>'
        end = (f'<w:commentRangeEnd w:id="{cid}"/>' + REF_RUN.format(cid=cid))
        i = p.rindex('</w:p>')
        p = p[:at] + start + p[at:i] + end + p[i:]

        self.doc.xml = self.doc.xml[:s] + p + self.doc.xml[e:]
        self.pending.append((cid, para_id, text))
        self.doc.applied.append(label or f'comment:{cid}')
        return self

    def write(self, root):
        """Grava comments.xml / commentsExtended.xml / commentsIds.xml / people.xml."""
        if not self.pending:
            return
        w = os.path.join(root, 'word')

        blocks = []
        for cid, para_id, text in self.pending:
            body = (f'<w:p w14:paraId="{para_id}" w14:textId="{para_id}">'
                    f'<w:pPr><w:pStyle w:val="Textodecomentrio"/><w:jc w:val="left"/></w:pPr>'
                    f'<w:r><w:rPr><w:rStyle w:val="Refdecomentrio"/></w:rPr>'
                    f'<w:annotationRef/></w:r>'
                    f'<w:r><w:t xml:space="preserve">{_esc(text)}</w:t></w:r></w:p>')
            blocks.append(f'<w:comment w:id="{cid}" w:author="{_esc(self.author)}" '
                          f'w:date="{self.date}" w:initials="{self.initials}">'
                          f'{body}</w:comment>')
        self._append(os.path.join(w, 'comments.xml'), '</w:comments>', ''.join(blocks))

        ex = ''.join(f'<w15:commentEx w15:paraId="{pid}" w15:done="0"/>'
                     for _, pid, _ in self.pending)
        self._append(os.path.join(w, 'commentsExtended.xml'), '</w15:commentsEx>', ex)

        ids = ''.join(f'<w16cid:commentId w16cid:paraId="{pid}" '
                      f'w16cid:durableId="{(0xC0DE0000 + cid):08X}"/>'
                      for cid, pid, _ in self.pending)
        self._append(os.path.join(w, 'commentsIds.xml'), '</w16cid:commentsIds>', ids)

        people = os.path.join(w, 'people.xml')
        if os.path.exists(people):
            s = open(people, encoding='utf-8').read()
            if f'w15:author="{self.author}"' not in s:
                self._append(people, '</w15:people>',
                             f'<w15:person w15:author="{_esc(self.author)}">'
                             f'<w15:presenceInfo w15:providerId="None" '
                             f'w15:userId="{_esc(self.author)}"/></w15:person>')

    @staticmethod
    def _append(path, closing, payload):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        s = open(path, encoding='utf-8').read()
        if closing not in s:
            raise ValueError(f'{path}: fechamento {closing} não encontrado')
        open(path, 'w', encoding='utf-8').write(s.replace(closing, payload + closing))
