const form = document.getElementById('student-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');

const params = new URLSearchParams(location.search);
const editIsu = params.get('id');

// Утилиты
function showError(fieldName, message) {
    const span = document.getElementById(`error-${fieldName}`);
    if (span) span.textContent = message || '';
    const input = form.elements[fieldName];
    if (input && input.type !== 'checkbox') {
        input.classList.toggle('input-error', !!message);
    }
}

function clearAllErrors() {
    ['name','group','isuId','dorm','room','date','notes'].forEach(f => showError(f, ''));
}

async function parseError(res) {
    try {
        const data = await res.json();
        return data?.error || { message: `Ошибка ${res.status}` };
    } catch {
        return { message: `Ошибка ${res.status}` };
    }
}

// Загрузка при редактировании
async function loadStudent(isuId) {
    try {
        const res = await fetch(`/api/requests/${isuId}`);
        if (!res.ok) {
            const err = await parseError(res);
            throw new Error(err.message);
        }
        const s = await res.json();

        form.name.value = s.name || '';
        form.group.value = s.group || '';
        form.isuId.value = s.isuId ?? '';
        form.dorm.value = s.dorm ?? '';
        form.room.value = s.room ?? '';
        form.date.value = s.date || '';
        form.isForeign.checked = !!s.isForeign;
        form.notes.value = s.notes || '';
    } catch (err) {
        alert('Студент не найден: ' + err.message);
        location.href = 'index.html';
    }
}

if (editIsu) {
    formTitle.textContent = 'Редактирование студента';
    submitBtn.textContent = 'Сохранить';
    form.isuId.disabled   = true;
    loadStudent(Number(editIsu));
}

//Клиентская валидация
function validateField(name, value) {
    switch (name) {
        case 'name': {
            const v = String(value || '').trim();
            if (!v) return 'ФИО обязательно';
            if (/\d/.test(v)) return 'ФИО не должно содержать цифр';
            const parts = v.split(/\s+/);
            if (parts.length < 3) return 'Укажите фамилию, имя и отчество (минимум 3 слова)';
            for (const p of parts) {
                if (p.length < 2) return 'Каждое слово минимум 2 буквы';
                if (!/^[A-Za-zА-Яа-яЁё\-]+$/.test(p)) return 'Только буквы и дефис';
            }
            return '';
        }
        case 'group': {
            const v = String(value || '').trim().toUpperCase();
            if (!v) return 'Группа обязательна';
            if (!/^[A-Z][1-9]\d{3}$/.test(v)) return 'Формат: буква и 4 цифры, например A1111';
            return '';
        }
        case 'isuId':
            if (value === '' || value === null) return 'ИСУ ID обязателен';
            if (!/^\d+$/.test(String(value))) return 'ИСУ ID должен быть числом';
            if (String(value).length !== 6) return 'ИСУ ID — ровно 6 цифр';
            return '';
        case 'dorm':
            if (value === '' || value === null) return 'Общежитие обязательно';
            if (!/^\d+$/.test(String(value))) return 'Только цифры';
            if (Number(value) < 1) return 'Не меньше 1';
            return '';
        case 'room':
            if (value === '' || value === null) return 'Комната обязательна';
            if (!/^\d+$/.test(String(value))) return 'Только цифры';
            if (Number(value) < 1 || Number(value) > 150) return 'Комната от 1 до 150';
            return '';
        case 'date': {
            if (!value) return 'Укажите дату заселения';
            const d = new Date(value);
            if (isNaN(d.getTime())) return 'Некорректная дата';
            const MIN_YEAR = 2000;
            if (d.getFullYear() < MIN_YEAR) return `Дата не может быть раньше ${MIN_YEAR} года`;
            const today = new Date(); today.setHours(23, 59, 59, 999);
            if (d > today) return 'Дата не может быть в будущем';
            return '';
        }
        case 'notes':
            if (value && value.length > 50) return 'Максимум 50 символов';
            return '';
        default:
            return '';
    }
}

function validateForm() {
    let ok = true;
    ['name','group','isuId','dorm','room','date','notes'].forEach(f => {
        const err = validateField(f, form.elements[f].value);
        if (err) { ok = false; showError(f, err); }
        else showError(f, '');
    });
    return ok;
}

// Отправка формы
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearAllErrors();
    if (!validateForm()) return;

    const studentData = {
        name: form.name.value.trim(),
        group: form.group.value.trim().toUpperCase(),
        isuId: Number(form.isuId.value),
        dorm: Number(form.dorm.value),
        room: String(form.room.value).trim(),
        date: form.date.value,
        isForeign: form.isForeign.checked,
        notes: form.notes.value.trim()
    };

    try {
        let res;
        if (editIsu) {
            delete studentData.isuId;
            res = await fetch(`/api/requests/${editIsu}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData)
            });
        } else {
            res = await fetch('/api/requests', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(studentData)
            });
        }

        if (!res.ok) {
            const err = await parseError(res);

            if (err.fields && typeof err.fields === 'object') {
                for (const [field, msg] of Object.entries(err.fields)) {
                    showError(field, Array.isArray(msg) ? msg.join(', ') : msg);
                }
                return;
            }

            if (res.status === 409) {
                showError('isuId', err.message || 'Такой ИСУ ID уже существует');
                return;
            }

            alert(err.message || 'Ошибка сохранения');
            return;
        }

        location.href = 'index.html';
    } catch (err) {
        console.error(err);
        alert('Ошибка сети: ' + err.message);
    }
});

// Авто-верхний регистр для группы
document.getElementById('group').addEventListener('input', (e) => {
    const p = e.target.selectionStart;
    e.target.value = e.target.value.toUpperCase();
    e.target.setSelectionRange(p, p);
});

// Живая валидация
form.addEventListener('input', (e) => {
    const n = e.target.name;
    if (!n) return;
    const v = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    showError(n, validateField(n, v));
});