from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout, authenticate,get_user_model
from django.http import JsonResponse
from .models import (Customer, Order, Service, Category)
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json



def submit_order(request):
    if request.user.is_authenticated:
        try:
            user = Customer.objects.get(username=request.user.username)
        except Customer.DoesNotExist:
            return render(request, '404.html') 

        if request.method == 'POST':

            service = request.POST.get('services')
            service_data = Service.objects.get(title=service)
            link = request.POST.get('link')
            quantity = int(request.POST.get('quantity'))
            price = Decimal(request.POST.get('price'))

            try:
                order = Order.objects.create(
                    customer=user,
                    service=service_data,
                    link=link,
                    status='Pending',
                    quantity=quantity,
                    charge=price
                )
                if user.funds >= price:
                    user.funds -= price
                    user.amount_spent += price
                    user.save()
                messages.success(request, 'Your order has been placed successfully.')
            except Exception as e:

                messages.error(request, 'An error occurred while processing your order.')

            return redirect('dashboard')
        return render(request, 'dashboard.html')
    else:
        return redirect('/')

@csrf_exempt
def get_guide_price(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        service_title = data.get('selectedValue')  
        service_data = Service.objects.get(title=service_title)
        price_per_1000 = service_data.price_per_1000
        guide_prompt = service_data.guide_prompt

        response_data = {
            'price_per_1000': price_per_1000,
            'guide_prompt': guide_prompt,
        }

        return JsonResponse(response_data)

@csrf_exempt
def get_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_title = data.get('category') 
        category = Category.objects.get(title=category_title)  
        services = Service.objects.filter(category=category).values('title') 

        return JsonResponse({'services': list(services)})

def add_funds(request):
    if request.user.is_authenticated:
        try:
            user = Customer.objects.get(username=request.user.username)
        except Customer.DoesNotExist:
            return render(request, '404.html')

        if request.method == "POST":
            try:
                amount = Decimal(request.POST.get('amount'))                
                if amount > 0:  # Check for positive value
                    user.funds += amount
                    user.save()
                    messages.success(request, "You added funds successfully!")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Please enter a valid amount (positive number).")
            except ValueError:  # Handle non-numeric input
                messages.error(request, "Please enter a valid amount (numbers only).")

        context = {
            "user": user,
        }
        return render(request, 'checkout.html', context)
    else:
        return redirect('/')

def change_custom_info(request):
    if request.user.is_authenticated:
        try:
            user = Customer.objects.get(username=request.user.username)
        except Customer.DoesNotExist:
            return render(request, '404.html') 
        if request.method == "POST":
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.country = request.POST.get('country')
            user.city = request.POST.get('city')

            user.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect('profile')
        context = {
            "user": user,
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('/')

def change_password(request):
    if request.user.is_authenticated:
        user = Customer.objects.get(username=request.user.username)
        if request.method == "POST":
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if check_password(current_password, user.password):
                if new_password == confirm_password:
                    user.set_password(new_password) 
                    user.save()
                    messages.success(request, "Your password has been updated successfully")
                    return redirect('profile')
                else:
                    messages.error(request, "Passwords don't match")
            else:
                messages.error(request, "Your old password is incorrect")
            return redirect('change_password') 
        context = {"user": user,}
        return render(request, 'change_password.html', context)
    else:
        return redirect('/')
        
def profile(request):
    if request.user.is_authenticated:
        user = Customer.objects.get(username=request.user.username)
        services = Service.objects.all()
        orders = Order.objects.filter(customer=user)
        context = {
            "services": services,
            "user": user,
            "orders": orders,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def dashboard(request):
    if request.user.is_authenticated:
        user = Customer.objects.get(username=request.user.username)
        services = Service.objects.all()
        category = Order.objects.all()
        context = {
            "services": services,
            "user": user,
            "category": category,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def orders(request):
    if request.user.is_authenticated:
        user = Customer.objects.get(username=request.user.username)
        orders_list = Order.objects.filter(customer=user)
        paginator = Paginator(orders_list, 10)  # Show 10 orders per page
        page_num = request.GET.get('page')
        try:
            orders = paginator.page(page_num)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)


        context = {
            "user": user,
            "orders": orders,
            "page_range": paginator.page_range,
            "current_page": orders.number,
        }

        return render(request, 'orders.html', context)
    else:
        return redirect('/')

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created! You are now logged in.')
                return redirect('/')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            form = UserRegistrationForm()
            return render(request, 'signup.html', {'form': form, 'title': 'Register Here'})
    else:
        return redirect('/dashboard')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')  # Redirect to dashboard if logged in
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(username=username)
            if customer.authenticate_user(password):
                login(request, customer)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')

            else:
                # Authentication failed
                messages.error(request, 'Invalid username or password')
                return render(request, 'hello.html', {'error_message': 'Invalid username or password'})
        
        except Customer.DoesNotExist:
            # Username not found
            messages.error(request, 'Invalid username or password')
            return render(request, 'hello.html', {'error_message': 'Invalid username or password'})
    
    return render(request, 'hello.html')

@login_required(login_url="hello")
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/')

