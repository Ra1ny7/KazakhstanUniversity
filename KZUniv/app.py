from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "supersecretkey_change_in_production"

# Расширенные данные университетов
universities = [
    {
        "id": 1,
        "name": "Nazarbayev University (NU)",
        "city": "Нур-Султан",
        "founded": 2010,
        "type": "Автономная исследовательская университет-корпорация",
        "tuition": "Гранты + платное (бакалавриат/магистратура; платно — существенно высокие ставки; есть стипендии)",
        "admission": "Отбор через NUET/внутренние экзамены, мотивационное письмо; IELTS/TOEFL для англоязычных программ (обычно ≥6.0)",
        "international_relations": "Партнёры: Duke, Wisconsin-Madison, NUS и др.; программы обмена, двойные дипломы",
        "academic_programs": "Инженерия, IT, Естественные науки, Медицина (на уровне клиник), Бизнес, Социальные науки",
        "conditions_of_study": "Международный англоязычный кампус, research-ориентированная среда, современные лаборатории, интенсивная нагрузка и project work",
        "long_info": "Флагман реформ высшего образования, сильный акцент на исследование и международную интеграцию; мощные стипендиальные программы для сильных абитуриентов."
    },
    {
        "id": 2,
        "name": "Al-Farabi Kazakh National University (KazNU)",
        "city": "Алматы",
        "founded": 1934,
        "type": "Государственный классический университет (национальный)",
        "tuition": "Гранты (большая часть мест) / платное (в зависимости от факультета; от умеренных до высоких ставок)",
        "admission": "Приём по результатам ЕНТ/тем/внутривузовских испытаний; есть подготовительные курсы; языки: казахский/русский/английский",
        "international_relations": "Широкая сеть партнерств в Европе, Азии; программы академической мобильности и двойных дипломов",
        "academic_programs": "Гуманитарные науки, естествознание, математика, физика, химия, биология, экономика, юриспруденция",
        "conditions_of_study": "Традиционный университетский формат, крупная библиотека и научные школы; обучение на каз./рус./англ.",
        "long_info": "Крупнейший классический вуз страны с большим числом факультетов и сильными фундаментальными школами."
    },
    {
        "id": 3,
        "name": "L. N. Gumilyov Eurasian National University (ENU)",
        "city": "Нур-Султан",
        "founded": 1996,
        "type": "Государственный университет (национальный)",
        "tuition": "Гранты / платное (в зависимости от специальности)",
        "admission": "ЕНТ/внутренние испытания; есть англоязычные программы с отдельными требованиями (IELTS/TOEFL)",
        "international_relations": "Проекты по Эразмус+, партнёрства с европейскими вузами, академическая мобильность",
        "academic_programs": "Гуманитарные и социальные науки, IT, инженерия, инженерно-технические дисциплины",
        "conditions_of_study": "Городской кампус, программы обмена, смешение рус./каз./англ. языков обучения",
        "long_info": "Один из ведущих столичных университетов, сильный в гуманитарных и региональных исследованиях."
    },
    {
        "id": 4,
        "name": "Satbayev University (KazNTU / Satbayev)",
        "city": "Алматы",
        "founded": 1934,
        "type": "Национальный исследовательский технический университет",
        "tuition": "Гранты / платное; ориентирован на технические специальности",
        "admission": "ЕНТ/конкурсы по предметам (математика, физика); есть целевые места от предприятий",
        "international_relations": "Партнёрства с техническими вузами Европы и Азии; международные исследовательские проекты",
        "academic_programs": "Горное дело, металлургия, машиностроение, электротехника, IT, прикладная математика",
        "conditions_of_study": "Практико-ориентированные лаборатории, тесная связь с индустрией, стажировки",
        "long_info": "Главный технический университет страны; сильный фокус на промышленную подготовку специалистов."
    },
    {
        "id": 5,
        "name": "KIMEP University",
        "city": "Алматы",
        "founded": 1992,
        "type": "Неприбыльный частный / англоязычный университет (американская модель)",
        "tuition": "Платное (стипендии/финансовая помощь доступны); относительно высокие расценки для бакалавриата/магистратуры",
        "admission": "Вступительные тесты, мотивация; требования к английскому (IELTS/TOEFL) для большинства программ",
        "international_relations": "Партнёры в США/Европе; программы обмена; аккредитации и сетевые программы",
        "academic_programs": "Бизнес, экономика, международные отношения, социология, право, IT (в контексте бизнеса)",
        "conditions_of_study": "Англоязычная среда, case-methods, карьерные сервисы, сильный фокус на employability",
        "long_info": "Известен сильной школой бизнеса и экономических дисциплин, готовит специалистов на международный рынок."
    },
    {
        "id": 6,
        "name": "Narxoz University",
        "city": "Алматы",
        "founded": 1963,
        "type": "Государственный / экономический университет",
        "tuition": "Гранты / платное; экономические программы популярны и платны",
        "admission": "ЕНТ/внутривузов. конкурсы; есть англоязычные треки",
        "international_relations": "Партнёры по бизнес-программам в Европе и Азии; двойные дипломы на отдельных кафедрах",
        "academic_programs": "Экономика, менеджмент, финансы, маркетинг, аналитика данных",
        "conditions_of_study": "Практико-ориентированные курсы, стажировки в компаниях, проекты",
        "long_info": "Один из ведущих экономических вузов страны с сильной связью с бизнесом."
    },
    {
        "id": 7,
        "name": "Abai Kazakh National Pedagogical University (Abai KAZNPU)",
        "city": "Алматы",
        "founded": 1931,
        "type": "Государственный педагогический университет (национальный)",
        "tuition": "Гранты / платное; программы подготовки учителей",
        "admission": "ЕНТ/педагогическое собеседование; профильные конкурсы",
        "international_relations": "Обмены и совместные проекты в педагогике, сотрудничество с ВУЗами СНГ и ЕС",
        "academic_programs": "Педагогика, филология, психология, методики преподавания",
        "conditions_of_study": "Практики в школьных классах, методические лаборатории, стажировки",
        "long_info": "Классическая школа педагогического образования в Казахстане; готовит учителей и методистов."
    },
    {
        "id": 8,
        "name": "S. D. Asfendiyarov Kazakh National Medical University",
        "city": "Алматы",
        "founded": 1931,
        "type": "Государственный медицинский университет (национальный)",
        "tuition": "Гранты / платное (медицинские программы традиционно дорогие при платной форме)",
        "admission": "ЕНТ/мед. вступительные экзамены; обязательны профильные предметы (биология, химия)",
        "international_relations": "Клинические и академические партнёрства с медицинскими школами и клиниками за рубежом",
        "academic_programs": "Общая медицина, стоматология, фармация, медицинские науки",
        "conditions_of_study": "Клинические ротации, лабораторная база, интенсивные практические часы",
        "long_info": "Ведущий медицинский вуз страны с крупной клинической базой и программами последипломного образования."
    },
    {
        "id": 9,
        "name": "Karaganda State University (E. A. Buketov)",
        "city": "Караганда",
        "founded": 1972,
        "type": "Государственный университет",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/внутривузовские испытания",
        "international_relations": "Партнёрства с вузами России и Европы; программы академической мобильности",
        "academic_programs": "Естественные науки, гуманитарные дисциплины, педагогика, право",
        "conditions_of_study": "Региональный кампус, сильные педагогические и фундаментальные школы",
        "long_info": "Крупнейший вуз Центрального Казахстана; традиционная университетская структура."
    },
    {
        "id": 10,
        "name": "Kazakh National Agrarian University",
        "city": "Алматы",
        "founded": 1991,
        "type": "Государственный аграрный университет",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/профильные конкурсы",
        "international_relations": "Сотрудничество с аграрными институтами Европы и Азии; проекты FAO/UN",
        "academic_programs": "Сельское хозяйство, агрономия, зоотехния, агробизнес",
        "conditions_of_study": "Практики на учебных полигонах, лаборатории, полевые практики",
        "long_info": "Фокус на аграрные науки и технологии, взаимодействие с аграрным бизнесом."
    },
    {
        "id": 11,
        "name": "Kazakh National Pedagogical University named after Abai (alternate listing)",
        "city": "Алматы",
        "founded": 1931,
        "type": "Государственный педагогический",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/педаг. конкурсы",
        "international_relations": "Педагогические обмены, совместные методические проекты",
        "academic_programs": "Педагогика, обучение языкам, психология",
        "conditions_of_study": "Широкая сеть практических площадок для будущих учителей",
        "long_info": "Ключевой центр педагогического образования."
    },
    {
        "id": 12,
        "name": "Almaty Technological University (ATU)",
        "city": "Алматы",
        "founded": 1934,
        "type": "Государственный технический/технологический университет",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/профильные испытания",
        "international_relations": "Партнёры в Азии и Европе по технологическим программам",
        "academic_programs": "Химическая технология, пищевые технологии, инженерия",
        "conditions_of_study": "Лаборатории, практические курсы, сотрудничество с предприятиями",
        "long_info": "Специализируется на прикладных технологических дисциплинах."
    },
    {
        "id": 13,
        "name": "Kazakh-British Technical University (KBTU)",
        "city": "Алматы",
        "founded": 2001,
        "type": "Частично коммерческий / технический университет с международным фокусом",
        "tuition": "Платное (есть гранты и целевые места)",
        "admission": "Вступительные экзамены + требования к английскому",
        "international_relations": "Партнёры из Великобритании и Европы, программы двойных дипломов",
        "academic_programs": "Нефтегазовое дело, энергетика, IT, инженерия",
        "conditions_of_study": "Англоязычные треки, сильный инженерный состав",
        "long_info": "Ориентирован на индустрию: нефть, газ, энергетика и информационные технологии."
    },
    {
        "id": 14,
        "name": "International IT University (IITU)",
        "city": "Алматы",
        "founded": 2009,
        "type": "Государственный/частный с ИТ-фокусом",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/профильные ИТ-тесты; есть англоязычные программы",
        "international_relations": "Партнёрства с ИТ-компаниями и зарубежными вузами",
        "academic_programs": "Программирование, кибербезопасность, AI, данные",
        "conditions_of_study": "Лаборатории по ПО, проекты в сотрудничестве с индустрией",
        "long_info": "Специализируется на практических IT-навыках и современных технологиях."
    },
    {
        "id": 15,
        "name": "Taraz State University named after M. Kh. Dulati",
        "city": "Тараз",
        "founded": 1992,
        "type": "Государственный региональный университет",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/региональные конкурсы",
        "international_relations": "Ограниченные региональные партнёрства",
        "academic_programs": "Гуманитарные и естественные науки, педагогика",
        "conditions_of_study": "Традиционная опора на местную учебную базу",
        "long_info": "Региональный образовательный центр южного Казахстана."
    },
    {
        "id": 16,
        "name": "South Kazakhstan State University (M. Auezov)",
        "city": "Шымкент",
        "founded": 1943,
        "type": "Государственный университет",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/внутривузовские испытания",
        "international_relations": "Партнёры СНГ и регионов",
        "academic_programs": "Гуманитарные, естественные, экономические дисциплины",
        "conditions_of_study": "Региональная направленность, практики",
        "long_info": "Крупный вуз южного региона с историческими образовательными школами."
    },
    {
        "id": 17,
        "name": "A. Baitursynov Kostanay State University",
        "city": "Костанай",
        "founded": 1939,
        "type": "Государственный региональный",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ",
        "international_relations": "Партнёры РФ/Европа (локальные обмены)",
        "academic_programs": "Педагогика, естественные науки, экономика",
        "conditions_of_study": "Региональный кампус, профильные факультеты",
        "long_info": "Обслуживает образовательные потребности Северо-Казахстанского региона."
    },
    {
        "id": 18,
        "name": "West Kazakhstan State University (Zhangir Khan)",
        "city": "Уральск",
        "founded": 1930,
        "type": "Государственный",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ",
        "international_relations": "Региональные международные связи",
        "academic_programs": "Агроинженерия, гуманитарные науки, педагогика",
        "conditions_of_study": "Региональная направленность, полевые практики",
        "long_info": "Ведущий вуз Западного Казахстана."
    },
    {
        "id": 19,
        "name": "East Kazakhstan State Technical University (D. Serikbayev)",
        "city": "Усть-Каменогорск (Өскемен)",
        "founded": 1958,
        "type": "Государственный технический университет",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/технические тесты",
        "international_relations": "Партнёрства с техническими вузами РФ/КНР",
        "academic_programs": "Горное дело, металлургия, инженерия",
        "conditions_of_study": "Сильный практический компонент, лаборатории",
        "long_info": "Фокус на добывающей и обрабатывающей промышленности региона."
    },
    {
        "id": 20,
        "name": "Karaganda State Medical University",
        "city": "Караганда",
        "founded": 1950,
        "type": "Государственный медицинский",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/мед. испытания",
        "international_relations": "Клинические партнёрства и обмены",
        "academic_programs": "Медицина, стоматология, фармация",
        "conditions_of_study": "Клиническая база в региональных больницах",
        "long_info": "Ведущий медицинский вуз центрального региона."
    },
    {
        "id": 21,
        "name": "Pavlodar State Pedagogical University (S. Toraigyrov)",
        "city": "Павлодар",
        "founded": 1930,
        "type": "Государственный педагогический",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/пед. конкурсы",
        "international_relations": "Региональные обмены в педагогике",
        "academic_programs": "Педагогика, филология, методики преподавания",
        "conditions_of_study": "Практики в школах региона, методические лаборатории",
        "long_info": "Готовит преподавателей для северо-востока Казахстана."
    },
    {
        "id": 22,
        "name": "Shakarim State University (Semey)",
        "city": "Семей",
        "founded": 1978,
        "type": "Государственный региональный",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ",
        "international_relations": "Партнёрства в регионе",
        "academic_programs": "Гуманитарные и естественные науки",
        "conditions_of_study": "Традиционный университетский формат",
        "long_info": "Региональный опорный вуз Северо-Восточного Казахстана."
    },
    {
        "id": 23,
        "name": "South Kazakhstan State Medical Academy",
        "city": "Шымкент",
        "founded": 1953,
        "type": "Государственный медицинский вуз",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ/мед. испытания",
        "international_relations": "Клинические связи с регионами и зарубежьем",
        "academic_programs": "Медицина, сестринское дело, фармация",
        "conditions_of_study": "Клинические практики, лаборатории",
        "long_info": "Крупный медицинский центр южного региона."
    },
    {
        "id": 24,
        "name": "Sh. Ualikhanov Kokshetau University",
        "city": "Кокшетау",
        "founded": 1996,
        "type": "Государственный региональный вуз",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ",
        "international_relations": "Сотрудничество с региональными вузами",
        "academic_programs": "Педагогика, гуманитарные и естественные направления",
        "conditions_of_study": "Маленький кампус, интенсивная связь с местным рынком труда",
        "long_info": "Ориентирован на подготовку специалистов для Акмолинской области."
    },
    {
        "id": 25,
        "name": "Kyzylorda State University (Korkyt Ata)",
        "city": "Кызылорда",
        "founded": 1996,
        "type": "Государственный",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ",
        "international_relations": "Региональные связи",
        "academic_programs": "Агротехнологии, педагогика, экономика",
        "conditions_of_study": "Практики и полевые работы, региональная направленность",
        "long_info": "Образовательный центр для Юго-Западного Казахстана."
    },
    {
        "id": 26,
        "name": "KIMEP College / KIMEP (branch info)",
        "city": "Алматы",
        "founded": 1992,
        "type": "Частный/международный (см. KIMEP выше)",
        "tuition": "Платное",
        "admission": "Тесты + английский",
        "international_relations": "Активные программы обмена с США и Европой",
        "academic_programs": "Бизнес/экономика/право/соц. науки",
        "conditions_of_study": "Англоязычные треки, case-studies",
        "long_info": "Сильный акцент на международной бизнес-образовании."
    },
    {
        "id": 27,
        "name": "Narxoz Graduate & Executive Programs (доп.)",
        "city": "Алматы",
        "founded": 1963,
        "type": "Государственный/частично автономный",
        "tuition": "Платное (магистратура и executive направления чаще платные)",
        "admission": "Профильные тесты и собеседования",
        "international_relations": "Партнёрства по MBA и обменам",
        "academic_programs": "MBA, финансы, аналитика, корпоративное управление",
        "conditions_of_study": "Вечерние и очные форматы, кейс-методы",
        "long_info": "Сильная деловая школа в национальном контексте."
    },
    {
        "id": 28,
        "name": "University of International Business (UIB)",
        "city": "Алматы",
        "founded": 1994,
        "type": "Частный / профильный",
        "tuition": "Платное",
        "admission": "Тесты, собеседования; требования к английскому на отдельных программах",
        "international_relations": "Партнёрства бизнес-школ, обмены",
        "academic_programs": "Международный бизнес, логистика, маркетинг",
        "conditions_of_study": "Практико-ориентированное обучение, проекты с компаниями",
        "long_info": "Фокус на международном бизнес-образовании."
    },
    {
        "id": 29,
        "name": "Turkestan / Turkistan regional university (example: Ahmet Yesevi Univ. branch)",
        "city": "Туркестан",
        "founded": 1991,
        "type": "Государственный / региональный (в т.ч. международные проекты)",
        "tuition": "Гранты / платное",
        "admission": "ЕНТ",
        "international_relations": "Связи с Турецкими вузами (Ahmet Yesevi и др.)",
        "academic_programs": "Гуманитарные, историко-культурные, педагогические",
        "conditions_of_study": "Фокус на региональном развитии, культурное наследие",
        "long_info": "Центр образования южного региона с интернациональными инициативами."
    },
    {
        "id": 30,
        "name": "University of Central Asia (UCA) — Campus/partnership in Kazakhstan",
        "city": "Текели / региональные кампусы",
        "founded": 2000,
        "type": "Международный региональный университет (Международный проект)",
        "tuition": "Платное / стипендии (UCA предлагает международные гранты)",
        "admission": "Конкурентный отбор; требования уровня английского",
        "international_relations": "UCA — международная сеть с партнёрами в США и Европе",
        "academic_programs": "Развитие регионов, горное дело, педагогика, устойчивое развитие",
        "conditions_of_study": "Международная среда, проектная работа, полевые исследования",
        "long_info": "Региональная инициатива с сильным международным компонентом и программами устойчивого развития."
    }
]

