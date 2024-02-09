import os, sys, asyncio
import django
from django.contrib.auth import get_user_model
from django.db import DatabaseError

# SETUP django --------------------------------
proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "parsing_servise.settings"
django.setup()
# END SETUP django --------------------------------

from parsing_functions.parser_engine import *
from parsing_app.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parsers = (
    (head_hunter, 'head_hunter'),
    (superjob, 'superjob'),
)
all_jobs, all_errors = [], []


def get_settings():
    """Получение уникальных наборов: Город, Язык"""
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    """Получение наборов urls, под пользователей"""
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_data
                urls.append(tmp)
    return urls


async def main_async(value):
    func, url, city, language = value
    job, error = await loop.run_in_executor(None, func, url, city, language)
    all_errors.extend(error)
    all_jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)

# Синхронный вариант
# # all_jobs, all_errors = [], []
# #
# # for data in url_list:
# #     print(data)
# #     print(data['city'])
# #     for func, key in parsers:
# #         url = data['url_data'][key]
# #         jobs, errors = func(url, data['city'], data['language'])
# #         all_jobs += jobs
# #         all_errors += errors

# Асинхронный вариант
loop = asyncio.get_event_loop()
tmp_task = [(func, data['url_data'][key], data['city'], data['language'])
            for data in url_list
            for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main_async(f)) for f in tmp_task])
loop.run_until_complete(tasks)
loop.close()

for job in all_jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if all_errors:
    for error in all_errors:
        errors = Error(**error).save()
