import sys
sys.path.insert(0, '.')
from nlp.nlp_processing import process_review

texts = [
    'Absolutely incredible, best mentor ever',
    'Pretty good, helped me a lot',
    'Okay, nothing special',
    'Not great, some issues',
    'Absolutely terrible, worst experience',
]

for text in texts:
    r = process_review(text)
    print(f'{r["sentiment"]:6.2f} | {text}')