# Симуляция базы данных пользователей
users = {
    "admin": {
        "password": "admin123",
        "favourites": [],
        "compare": []
    },
    "test": {
        "password": "123",
        "favourites": [],
        "compare": []
    }
}

# Функция для получения или создания пользователя
def get_user_data(username):
    """Получить данные пользователя, создать если не существует"""
    if username not in users:
        users[username] = {
            "password": None,  # Пароль не сохраняем для восстановленных пользователей
            "favourites": [],
            "compare": []
        }
    return users[username]

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        # Убедимся, что пользователь существует в системе
        get_user_data(session['user'])
        return f(*args, **kwargs)
    return decorated_function

# Главная страница
@app.route("/")
def index():
    return render_template(
        "index.html",
        universities=universities,
        current_user=session.get("user")
    )

# Каталог университетов
@app.route("/universities")
def universities_page():
    return render_template(
        "universities.html",
        universities=universities,
        current_user=session.get("user")
    )

# Избранное
@app.route("/favorites")
@login_required
def favorites():
    username = session.get("user")
    user_data = get_user_data(username)
    fav_ids = user_data["favourites"]
    fav_univs = [u for u in universities if u["id"] in fav_ids]
    return render_template(
        "favorites.html",
        universities=fav_univs,
        current_user=username
    )

