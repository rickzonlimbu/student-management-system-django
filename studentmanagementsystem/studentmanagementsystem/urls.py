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

    path('hod/Subject/Add', hod_views.ADD_SUBJECT, name='add_subject'),
    path('hod/Subject/View', hod_views.VIEW_SUBJECT, name='view_subject'),
    path('hod/Subject/Edit/<str:id>', hod_views.EDIT_SUBJECT, name='edit_subject'),
    path('hod/Subject/Update', hod_views.UPDATE_SUBJECT, name='update_subject'),
    path('hod/Subject/Delete/<str:id>', hod_views.DELETE_SUBJECT, name='delete_subject'),

    path('hod/Batch/Add', hod_views.ADD_BATCH, name='add_batch'),
    path('hod/Batch/View', hod_views.VIEW_BATCH, name='view_batch'),
    path('hod/Batch/Edit/<str:id>', hod_views.EDIT_BATCH, name='edit_batch'),
    path('hod/Batch/Update', hod_views.UPDATE_BATCH, name='update_batch'),
    path('hod/Batch/Delete/<str:id>', hod_views.DELETE_BATCH, name='delete_batch'),

    path('hod/Staff/Send_Notification', hod_views.STAFF_SEND_NOTIFICATION, name='staff_send_notification'),
    path('hod/Staff/Save_Notification', hod_views.SAVE_STAFF_NOTIFICATION, name='save_staff_notification'),
    path('hod/Student/send_notification',hod_views.STUDENT_SEND_NOTIFICATION, name='student_send_notification'),
    path('hod/Staff/save_notification', hod_views.SAVE_STUDENT_NOTIFICATION, name='save_student_notification'),

    path('hod/Staff/Leave_view', hod_views.Staff_Leave_view, name='staff_leave_view'),
    path('hod/Staff/approve_leave/<str:id>', hod_views.Staff_Approve_Leave, name='staff_approve_leave'),
    path('hod/Staff/reject_leave/<str:id>', hod_views.Staff_Reject_Leave, name='staff_reject_leave'),

    path('hod/Staff/feedback', hod_views.STAFF_FEEDBACK, name='staff_feedback_reply'),
    path('hod/Staff/feedback/save', hod_views.STAFF_FEEDBACK_SAVE, name='staff_feedback_reply_save'),

    path('hod/Student/feedback', hod_views.STUDENT_FEEDBACK, name='get_student_feedback'),
    path('hod/Student/feedback/reply/save', hod_views.REPLY_STUDENT_FEEDBACK, name='reply_student_feedback'),

    #this is staffs urls
    path('staff/Home', staff_views.HOME, name='staff_home'),

    path('staff/Notifications', staff_views.NOTIFICATION, name='notifications'),
    path('staff/mark_as_done/<str:status>',staff_views.STAFF_NOTIFICATION_MARK_AS_DONE, name='staff_notification_mark_as_done'),

    path('staff/Apply_leave', staff_views.STAFF_APPLY_LEAVE, name='staff_apply_leave'),
    path('staff/Apply_leave_save', staff_views.STAFF_APPLY_LEAVE_SAVE, name='staff_apply_leave_save'),

    path('staff/Feedback', staff_views.STAFF_FEEDBACK, name='staff_feedback'),
    path('staff/Feedback/Save', staff_views.STAFF_FEEDBACK_SAVE, name='staff_feedback_save'),

    #this is student urls
    path('student/Home', student_views.HOME, name='student_home'),
    path('student/Notifications', student_views.STUDENT_NOTIFICATION, name='student_notification'),
    path('student/mark_as_done/<str:status>', student_views.STUDENT_NOTIFICATION_MARK_AS_DONE,name='student_notification_mark_as_done'),

    path('student/Feedback', student_views.STUDENT_FEEDBACK, name='student_feedback'),
    path('student/Feedback/Save', student_views.STUDENT_FEEDBACK_SAVE, name='student_feedback_save'),

    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
