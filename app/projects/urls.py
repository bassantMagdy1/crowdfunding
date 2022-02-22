from django.urls import path

from . import views
from .views import AddProjects, ViewProject, AllProjects, DeleteProject, AddReport,AddComment
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('create-projects/', AddProjects, name='create-projects'),
    path('projectcomment/<int:pk>', AddComment, name='projectcomment'),
    path('view-project/<int:pk>',ViewProject, name='view-project'),
    path('all-projects/',AllProjects, name='all-projects'),
    path('delete-projects/<int:pk>',DeleteProject, name='delete-project'),
    # path('project/<str:project_id>', views.home, name='proj_no'),
    path('update_rating/<int:project_id>', views.update_rating, name='update_rating'),
    path('donate/<int:project_id>', views.donate, name='donate'),
    path('report-project/<int:pk>',AddReport , name='report-project'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)