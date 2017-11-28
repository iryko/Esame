from flask import Flask
from flask_restful import Api, Resource, reqparse
from http.client import NO_CONTENT, NOT_FOUND, CREATED, OK

app = Flask(__name__)
api = Api(app)

events = {}
cur_id = 0

# events = {
#     "birthday_01/11/2017": {
#         "title": "birthday",
#         "description": "Mary's birthday",
#         "date": "2017/10/12"
#     },
#     "baptism_10/12/2017": {
#         "title": "baptism",
#         "description": "Peter's baptism",
#         "date": "2017/11/01"
#     }
# }

def non_empty_str(val, name):
    if not str(val).strip():
        raise ValueError('The argument {0} is empty'.format(name))
    return str(val)


class Events(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=non_empty_str, required=True)
        parser.add_argument('description', type=non_empty_str, required=True)
        parser.add_argument('date', type=non_empty_str, required=True)
        args = parser.parse_args(strict=True)

        event_id = args['title'] + "_" + args['date']
        events[events_id] = {
            'title': args['title'],
            'description': args['description'],
            'date': args['date'],
        }
        return events[event_id], CREATED

    def get(self):
        return list(events.values()), OK

class Event(Resource):
    def get(self, title, date):
        event_id = title + "_" + date
        if event_id in events:
            return events[event_id], OK
        else:
            return None, NOT_FOUND

    #def put(self, title, date):
    
    def delete(self, title, date):
        event_id = title + "_" + date
        if event_id in events:
            del events[event_id]
            return None, NO_CONTENT
        else:
            return None, NOT_FOUND

api.add_resource(Events, '/events/')
api.add_resource(Event, '/event/<title>/<date>')