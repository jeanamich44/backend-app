from . import legal, numeros_utiles, questions

# ----------------------------------------------------------------------


def draw(c, doc):
    if not doc.visible.footer:
        return
    if getattr(doc.visible, "footer_numeros_utiles", True):
        numeros_utiles.draw(c, doc)
    if getattr(doc.visible, "footer_questions", True):
        questions.draw(c, doc)
    if getattr(doc.visible, "footer_legal", True):
        legal.draw(c, doc)
