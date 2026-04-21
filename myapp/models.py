from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
# Model #1 - Parent Model
class AttackCategory(models.Model):
    """categorize the type of attack"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# Model #2 - Main Data Model (using ForeignKey and Choices)
class SecurityEvent(models.Model):
    #Requirement: At least 1 ForeignKey relationship
    category = models.ForeignKey(AttackCategory, on_delete=models.CASCADE, related_name='events')
    timestamp = models.DateTimeField()
    packet_length = models.FloatField(null=True, blank=True)

    ACTION_CHOICES = [
        ('blocked','Blocked'),
        ('logged','Logged'),
        ('ignored','Ignored'),
    ]

    action_taken = models.CharField(
        max_length =20,
        choices = ACTION_CHOICES,
        default='logged'
    )

    #Requirement: At least 1 field with choices
    SEVERITY_CHOICES =[
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
        ('critical','Critical'),
    ]
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)

    #Requirment: field for Proj 1 and 2 continuity 
    SOURCE_CHOICES = [
        ('csv','CSV Import'),
        ('api','API Fetch'),
    ]

    source = models.CharField(max_length=10, choices = SOURCE_CHOICES, default ='csv')

    #Requirment : validator or specific field type
    threat_score = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        #requirement: ordering and unique_together
        ordering = ['-timestamp']
        #prevent duplicate logs for the same cat
        unique_together = ['category', 'timestamp']

    def __str__(self):
        return f"{self.category.name} - {self.severity}"
    
#Model #3 - Metadata model 
class DataIngestionLog(models.Model):
    """Tracks when seed_data or fetch_data commands run """
    run_date= models.DateTimeField(auto_now_add = True)
    records_added = models.IntegerField()
    status = models.CharField(max_length=50)

#For API Intergration: 
class City(models.Model):
    name = models.CharField(max_length=100, unique =True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name 
        
class WeatherRecord(models.Model):
    city = models.ForeignKey(City, on_delete = models.CASCADE, related_name='weather_records')
    date = models.DateField()
    temperature_max = models.FloatField()
    temperature_min = models.FloatField()
    precipitation = models.FloatField(default = 0.0)
    source = models.CharField(max_length=100, default='Open-Mateo API')

    def __str__(self):
        return f"{self.city.name} - {self.date}"    