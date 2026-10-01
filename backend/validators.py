import re
from datetime import date, datetime


def validate_student(data):
    errors = {}

    if not isinstance(data, dict):
        return {"request": "JSON должен быть объектом"}

    required_fields = ["name", "group", "isuId", "dorm", "room", "date"]
    for field in required_fields:
        if field not in data:
            errors[field] = "Обязательное поле"

    if errors:
        return errors

    validate_name(data.get("name"), errors)
    validate_group(data.get("group"), errors)
    validate_isu_id(data.get("isuId"), errors)
    validate_dorm(data.get("dorm"), errors)
    validate_date(data.get("date"), errors)
    validate_room(data.get("room"), errors)
    validate_is_foreign(data.get("isForeign", False), errors)
    validate_notes(data.get("notes", ""), errors)

    return errors


def validate_name(value, errors):
    if not isinstance(value, str):
        errors["name"] = "ФИО должно быть строкой"
        return
    value = value.strip()
    if len(value) < 5 or len(value) > 50:
        errors["name"] = "ФИО должно содержать от 5 до 50 символов"
        return
    if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\-]+(\s+[A-Za-zА-Яа-яЁё\-]+){2,}", value):
        errors["name"] = "Укажите минимум три слова, только буквы и дефисы"


def validate_group(value, errors):
    if not isinstance(value, str):
        errors["group"] = "Группа должна быть строкой"
        return
    if not re.fullmatch(r"[A-Za-z][1-9]\d{3}", value):
        errors["group"] = "Формат группы: латинская буква и 4 цифры"


def validate_isu_id(value, errors):
    if isinstance(value, bool) or not isinstance(value, int):
        errors["isuId"] = "ИСУ ID должен быть целым числом"
        return
    if value < 100000 or value > 999999:
        errors["isuId"] = "ИСУ ID должен содержать 6 цифр"


def validate_dorm(value, errors):
    if isinstance(value, bool) or not isinstance(value, int):
        errors["dorm"] = "Номер общежития должен быть целым числом"
        return
    if value < 1:
        errors["dorm"] = "Номер общежития должен быть не меньше 1"


def validate_date(value, errors):
    if not isinstance(value, str):
        errors["date"] = "Дата должна быть строкой в формате YYYY-MM-DD"
        return
    try:
        student_date = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        errors["date"] = "Некорректная дата"
        return
    min_date = date(2000, 1, 1)
    today = date.today()
    if student_date < min_date:
        errors["date"] = "Дата не может быть раньше 2000-01-01"
        return
    if student_date > today:
        errors["date"] = "Дата не может быть позже сегодняшнего дня"


def validate_is_foreign(value, errors):
    if not isinstance(value, bool):
        errors["isForeign"] = "isForeign должен быть true или false"


def validate_notes(value, errors):
    if not isinstance(value, str):
        errors["notes"] = "Заметки должны быть строкой"
        return
    if len(value) > 50:
        errors["notes"] = "Заметки не должны превышать 50 символов"


def validate_patch(data):
    errors = {}
    if "isuId" in data:
        errors["isuId"] = "ИСУ ID нельзя изменять"
    if "name" in data:
        validate_name(data["name"], errors)
    if "group" in data:
        validate_group(data["group"], errors)
    if "dorm" in data:
        validate_dorm(data["dorm"], errors)
    if "room" in data:
        validate_room(data["room"], errors)
    if "date" in data:
        validate_date(data["date"], errors)
    if "isForeign" in data:
        validate_is_foreign(data["isForeign"], errors)
    if "notes" in data:
        validate_notes(data["notes"], errors)
    return errors


def validate_filters(data):
    errors = {}
    filters = {}

    allowed_filters = {"group", "dormitory", "isForeign"}

    for field in data:
        if field not in allowed_filters:
            errors[field] = "Неизвестный фильтр"

    if "group" in data:
        group = data["group"]
        if not isinstance(group, str):
            errors["group"] = "Группа должна быть строкой"
        elif not re.fullmatch(r"[A-Za-z][1-9]\d{3}", group):
            errors["group"] = "Формат группы: латинская буква и 4 цифры"
        else:
            filters["group"] = group.upper()

    if "dormitory" in data:
        dormitory = data["dormitory"]
        if isinstance(dormitory, str):
            if not dormitory.isdigit():
                errors["dormitory"] = "Номер общежития должен быть целым числом"
            else:
                dormitory = int(dormitory)
        elif isinstance(dormitory, bool) or not isinstance(dormitory, int):
            errors["dormitory"] = "Номер общежития должен быть целым числом"

        if "dormitory" not in errors:
            if dormitory < 1:
                errors["dormitory"] = "Номер общежития должен быть не меньше 1"
            else:
                filters["dormitory"] = dormitory

    if "isForeign" in data:
        is_foreign = data["isForeign"]
        if isinstance(is_foreign, str):
            if is_foreign.lower() == "true":
                filters["isForeign"] = True
            elif is_foreign.lower() == "false":
                filters["isForeign"] = False
            else:
                errors["isForeign"] = "isForeign должен быть true или false"
        elif isinstance(is_foreign, bool):
            filters["isForeign"] = is_foreign
        else:
            errors["isForeign"] = "isForeign должен быть true или false"

    return filters, errors


def validate_room(value, errors):
    if not isinstance(value, str):
        errors["room"] = "Комната должна быть строкой"
        return
    value = value.strip()
    if not value:
        errors["room"] = "Комната обязательна"
        return
    if not value.isdigit():
        errors["room"] = "Номер комнаты должен содержать только цифры"
        return
    room_number = int(value)
    if room_number < 1 or room_number > 150:
        errors["room"] = "Номер комнаты должен быть от 1 до 150"