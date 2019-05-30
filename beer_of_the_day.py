
from __future__ import print_function
import json
from botocore.vendored import requests
from random import randint

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


b = [{"Brewery": "Odell Brewing Company", "Beer": "Easy Street", "ABV": "4.6"},
{"Brewery": "Avery Brewing Company", "Beer": "White Rascal", "ABV": "5.6"},
{"Brewery": "Echo Brewing Company", "Beer": "Pika Porter", "ABV": "6"},
{"Brewery": "Upslope Brewing Company", "Beer": "Citra Pale Ale", "ABV": "5.8"},
{"Brewery": "Crazy Mountain Brewing", "Beer": "Creedence Pilsner", "ABV": "4.9"},
{"Brewery": "Oskar Blues Brewery", "Beer": "Dales Pale Ale", "ABV": "6.5"}]

def get_beer():
    session_attributes = {}
    card_title = "Beer"
    item = b[randint(0,5)]
    beer = item["Beer"]
    abv = item["ABV"]
    brewery = item['Brewery']

    if "IPA" in beer:
        beer = beer.replace("IPA", "I.P.A.")

    speech_output = "Your random beer is the " + \
                    beer + \
                    ", From the " + \
                    brewery + \
                    " with an ABV of " + \
                    abv + \
                    "%. You can ask for another beer or say cancel to exit. "

    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Beer of the Day " \
                    ". " \

    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help():

    session_attributes = {}
    card_title = "Help"
    speech_output = "Beer of the day is designed to give you a random beer. " \
                    " You can ask me for a beer or simply open the skill to recieve " \
                    "one. Say cancel or stop to exit the skill. Would you like a random beer? "

    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Beer of the Day. " \
                    "Cheers! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def fall_back():
    session_attributes = {}
    card_title = "Fallback"
    should_end_session = False
    speech_output = "Sorry I don't know that one " \
                    "."
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return get_beer()

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "BeerIntent":
        return get_beer()
    elif intent_name == "AnotherIntent":
        return get_beer()
    elif intent_name == "AMAZON.FallbackIntent":
        return fall_back()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])


    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])