import datetime
import os, sys
import django

from django.core.mail import EmailMultiAlternatives, send_mail

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from parsing_servise.settings import (
    EMAIL_HOST_USER,
    EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_PORT
)

# SETUP django --------------------------------
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "parsing_servise.settings"
django.setup()
# END SETUP django --------------------------------

from parsing_app.models import Vacancy, Error, Url

# EmailMultiAlternativesl: TEST html message
ADMIN_USER = EMAIL_HOST_USER
today = datetime.date.today()
subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий {today}"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по Вашим предпочтениям данных нет. </h2>'


# Формируем словарь вида {(city_id, lang_id): email, ...}
User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}
for user in qs:
    users_dict.setdefault((user['city'], user['language']), [])
    users_dict[(user['city'], user['language'])].append(user['email'])

# проверка основания рассылки сообщений
if users_dict:
    # __in говорит о том, что мы должны найти city_id в заданном поле фильтрации
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()

    # Формируем словарь вида {(city_id, lang_id): [vacancy_obj1, vacancy_obj2, ...], ...}
    vacancies = {}
    for vacancy in qs:
        # values() без параметров, из ForeignKey делает name_id
        vacancies.setdefault((vacancy['city_id'], vacancy['language_id']), [])
        vacancies[(vacancy['city_id'], vacancy['language_id'])].append(vacancy)
    print(users_dict.keys())
    print(vacancies.keys())
    for keys, emails in users_dict.items():
        print(keys, emails)
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            url = row["url"]
            html += f'<h3><a href=\'{row["url"]}\'>{row["title"]}<a/></h3>\n'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty
        # for email in emails:
        #     to = email
        #     msg = EmailMultiAlternatives(
        #         subject, text_content, from_email, [to]
        #     )
        #     msg.attach_alternative(_html, "text/html")
        #     msg.send()

qs = Error.objects.filter(timestamp=today).values()
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''

if qs.exists():
    for er in qs:
        print(er)
        _html += f'<p"><a href="{ er["url"] }">Error: { er["error"] }</a></p><br>'
    subject += f"Ошибки парсинга {today}"
    text_content += "Ошибки парсинга"
    print(_html)
    msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to]
        )
    msg.attach_alternative(_html, "text/html")
    msg.send()


# send_mail: TEST message
# ADMIN_USER = EMAIL_HOST_USER
# subject, text, from_email, to = "hello", "oaoommmmm", EMAIL_HOST_USER, "meevelit@gmail.com"
# send_mail(subject, text, EMAIL_HOST_USER, [to])
