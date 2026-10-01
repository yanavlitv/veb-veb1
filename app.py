import os
from flask import Flask, send_from_directory
from backend.routes import api
from backend.errors import error_response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
app.register_blueprint(api)



@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)



@app.errorhandler(404)
def handle_404(error):
    return error_response("Ресурс не найден", 404)


@app.errorhandler(405)
def handle_405(error):
    return error_response("Метод не поддерживается", 405)


@app.errorhandler(500)
def handle_500(error):
    return error_response("Внутренняя ошибка сервера", 500)


if __name__ == "__main__":
    app.run(debug=True)