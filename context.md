# good-news
let's figure it out

## (rough) proj description
Good News is a project about the process of a news story becoming data. A story gets written about an event, and the judgments contained within that story are categorized and converted into numerical values which are then commodified for data points. Good News takes that process as its material.<br>
<br>


## structure: two windows (ping / pong) 
this piece runs across two windows, which i named them as "ping" and "pong". The point of splitting it this way is to let people witness the computation of each stage in the news-to-data process as a time based sequence. the full sequence a single headline goes through is divided into phase1 and phase2. So far only phase1 has been designed.<br>
<br>
### phase 1
phase1 is about showing the process of a headline turning into data. every stage strips away a bit of the original sentence's specific content and replaces it with something more generic and machine-readable.<br>
<br>
the sequence goes:

1. original headline
2. headline → `shape`
3. headline → `lemma`
4. headline → `pos`
5. headline → `tag`
6. headline → `is_stop` (shown as True/False per token)
7. is_stop result applied: `True` tokens shown as `shape`, `False` tokens shown as the original word
8. only the words picked up by sentiment assessments are kept; the rest disappear
9. those surviving words shown with their individual sentiment scores
10. final polarity score

every stage is just the raw output from spaCy and TextBlob. the whole point of this visualization is to make that reductive abstraction(language getting flattened into data) more visible.<br>
<img width="400" height="auto" alt="spongebob_reductive_abstraction" src="https://github.com/user-attachments/assets/d917e413-d95e-49c4-86ce-ad5f46817df3" />
<br>
here are the keynote animation outputted as .mp4 for reference what it should look like.
- [phase1-example1.mp4](https://github.com/zuhuikang/good-news/blob/main/reference/phase1-example1.mp4) 
- [phase1-example2.mp4](https://github.com/zuhuikang/good-news/blob/main/reference/phase1-example2.mp4)

the difficulty that i'm having atm is to get it right on the transition part. words appearing one letter/word at a time (one idea is to visualize it by manipulating the opacity setting, like from 0 to 1), then each stage's word being directly replaced by the next stage's words in place, or hiding the words (this can also be visualized by opacity manipulation, like from 1 to 0). right now the code just swapts each stage's text all at once. the word-by-word transition hasn't been implemented yet. which I need help for.<br>
<br>
### phase 2
this is the part where the final polarity score from phase1 would somehow reach back and mess with the original headline (the one sitting on ping the whole time). but i haven't figure this part out yet.<br>
<br><br>
### installation plan
<img width="300" height="auto" alt="installation_plan" src="https://github.com/user-attachments/assets/66fc0879-9330-4bbe-a73c-f023644735a5" /><br>
or this(if possible):<br>
<img width="300" height="auto" alt="vertical_throw" src="https://github.com/user-attachments/assets/a6e0a744-556c-4559-8ddf-05bd9bbd2c94" />




