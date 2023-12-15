# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from rasa_sdk.events import ActionExecuted
import os
from rasa_sdk.events import SlotSet

logger = logging.getLogger(__name__)
class ActionHaystack(Action):

    def name(self) -> Text:
        return "call_haystack"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = "http://haystack_api:8000/query"
        payload = {"query": str(tracker.latest_message["text"])}
        headers = {
            'Content-Type': 'application/json'
        }
        logger.info("222222222222222222222222222222222222222222222222222222222222222222")
        response = requests.request("POST", url, headers=headers, json=payload).json()

        if response["answers"]:
            answer = response["answers"][0]["answer"]
            logger.info("4444444444444444444444444444444444444444444444")
            logger.info(response["answers"][0]['score'])
            score=response["answers"][0]['score']
        else:
            answer = "No Answer Found!"

        dispatcher.utter_message(text=answer,score=score)


        return []


class ActionRequestHuman(Action):
    def name(self):
        return 'action_request_human'

    def run(self, dispatcher, tracker, domain):
        print("I REQUEST HUMAN AND I SEND TO CHANNEL TO CONNECT TO SOMEONE ELSE")
        return []


class ActionSessionStart(Action):
    def name(self):
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # desired_value = tracker.latest_message.get("entities", {}).get("userName", None)

        # custom_data = tracker.get_slot("userName")
        # logger.info("WTFFFFFFFFFFFFFFFFFFF")
        # SlotSet("language",tracker.get_slot("language"))
        #
        # language_value=custom_data
        # SlotSet("language", custom_data)
        # # print("I USERNAME TOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO : " )
        # print(custom_data)

        # print("I SET LANGUAGE TO : "+language_value)
        # language_value = 'Greek'
        if tracker.get_slot("userName") in ["English", "Greek"]:
            logger.info("MPIKEEEEEEEEEEEEEEEEEEEEEEE")
            return [SlotSet("language", language_value)]
        return [ActionExecuted("action_session_start")]

class SetLanguageSlotAction(Action):
    def name(self) -> Text:
        return "action_set_language_slot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Fetch the value of the environment variable
        language_value = tracker.get_slot("language") # Replace with your environment variable name
        # language_value = 'Greek'
        if language_value in ["English", "Greek"]:
            return [SlotSet("language", language_value)]


