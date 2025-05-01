from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import spacy
from .backend.main import get_route_summary

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
        if origin and destination:
            # Call the function to get route summary
            route_summary = get_route_summary(origin, destination)
            dispatcher.utter_message(text=f"Route Summary: {route_summary}")
        else:
            dispatcher.utter_message(text="Could not extract origin or destination.")
        return [SlotSet("origin", origin), SlotSet("destination", destination)]
