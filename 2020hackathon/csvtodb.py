import csv
import os
import django
import sys

os.chdir('.')
print("Current dir=", end=""), print(os.getcwd())
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "video_stream.settings")	# 1. 여기서 프로젝트명.settings입력
django.setup()

# 위의 과정까지가 python manage.py shell을 키는 것과 비슷한 효과
###########################################################################################


CSV_PATH = 'streamapp/beer_alcohol.csv'	# 3. csv 파일 경로

from streamapp.models import Alcohol	# 2. App이름.models

bulk_list = []
with open(CSV_PATH, encoding='UTF-8') as csvfile:	# 4. newline =''
    data_reader = csv.reader(csvfile)
    next(data_reader, None)
    for row in data_reader:
        bulk_list.append(Alcohol(		# 5. class명.objects.create
            nation = row[0],
            name = row[1],
            alcohol_type = row[2],
            tag = row[3],
            alcohol = row[4],
        ))

Alcohol.objects.bulk_create(bulk_list)


print('Okay')