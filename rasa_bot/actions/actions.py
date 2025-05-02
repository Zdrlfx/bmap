from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import spacy

nlp = spacy.load("en_core_web_sm")

class ActionExtractLocations(Action):
    def name(self):
        return "action_extract_locations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        text = tracker.latest_message.get("text", "")
        doc = nlp(text)

        # Start clean
        origin = None
        destination = None

        # First pass: standard 'from'/'to' logic
        for token in doc:
            if token.dep_ == "pobj" and token.head.text.lower() == "from":
                origin = token.text
            elif token.dep_ == "pobj" and token.head.text.lower() == "to":
                destination = token.text

        # Try pulling previous slot values (if user is replying turn-by-turn)
        prev_origin = tracker.get_slot("origin")
        prev_destination = tracker.get_slot("destination")

        # If origin is still missing, try from last message using pobj or ROOT
        if prev_destination and not prev_origin:
            for token in doc:
                if token.dep_ == "pobj":
                    origin = token.text
                elif token.dep_ == "ROOT" and not origin:
                    origin = token.text
        else:
            origin = origin or prev_origin

        # Same for destination
        if prev_origin and not prev_destination:
            for token in doc:
                if token.dep_ == "pobj":
                    destination = token.text
                elif token.dep_ == "ROOT" and not destination:
                    destination = token.text
        else:
            destination = destination or prev_destination

        # Now decide how to respond
        if not origin:
            dispatcher.utter_message("Where are you now?")
            return [SlotSet("origin", None), SlotSet("destination", destination)]

        if not destination:
            dispatcher.utter_message("Where do you want to go?")
            return [SlotSet("origin", origin), SlotSet("destination", None)]

        # Both filled — now call backend and reset
        from .backend.main import get_route_summary
        result = get_route_summary(origin, destination)
        dispatcher.utter_message(text=result)

        return [SlotSet("origin", None), SlotSet("destination", None)]
