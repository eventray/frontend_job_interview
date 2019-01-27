'''Skeleton app for airline ticket REST API

To set up the development environment:

    - Put this file wherever you want.  (It shouldn't be in the
      same directory as the virtualenv you will be creating in just
      a moment.)

    - Install Python3
        https://www.python.org/downloads/

    - Create a virtualenv for this project and activate it:
      % python3 -m venv venv
      % source venv/bin/activate

    - Install Pyramid:
      % pip install pyramid

    - Run this app:
      % python app.py

    You can now access the REST API at http://localhost:5000.  Changes made to
    this file while the Pyramid server is running are not automatically picked
    up, so you'll have to kill and restart the process (^C in the terminal will
    work).
'''

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import json
import random
import string

def get_confirmation_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def flights(request):
    with open('flights.json') as f:
        content = json.loads(f.read())

    return content

def book(request):
    if random.randint(0,100) < 20:
        return {
            "success": False,
            "message": "This flight is full."
        }
    else:
        errors = []
        try:
            if 'first_name' not in request.json:
                errors.append({
                    "field": "first_name",
                    "error": "is_required",
                })

            if 'last_name' not in request.json:
                errors.append({
                    "field": "last_name",
                    "error": "is_required",
                })
        except:
            errors.append({
                "field": "all",
                "error": "empty_request"
            })

        if not errors:
            return {
                "success": True,
                "confirmation": get_confirmation_number()
            }
        else:
            return {
                "success": False,
                "message": "You did not pass a valid request.",
                "errors": errors,
            }

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('flights', '/flights')
        config.add_view(
            flights, route_name='flights', renderer='json'

        )
        config.add_route('book', '/book')
        config.add_view(
            book, route_name='book', renderer='json'
        )

        app = config.make_wsgi_app()
    print('Servers on http://0.0.0.0:5000')
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
