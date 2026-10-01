_INITIAL_STUDENTS = [
    {
        "name": "Иванов Иван Иванович",
        "group": "M3301",
        "isuId": 123456,
        "dorm": 8,
        "room": "55",
        "date": "2024-09-01",
        "isForeign": False,
        "notes": "Староста группы"
    },
    {
        "name": "Петрова Анна Сергеевна",
        "group": "M3302",
        "isuId": 234567,
        "dorm": 8,
        "room": "102",
        "date": "2024-09-02",
        "isForeign": False,
        "notes": ""
    },
    {
        "name": "Smith John Michael",
        "group": "M3301",
        "isuId": 345678,
        "dorm": 11,
        "room": "210",
        "date": "2024-08-28",
        "isForeign": True,
        "notes": "Из США, обмен"
    },
    {
        "name": "Сидоров Пётр Алексеевич",
        "group": "M3303",
        "isuId": 456789,
        "dorm": 11,
        "room": "5",
        "date": "2024-09-05",
        "isForeign": False,
        "notes": "Нужен пропуск в общежитие"
    },
    {
        "name": "Кузнецова Мария Дмитриевна",
        "group": "M3302",
        "isuId": 567890,
        "dorm": 8,
        "room": "77",
        "date": "2024-09-03",
        "isForeign": False,
        "notes": ""
    }
]


students = {s["isuId"]: s for s in _INITIAL_STUDENTS}


def get_all():
    return list(students.values())

def get_by_id(isu_id):
    return students.get(isu_id)

def exists(isu_id):
    return isu_id in students


def add(student):
    students[student["isuId"]] = student

def update(student):
    students[student["isuId"]]=student

def delete(isu_id):
    del students[isu_id]