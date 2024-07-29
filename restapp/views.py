from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.views import View
from django.urls import path
import base64
from io import BytesIO
from PIL import Image
from django.urls import reverse
import io
import os
from django.conf import settings
from django.http import JsonResponse
from .models import Cargo
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import requests

class LoginMixin(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth') 
    redirect_field_name = 'next'

class StartPageView(View):
    def get(self, request: HttpRequest):
        user = request.user
        context = {'user': user}
        return render(request, 'startpage.html', context)
    
class PriemkaView(LoginMixin):
    def get(self, request: HttpRequest):
        return render(request, 'priemka.html')
    
    def post(self, request: HttpRequest):
        if 'photo1' in request.FILES and 'photo2' in request.FILES:
            photo1 = request.FILES['photo1']
            photo2 = request.FILES['photo2']
            transport_type = request.POST.get('transport_type')

            print(f'photo1 {photo1} \nи photo2 {photo2} получены \n и transport_type {transport_type} получены')

            buffered1 = BytesIO()
            buffered2 = BytesIO()

            for chunk in photo1.chunks():
                buffered1.write(chunk)
            for chunk in photo2.chunks():
                buffered2.write(chunk)

            original_image_content1 = base64.b64encode(buffered1.getvalue()).decode('utf-8')
            original_image_content2 = base64.b64encode(buffered2.getvalue()).decode('utf-8')

            request.session['photo1'] = original_image_content1
            request.session['car_number_photo'] = original_image_content2
            request.session['transport_type'] = transport_type

            return HttpResponseRedirect(reverse('pre_process'))

        return render(request, 'priemka.html')


class PreProcessView(LoginMixin):
    def get(self, request: HttpRequest):
        photo1 = request.session.get('photo1')
        car_number_photo = request.session.get('car_number_photo')

        if not photo1 or not car_number_photo:
            return redirect('priemka')

        context = {
            'photo1': photo1,
            'car_number_photo': car_number_photo,
        }
        return render(request, 'pre_process.html', context)
    
    def post(self, request: HttpRequest):
        car_number_photo = request.session.get('car_number_photo')


        decoded_car_image = base64.b64decode(car_number_photo)
        buffer = io.BytesIO(decoded_car_image)
        # image_car = Image.open(io.BytesIO(decoded_car_image))

        files = {
            "base64Image": car_number_photo
            }


        if car_number_photo:
            response = requests.post('https://70c2-95-54-230-29.ngrok-free.app/predict_plate_text', json=files)
            if response.status_code == 200:
                car_number = response.text 
                print(car_number)
                request.session['car_number'] = car_number
                return HttpResponseRedirect(reverse('savedata'))
            else:
                print('mistake')
                request.session['car_number'] = 'Не удалось обработать фотографию'
                return HttpResponseRedirect(reverse('savedata'))
        else:
            return render(request, 'pre_process.html', {'error': 'нет фото в сессии'})


class SaveDataView(LoginMixin):
    def get(self, request: HttpRequest):
        # photo1 = request.session.get('photo1')
        # photo2 = request.session.get('photo2')
        transport_type = request.session.get('transport_type')
        car_number = request.session.get('car_number')

        # decoded_image = base64.b64decode(photo2)
        # image = Image.open(io.BytesIO(decoded_image))

        if transport_type == 'car':
            transport_type = 'Машина'
        elif transport_type == 'train':
            transport_type = 'Поезд'
        elif transport_type == 'ship':
            transport_type = 'Корабль'
        else:
            transport_type = 'Неизвестно'

        context = {
            'transport_type': transport_type,
            'car_number': car_number,
        }

        return render(request, 'savedata.html', context)
    

class ReportView(LoginMixin):
    def get(self, request: HttpRequest):
        cargos = Cargo.objects.all()

    # Получение фильтров из GET-запроса
        supplier = request.GET.get('supplier', '')
        print(supplier)
        if supplier:
            print('я получил')
            cargos = cargos.filter(supplier__startswith=supplier)

        application_number = request.GET.get('application_number', '')
        if application_number:
            cargos = cargos.filter(application_number__startswith=application_number)

        recipient = request.GET.get('recipient', '')
        if recipient:
            cargos = cargos.filter(recipient__startswith=recipient)

        cargo_description = request.GET.get('cargo_description', '')
        if cargo_description:
            cargos = cargos.filter(cargo_description__startswith=cargo_description)

        cargo_weight = request.GET.get('cargo_weight', '')
        if cargo_weight:
            cargos = cargos.filter(cargo_weight__startswith=cargo_weight)

        contract_number = request.GET.get('contract_number', '')
        if contract_number:
            cargos = cargos.filter(contract_number__startswith=contract_number)

        delivery_date = request.GET.get('delivery_date', '')
        if delivery_date:
            cargos = cargos.filter(delivery_date__startswith=delivery_date)

        vehicle_type = request.GET.get('vehicle_type', '')
        if vehicle_type:
            cargos = cargos.filter(vehicle_type__startswith=vehicle_type)

        vehicle_number = request.GET.get('vehicle_number', '')
        if vehicle_number:
            cargos = cargos.filter(vehicle_number__startswith=vehicle_number)

        shipment_date = request.GET.get('shipment_date', '')
        if shipment_date:
            cargos = cargos.filter(shipment_date__startswith=shipment_date)

        arrival_date = request.GET.get('arrival_date', '')
        if arrival_date:
            cargos = cargos.filter(arrival_date__startswith=arrival_date)

        paginator = Paginator(cargos, 100) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'report.html', {'page_obj': page_obj})
    
