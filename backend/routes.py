from flask import Blueprint, request #способ вынести маршруты фласк из апп
import backend.services as services


api = Blueprint("api", __name__)


@api.get("/api/requests")
def get_students():
    filter_data= request.args.to_dict()
    students, errors, status = services.get_students(filter_data)
    if status==422:
        return{
            "error" :{
                "message":"Ошибка фильтрации",
                "fields": errors
            }
        },422
    return students, 200

@api.get("/api/requests/<int:isu_id>")
def get_student(isu_id):
    student = services.get_student(isu_id)
    
    if student is None:
        return {
            "error": {
                "message": "Студент не найден"
            }
        }, 404
    return student, 200


@api.post("/api/requests")
def create_student():
    if not request.is_json:
        return {
            "error": {
                "message": "Ожидается JSON"
            }
        }, 400

    data = request.get_json(silent=True)

    if data is None:
        return {
            "error": {
                "message": "Некорректный JSON"
            }
        }, 400
    
    if not isinstance(data, dict):
        return {
            "error": {
                "message": "JSON должен быть объектом"
            }
        }, 400

    student, errors, status = services.create_student(data)

    if status == 422:
        return {
            "error": {
                "message": "Ошибка валидации",
                "fields": errors
            }
        }, 422

    if status == 409:
        return {
            "error": {
                "message": "Студент с таким ИСУ ID уже существует"
            }
        }, 409 #дубликат ису

    return student, 201 #201-студент создан пост
@api.patch("/api/requests/<int:isu_id>")
def update_student(isu_id):
    if not request.is_json:
        return {"error": {"message": "Ожидается JSON"}}, 400

    data = request.get_json(silent=True)
    if data is None:
        return {"error": {"message": "Некорректный JSON"}}, 400
    if not isinstance(data, dict):
        return {"error": {"message": "JSON должен быть объектом"}}, 400 #400- плохой джсон/структура

    student, errors, status = services.update_student(isu_id, data)

    if status == 404:
        return {"error": {"message": "Студент не найден"}}, 404 #404- ресурс или студент не найден

    if status == 422:
        return {
            "error": {
                "message": "Ошибка валидации",
                "fields": errors
            }
        }, 422

    return student, 200
@api.delete("/api/requests/<int:isu_id>")
def delete_student(isu_id):
    deleted=services.delete_student(isu_id)
    if not deleted:
        return{
            "error":{
                "message":"Студент не найден"
            }
        }, 404
    return "",204 # студент удален

@api.route("/api/requests", methods=["QUERY"])
def query_students():
    if not request.is_json:
        return {
            "error": {
                "message": "Ожидается JSON"
            }
        }, 400
    data=request.get_json(silent=True)
    if data is None:
        return {
            "error": {
                "message": "Некорректный JSON"
            }
        }, 400
    if not isinstance(data, dict):
        return {
            "error": {
                "message": "JSON должен быть объектом"
            }
        }, 400 #проблема со структурой самого запроса бед рекьест
    students, errors, status = services.get_students(data)

    if status == 422:
        return {
            "error": {
                "message": "Ошибка фильтрации",
                "fields": errors
            }
        }, 422 #422 - запрос синт понятный, но значения неправильные

    return students, 200 #200- гет/патч/квери успешно
    