import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "parsing_servise.settings"

import django
django.setup()

from parsing_functions.parser_engine import *
from parsing_app.models import Vacancy, City, Language

parsers = (
    (head_hunter, 'https://spb.hh.ru/vacancies/programmist_python?hhtmFromLabel=rainbow_profession&hhtmFrom=main'),
    (superjob, 'https://spb.superjob.ru/vakansii/programmist.html'),
)
city = City.objects.filter(slug='moskva')
all_jobs, all_errors = [], []

for func, url in parsers:
    jobs, errors = func(url)
    all_jobs += jobs
    all_errors += errors

print(len(all_jobs))
print(all_jobs[1])
print(all_jobs[30])
print(all_jobs[60])
print(all_jobs[70])

# def write_jobs():
#     with codecs.open('parsing_functions/hh.json', 'w', 'utf-8') as file:
#         file.write(str(jobs))
#
#
# def write_errors():
#     with codecs.open('parsing_functions/errors.json', 'w', 'utf-8') as file:
#         file.write(str(errors))
