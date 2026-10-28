from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render,redirect
from .models import Doctor,Appointment,Specialty
from .forms import AppointmentForm

def is_hx(r): return r.headers.get('HX-Request')=='true'
def doctor_list(request):
    qs=Doctor.objects.select_related('specialty').all(); q=request.GET.get('q','').strip(); spec=request.GET.get('specialty',''); sort=request.GET.get('sort','name')
    if q: qs=qs.filter(full_name__icontains=q) | qs.filter(bio__icontains=q)
    if spec: qs=qs.filter(specialty__slug=spec)
    qs=qs.order_by({'fee_low':'consultation_fee','fee_high':'-consultation_fee','name':'full_name'}.get(sort,'full_name'))
    ctx={'doctors':qs,'specialties':Specialty.objects.all(),'q':q,'selected_specialty':spec,'sort':sort}
    return render(request,'clinic/partials/_doctor_grid.html' if is_hx(request) else 'clinic/doctor_list.html',ctx)
def doctor_detail(request,pk): return render(request,'clinic/doctor_detail.html',{'doctor':get_object_or_404(Doctor,pk=pk)})
def book(request,pk):
    doctor=get_object_or_404(Doctor,pk=pk)
    if not doctor.is_accepting: return HttpResponse('This doctor is not accepting appointments.',status=400)
    form=AppointmentForm(request.POST or None,doctor=doctor)
    if request.method=='POST' and form.is_valid():
        a=form.save(commit=False); a.doctor=doctor; a.save()
        if is_hx(request):
            r=HttpResponse(status=204); r['HX-Redirect']=f'/appointments/{a.pk}/confirmation/'; r['HX-Trigger']='{"toast":{"type":"success","message":"Appointment booked"}}'; return r
        return redirect('confirmation',pk=a.pk)
    return render(request,'clinic/partials/_appointment_form.html' if is_hx(request) else 'clinic/appointment_form.html',{'doctor':doctor,'form':form})
def slots(request,pk):
    doctor=get_object_or_404(Doctor,pk=pk); d=request.GET.get('appointment_date'); booked=set(Appointment.objects.filter(doctor=doctor,appointment_date=d).exclude(status='Cancelled').values_list('time_slot',flat=True)) if d else set()
    return render(request,'clinic/partials/_slot_options.html',{'slots':Appointment.SLOTS,'booked':booked})
def confirmation(request,pk): return render(request,'clinic/appointment_success.html',{'appointment':get_object_or_404(Appointment,pk=pk)})
def doctor_manage(request): return render(request,'clinic/doctor_manage.html',{'doctors':Doctor.objects.all()})
def appointment_manage(request): return render(request,'clinic/appointment_manage.html',{'appointments':Appointment.objects.select_related('doctor').all()})
def appointment_action(request,pk,action):
    a=get_object_or_404(Appointment,pk=pk); a.status='Confirmed' if action=='confirm' else 'Cancelled'; a.save(update_fields=['status'])
    return render(request,'clinic/partials/_appointment_row.html',{'a':a})
