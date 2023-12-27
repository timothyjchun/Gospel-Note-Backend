from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CreateUserView,
    SaveUserGospelNote,
    UserAuthenticationCheckView,
    GospelNoteView,
    GetMostRecentGospelNote,
    UserNoteView,
    GetIndivisualUserNote,
    CreateProgressCalendar,
)

urlpatterns = [
    # JWT authentication views
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # My Views
    path("auth_check/", UserAuthenticationCheckView.as_view(), name="auth_check"),
    path("create_user/", CreateUserView.as_view(), name="create_user"),
    path("save_note/", SaveUserGospelNote.as_view(), name="save_note"),
    path("select_gnote/", GospelNoteView.as_view(), name="select_gnote"),
    path("recent_gnote/", GetMostRecentGospelNote.as_view(), name="recent_gnote"),
    path("get_usernote/", UserNoteView.as_view(), name="get_usernote"),
    path(
        "get_indivisual_usernote/",
        GetIndivisualUserNote.as_view(),
        name="get_indivisual_usernote",
    ),
    path(
        "create_progress_cal/",
        CreateProgressCalendar.as_view(),
        name="create_progress_cal",
    ),
]
