from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from smsapp.models import Staff, Student, Staff_Notification, Staff_Leave, Staff_Feedback, Batch_Year, Subject, Attendance, Attendance_Report


@login_required(login_url='/')
def HOME(request):
    return render(request,'staff/home.html')

@login_required(login_url='/')
def NOTIFICATION(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id

        notification = Staff_Notification.objects.filter(staff_id = staff_id)

        context = {
            'notification':notification,
        }
    return render(request,'staff/notification.html',context)

@login_required(login_url='/')
def STAFF_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('notifications')

@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id

        staff_leave_history = Staff_Leave.objects.filter(staff_id = staff_id)

        context = {
            'staff_leave_history':staff_leave_history,
        }
    return render(request, 'staff/apply_leave.html',context)

@login_required(login_url='/')
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_reason = request.POST.get('leave_reason')

        staff = Staff.objects.get(admin = request.user.id)

        leave = Staff_Leave(
            staff_id = staff,
            date = leave_date,
            message = leave_reason,
        )
        leave.save()
        messages.success(request,'Leave Successfully Applied')
        return redirect('staff_apply_leave')


def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)

    context = {
        'feedback_history':feedback_history,
    }
    return render(request,'staff/feedback.html',context)


def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(admin=request.user.id)
        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply = "",
        )
        feedback.save()
        return redirect('staff_feedback')


def STAFF_TAKE_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff = staff_id)
    batch_year = Batch_Year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_batch_year = None
    students = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            batch_year_id = request.POST.get('batch_year_id')

            get_subject = Subject.objects.get(id = subject_id)
            get_batch_year = Batch_Year.objects.get(id = batch_year_id)

            subject = Subject.objects.filter(id = subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id = student_id)


    context = {
        'subject':subject,
        'batch_year':batch_year,
        'get_subject':get_subject,
        'get_batch_year':get_batch_year,
        'action':action,
        'students':students,
    }
    return render(request,'staff/take_attendance.html',context)


def STAFF_SAVE_ATTENDANCE(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        batch_year_id = request.POST.get('batch_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id = subject_id)
        get_batch_year = Batch_Year.objects.get(id = batch_year_id)

        attendance = Attendance(
            subject_id = get_subject,
            attendance_date = attendance_date,
            batch_year_id = get_batch_year,
        )
        attendance.save()
        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)

            p_students = Student.objects.get(id = int_stud)
            attendance_report = Attendance_Report(
                student_id = p_students,
                attendance_id = attendance,
            )
            attendance_report.save()

    return redirect('staff_take_attendance')


def STAFF_VIEW_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin = request.user.id)

    subject = Subject.objects.filter(staff_id = staff_id)
    batch_year = Batch_Year.objects.all()

    action = request.GET.get('action')
    get_subject = None
    get_batch_year = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            batch_year_id = request.POST.get('batch_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id = subject_id)
            get_batch_year = Batch_Year.objects.get(id = batch_year_id)
            attendance = Attendance.objects.filter(subject_id = get_subject, attendance_date = attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id = attendance_id)
    context = {
        'subject':subject,
        'batch_year':batch_year,
        'action':action,
        'get_subject':get_subject,
        'get_batch_year':get_batch_year,
        'attendance_date':attendance_date,
        'attendance_report':attendance_report,
    }
    return render(request,'staff/view_attendance.html',context)