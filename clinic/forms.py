import re
from datetime import date
from django import forms
from .models import Doctor,Appointment
class DoctorForm(forms.ModelForm):
    class Meta:
        model=Doctor; fields=['full_name','specialty','bio','consultation_fee','photo','is_accepting']
        labels={'full_name':'Doctor name','consultation_fee':'Consultation fee (PHP)'}
        help_texts={'bio':'Brief professional profile.','photo':'JPEG or PNG portrait.'}
        widgets={'bio':forms.Textarea(attrs={'rows':4,'placeholder':'Specialization and clinic experience'})}
    def clean_consultation_fee(self):
        fee=self.cleaned_data['consultation_fee']
        if fee <= 0: raise forms.ValidationError('Consultation fee must be greater than 0.')
        return fee
class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment; fields=['patient_name','email','phone','appointment_date','time_slot','visit_type','reason']
        labels={'patient_name':'Patient name','appointment_date':'Appointment date','time_slot':'Available time','reason':'Reason for visit'}
        help_texts={'phone':'Use 09XXXXXXXXX or +639XXXXXXXXX.','reason':'At least 10 characters; maximum 300.'}
        widgets={'appointment_date':forms.DateInput(attrs={'type':'date'}),'reason':forms.Textarea(attrs={'rows':4,'maxlength':300})}
    def __init__(self,*args,doctor=None,**kwargs): self.doctor=doctor; super().__init__(*args,**kwargs)
    def clean_phone(self):
        p=self.cleaned_data['phone'].strip()
        if not re.fullmatch(r'(09\d{9}|\+639\d{9})',p): raise forms.ValidationError('Enter 09XXXXXXXXX or +639XXXXXXXXX.')
        return p
    def clean_appointment_date(self):
        d=self.cleaned_data['appointment_date']
        if d < date.today(): raise forms.ValidationError('Appointment date cannot be in the past.')
        if d.weekday()==6: raise forms.ValidationError('The clinic is closed on Sundays.')
        return d
    def clean(self):
        c=super().clean(); email=c.get('email'); visit=c.get('visit_type'); reason=(c.get('reason') or '').strip(); d=c.get('appointment_date'); slot=c.get('time_slot')
        if visit=='Teleconsultation' and not email: self.add_error('email','Email is required for Teleconsultation.')
        if len(reason)<10: self.add_error('reason','Reason must have at least 10 characters.')
        if self.doctor and d and slot and Appointment.objects.filter(doctor=self.doctor,appointment_date=d,time_slot=slot).exclude(status='Cancelled').exists(): raise forms.ValidationError('That time slot has already been booked.')
        return c
