from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Specialty', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('name', models.CharField(max_length=80)),('slug', models.SlugField(unique=True))]),
        migrations.CreateModel(name='Doctor', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('full_name', models.CharField(max_length=120)),('bio', models.TextField()),('consultation_fee', models.DecimalField(decimal_places=2, max_digits=8)),('photo', models.ImageField(upload_to='doctors/')),('is_accepting', models.BooleanField(default=True)),('date_created', models.DateTimeField(auto_now_add=True)),('specialty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.specialty'))]),
        migrations.CreateModel(name='Appointment', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('patient_name', models.CharField(max_length=120)),('email', models.EmailField(blank=True, max_length=254)),('phone', models.CharField(max_length=13)),('appointment_date', models.DateField()),('time_slot', models.CharField(choices=[('09:00','09:00'),('10:00','10:00'),('11:00','11:00'),('13:00','13:00'),('14:00','14:00'),('15:00','15:00')], max_length=5)),('visit_type', models.CharField(choices=[('In-Clinic','In-Clinic'),('Teleconsultation','Teleconsultation')], max_length=20)),('reason', models.CharField(max_length=300)),('status', models.CharField(choices=[('Pending','Pending'),('Confirmed','Confirmed'),('Cancelled','Cancelled')], default='Pending', max_length=10)),('date_created', models.DateTimeField(auto_now_add=True)),('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clinic.doctor'))])
    ]
