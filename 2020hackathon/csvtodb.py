import csv
import os
import django
import sys
from streamapp.models import Cook

os.chdir('.')
print("Current dir=", end=""), print(os.getcwd())
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "video_stream.settings")	
django.setup()

#경로 설정해주셔야합니다!
CSV_PATH = r'C:\Users\LHS\Desktop\2_git_team\2020hackathon\streamapp\cook.csv'	

bulk_list = []
with open(CSV_PATH, encoding='UTF-8') as csvfile:
    data_reader = csv.reader(csvfile)
    next(data_reader, None)
    for row in data_reader:
        bulk_list.append(Cook(		
            link = row[0],
            food = row[1],
            img = row[2],
            tag = row[3],
            material = row[4],
            cooking_time = row[5],
            scrap = row[6],
        ))

Cook.objects.bulk_create(bulk_list)

