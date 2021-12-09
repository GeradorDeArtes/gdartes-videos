from flask import Flask
from flasgger import Swagger
from api.route.home import home_api
from api.route.video import video_api
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)
    cors = CORS(app)

    app.config['SWAGGER'] = {
        'title': 'Moviepy API interface',
    }
    app.config['CORS_HEADERS'] = 'Content-Type'
    swagger = Swagger(app)
     ## Initialize Config
    app.config.from_pyfile('config.py')
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(video_api, url_prefix='/video')

    return app

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()
    app.run(host='0.0.0.0', port=port)


#https://livecodestream.dev/post/python-flask-api-starter-kit-and-project-layout/
#pipenv run python -m flask run
#pipenv run python -m unittest