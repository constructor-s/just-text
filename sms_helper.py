from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = "AC8d75b2a41d613d53d67bb1ea5d969460"
AUTH_TOKEN = "" # AUTH_TOKEN for Twilio

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

from_number ="+12268870818"


def get_from_number():
    return from_number


def send_mms(to, from_, body, media_url):
    message = client.messages.create(
            to=to,
            from_=from_,
            body=body,
            media_url=media_url)