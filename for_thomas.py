import pyglet
import random
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import time #?
from pyglet.gl import *


with open("headline_with_source.txt", "r") as myTxt:
    eachLine = []
    for line in myTxt:
        if line.strip():
            eachLine.append(line.strip())
    #print(eachLine)

    headLines = []
    for line in eachLine:
        if "|" in line:
            title, source = line.split("|",1)
            headLines.append({"title": title.strip(), "source": source.strip()})
        else:
            headLines.append({"title": line.strip(), "source": ""}) #소스가 없을경우 빈 스트링으로 리턴해주길
    #print(headLines)

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

# lable also
labelPing = pyglet.text.Label( 
    "",
    font_name="Monospace",
    font_size=70,
    x=ping.width // 2,
    y=ping.height // 2,
    anchor_x="center",
    anchor_y="center",
    # color=(lbColor['lb_r'], lbColor['lb_g'], lbColor['lb_b'], 255)
    width=ping.width - 300,
    align="center",
    multiline=True
)

labelPong = pyglet.text.Label( 
    "",
    font_name="Monospace",
    font_size=70,
    x=pong.width // 2,
    y=pong.height // 2,
    anchor_x="center",
    anchor_y="center",
    width=pong.width - 300,
    align="center",
    multiline=True
)

labelSource = pyglet.text.Label(
    "",
    font_name="Monospace",
    font_size=40,
    x=ping.width // 2,
    y=70,
    anchor_x="center",
    anchor_y="bottom",
)


@ping.event
def on_draw():
    glClearColor(bgColor["bg_r"], bgColor["bg_g"], bgColor["bg_b"], 1)
    ping.clear()
    labelPing.color = (
        int(pongBgColor["r"] * 255),
        int(pongBgColor["g"] * 255),
        int(pongBgColor["b"] * 255),
        255
    )
    labelPing.draw()
    labelSource.color = (
        int(pongBgColor["r"] * 255),
        int(pongBgColor["g"] * 255),
        int(pongBgColor["b"] * 255),
        255
    )
    labelSource.draw()

@pong.event
def on_draw():
    glClearColor(pongBgColor["r"], pongBgColor["g"], pongBgColor["b"], 1)
    pong.clear()
    labelPong.color = (
        int(bgColor["bg_r"] * 255),
        int(bgColor["bg_g"] * 255),
        int(bgColor["bg_b"] * 255),
        255
    )
    labelPong.draw()



# headline = headLines[0]
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob')

headlineRaw = headlineDic["title"]
currentBall = headlineRaw

def turn1(headlineDic, labelPing, labelPong, labelSource):
    labelPing.text = headlineDic["title"]
    labelPong.text = headlineDic["title"]
    labelSource.text = headlineDic["source"]
    return headlineDic["title"]

def turn2(headline, label):
    doc = nlp(headline)
    shapes = [token.shape_ for token in doc]
    result = " ".join(shapes)
    label.text = result
    return result

def turn3(headline, label):
    doc = nlp(headline)
    lemmas = [token.lemma_ for token in doc]
    result = " ".join(lemmas)
    label.text = result
    return result

def turn4(headline, label):
    doc = nlp(headline)
    pos = [token.pos_ for token in doc]
    result = " ".join(pos)
    label.text = result
    return result

def turn5(headline, label):
    doc = nlp(headline)
    tags = [token.tag_ for token in doc]
    result = " ".join(tags)
    label.text = result
    return result

def turn6(headline, label):
    doc = nlp(headline)
    stops = [str(token.is_stop) for token in doc]
    result = " ".join(stops)
    label.text = result
    return result

def turn7(headline, label):
    doc = nlp(headline)
    words = []
    for token in doc:
        if token.is_stop:
            words.append(token.shape_)
        else:
            words.append(token.text)
    result = " ".join(words)
    label.text = result
    return result

def turn8(headline, label, bgColor):
    doc = nlp(headline)
    assessments = doc._.blob.sentiment_assessments.assessments
    tokens = [token.text.lower() for token in doc]

    matchedPositions = set()
    for words, polarity, subjectivity, assessLabel in assessments:
        n = len(words)
        for i in range(len(tokens) - n + 1):
            if tokens[i:i+n] == words:
                for j in range(i, i+n):
                    matchedPositions.add(j)

    words_out = [tokens[i] if i in matchedPositions else "" for i in range(len(tokens))]
    result = " ".join(words_out)
    label.text = result
    return result

def turn9(headline, label):
    doc = nlp(headline)
    assessments = doc._.blob.sentiment_assessments.assessments
    
    lines = []
    for words, polarity, subjectivity, assessLabel in assessments:
        phrase = " ".join(words)
        lines.append(f"{phrase} {polarity}")
    
    result = "\n".join(lines)
    label.text = result
    return result

def turn10(headline, label):
    doc = nlp(headline)
    polarity = doc._.blob.polarity
    result = str(polarity)
    label.text = result
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
        labelPing.text = ""
        labelPong.text = ""
        labelSource.text = ""
    
    elif turn == 1:
        currentBall = turn1(headlineDic, labelPing, labelPong, labelSource)

    elif turn == 2:
        currentBall = turn2(headlineRaw, labelPong)
    
    elif turn == 3:
        currentBall = turn3(headlineRaw, labelPong)
    
    elif turn == 4:
        currentBall = turn4(headlineRaw, labelPong)

    elif turn == 5:
        currentBall = turn5(headlineRaw, labelPong)

    elif turn == 6:
        currentBall = turn6(headlineRaw, labelPong)

    elif turn == 7:
        currentBall = turn7(headlineRaw, labelPong)

    elif turn == 8:
        currentBall = turn8(headlineRaw, labelPong, bgColor)

    elif turn == 9:
        currentBall = turn9(headlineRaw, labelPong)

    elif turn == 10:
        currentBall = turn10(headlineRaw, labelPong)

    turn += 1
    print(turn)

    if turn > 11:
        turn = 0
        labelPing.text = ""
        labelPong.text = ""
        labelSource.text = ""
        bgColor = getRandomColor()
        pongBgColor = getComplementaryColor(bgColor)

        headlineIndex = (headlineIndex + 1) % len(headLines)
        headlineDic = headLines[headlineIndex]
        headlineRaw = headlineDic["title"]




pyglet.clock.schedule_interval(updateWindow, 2)
pyglet.app.run()