# Сравнение
@app.route("/compare")
@login_required
def compare():
    username = session.get("user")
    user_data = get_user_data(username)
    compare_ids = user_data["compare"]
    compare_univs = [u for u in universities if u["id"] in compare_ids]
    return render_template(
        "compare.html",
        universities=compare_univs,
        current_user=username
    )

# Помощник
@app.route("/assistant")
def assistant():
    return render_template(
        "assistant.html",
        universities=universities,
        current_user=session.get("user")
    )

# Вход
@app.route("/login", methods=["GET", "POST"])
def login():
    # Если уже авторизован, перенаправляем на главную
    if 'user' in session:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # Проверка учетных данных
        if username in users and users[username].get("password") == password:
            session["user"] = username
            return redirect(url_for('index'))
        
        return render_template("login.html", error="Неверный логин или пароль")
    
    return render_template("login.html", error=None)

# Регистрация
@app.route("/register", methods=["GET", "POST"])
def register():
    # Если уже авторизован, перенаправляем на главную
    if 'user' in session:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # Валидация
        if not username or not password:
            return render_template("register.html", error="Заполните все поля")
        
        if len(username) < 3:
            return render_template("register.html", error="Логин должен содержать минимум 3 символа")
        
        if len(password) < 3:
            return render_template("register.html", error="Пароль должен содержать минимум 3 символа")
        
        # Проверка существования пользователя
        if username in users and users[username].get("password"):
            return render_template("register.html", error="Пользователь уже существует")
        
        # Создание нового пользователя
        users[username] = {
            "password": password,
            "favourites": [],
            "compare": []
        }
        
        session["user"] = username
        return redirect(url_for('index'))
    
    return render_template("register.html", error=None)

