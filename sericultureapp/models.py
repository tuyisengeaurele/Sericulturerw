from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True) 
    phone = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=50 , blank=True)
    sex = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female')])
    role = models.CharField(max_length=20, choices=[('Farmer', 'Farmer'), ('Researcher', 'Researcher')])
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sericulture_User',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sericulture_User_permissions',
        blank=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Farm(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    size = models.FloatField(help_text="Size of the farm in hectares")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SilkwormBatch(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='silkworm_batches')
    batch_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    quantity = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.batch_name} - {self.farm.name}"

class Production(models.Model):
    silkworm_batch = models.ForeignKey(SilkwormBatch, on_delete=models.CASCADE, related_name='productions')
    production_date = models.DateField()
    quantity = models.FloatField(help_text="Quantity of silk produced in kilograms")
    quality_grade = models.CharField(max_length=50, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])

    def __str__(self):
        return f"{self.quantity} kg - {self.silkworm_batch.batch_name}"

class Course(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    learners = models.ManyToManyField(User, related_name='courses')  
    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True) 
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"Feedback by {self.name}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class IoTDevice(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='iot_devices')
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    last_communication = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.device_name

class PestOrDisease(models.Model):
    issue_id = models.AutoField(primary_key=True)
    silkwormbatch = models.ForeignKey(SilkwormBatch, on_delete=models.CASCADE)  
    issue_type = models.CharField(max_length=50,blank=True, null=True) 
    description =  models.CharField(max_length=100)
    detection_date = models.DateField()
    resolution =  models.CharField(max_length=100,blank=True, null=True)
    resolved_date = models.DateField(blank=True, null=True)
    def __str__(self):
        return f"{self.issue_type} - {self.silkwormbatch}"

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_joined = models.DateField()
    def __str__(self):
        return self.name

class WeatherMonitoring(models.Model):
    weather_id = models.AutoField(primary_key=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Weather at {self.farm} on {self.timestamp}"

class GrowthStage(models.Model):
    STAGES = [
        ('Egg', 'Egg'),
        ('Larva', 'Larva'),
        ('Pupa', 'Pupa'),
        ('Adult', 'Adult'),
    ]
    silkworm_batch = models.ForeignKey(
        SilkwormBatch, 
        on_delete=models.CASCADE, 
        related_name='growth_stages'
    )
    stage = models.CharField(max_length=20, choices=STAGES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.silkworm_batch.batch_name} - {self.stage}"

class FeedingSchedule(models.Model):
    silkworm_batch = models.ForeignKey(
        SilkwormBatch, 
        on_delete=models.CASCADE, 
        related_name='feeding_schedules'
    )
    feed_date = models.DateField(help_text="Date of feeding")
    feed_time = models.TimeField(help_text="Time of feeding")
    feed_quantity = models.FloatField(help_text="Quantity of feed in grams")
    feed_type = models.CharField(max_length=100, help_text="Type of feed given")
    remarks = models.TextField(blank=True, null=True, help_text="Any observations or notes about the feeding")
    def __str__(self):
        return f"Feeding for {self.silkworm_batch.batch_name} on {self.feed_date} at {self.feed_time}"
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"    

