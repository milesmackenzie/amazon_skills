
from __future__ import print_function
import json
from botocore.vendored import requests
from random import randint

def build_speechlet_response_final(title, output, reprompt_text, should_end_session, cocktail):
    
    if cocktail == "manhattan" or cocktail == "Manhattan":
        summary = "\n" + "-----------------------------------------------" + "\n" + \
                    " Maraschino cherry: 1" + "\n" + \
                    " Angostura Bitters: 2 Dashes" +  "\n" + \
                    " Jack Daniel's Whiskey: 2 ounces" +  "\n" + \
                    " Dolin Blanc Vermouth: 3/4 ounces" +  "\n" + \
                    "-----------------------------------------------"

    elif cocktail == "negroni":
        summary = "\n" + "-----------------------------------------------" + "\n" + \
                    " Bombay Sapphire Gin: 1 ounce" + "\n" + \
                    " Dolin Rouge Red Sweet Vermouth: 1 ounce" +  "\n" + \
                    " Campari Aperitivo: 1 ounce" +  "\n" + \
                    " * Orange Peel * " +  "\n" + \
                    "-----------------------------------------------"
    elif cocktail == "old fashioned" or cocktail == "old fashion":
        summary = "\n" + "-----------------------------------------------" + "\n" + \
                    " Bulleit Bourbon: 2 ounces" + "\n" + \
                    " Angostura Bitters: 2 Dashes" +  "\n" + \
                    " Sugar Cube: 1" +  "\n" + \
                    " Plain Water: 2 Dashes" +  "\n" + \
                    "-----------------------------------------------"
    elif cocktail == "moscow mule" or cocktail == "Moscow mule" or cocktail == "Moscow Mule":
        summary = "\n" + "-----------------------------------------------" + "\n" + \
                    " Grey Goose Vodka: 1.5 ounces" + "\n" + \
                    " Fresh squeezed lime juice: 1/2 ounce" +  "\n" + \
                    " Gosling's Ginger Beer: 1/2 cup" +  "\n" + \
                    " * One lime wedge (Garnish) *" +  "\n" + \
                    "-----------------------------------------------"
    elif cocktail == 'margarita':
        summary = "\n" + "-----------------------------------------------" + "\n" + \
                    " Jose Cuervo Gold Tequila: 3 ounces" + "\n" + \
                    " Fresh squeezed lime juice: 2 ounces" +  "\n" + \
                    " Simple Syrup: 1 ounce" +  "\n" + \
                    " Orange Liqueur: 1 teaspoon" +  "\n" + \
                    " * Salt rim to taste *" +  "\n" + \
                    "-----------------------------------------------"

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': title,
            'text': summary,
            "image": {
              "smallImageUrl": None,
              "largeImageUrl": None
            }
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
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


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
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


def get_cocktail(intent, session):
    print(intent)
    print (session)
    session_attributes = {}
    if len(intent['slots']['Cocktail']) > 2:
        cocktail = intent['slots']['Cocktail']['value']
        print (cocktail)
    else:
        cocktail = "none"
    if cocktail == "manhattan" or cocktail == "Manhattan":
        speech_output = "A Manhattan uses a Maraschino cherry, Angostura Bitters, Vermouth and your choice of rye or bourbon. Check the home tab of your alexa app for our recommendations and proportions."

    elif cocktail == "negroni":
        speech_output = "A Negroni uses campari, vermouth, an orange peel and your choice of gin. Check the home tab of your alexa app for our recommendations and proportions."

    elif cocktail == "old fashioned" or cocktail == "old fashion":
        speech_output = "An Old Fashioned uses Angostura Bitters, a sugar cube (or simple syrup), an orange peel and your choice of rye or bourbon. Check the home tab of your alexa app for our recommendations and proportions."

    elif cocktail == "moscow mule" or cocktail == "Moscow mule" or cocktail == "Moscow Mule":
        speech_output = "A Moscow mule uses ginger beer, lime and your choice of vodka. Check the home tab of your alexa app for our recommendations and proportions."

    elif cocktail == 'margarita':
        speech_output = 'Our Margarita uses fresh squeezed lime juice, simple syrup, orange liqueur, and your choice of tequila. Check the home tab of your alexa app for our recommendations and proportions.'

    else:
        return fall_back()
    


    card_title = cocktail.title() + " Recipe"
    reprompt_text = None
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response_final(
        card_title, speech_output, reprompt_text, should_end_session, cocktail))



def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Cocktail Builder. You can ask for recipes of a Moscow Mule, Negroni, Manhattan, Dark and Stormy, Margarita or Old Fashioned" \
                    ". For example you could say, what is in a Moscow Mule." \

    reprompt_text = "You can ask, what is in a Manhattan."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help():

    session_attributes = {}
    card_title = "Help"
    speech_output = "Cocktail Builder is designed to give you ingredients for popular cocktails. " \
                    " You can ask how to make a certain cocktail or what is inside. " \
                    "one. Say cancel or stop to exit the skill. "

    reprompt_text = "You can ask, what is in a Manhattan."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Cocktail Builder. " \
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
    reprompt_text = "Sorry I don't know that one."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return get_welcome_response()

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "AskIntent":
        return get_cocktail(intent, session)
    elif intent_name == "AMAZON.FallbackIntent":
        return fall_back()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        return fall_back()


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
