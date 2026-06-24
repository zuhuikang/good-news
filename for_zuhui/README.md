to properly and consistently run this project pls do the following steps to setup all dependencies properly. 

1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. python -m spacy download en_core_web_sm
5. python -m textblob.download_corpora

now every time you open a new terminal session you need to run: 

source .venv/bin/activate