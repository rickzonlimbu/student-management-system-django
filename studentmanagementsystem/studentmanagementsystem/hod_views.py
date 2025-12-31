from django.db.models.fields import return_None
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import request
from smsapp.models import Course, Batch_Year, CustomUser, Student, Staff, Subject, Staff_Notification, Staff_Leave
from django.contrib import messages

@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()

    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
    }

    return render(request, 'hod/home.html',context)

@login_required(login_url='/')
def ADD_STUDENT(request):
    courses = Course.objects.all()
    batch_years = Batch_Year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        batch_year_id = request.POST.get('batch_year_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_student')

        # Create user
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            profile_pic=profile_pic,
            user_type=3  # student
        )
        user.set_password(password)
        user.save()

        # Get related objects
        course_instance = Course.objects.get(id=course_id)
        batch_instance = Batch_Year.objects.get(id=batch_year_id)  # ✅ single instance

        # Create student
        student = Student(
            admin=user,
            address=address,
            batch_year_id=batch_instance,  # ✅ assign instance, not queryset
            course_id=course_instance,
            gender=gender,
        )
        student.save()
        messages.success(request, f"{user.first_name} {user.last_name} Added Successfully")
        return redirect('add_student')

    context = {
        'course': courses,
        'batch_year': batch_years
    }
    return render(request, 'hod/add_student.html', context)


@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()

    context = {
        'student':student,
    }
    return render(request,'hod/view_student.html',context)


def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    batch_year = Batch_Year.objects.all()

    context = {
        'student':student,
        'course':course,
        'batch_year':batch_year,
    }

    return render(request, 'hod/edit_student.html',context)

@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id = student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        if password != None and password != "":
            user.set_password(password)
        user.save()

        student  = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id = course_id)
        student.course_id = course

        batch_year = Batch_Year.objects.get(id = session_year_id)
        student.batch_year_id = batch_year

        student.save()
        messages.success(request,'Record Are Saved Successfully')
        return redirect('view_student')



    return render(request,'hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request, id):
    student = CustomUser.objects.get(id = id)
    student.delete()
    messages.success(request,'Record Are Deleted Successfully')
    return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')

        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request, 'Course Are Successfully Saved')
        return redirect('add_course')
    return render(request, 'hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context={
        'course':course
    }
    return render(request,'hod/view_course.html', context)

@login_required(login_url='/')
def EDIT_COURSE(request, id):
    course = Course.objects.get(id = id)

    context = {
        'course':course,
    }
    return render(request,'hod/edit_course.html',context)

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')

        course = Course.objects.get(id = course_id)
        course.name = name
        course.save()
        messages.success(request,'Course Are Updated Successfully')
        return redirect('view_course')

    return render(request,'hod/edit_course.html')

@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request,'Course Are Deleted Successfully')

    return redirect('view_course')

@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email Is Already Taken')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username Is Already Taken')
            return redirect('add_staff')

        else:
            user = CustomUser(first_name = first_name, last_name = last_name, email = email, profile_pic = profile_pic, username = username, user_type = 2)
            user.set_password(password)
            user.save()

            staff = Staff(
                admin = user,
                address = address,
                gender = gender,
            )
            staff.save()
            messages.success(request,'Staff Are Added Successfully')
            return redirect('add_staff')

    return render(request,'hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff':staff
    }
    return render(request,'hod/view_staff.html',context)

@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.get(id = id)
    context = {
        'staff':staff,
    }
    return render(request,'hod/edit_staff.html',context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id = staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        if password != None and password != "":
            user.set_password(password)
        user.save()

        staff = Staff.objects.get(admin = staff_id)
        staff.gender = gender
        staff.address = address
        staff.save()
        messages.success(request,'Staff Is Updated Successfully')
        return redirect('view_staff')

    return render(request, 'hod/edit_staff.html')

@login_required(login_url='/')
def DELETE_STAFF(request,admin):
    staff = CustomUser.objects.get(id = admin)
    staff.delete()
    messages.success(request,'Staff Are Successfully Deleted')
    return redirect('view_staff')


@login_required(login_url='/')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()

        messages.success(request, 'Subjects Are Successfully Added')
        return redirect('add_subject')

    context = {
        'course': course,
        'staff': staff,
    }
    return render(request, 'hod/add_subject.html', context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()

    context = {
        'subject':subject,
    }
    return render(request,'hod/view_subject.html',context)

@login_required(login_url='/')
def EDIT_SUBJECT(request,id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    staff = Staff.objects.all()

    context = {
        'subject':subject,
        'course':course,
        'staff':staff,
    }

    return render(request,'hod/edit_subject.html',context)

@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        subject = Subject.objects.get(id=subject_id)
        subject.name = subject_name
        subject.course_id = course_id
        subject.staff_id = staff_id
        subject.save()

        messages.success(request, 'Subject Successfully Updated')
        return redirect('view_subject')

@login_required(login_url='/')
def DELETE_SUBJECT(request,id):
    subject = Subject.objects.filter(id = id)
    subject.delete()
    messages.success(request, 'Subject Are Successfully Deleted')
    return redirect('view_subject')

@login_required(login_url='/')
def ADD_BATCH(request):
    if request.method == "POST":
        batch_year_start = request.POST.get('batch_year_start')
        batch_year_end = request.POST.get('batch_year_end')

        batch = Batch_Year(
            batch_start = batch_year_start,
            batch_end =  batch_year_end,
        )
        batch.save()
        messages.success(request,'Batch Are Successfully Created')
        return redirect('add_batch')

    return render(request, 'hod/add_batch.html')

@login_required(login_url='/')
def VIEW_BATCH(request):
    batch = Batch_Year.objects.all()

    context = {
        'batch':batch,
    }
    return render(request,'hod/view_batch.html',context)

@login_required(login_url='/')
def EDIT_BATCH(request,id):
    batch = Batch_Year.objects.filter(id = id)

    context = {
        'batch':batch,
    }

    return render(request,'hod/edit_batch.html',context)

def UPDATE_BATCH(request):
    if request.method == "POST":
        batch_id = request.POST.get('batch_id')
        batch_year_start = request.POST.get('batch_year_start')
        batch_year_end = request.POST.get('batch_year_end')

        batch = Batch_Year(
            id = batch_id,
            batch_start = batch_year_start,
            batch_end = batch_year_end,
        )
        batch.save()
        messages.success(request,'Batch Are Successfully Updated')
        return redirect('view_batch')


def DELETE_BATCH(request,id):
    batch = Batch_Year.objects.get(id = id)
    batch.delete()
    messages.success(request,'Batch Are Successfully Deleted')
    return redirect('view_batch')


def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]

    context = {
        'staff':staff,
        'see_notification':see_notification,
    }
    return render(request, 'hod/staff_notification.html',context)


def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request,'Notification Are Successfully Sent')
    return redirect('staff_send_notification')


def Staff_Leave_view(request):
    staff_leave = Staff_Leave.objects.all()

    context = {
        'staff_leave':staff_leave,
    }

    return render(request,'hod/staff_leave.html',context)


def Staff_Approve_Leave(request,id):
    leave = Staff_Leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')


def Staff_Reject_Leave(request,id):
    leave = Staff_Leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')