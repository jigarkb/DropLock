import os
from google.appengine.api import mail
from google.appengine.ext import db

def template(file_name, directory="templates"):
  return os.path.join(os.path.dirname(__file__), directory, file_name)


def send_mail(receiver_email, body, subject):
    message = mail.EmailMessage(sender="Drop Lock Team <jigarbhatt93@gmail.com>",
                                subject=subject)
    message.body = body
    message.body += '\n\nRegards,\nDrop Lock Team'
    message.to = [receiver_email]
    message.bcc = ['jigarbhatt93@gmail.com']
    message.reply_to = 'jigarbhatt93@gmail.com'
    message.send()


def fetch_gql(query_string, fetchsize=50):
    q = db.GqlQuery(query_string)
    cursor = None
    results = []
    while True:
        q.with_cursor(cursor)
        intermediate_result = q.fetch(fetchsize)
        if len(intermediate_result) == 0:
            break
        cursor = q.cursor()
        results += intermediate_result

    return results