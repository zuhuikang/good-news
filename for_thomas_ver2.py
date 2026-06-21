import pyglet
import random
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import time #?
from pyglet.text.document import FormattedDocument
from pyglet.text.layout import TextLayout
from pyglet.gl import *


with open("headline_with_source.txt", "r") as myTxt:
    eachLine = []
    for line in myTxt:
        if line.strip():
            eachLine.append(line.strip())

    headLines = []
    for line in eachLine:
        if "|" in line:
            title, source = line.split("|",1)
            headLines.append({"title": title.strip(), "source": source.strip()})
        else:
            headLines.append({"title": line.strip(), "source": ""})

headlineDic = {
    "title": headLines[0]["title"],
    "source": headLines[0]["source"],
}




def getRandomColor():
    return {"bg_r": random.random(), "bg_g": random.random(), "bg_b": random.random()}

def getComplementaryColor(color):
    return {"r": 1.0 - color["bg_r"], "g": 1.0 - color["bg_g"], "b": 1.0 - color["bg_b"]}


bgColor = getRandomColor()
pongBgColor = getComplementaryColor(bgColor)


# construct window
ping = pyglet.window.Window(800, 500, caption="ping", resizable=True)
pong = pyglet.window.Window(800, 500, caption="pong",resizable=True)

# --- FormattedDocument + TextLayout

FONT_NAME = "Monospace"
FONT_SIZE = 70
SOURCE_FONT_SIZE = 40

pingDoc = FormattedDocument("")
pingLayout = TextLayout(pingDoc, width=ping.width - 300, multiline=True)
pingLayout.x = ping.width // 2
pingLayout.y = ping.height // 2
pingLayout.anchor_x = 'center'
pingLayout.anchor_y = 'center'


pongDoc = FormattedDocument("")
pongLayout = TextLayout(pongDoc, width=pong.width - 300, multiline=True)
pongLayout.x = pong.width // 2
pongLayout.y = pong.height // 2
pongLayout.anchor_x = 'center'
pongLayout.anchor_y = 'center'


sourceDoc = FormattedDocument("")
sourceLayout = TextLayout(sourceDoc, multiline=False)
sourceLayout.x = ping.width // 2
sourceLayout.y = 70
sourceLayout.anchor_x = 'center'
sourceLayout.anchor_y = 'bottom'


def rgbaFromFloat(colorDict):
    return (int(colorDict["bg_r"] * 255), int(colorDict["bg_g"] * 255), int(colorDict["bg_b"] * 255), 255)

def rgbaFromComplement(colorDict):
    return (int(colorDict["r"] * 255), int(colorDict["g"] * 255), int(colorDict["b"] * 255), 255)


def setDocText(doc, text, color, fontSize=FONT_SIZE):
    doc.delete_text(0, len(doc.text))
    if text:
        doc.insert_text(0, text)
        doc.set_style(0, len(text), {
            'color': color,
            'font_name': FONT_NAME,
            'font_size': fontSize,
            'align': 'center',
        })


def setDocTextWithSpans(doc, text, spans, matchedColor, fadedColor, fontSize=FONT_SIZE):
    # to hide some words
    doc.delete_text(0, len(doc.text))
    if text:
        doc.insert_text(0, text)
        for start, end, isMatched in spans:
            color = matchedColor if isMatched else fadedColor
            doc.set_style(start, end, {
                'color': color,
                'font_name': FONT_NAME,
                'font_size': fontSize,
                'align': 'center',
            })


@ping.event
def on_draw():
    glClearColor(bgColor["bg_r"], bgColor["bg_g"], bgColor["bg_b"], 1)
    ping.clear()
    pingLayout.draw()
    sourceLayout.draw()

@pong.event
def on_draw():
    glClearColor(pongBgColor["r"], pongBgColor["g"], pongBgColor["b"], 1)
    pong.clear()
    pongLayout.draw()

@ping.event
def on_resize(width, height):
    pingLayout.x = width // 2
    pingLayout.y = height // 2
    pingLayout.width = width - 300
    sourceLayout.x = width // 2
    sourceLayout.y = 70

@pong.event
def on_resize(width, height):
    pongLayout.x = width // 2
    pongLayout.y = height // 2
    pongLayout.width = width - 300

@ping.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.F:
        ping.set_fullscreen(not ping.fullscreen)
    elif symbol == pyglet.window.key.ESCAPE:
        pass
 
@pong.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.F:
        pong.set_fullscreen(not pong.fullscreen)
    elif symbol == pyglet.window.key.ESCAPE:
        pass


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob')

headlineRaw = headlineDic["title"]
currentBall = headlineRaw

def turn1(headlineDic):
    pingColor = rgbaFromComplement(pongBgColor)
    setDocText(pingDoc, headlineDic["title"], pingColor)
    setDocText(pongDoc, headlineDic["title"], rgbaFromFloat(bgColor))
    setDocText(sourceDoc, headlineDic["source"], pingColor, fontSize=SOURCE_FONT_SIZE)
    return headlineDic["title"]
 
