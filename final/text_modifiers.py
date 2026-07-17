from for_zuhui.headline import Headline
from for_zuhui.logic import Color
from for_zuhui.nlp_processors import getNLPPolarity
from for_zuhui.sourceline import SourceLine


def displayTextPolarity(headline: Headline):
    document = headline.getDocument()
    document.text = getNLPPolarity(headline.text)
    document.set_style(0, len(document.text), {"font_size": 180})


def clearText(headline: Headline):
    document = headline.getDocument()
    document.text = ""


def setTextColor(texts: list[Headline | SourceLine], color: Color):
    for text in texts:
        document = text.getDocument()
        document.set_style(0, len(document.text), {"color": color.get_rgba()})
