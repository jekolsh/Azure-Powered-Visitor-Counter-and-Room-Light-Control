import json
import logging
import azure.functions as func
import requests

endpoint = "***********************"
chat_id = "***********************"
token = "***********************"


def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    logging.info('Python EventGrid trigger processed an event: %s', result)

    result_dict = json.loads(result)

    counter = result_dict['data']['body']['visitorCount']
    
    if counter > 5:
        message_data = f"Too crowded in the room! Number of people inside: {counter}"
    elif counter > 0:
        message_data = f"Someone is in the room, LED is turned on. Number of people inside: {counter}"
    elif counter == 0:
        message_data = "No one is in the room, LED is turned off"
    else:
        message_data = "Unknown event type"

    message = f'{message_data}'

    telegram_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"

    try:
        response = requests.get(telegram_url)
        response.raise_for_status()
        logging.info("Telegram response: %s", response.text)
    except requests.exceptions.RequestException as e:
        logging.error("Error sending message to Telegram: %s", e)



