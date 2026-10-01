from flask import Flask
from backend.routes import api
from errors import error_response
app = Flask(__name__)
app.register_blueprint(api)

@app.errorhandler(404)
def handle_404(error):
    return error_response("Ресурс не найден",404)

@app.errorhandler(405)
def handle_405(error):
    return error_response("Метод не поддерживается", 405)

@app.errorhandler(500)
def handle_500(error):
    return error_response("Внутренняя ошибка сервера", 500)


if __name__=="__main__":
    app.run(debug=True)