def report(request):
    cargos = Cargo.objects.all()

    # Получение фильтров из GET-запроса
    supplier = request.GET.get('supplier', '')
    print(supplier)
    if supplier:
        print('я получил')
        cargos = cargos.filter(supplier__startswith=supplier)

    application_number = request.GET.get('application_number', '')
    if application_number:
        cargos = cargos.filter(application_number__startswith=application_number)

    recipient = request.GET.get('recipient', '')
    if recipient:
        cargos = cargos.filter(recipient__startswith=recipient)

    cargo_description = request.GET.get('cargo_description', '')
    if cargo_description:
        cargos = cargos.filter(cargo_description__startswith=cargo_description)

    cargo_weight = request.GET.get('cargo_weight', '')
    if cargo_weight:
        cargos = cargos.filter(cargo_weight__startswith=cargo_weight)

    contract_number = request.GET.get('contract_number', '')
    if contract_number:
        cargos = cargos.filter(contract_number__startswith=contract_number)

    delivery_date = request.GET.get('delivery_date', '')
    if delivery_date:
        cargos = cargos.filter(delivery_date__startswith=delivery_date)

    vehicle_type = request.GET.get('vehicle_type', '')
    if vehicle_type:
        cargos = cargos.filter(vehicle_type__startswith=vehicle_type)

    vehicle_number = request.GET.get('vehicle_number', '')
    if vehicle_number:
        cargos = cargos.filter(vehicle_number__startswith=vehicle_number)

    shipment_date = request.GET.get('shipment_date', '')
    if shipment_date:
        cargos = cargos.filter(shipment_date__startswith=shipment_date)

    arrival_date = request.GET.get('arrival_date', '')
    if arrival_date:
        cargos = cargos.filter(arrival_date__startswith=arrival_date)

    paginator = Paginator(cargos, 100) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'report.html', {'page_obj': page_obj})

def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Успешный вход для пользователя:", username)
            login(request, user)
            print(request.user.is_authenticated)
            print(request.user)
            return redirect('startpage')
        else:
            error_message = "Неправильный пароль или логин"
            return render(request, 'auth.html', {'error_message': error_message})

    return render(request, 'auth.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth'))