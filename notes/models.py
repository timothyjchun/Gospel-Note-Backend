from django.db import models

# Create your models here.

from users.models import User


class GospelNote(models.Model):
    general_title = models.CharField(
        max_length=30, blank=False, null=False, unique=True
    )
    passage = models.CharField(
        max_length=30,
        blank=True,
    )
    specific_title = models.CharField(max_length=15, blank=True)
    url = models.CharField(max_length=15, blank=False, null=False)

    video_upload_date = models.DateField(auto_now_add=True)


class UserNote(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question_progress_dictionary = {
            "first": 0,
            "second": 0,
            "third": 0,
            "on_time": 0,
        }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gospel_note = models.ForeignKey(GospelNote, on_delete=models.PROTECT)

    first_question = models.TextField()
    second_question = models.TextField()
    third_question = models.TextField()

    create_date = models.DateField(auto_now_add=True)

    @property
    def original_video_upload_date(self):
        return self.gospel_note.video_upload_date

    @property
    def is_created_on_time(self):
        return self.original_video_upload_date == self.create_date

    @property
    def progress_color(self):
        # Q1+Q2+Q3+on_time
        # The logic needs to be verified, and also considering that the condition of each question is needed, this might not the most ideal way. But 나중에 지우더라도, I'm doing it for now.
        if self.first_question:
            self.question_progress_dictionary["first"] = 1
        if self.second_question:
            self.question_progress_dictionary["second"] = 1
        if self.third_question:
            self.question_progress_dictionary["third"] = 1
        if self.is_created_on_time:
            self.question_progress_dictionary["on_time"] = 1

        # dict_values() weirdly does't support .count()
        # defualt can't be "0" but has to be 20. so added the defalut value(20)
        return str(list(self.question_progress_dictionary.values()).count(1) * 20 + 20)
