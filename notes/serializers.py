from rest_framework.serializers import ModelSerializer

from notes.models import GospelNote, UserNote


class GospelNoteSerializer(ModelSerializer):
    class Meta:
        model = GospelNote
        fields = "__all__"


class UserNoteSerializer(ModelSerializer):
    class Meta:
        model = UserNote
        # fields = "__all__"
        fields = [
            "id",
            "create_date",
            "first_question",
            "second_question",
            "third_question",
            "gospel_note",
            "user",
            "progress_color",
            "is_created_on_time",
        ]

    def to_representation(
        self, instance
    ):  # Override Method So That GospelNote Data Can Be Added
        ret = super().to_representation(instance)
        gospel_note_id = ret.get("gospel_note")  # ?
        gospel_note = GospelNote.objects.get(id=gospel_note_id)
        ret["general_title"] = gospel_note.general_title
        ret["passage"] = gospel_note.passage
        ret["specific_title"] = gospel_note.specific_title
        ret["url"] = gospel_note.url
        return ret
