import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("spacytextblob")


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