def turn2(headline):
    doc = nlp(headline)
    shapes = [token.shape_ for token in doc]
    result = " ".join(shapes)
    setDocText(pongDoc, result, rgbaFromFloat(bgColor))
    return result
 
def turn3(headline):
    doc = nlp(headline)
    lemmas = [token.lemma_ for token in doc]
    result = " ".join(lemmas)
    setDocText(pongDoc, result, rgbaFromFloat(bgColor))
    return result
 
def turn4(headline):
    doc = nlp(headline)
    pos = [token.pos_ for token in doc]
    result = " ".join(pos)
    setDocText(pongDoc, result, rgbaFromFloat(bgColor))
    return result
 
def turn5(headline):
    doc = nlp(headline)
    tags = [token.tag_ for token in doc]
    result = " ".join(tags)
    setDocText(pongDoc, result, rgbaFromFloat(bgColor))
    return result
 
def turn6(headline):
    doc = nlp(headline)
    stops = [str(token.is_stop) for token in doc]
    result = " ".join(stops)
    setDocText(pongDoc, result, rgbaFromFloat(bgColor))
    return result
 
def turn7(headline):
    doc = nlp(headline)
    words = []
    for token in doc:
        if token.is_stop:
            words.append(token.shape_)
        else:
            words.append(token.text)
    result = " ".join(words)
    setDocText(pongDoc, result, rgbaFromFloat(bgColor))
    return result
 
def turn8(headline):
    doc = nlp(headline)
    assessments = doc._.blob.sentiment_assessments.assessments
    tokens = [token.text.lower() for token in doc]
 
    matchedPositions = set()
    for words, polarity, subjectivity, assessLabel in assessments:
        n = len(words)
        for i in range(len(tokens) - n + 1):
            if tokens[i:i + n] == words:
                for j in range(i, i + n):
                    matchedPositions.add(j)
 
    text = ""
    spans = []
    for i, word in enumerate(tokens):
        start = len(text)
        text += word
        end = len(text)
        spans.append((start, end, i in matchedPositions))
        text += " "
 
    matchedColor = rgbaFromFloat(bgColor)
    fadedColor = (int(pongBgColor["r"] * 255), int(pongBgColor["g"] * 255), int(pongBgColor["b"] * 255), 0)
    # matched words are displayed as is, mismatched words are displayed as 0 in opacity
    setDocTextWithSpans(pongDoc, text, spans, matchedColor=matchedColor, fadedColor=fadedColor)
    return text
 
def turn9(headline):
    doc = nlp(headline)
    assessments = doc._.blob.sentiment_assessments.assessments
 
    lines = []
    for words, polarity, subjectivity, assessLabel in assessments:
        phrase = " ".join(words)
        lines.append(f"{phrase} {round(polarity, 2)}")
 
    result = "\n".join(lines)
    setDocText(pongDoc, result, rgbaFromFloat(bgColor))
    return result
 
def turn10(headline):
    doc = nlp(headline)
    polarity = doc._.blob.polarity
    result = str(round(polarity, 2))
    setDocText(pongDoc, result, rgbaFromFloat(bgColor), fontSize=180)
    return result
 
 
turn = 0
headlineIndex = 0
 
 
def updateWindow(dt):
    global turn
    global headlineDic
    global bgColor
    global pongBgColor
    global currentBall
    global headlineRaw
    global headlineIndex
 
    if turn == 0:
        setDocText(pingDoc, "", (0, 0, 0, 255))
        setDocText(pongDoc, "", (0, 0, 0, 255))
        setDocText(sourceDoc, "", (0, 0, 0, 255))
 
    elif turn == 1:
        currentBall = turn1(headlineDic)
 
    elif turn == 2:
        currentBall = turn2(headlineRaw)
 
    elif turn == 3:
        currentBall = turn3(headlineRaw)
 
    elif turn == 4:
        currentBall = turn4(headlineRaw)
 
    elif turn == 5:
        currentBall = turn5(headlineRaw)
 
    elif turn == 6:
        currentBall = turn6(headlineRaw)
 
    elif turn == 7:
        currentBall = turn7(headlineRaw)
 
    elif turn == 8:
        currentBall = turn8(headlineRaw)
 
    elif turn == 9:
        currentBall = turn9(headlineRaw)
 
    elif turn == 10:
        currentBall = turn10(headlineRaw)
 
    turn += 1
    print(turn)
 
    if turn > 11:
        turn = 0
        setDocText(pingDoc, "", (0, 0, 0, 255))
        setDocText(pongDoc, "", (0, 0, 0, 255))
        setDocText(sourceDoc, "", (0, 0, 0, 255))
        bgColor = getRandomColor()
        pongBgColor = getComplementaryColor(bgColor)
 
        headlineIndex = (headlineIndex + 1) % len(headLines)
        headlineDic = headLines[headlineIndex]
        headlineRaw = headlineDic["title"]
 
 
pyglet.clock.schedule_interval(updateWindow, 2)
pyglet.app.run()