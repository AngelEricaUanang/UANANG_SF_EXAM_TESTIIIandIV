from django.db import models
class Specialty(models.Model):
    name=models.CharField(max_length=80); slug=models.SlugField(unique=True)
    def __str__(self): return self.name
class Doctor(models.Model):
    full_name=models.CharField(max_length=120); specialty=models.ForeignKey(Specialty,on_delete=models.PROTECT)
    bio=models.TextField(); consultation_fee=models.DecimalField(max_digits=8,decimal_places=2)
    photo=models.ImageField(upload_to='doctors/'); is_accepting=models.BooleanField(default=True); date_created=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.full_name
class Appointment(models.Model):
    SLOTS=[(x,x) for x in ['09:00','10:00','11:00','13:00','14:00','15:00']]
    VISITS=[('In-Clinic','In-Clinic'),('Teleconsultation','Teleconsultation')]
    STATUS=[('Pending','Pending'),('Confirmed','Confirmed'),('Cancelled','Cancelled')]
    doctor=models.ForeignKey(Doctor,on_delete=models.PROTECT); patient_name=models.CharField(max_length=120)
    email=models.EmailField(blank=True); phone=models.CharField(max_length=13); appointment_date=models.DateField(); time_slot=models.CharField(max_length=5,choices=SLOTS)
    visit_type=models.CharField(max_length=20,choices=VISITS); reason=models.CharField(max_length=300); status=models.CharField(max_length=10,choices=STATUS,default='Pending'); date_created=models.DateTimeField(auto_now_add=True)
    @property
    def reference(self): return f'MB-{self.pk:05d}' if self.pk else 'MB-NEW'
