import json
import os
import django
import datetime
import pprint

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")

# Initialize Django
django.setup()

# Now you can import the model
from notes.models import GospelNote

f = open("./gospel_notes.txt", "r")
content = json.loads(f.read())
print(content[-1])
print(len(content))

for gospel_note in content:
    date_st = gospel_note["general_title"]
    year = int(date_st.split("년")[0])
    date_st = date_st.split("년")[1]

    month = int(date_st.split("월")[0])
    date_st = date_st.split("월")[1]

    day = int(date_st.split("일")[0])

    date = datetime.date(year, month, day)
    if len(GospelNote.objects.filter(general_title=gospel_note["general_title"])) != 0:
        GospelNote.objects.filter(general_title=gospel_note["general_title"]).update(
            general_title=gospel_note["general_title"],
            passage=gospel_note["passage"],
            specific_title=gospel_note["specific_title"],
            url=gospel_note["url"],
            video_upload_date=date,
        )
    else:
        GospelNote.objects.create(
            general_title=gospel_note["general_title"],
            passage=gospel_note["passage"],
            specific_title=gospel_note["specific_title"],
            url=gospel_note["url"],
            video_upload_date=date,
        )


f.close()
