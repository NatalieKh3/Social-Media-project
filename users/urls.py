from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
urlpatterns = [
    path("register/",register_page,name="register_page"),
    path("login/",login_page,name="login_page"),
    path("main",main_page,name="main_page"),
    path("user_logout/", user_logout, name="user_logout"),
    path("profile/",profile_page, name="profile_page"),
    path("possible_friends",friend_list,name="possible_friends"),
    path("add_friend/<int:user_id>",add_friend,name="add_friend"),
    path("friend_requests/",requests,name="friend_requests"),
    path("accept_friend/<int:user_id>",accept_friend,name="accept_friend"),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)