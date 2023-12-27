from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from users.models import User

from django.contrib.auth.models import User as DjangoUser

from notes.models import GospelNote, UserNote

from notes.serializers import GospelNoteSerializer, UserNoteSerializer

from create_user_calendar import Progress_Calendar

import json


class UserAuthenticationCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(200)


# Creating User
class CreateUserView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("name", None)
        username = data.get("username", None)
        password = data.get("password", None)
        if name and username and password:
            if User.objects.filter(username=username):  # 중복 아이디 검사
                return Response({"message": "이미 사용중인 아이디입니다"}, status=400)
            superuser_username = DjangoUser.objects.filter(is_superuser=True)[
                0
            ].username
            if username == superuser_username:
                return Response({"message": "이미 사용중인 아이디입니다"}, status=400)
            first_name = name[1:]  # 이름
            last_name = name[:1]  # 성
            new_user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            new_user.save()
            return Response(status=200)
        else:
            return Response({"message": "이름, 아이디, 비밀번호가 바르게 입력되지 않았습니다"}, status=400)


# Gospel Note Pagination
class GospelNotePagination(PageNumberPagination):
    page_size = 3


class GospelNoteView(generics.ListAPIView):
    queryset = GospelNote.objects.all()[::-1]
    serializer_class = GospelNoteSerializer
    pagination_class = GospelNotePagination


class UserNotePagination(PageNumberPagination):
    page_size = 4


class UserNoteView(generics.ListAPIView):
    # queryset = UserNote.objects.all()[::-1]
    permission_class = [IsAuthenticated]
    serializer_class = UserNoteSerializer
    pagination_class = UserNotePagination

    def list(self, request, *args, **kwargs):
        queryset = UserNote.objects.filter(user_id=request.user.id)[::-1]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Saving User Gospel Notes
class SaveUserGospelNote(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # What if there is an exsisting Object?
        user_id = request.user.id
        data = request.data
        gospel_note = GospelNote.objects.filter(url=data["url"])[0]
        gospel_note_id = gospel_note.id
        does_usernote_exist = (
            len(
                User.objects.get(id=user_id).usernote_set.filter(
                    gospel_note_id=gospel_note_id
                )
            )
            > 0
        )
        if does_usernote_exist:  # Update not create
            existant_note = User.objects.get(id=user_id).usernote_set.filter(
                gospel_note_id=gospel_note_id
            )[0]
            existant_note.first_question = (
                data["firstQuestion"]
                if data["firstQuestion"]
                else existant_note.first_question
            )
            existant_note.second_question = (
                data["secondQuestion"]
                if data["secondQuestion"]
                else existant_note.second_question
            )
            existant_note.third_question = (
                data["thirdQuestion"]
                if data["thirdQuestion"]
                else existant_note.third_question
            )
            existant_note.save()
        else:  # Create
            new_note = UserNote(
                user=User.objects.get(id=request.user.id),
                gospel_note=gospel_note,
                first_question=data["firstQuestion"],
                second_question=data["secondQuestion"],
                third_question=data["thirdQuestion"],
            )
            new_note.save()
        return Response(status=200)


class GetMostRecentGospelNote(APIView):
    def get(self, request):
        obj = GospelNote.objects.last()
        obj_seri = GospelNoteSerializer(obj).data
        return Response(obj_seri, status=200)


class GetIndivisualUserNote(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_note_id = int(request.GET.get("id"))
        note = UserNote.objects.get(id=user_note_id)
        if note.user.id != request.user.id:
            return Response({"message": "User Has No Ownership to Note"}, status=401)
        else:
            serializer = UserNoteSerializer(note)
            return Response(serializer.data, status=200)


class CreateProgressCalendar(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requested_year = int(request.query_params["year"])
        user = User.objects.get(id=request.user.id)
        pc = Progress_Calendar(year=requested_year, request_user=user)
        progress_calendar = pc.create_progress_calendar()
        return Response({"calendar": progress_calendar}, status=200)
