from django.urls import path
from .views import Profiles, UserProfile, LoginUser, LogoutUser, RegisterUser, UserAccount, EditAccount, CreateSkill, \
    UpdateSkill, DeleteSkill, Inbox, ViewMessage, CreateMessage

urlpatterns = [
    path('login/', LoginUser, name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('register/', RegisterUser, name='register'),
    path('', Profiles, name='profiles'),
    path('profile/<str:pk>', UserProfile, name='user-profiles'),
    path('account', UserAccount, name='account'),
    path('edit-account', EditAccount, name='edit-account'),
    path('create-skill/', CreateSkill, name='create-skill'),
    path('update-skill/<str:pk>/', UpdateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', DeleteSkill, name='delete-skill'),
    path('inbox/', Inbox, name='inbox'),
    path('message/<str:pk>/', ViewMessage, name='message'),
    path('create-message/<str:pk>/', CreateMessage, name='create-message'),
]
