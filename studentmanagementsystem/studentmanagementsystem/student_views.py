from pyexpat.errors import messages

from django.shortcuts import render,redirect
from smsapp.models import Student, Student_Notification, Student_Feedback

def HOME(request):
    return render(request,'student/home.html')


def STUDENT_NOTIFICATION(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id
        notification = Student_Notification.objects.filter(student_id=student_id)

        context = {
            'notification':notification,
        }

    return render(request,'student/notification.html',context)


def STUDENT_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Student_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')


def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id=student_id)

    context = {
        'feedback_history':feedback_history,
    }
    return render(request,'student/feedback.html',context)


def STUDENT_FEEDBACK_SAVE(request):
    student = Student.objects.get(admin = request.user.id)
    if request.method == "POST":
        feedback = request.POST.get('feedback')

        feedbacks = Student_Feedback(
            student_id = student,
            feedback = feedback,
            feedback_reply = ""
        )
        feedbacks.save()
        return redirect('student_feedback')