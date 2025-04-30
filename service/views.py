from django.views import View
from django.http import HttpResponseRedirect

from django.shortcuts import render
class KeycloakLogin(View):
    def get(self, request):
        return HttpResponseRedirect('/oauth/login/keycloak/')
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    try:
        social_user = request.user.social_auth.get(provider='keycloak')
        social_data = social_user.extra_data
    except:
        social_data = None
    return render(request, 'profile.html', {
        'social_data': social_data,
        'user': request.user
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Appointment, PriceImage
from service.forms import AppointmentForm

# Базовые страницы
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def price_list(request):
    price = PriceImage.objects.last()  # Показываем последнюю загруженную версию
    return render(request, 'price.html', {'price': price})

def contacts(request):
    return render(request, 'contacts.html')

from django.contrib import messages
from .forms import ProfileForm
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakError
from django.conf import settings


@login_required
def cabinet(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                # Сохраняем данные в Django
                user = form.save()
                profile = user.profile
                profile.patronymic = form.cleaned_data['patronymic']
                profile.phone = form.cleaned_data['phone']
                profile.save()

                # Инициализация Keycloak Admin
                keycloak_admin = KeycloakAdmin(
                    server_url=settings.KEYCLOAK_SERVER_URL,
                    client_id=settings.KEYCLOAK_CLIENT_ID,
                    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
                    realm_name=settings.KEYCLOAK_REALM,
                    verify=False
                )

                # Ищем пользователя по email
                users = keycloak_admin.get_users({"email": user.email})
                if not users:
                    raise Exception("User not found in Keycloak")
                user_id = users[0]["id"]

                update_data = {
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'email': user.email, 
                    'emailVerified': True, 
                    'attributes': {
                        'patronymic': profile.patronymic,
                        'phone': profile.phone,
                    }
                }

                keycloak_admin.update_user(user_id, update_data)
                
                messages.success(request, 'Данные успешно обновлены!')
            except KeycloakError as e:
                messages.error(request, f'Ошибка Keycloak: {e.response_body.decode()}')
            except Exception as e:
                messages.error(request, f'Ошибка: {str(e)}')
            
            return redirect('cabinet')
    else:
        initial_data = {
            'patronymic': request.user.profile.patronymic,
            'phone': request.user.profile.phone
        }
        form = ProfileForm(instance=request.user, initial=initial_data)
    
    return render(request, 'cabinet.html', {'form': form})

# Запись на прием
@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('cabinet')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})

# Админ-панель
@staff_member_required
def admin_panel(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin_panel.html', {'appointments': appointments})

@staff_member_required
def approve_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'approved'
    appointment.save()
    return redirect('admin_panel')

@staff_member_required
def reject_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = 'rejected'
    appointment.save()
    return redirect('admin_panel')