from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class ActionExtractLocations(Action):
    def name(self):
        return "action_extract_locations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        text = tracker.latest_message.get("text", "")
        doc = nlp(text)

        origin = None
        destination = None

        for token in doc:
            if token.dep_ == "pobj" and token.head.text.lower() == "from":
                origin = token.text
            elif token.dep_ == "pobj" and token.head.text.lower() == "to":
                destination = token.text

        dispatcher.utter_message(text=f"Origin: {origin}, Destination: {destination}")
        return [SlotSet("origin", origin), SlotSet("destination", destination)]
