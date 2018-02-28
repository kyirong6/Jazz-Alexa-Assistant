"""
A skill built with the Amazon Alexa Skills Kit that gives you a jazz artist.
"""

from __future__ import print_function
import random



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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



"""
A function that holds jazz artists according to style/era
"""
def build_artist(artist):
    bop = ["Charlie Parker", "Dizzy Gillespie", "Bud Powell", "Thelonious Monk",
            "Max Roach", "Dexter Gordon", "Chet Baker", "Keith Jarrett"]
            
    modern = ["Aaron Parks", "Kurt Rosenwinkel", "Brian Blade", "Matt Brewer",
            "Ben Wendel", "Brad Mehldau"]
            
    fusion = ["Nir Felder", "Miles Davis", "Chick Corea", "Weather Report", 
                "John McLaughlin"]
    
    if artist == "bop":
        return random.choice(bop)
    elif artist == "modern":
        return random.choice(modern)
    elif artist == "fusion":
        return random.choice(fusion)


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Jazz Artist of The Day! Would you like" + " a bop, modern, or fusion artist?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what type of jazz artist you want. Bop" + " Modern, or fusion?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    """ An intent to provide more information.
    """
    session_attributes = {}
    card_title = "Extra"
    speech_output = "Hello, i'm glad you asked for help. I can recommend you a jazz artist to listen to based on a era you tell me. So far, i am limited to bop, modern, and fusion. So, which era would you like?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for visiting Jazz Artist of the Day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_bop(intent, session):
    """
    return a bop based artist
    """
    card_title = "Bop Artist"
    reprompt_text = None
    response_string = "Taking it back old school... {a} is the way to go today. He's personally one of my favorites. The language of bebop is so complex".format(a=build_artist("bop"))
    
    return build_response({}, build_speechlet_response(
        card_title, response_string, reprompt_text, True))
        
        
def get_modern(intent, session):
    """
    return a modern jazz artist
    """
    card_title = "Modern Artist"
    reprompt_text = None
    response_string = "Modern i see... {a} is your artist for today! Spectacular he is. Truly mindblowing, and the way he expresses himself is beautiful".format(a=build_artist("modern"))
    
    return build_response({}, build_speechlet_response(
        card_title, response_string, reprompt_text, True))
    
        
def get_fusion(intent, session):
    """
    return a jazz fusion artist
    """
    card_title = "Fusion Artist"
    reprompt_text = None
    response_string = "oh, i personally love this era. I recommend {a}. He is amazing and has an interesting appraoch to his craft.".format(a=build_artist("fusion"))
    
    return build_response({}, build_speechlet_response(
        card_title, response_string, reprompt_text, True))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "get_bop":
        return get_bop(intent, session)
    elif intent_name == "get_modern":
        return get_modern(intent, session)
    elif intent_name == "get_fusion":
        return get_fusion(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])


    if (event['session']['application']['applicationId'] !=
            "MY_APPLICATION_ID"):
       raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
