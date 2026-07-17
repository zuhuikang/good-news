import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")


def getNLPTokens(text: str) -> list[str]:
    doc = nlp(text)
    return [token.text for token in doc]


def tokenizeForDisplay(text: str) -> str:
    """
    Re-render `text` so every space-separated word is exactly one spaCy
    token: "son's" -> "son 's", "wedding:" -> "wedding :".

    Every function below (getNLPShape, getNLPLemma, ...) and every
    animation in text_animations.py that does `.split(" ")` assumes
    "word" == "spaCy token". That's only true if the text was already
    laid out this way before it was ever shown on screen. Call this once,
    at load time, on raw headline text - title strings stored anywhere
    downstream (Headline, SourceLine, the animations) should already be
    the output of this function, not the raw file line.

    This replaces the earlier char-span grouping approach. That approach
    kept the original "son's" intact and merged spaCy's two token
    results back into one display slot with a "/" separator. This does
    the opposite: it changes what counts as a "word" so there's nothing
    to merge or hide. The original text now visibly gets an extra space
    before attached punctuation.
    """
    return " ".join(getNLPTokens(text))


def getNLPShape(text: str) -> list[str]:
    doc = nlp(text)
    return [token.shape_ for token in doc]


def getNLPLemma(text: str) -> list[str]:
    doc = nlp(text)
    return [token.lemma_ for token in doc]


def getNLPPos(text: str) -> list[str]:
    doc = nlp(text)
    return [token.pos_ for token in doc]


def getNLPTag(text: str) -> list[str]:
    doc = nlp(text)
    return [token.tag_ for token in doc]


def getNLPIsStop(text: str) -> list[str]:
    doc = nlp(text)
    return [str(token.is_stop) for token in doc]


def getNLPSentiment(text: str) -> list[tuple[list[str], float, float, str]]:
    doc = nlp(text)
    return doc._.blob.sentiment_assessments.assessments


def getSentimentTexts(
    text: str,
) -> list[list[str]]:
    sentiments = getNLPSentiment(text)
    return [sentiment[0] for sentiment in sentiments]


def getNLPPolarity(text: str) -> str:
    doc = nlp(text)
    polarity = doc._.blob.polarity
    return f"{polarity:.2f}"


# check what turn 7 does


# def turn8(headline):
#     doc = nlp(headline)
#     assessments = doc._.blob.sentiment_assessments.assessments
#     tokens = [token.text.lower() for token in doc]

#     matchedPositions = set()
#     for words, polarity, subjectivity, assessLabel in assessments:
#         n = len(words)
#         for i in range(len(tokens) - n + 1):
#             if tokens[i : i + n] == words:
#                 for j in range(i, i + n):
#                     matchedPositions.add(j)

#     text = ""
#     spans = []
#     for i, word in enumerate(tokens):
#         start = len(text)
#         text += word
#         end = len(text)
#         spans.append((start, end, i in matchedPositions))
#         text += " "

#     matchedColor = rgbaFromFloat(bgColor)
#     fadedColor = (
#         int(pongBgColor["r"] * 255),
#         int(pongBgColor["g"] * 255),
#         int(pongBgColor["b"] * 255),
#         0,
#     )
#     # matched words are displayed as is, mismatched words are displayed as 0 in opacity
#     setDocTextWithSpans(
#         pongDoc, text, spans, matchedColor=matchedColor, fadedColor=fadedColor
#     )
#     return text


# def turn9(headline):
#     doc = nlp(headline)
#     assessments = doc._.blob.sentiment_assessments.assessments

#     lines = []
#     for words, polarity, subjectivity, assessLabel in assessments:
#         phrase = " ".join(words)
#         lines.append(f"{phrase} {round(polarity, 2)}")

#     result = "\n".join(lines)
#     setDocText(pongDoc, result, rgbaFromFloat(bgColor))
#     return result


# def turn10(headline):
#     doc = nlp(headline)
#     polarity = doc._.blob.polarity
#     result = str(round(polarity, 2))
#     setDocText(pongDoc, result, rgbaFromFloat(bgColor), fontSize=180)
#     return result