# API для избранного
@app.route("/api/favourite", methods=["POST"])
def api_favourite():
    username = session.get("user")
    if not username:
        return jsonify({"error": "Не авторизован"}), 401
    
    try:
        user_data = get_user_data(username)
        data = request.json
        univ_id = int(data.get("university_id"))
        
        # Проверка существования университета
        if not any(u["id"] == univ_id for u in universities):
            return jsonify({"error": "Университет не найден"}), 404
        
        # Добавление или удаление из избранного
        if univ_id in user_data["favourites"]:
            user_data["favourites"].remove(univ_id)
            status = "removed"
        else:
            user_data["favourites"].append(univ_id)
            status = "added"
        
        return jsonify({"status": status})
    
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Неверный запрос"}), 400

# API для сравнения
@app.route("/api/compare", methods=["POST"])
def api_compare():
    username = session.get("user")
    if not username:
        return jsonify({"error": "Не авторизован"}), 401
    
    try:
        user_data = get_user_data(username)
        data = request.json
        univ_id = int(data.get("university_id"))
        
        # Проверка существования университета
        if not any(u["id"] == univ_id for u in universities):
            return jsonify({"error": "Университет не найден"}), 404
        
        # Добавление или удаление из сравнения
        if univ_id in user_data["compare"]:
            user_data["compare"].remove(univ_id)
            status = "removed"
        else:
            # Ограничение на количество университетов для сравнения
            if len(user_data["compare"]) >= 5:
                return jsonify({"error": "Максимум 5 университетов для сравнения"}), 400
            user_data["compare"].append(univ_id)
            status = "added"
        
        return jsonify({"status": status})
    
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Неверный запрос"}), 400

# Выход
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))

# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 if False else redirect(url_for('index'))

# API для получения состояния пользователя (избранное и сравнение)
@app.route("/api/user-states", methods=["GET"])
def api_user_states():
    """Возвращает списки избранного и сравнения для текущего пользователя"""
    username = session.get("user")
    if not username:
        return jsonify({"favourites": [], "compare": []})
    
    user_data = get_user_data(username)
    return jsonify({
        "favourites": user_data.get("favourites", []),
        "compare": user_data.get("compare", [])
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)