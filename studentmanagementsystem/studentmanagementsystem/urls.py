from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views,hod_views,staff_views,student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    #login path
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

    #profile update
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),




    #this is hod panel url
    path('hod/Home', hod_views.HOME, name='hod_home'),
    path('hod/Student/Add',hod_views.ADD_STUDENT, name='add_student'),
    path('hod/Student/View', hod_views.VIEW_STUDENT, name='view_student'),
    path('hod/Student/Edit/<str:id>',hod_views.EDIT_STUDENT, name='edit_student'),
    path('hod/Student/Update',hod_views.UPDATE_STUDENT, name='update_student'),
    path('hod/Student/Delete/<str:id>', hod_views.DELETE_STUDENT, name='delete_student'),

    path('hod/Staff/Add', hod_views.ADD_STAFF, name='add_staff'),
    path('hod/Staff/View', hod_views.VIEW_STAFF, name='view_staff'),
    path('hod/Staff/Edit/<str:id>', hod_views.EDIT_STAFF, name='edit_staff'),
    path('hod/Staff/Update', hod_views.UPDATE_STAFF, name='update_staff'),
    path('hod/Staff/Delete/<str:admin>', hod_views.DELETE_STAFF, name='delete_staff'),

    path('hod/Course/Add', hod_views.ADD_COURSE, name='add_course'),
    path('hod/Course/View', hod_views.VIEW_COURSE, name='view_course'),
    path('hod/Course/Edit/<str:id>', hod_views.EDIT_COURSE, name='edit_course'),
    path('hod/Course/Update', hod_views.UPDATE_COURSE, name='update_course'),
    path('hod/Course/Delete/<str:id>', hod_views.DELETE_COURSE, name='delete_course'),
    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
