from flask import Flask
from flask_restful import Api, Resource, reqparse
from http.client import NO_CONTENT, NOT_FOUND, CREATED, OK

app = Flask(__name__)
api = Api(app)

events = {}

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
        events[event_id] = {
            'title': args['title'],
            'description': args['description'],
            'date': args['date'],
        }
        if events[event_id]['title'] and events[event_id]['date'] not in events[event_id]:
            return events[event_id], CREATED

    def get(self):
        return list(events.values()), OK

class Event(Resource):
    def put(self, event_id):
        if event_id in events:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=non_empty_str, required=True)
            parser.add_argument('description', type=non_empty_str, required=True)
            parser.add_argument('date', type=non_empty_str, required=True)
            args = parser.parse_args(strict=True)

            events[event_id] = {
                'title': args['title'],
                'description': args['description'],
                'date': args['date'],
            }
            return OK
        else:
            return None, NOT_FOUND

    def delete(self, event_id):
        if event_id in events:
            del events[event_id]
            return None, NO_CONTENT
        else:
            return None, NOT_FOUND

api.add_resource(Events, '/events/')
api.add_resource(Event, '/events/<event_id>')