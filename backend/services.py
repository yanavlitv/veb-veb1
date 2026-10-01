#можно ли создать студента, как изменить студента
import backend.repository as repository
from backend.validators import validate_student, validate_patch, validate_filters

def get_students(filter_data=None):
    if filter_data is None:
        filter_data={}
    filters, errors= validate_filters(filter_data)

    if errors:
        return None, errors, 422 #422 - сервер понял синтаксис запроса, но не смог его выполнить из-за логических ошибок или сбоя валидации данных
    
    students= repository.get_all()
    result=[]
    for student in students:
        if "group" in filters:
            if student["group"]!= filters["group"]:
                continue
        if "dormitory" in filters:
            if student["dorm"]!=filters["dormitory"]:
                continue
        if "isForeign" in filters:
            if student["isForeign"]!=filters["isForeign"]:
                continue
        result.append(student)
    return result, None, 200

def get_student(isu_id):
    return repository.get_by_id(isu_id)


def create_student(data):
    errors = validate_student(data)

    if errors:
        return None, errors, 422

    isu_id = data["isuId"]

    if repository.exists(isu_id):
        return None, None, 409

    student = {
        "name": data["name"].strip(),
        "group": data["group"].upper(),
        "isuId": data["isuId"],
        "dorm": data["dorm"],
        "room": data["room"],
        "date": data["date"],
        "isForeign": data.get("isForeign", False),
        "notes": data.get("notes", "").strip()
    }

    repository.add(student)

    return student, None, 201



def update_student(isu_id, data):
    student = repository.get_by_id(isu_id)

    if student is None:
        return None, None, 404

    errors = validate_patch(data)

    if errors:
        return None, errors, 422

    updated_student = student.copy()

    if "name" in data:
        updated_student["name"] = data["name"].strip()

    if "group" in data:
        updated_student["group"] = data["group"].upper()

    if "dorm" in data:
        updated_student["dorm"] = data["dorm"]

    if "room" in data:
        updated_student["room"] = data["room"]

    if "date" in data:
        updated_student["date"] = data["date"]

    if "isForeign" in data:
        updated_student["isForeign"] = data["isForeign"]

    if "notes" in data:
        updated_student["notes"] = data["notes"].strip()

    repository.update(updated_student)

    return updated_student, None, 200
def delete_student(isu_id):
    student=repository.get_by_id(isu_id)
    if student is None:
        return False
    repository.delete(isu_id)
    return True