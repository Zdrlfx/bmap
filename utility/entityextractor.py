# spacy_test.py

import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Example text
text =input("How can i help you?\n")

# Parse the sentence
doc = nlp(text)

origin = None
destination = None


for token in doc:
    if token.dep_ == "pobj" and token.head.text.lower() == "from":
        origin = token.text
    elif token.dep_ == "pobj" and token.head.text.lower() == "to":
        destination = token.text

while origin is None or destination is None:
    if origin is None:
        text = input("Where are you now?")
        doc = nlp(text)
        for token in doc:
            if token.dep_ == "pobj":
                origin = token.text
            elif token.dep_ == "ROOT":
                origin = token.text

    if destination is None:
        text = input("Where do you want to go?")
        doc = nlp(text)
        for token in doc:
            if token.dep_ == "pobj":
                destination = token.text
            elif token.dep_ == "ROOT":
                destination = token.text

    

print(f"Origin: {origin}")
print(f"Destination: {destination}")