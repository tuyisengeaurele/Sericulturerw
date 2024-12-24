from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.db.models import Avg, Sum, Count, F, Q
from datetime import timedelta,datetime
from django.utils import timezone
import json
from django.core.mail import send_mail
from django.conf import settings

def display(request):
    return render(request,'Home.html')

def dlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}") 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admindashboard')
            else:
                return redirect('userdashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def dforgot(request):
    return render(request,'forgot password.html')

def dregister(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        sex = request.POST.get('sex')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            sex=sex,
            role=role
        )
        
    return render(request, 'register.html')

def dabout(request):
    return render(request,'about us.html')

def dservices(request):
    return render(request,'services.html')

@login_required
def dadmin(request):
    if request.user.username == 'auris': 
        user_count = User.objects.count() 
        farm_count = Farm.objects.count()  
        course_count = Course.objects.count() 
        feedback_count= Feedback.objects.count()
        context = {
            'username': request.user.username,
            'user_count': user_count,
            'farm_count': farm_count,
            'course_count': course_count,
            'feedback_count':feedback_count,
        }
        return render(request, 'admindashboard.html', context)
    else:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
@login_required
def duser(request):
    user = request.user
    my_farm_count = Farm.objects.filter(owner=user).count()
    my_course_count = user.courses.count()
    notification_count = Notification.objects.filter(user=user, read=False).count()
    feedback_count = Feedback.objects.count()  
    context = {
        'user': user,
        'my_farm_count': my_farm_count,
        'my_course_count': my_course_count,
        'notification_count': notification_count,
        'feedback_count': feedback_count,
    }
    return render(request, 'userdashboard.html', context)

def duser_management(request):
    users = User.objects.all()
    print(users)
    return render(request, 'user_management.html', {'users': users})

def dfarm_management(request):
    farms = Farm.objects.all()  
    return render(request, 'farm_management.html', {'farms': farms})

def dproduction_management(request):
    return render(request, 'production_management.html')

def dcontent_management(request):
    return render(request, 'content_management.html')

def dprojects(request):
    return render(request, 'projects.html')

def dcontact(request):
    return render(request, 'contact_us.html')

def dadd_farm(request):
    return render(request,'add_farm.html')

def feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at') 
    return render(request, 'feedback.html', {'feedback_list': feedback_list})

def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')  
        message = request.POST.get('message')
        rating = request.POST.get('rating')
        feedback = Feedback(name=name, message=message)
        feedback.save()
        if email: 
            try:
                send_mail(
                    subject="Thank You for Your Feedback",
                    message=f"Dear {name or 'User'},\n\n"
                            "Thank you for your feedback! We have received your message:\n"
                            f"\"{message}\"\n\n"
                            "We will get back to you soon if needed.\n\n"
                            "Best regards,\nSericulture Rwanda Team",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")  
        return redirect('contact_us')
    return redirect('contact_us') 

def farm_details(request):
    dfarm = Farm.objects.prefetch_related(
        'staff_set',
        'weathermonitoring_set',
        'silkworm_batches__pestordisease_set',
        'silkworm_batches__productions'
    ).all()
    productions_data = {
        "labels": ["January", "February", "March", "April", "May"],
        "values": [12, 19, 3, 5, 2],
    }
    return render(request, 'farm_details.html', {
        'dfarm': dfarm,  
        'productions_data': productions_data, 
    })

def farm_details1(request):
    dfarm = Farm.objects.prefetch_related(
        'staff_set',
        'weathermonitoring_set',
        'silkworm_batches__pestordisease_set',
        'silkworm_batches__productions'
    ).all()
    productions_data = {
        "labels": ["January", "February", "March", "April", "May"],
        "values": [12, 19, 3, 5, 2],
    }
    return render(request, 'farm_details.html', {
        'dfarm': dfarm,  
        'productions_data': productions_data, 
    })

def farm_details2(request):
    dfarm = Farm.objects.prefetch_related(
        'staff_set',
        'weathermonitoring_set',
        'silkworm_batches__pestordisease_set',
        'silkworm_batches__productions'
    ).all()
    productions_data = {
        "labels": ["January", "February", "March", "April", "May"],
        "values": [12, 19, 3, 5, 2],
    }
    return render(request, 'farm_details.html', {
        'dfarm': dfarm,  
        'productions_data': productions_data, 
    })

def my_farms(request):
    return render(request, 'my_farms.html')

def user_feedback(request):
    return render(request, 'user_feedback.html')

def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at') 
    return render(request, 'user_notification.html', {'notifications': notifications})

def my_courses(request):
    return render(request, 'my_courses.html')

def userprofile(request):
    return render(request,'userprofile.html')

def manage_staff(request):
    user_farm = Farm.objects.filter(owner=request.user).first() 
    if user_farm: 
        staff_list = Staff.objects.filter(farm=user_farm)  
    else:
        staff_list = [] 
    return render(request, 'manage_staff.html', {'staff_list': staff_list})

def reports(request):
    user = request.user  
    user_farms = Farm.objects.filter(owner=user)
    user_total_production = Production.objects.filter(silkworm_batch__farm__owner=user).aggregate(
        total=Sum('quantity')
    )['total'] or 0
    user_active_farms = user_farms.filter(description__icontains='Active').count()
    user_silkworm_batches = SilkwormBatch.objects.filter(farm__owner=user).count()
    production_queryset = (
        Production.objects.filter(silkworm_batch__farm__owner=user)
        .annotate(month=F('production_date__month'))
        .values('month')
        .annotate(total_production=Sum('quantity'))
        .order_by('month')
    )
    production_data = {
        "labels": [f"Month {entry['month']}" for entry in production_queryset],
        "values": [entry['total_production'] for entry in production_queryset],
    }
    silkworm_queryset = SilkwormBatch.objects.filter(farm__owner=user).values('batch_name', 'quantity')
    growth_data = {
        "labels": [entry['batch_name'] for entry in silkworm_queryset],
        "values": [entry['quantity'] for entry in silkworm_queryset],
    }
    low_performance_farms = user_farms.filter(silkworm_batches__productions__quantity__lt=50).distinct()
    context = {
        "user_farms": user_farms,
        "user_total_production": user_total_production,
        "user_active_farms": user_active_farms,
        "user_silkworm_batches": user_silkworm_batches,
        "user_production_data": production_data,
        "user_growth_data": growth_data,
        "low_performance_farms": low_performance_farms,
    }
    return render(request, "reports.html", context)

def analytics(request):
    farms = Farm.objects.all()
    production_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "values": [120, 150, 130, 170, 180, 200] 
    }
    growth_data = {
        "labels": ["Batch 1", "Batch 2", "Batch 3", "Batch 4"],
        "values": [80, 85, 90, 95]  
    }
    context = {
        "farms": farms,
        "total_production": Production.objects.aggregate(total=Sum('quantity'))['total'],
        "active_farms": farms.count(),
        "silkworm_batches": SilkwormBatch.objects.count(),
        "production_data": production_data,
        "growth_data": growth_data,
    }
    return render(request, "analytics.html", context)

def my_farms(request):
    farms = Farm.objects.filter(owner=request.user).prefetch_related('silkworm_batches__productions')
    return render(request, 'my_farms.html', {'farms': farms})

def add_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user 
            farm.save()
            return redirect('my_farms')
    else:
        form = FarmForm()
    return render(request, 'add_farm.html', {'form': form})

def view_farm(request):
    return render(request,'view_farm.html')

def view_farm(request):
    farms = Farm.objects.filter(owner=request.user)
    return render(request, 'view_farm.html', {'farms': farms})

TEMP_THRESHOLD_HIGH = 35.0  
TEMP_THRESHOLD_LOW = 15.0 
HUMIDITY_THRESHOLD_HIGH = 80.0  
HUMIDITY_THRESHOLD_LOW = 30.0  

def farm_conditions(request):
    user_farms = Farm.objects.filter(owner=request.user)
    farm = user_farms.first()  
    weather_data = WeatherMonitoring.objects.filter(farm__in=user_farms).order_by('-timestamp')[:10]
    avg_conditions = WeatherMonitoring.objects.filter(farm__in=user_farms).aggregate(
        avg_temp=Avg('temperature'),
        avg_humidity=Avg('humidity')
    )
    avg_temp = avg_conditions['avg_temp']
    avg_humidity = avg_conditions['avg_humidity']
    alerts = []
    if avg_temp and (avg_temp > TEMP_THRESHOLD_HIGH or avg_temp < TEMP_THRESHOLD_LOW):
        alerts.append(f"Temperature is {'too high' if avg_temp > TEMP_THRESHOLD_HIGH else 'too low'}!")
    if avg_humidity and (avg_humidity > HUMIDITY_THRESHOLD_HIGH or avg_humidity < HUMIDITY_THRESHOLD_LOW):
        alerts.append(f"Humidity is {'too high' if avg_humidity > HUMIDITY_THRESHOLD_HIGH else 'too low'}!")
    return render(request, 'farm_conditions.html', {
        'farm': farm,
        'weather_data': weather_data,
        'avg_temp': avg_temp,
        'avg_humidity': avg_humidity,
        'alerts': alerts,
    })

def silkworm_batches(request):
    farm = get_object_or_404(Farm, owner=request.user)
    batches = SilkwormBatch.objects.filter(farm=farm)
    batch_names = [batch.batch_name for batch in batches]
    batch_quantities = [batch.quantity for batch in batches]
    start_dates = [batch.start_date for batch in batches]
    if request.method == "POST":
        form = SilkwormBatchForm(request.POST)
        if form.is_valid():
            new_batch = form.save(commit=False)
            new_batch.farm = farm
            new_batch.save()
            Notification.objects.create(
                title=f"New Silkworm Batch Added: {new_batch.batch_name}", 
                user=request.user,
                message=f"A new silkworm batch '{new_batch.batch_name}' has been added to your farm.",
                read=False
            )
            messages.success(request, 'Silkworm batch added successfully.')
            return redirect('silkworm_batches')
    else:
        form = SilkwormBatchForm()
    context = {
        'farm': farm,
        'batches': batches,
        'batch_names': batch_names,
        'batch_quantities': batch_quantities,
        'start_dates': start_dates,
        'form': form,  
    }
    return render(request, 'silkworm_batches.html', context)

def production(request):
    user = request.user
    farms = user.farms.all()
    batches = SilkwormBatch.objects.filter(farm__owner=user)
    production_dates = []
    production_quantities = []
    quality_grades = []
    productions = Production.objects.filter(silkworm_batch__in=batches)
    for prod in productions:
        production_dates.append(prod.production_date)
        production_quantities.append(prod.quantity)
        quality_grades.append(prod.quality_grade)
    grade_totals = productions.values('quality_grade').annotate(total_quantity=Sum('quantity'))
    grade_labels = ['A', 'B', 'C']
    grade_data = [0, 0, 0]
    for grade in grade_totals:
        if grade['quality_grade'] == 'A':
            grade_data[0] = grade['total_quantity']
        elif grade['quality_grade'] == 'B':
            grade_data[1] = grade['total_quantity']
        elif grade['quality_grade'] == 'C':
            grade_data[2] = grade['total_quantity']
    form = ProductionForm()
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            production = form.save(commit=False)
            if production.silkworm_batch in batches:
                production.save()
                title = f"New production: {production.silkworm_batch.batch_name}" 
                notification_message = f"A new production of {production.quantity}kg has been added to your batch {production.silkworm_batch.batch_name}."
                Notification.objects.create(user=user, title=title, message=notification_message)
                messages.success(request, 'Production added successfully.')
                return redirect('production') 
    context = {
        'form': form, 
        'batches': batches,
        'productions': productions,
        'production_dates': production_dates,
        'production_quantities': production_quantities,
        'quality_grades': quality_grades,
        'grade_labels': grade_labels,
        'grade_data': grade_data,
    }
    return render(request, 'production.html', context)

def device_deployed(request):
    user = request.user
    farms = user.farms.all()
    devices = IoTDevice.objects.filter(farm__owner=user)
    status_counts = devices.values('status').annotate(count=Count('status'))
    last_comm_30_days = devices.filter(last_communication__gte=timezone.now() - timedelta(days=30))
    device_names = [device.device_name for device in devices]
    device_types = [device.device_type for device in devices]
    device_statuses = [device.status for device in devices]
    last_communications = [device.last_communication for device in devices]
    status_labels = ['Active', 'Inactive']
    status_data = [0, 0] 
    for status in status_counts:
        if status['status'] == 'Active':
            status_data[0] = status['count']
        elif status['status'] == 'Inactive':
            status_data[1] = status['count']
    context = {
        'user': user,
        'farms': farms,
        'devices': devices,
        'device_names': device_names,
        'device_types': device_types,
        'device_statuses': device_statuses,
        'last_communications': last_communications,
        'status_labels': status_labels,
        'status_data': status_data,
        'last_comm_30_days': last_comm_30_days,
    }
    return render(request, 'device_deployed.html', context)

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            farm = Farm.objects.filter(owner=request.user).first() 
            if not farm:
                messages.error(request, "You do not have a farm associated with your account.")
                return redirect('manage_staff')
            staff.farm = farm
            staff.user = request.user 
            staff.save()
            Notification.objects.create(
                user=request.user,
                title=f"New Staff Added: {staff.name}",
                message=f"A new staff member, {staff.name}, has been added to your farm.",
                created_at=datetime.now(),
                read=False
            )
            messages.success(request, "Staff added successfully!")
            return redirect('add_staff')
    else:
        form = StaffForm()
    farm = Farm.objects.filter(owner=request.user).first() 
    staff_list = Staff.objects.filter(farm=farm) if farm else []

    return render(request, 'add_staff.html', {
        'form': form,
        'staff_list': staff_list
    })
from collections import Counter

def pest_and_diseases(request):
    user = request.user
    issues = PestOrDisease.objects.filter(silkwormbatch__farm__owner=user)
    if request.method == 'POST':
        form = PestOrDiseaseForm(request.POST)
        if form.is_valid():
            new_issue = form.save()
            notification = Notification(
                user=request.user,
                title=f"New Pest/Disease Reported: {new_issue.issue_type}",
                message=f"A new pest/disease issue '{new_issue.issue_type}' has been reported in batch '{new_issue.silkwormbatch.batch_name}'.",
                created_at=timezone.now(),
                read=False
            )
            notification.save()
            messages.success(request, 'Pest/Disease reported successfully.')
            return redirect('pest_and_diseases')
    else:
        form = PestOrDiseaseForm()
    silkworm_batches = SilkwormBatch.objects.filter(farm__owner=user)
    issue_counts = Counter(issue.issue_type for issue in issues)
    issue_types = list(issue_counts.keys())
    issue_counts_values = list(issue_counts.values())
    chart_data = {
        'labels': issue_types,
        'data': issue_counts_values,
    }
    context = {
        'issues': issues,
        'form': form,
        'silkworm_batches': silkworm_batches, 
        'chart_data': chart_data,
    }
    return render(request, 'pest_and_diseases.html', context)

def track_growth(request):
    user = request.user
    growth_stages = GrowthStage.objects.filter(silkworm_batch__farm__owner=user)
    stage_counts = (
        growth_stages.values('stage')
        .annotate(count=models.Count('stage'))
        .order_by('stage')
    )
    stage_counts = list(stage_counts)
    durations = [
        {
            'stage': stage['stage'],
            'duration': (stage['end_date'] - stage['start_date']).days if stage['end_date'] else 0,
        }
        for stage in growth_stages.values('stage', 'start_date', 'end_date')
    ]
    if request.method == 'POST':
        silkworm_batch_id = request.POST.get('silkworm_batch')
        stage = request.POST.get('stage')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        observations = request.POST.get('observations')
        silkworm_batch = SilkwormBatch.objects.get(id=silkworm_batch_id)
        growth_stage = GrowthStage(
            silkworm_batch=silkworm_batch,
            stage=stage,
            start_date=start_date,
            end_date=end_date if end_date else None,
            observations=observations,
        )
        growth_stage.save()
        notification = Notification(
            user=request.user,
            title=f"New Growth Stage: {stage}",
            message=f"A new stage '{stage}' has been added to batch '{silkworm_batch.batch_name}'.",
            created_at=timezone.now(),
            read=False
        )
        notification.save()
        messages.success(request, 'Growth stage added successfully.')
        return redirect('track_growth')
    silkworm_batches = SilkwormBatch.objects.filter(farm__owner=user)

    context = {
        'growth_stages': growth_stages,
        'stage_counts': json.dumps(stage_counts),
        'durations': json.dumps(durations),  
        'silkworm_batches': silkworm_batches,
    }
    return render(request, 'track_growth.html', context)

def feeding_schedule(request):
    user_farms = request.user.farms.all()  
    feeding_schedules = FeedingSchedule.objects.filter(silkworm_batch__farm__in=user_farms)
    context = {
        'feeding_schedules': feeding_schedules,
    }
    return render(request, 'feeding_schedule.html', context)

def user_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    context = {
        'notifications': notifications
    }
    return render(request, 'user_notifications.html', context)

def community_chatroom(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            ChatMessage.objects.create(user=request.user, content=content)
            return redirect("community_chatroom") 
    messages = ChatMessage.objects.order_by("timestamp")
    return render(request, "community_chatroom.html", {"messages": messages})

def admin_notifications(request):
    if not request.user.is_staff:
        return render(request, "403.html", status=403) 
    notifications = Notification.objects.all().order_by('-created_at')
    context = {
        'notifications': notifications,
    }
    return render(request, 'admin_notifications.html', context)