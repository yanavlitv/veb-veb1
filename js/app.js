// Аудио
const music = document.getElementById('bg-music');
const musicBtn = document.getElementById('music-btn');

musicBtn.addEventListener('click', () => {
    if (music.paused) {
        music.play();
        musicBtn.textContent = 'Выключить музыку';
    } else {
        music.pause();
        musicBtn.textContent = 'Включить музыку';
    }
});

// DOM
const tbody = document.getElementById('students-body');
const modal = document.getElementById('student-dossier');
const closeBtn = document.querySelector('.close-btn');

let studentsCache     = [];
let currentStudentIsu = null;
let currentFilters    = {};

// Утилиты
async function parseError(res) {
    try {
        const data = await res.json();
        return data?.error || { message: `Ошибка ${res.status}` };
    } catch {
        return { message: `Ошибка ${res.status}` };
    }
}

// Загрузка
async function loadAndRender(filters = currentFilters) {
    try {
        const params = new URLSearchParams();
        if (filters.group)     params.set('group', filters.group);
        if (filters.dormitory) params.set('dormitory', filters.dormitory);
        if (filters.isForeign) params.set('isForeign', filters.isForeign);

        const url = '/api/requests' + (params.toString() ? `?${params}` : '');
        const res = await fetch(url);

        if (!res.ok) {
            const err = await parseError(res);
            throw new Error(err.message);
        }

        const list = await res.json();
        renderTable(list);
    } catch (err) {
        console.error('Ошибка загрузки:', err);
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center;padding:30px;color:#c5221f">
                    ${err.message}
                </td>
            </tr>`;
    }
}

// Отрисовка
function renderTable(students) {
    studentsCache = students;
    tbody.innerHTML = '';

    if (!students.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center;padding:30px;color:#888">
                    Пока никого нет. <a href="form.html">Добавить первого студента</a>
                </td>
            </tr>`;
        return;
    }

    students.forEach(student => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td data-label="ФИО">${student.name}</td>
            <td data-label="Группа">${student.group}</td>
            <td data-label="ИСУ ID">${student.isuId}</td>
            <td data-label="Общежитие">${student.dorm}</td>
            <td data-label="Действия">
                <div class="actions">
                    <button class="btn-view" data-isu="${student.isuId}">Посмотреть</button>
                    <a class="btn-edit-row" href="form.html?id=${student.isuId}">Редактировать</a>
                    <button class="btn-delete-row" data-isu="${student.isuId}">Удалить</button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Модалка
function openDossier(student) {
    currentStudentIsu = student.isuId;

    document.getElementById('dossier-name').textContent = student.name;
    document.getElementById('dossier-group').textContent = student.group;
    document.getElementById('dossier-isu').textContent = student.isuId;
    document.getElementById('dossier-dorm').textContent = student.dorm;
    document.getElementById('dossier-room').textContent = student.room;
    document.getElementById('dossier-date').textContent = student.date;
    document.getElementById('dossier-foreign').textContent = student.isForeign ? 'Да' : 'Нет';
    document.getElementById('dossier-notes').textContent = student.notes || 'Нет заметок';

    modal.classList.remove('hidden');
}
function closeDossier() { modal.classList.add('hidden'); }

closeBtn.addEventListener('click', closeDossier);
modal.addEventListener('click', e => { if (e.target === modal) closeDossier(); });
document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !modal.classList.contains('hidden')) closeDossier();
});

document.getElementById('dossier-edit-btn').addEventListener('click', () => {
    if (currentStudentIsu != null) {
        location.href = `form.html?id=${currentStudentIsu}`;
    }
});

document.getElementById('dossier-delete-btn').addEventListener('click', async () => {
    if (currentStudentIsu == null) return;
    const s = studentsCache.find(x => x.isuId === currentStudentIsu);
    if (!s) return;
    if (!confirm(`Удалить "${s.name}"?`)) return;

    try {
        const res = await fetch(`/api/requests/${currentStudentIsu}`, { method: 'DELETE' });
        if (res.status !== 204 && !res.ok) {
            const err = await parseError(res);
            throw new Error(err.message);
        }
        closeDossier();
        await loadAndRender();
    } catch (err) {
        alert('Не удалось удалить: ' + err.message);
    }
});

tbody.addEventListener('click', async (event) => {
    const btn = event.target.closest('button');
    if (!btn) return;

    const isuId   = Number(btn.dataset.isu);
    const student = studentsCache.find(s => s.isuId === isuId);

    if (btn.classList.contains('btn-view') && student) {
        openDossier(student);
    }

    if (btn.classList.contains('btn-delete-row') && student) {
        if (!confirm(`Удалить "${student.name}"?`)) return;
        try {
            const res = await fetch(`/api/requests/${isuId}`, { method: 'DELETE' });
            if (res.status !== 204 && !res.ok) {
                const err = await parseError(res);
                throw new Error(err.message);
            }
            await loadAndRender();
        } catch (err) {
            alert('Не удалось удалить: ' + err.message);
        }
    }
});

// Фильтры
const filterGroup   = document.getElementById('filter-group');
const filterDorm    = document.getElementById('filter-dorm');
const filterForeign = document.getElementById('filter-isForeign');
const filterBtn     = document.getElementById('filter-btn');
const resetBtn      = document.getElementById('filter-reset');

if (filterBtn) {
    filterBtn.addEventListener('click', () => {
        currentFilters = {};

        const g = filterGroup.value.trim().toUpperCase();
        const d = filterDorm.value.trim();
        const f = filterForeign.value;

        if (g) currentFilters.group     = g;
        if (d) currentFilters.dormitory = d;
        if (f !== '') currentFilters.isForeign = f;

        loadAndRender();
    });
}

if (resetBtn) {
    resetBtn.addEventListener('click', () => {
        filterGroup.value   = '';
        filterDorm.value    = '';
        filterForeign.value = '';
        currentFilters      = {};
        loadAndRender();
    });
}

// Старт
loadAndRender();