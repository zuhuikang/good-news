from for_zuhui.headline import Headline
from for_zuhui.nlp_processors import getNLPPolarity


def displayTextPolarity(headline: Headline):
    document = headline.getDocument()
    document.text = getNLPPolarity(headline.text)
    document.set_style(0, len(document.text), {"font_size": 180})


def clearText(headline: Headline):
    document = headline.getDocument()
    document.text = ""
