import calendar


# import os
# import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")
# django.setup()

from notes.serializers import UserNoteSerializer
from users.models import User


class Progress_Calendar:
    def __init__(self, year, request_user):
        self.cal = calendar.Calendar()

        self.year = year
        self.request_user = request_user

        self.color_data = [
            "#5197e0",
            "#e32f9c",
            "#32cd26",
            "#aa1df9",
            "#f5e36b",
            "#6ccca7",
            "#e7BB48",
            "#385bb7",
            "#ff6d6d",
            "#00c2ff",
            "#ffb72b",
            "#ff82fa",
        ]
        self.user_notes = []
        self.dates = []
        self.progress_calendar = []

    def get_user_year_notes(self, year, user):
        # user_notes = user.usernote_set.filter(create_date__year=year) # -> create_date == year 가 아니라 original_create_date == year로 해야함
        all_user_notes = user.usernote_set.all()
        user_notes = []
        for un in all_user_notes:
            if un.original_video_upload_date.year == year:
                user_notes.append(un)
        user_notes = sorted(
            user_notes, key=lambda note: note.original_video_upload_date
        )  # Getting User Notes Sequentially
        return user_notes

    def get_user_notes(self):
        self.user_notes = self.get_user_year_notes(self.year, self.request_user)

    # making void progress calendar
    def create_void_progress_calendar(self):
        for _ in range(7):
            self.progress_calendar.append([0] * 53)

    def get_dates_in_year(self):
        # getting all dates in year in a list
        for month in range(1, 13):
            month_dates_generator = self.cal.itermonthdates(self.year, month)
            for days in month_dates_generator:
                # check if year is different (cuz of the thingy)
                if str(days)[3] != str(self.year)[3]:
                    continue
                # check if already exists cuz of the thingy you know
                if str(days) in self.dates:
                    continue
                else:
                    self.dates.append(str(days))

    def create_progress_calendar(self):
        # creating progress calendar
        self.get_user_notes()
        self.create_void_progress_calendar()
        self.get_dates_in_year()
        cnt = 0
        color_cnt = 0
        current_month = self.dates[0][5:7]
        for column in range(53):
            for row in range(7):
                if self.dates[cnt][5:7] != current_month:
                    current_month = self.dates[cnt][5:7]  # 달 별로 다른
                    color_cnt += 1

                self.progress_calendar[row][column] = []
                self.progress_calendar[row][column].append(self.dates[cnt])
                self.progress_calendar[row][column].append(self.color_data[color_cnt])
                if len(self.user_notes) != 0 and self.dates[cnt] == str(
                    self.user_notes[0].original_video_upload_date
                ):
                    # print(self.dates[cnt]) #-> The days that have a GospelNote
                    self.progress_calendar[row][column].append(
                        UserNoteSerializer(self.user_notes[0]).data
                    )
                    self.user_notes.pop(0)

                cnt += 1
                # when cnt variable value is the same as dates in year
                if cnt == len(self.dates):
                    return self.progress_calendar

    # printing progress calendar
    def print_progress_calendar(self):
        for row in range(7):
            for day in range(53):
                print(self.progress_calendar[row][day], end=" ")
            print("\n")


if __name__ == "__main__":
    u = User.objects.get(username="timothychun")
    pc = Progress_Calendar(year=2023, request_user=u)
    pc.create_progress_calendar()
    pc.print_progress_calendar()
