from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Import both models here, clean and simple
from .models import Product, CustomUser

# --- HOME DASHBOARD (UPDATED TO FIX "0" COUNT) ---
def home(request):
    # 1. Fetch all products from the database
    products = Product.objects.all()
    
    # 2. Create a dictionary (context) to hold the data
    context = {
        'products': products
    }
    
    # 3. Send the data to the template
    return render(request, 'home.html', context)


# --- PRODUCT LIST ---
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# --- ADD PRODUCT ---
def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        Product.objects.create(
            name=name,
            price=price,
            description=description
        )
        return redirect('product_list')

    return render(request, 'add_product.html')


# --- EDIT PRODUCT ---
def edit_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        return redirect('product_list')

    return render(request, 'edit_product.html', {'product': product})


# --- DELETE PRODUCT ---
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product_list')


# --- USER REGISTRATION ---
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        gmail = request.POST.get('gmail')
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'passwords do not match'})
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        user = CustomUser.objects.create_user(
            username=username,
            name=name,
            gmail=gmail,
            password=password,
            phonenumber=phonenumber
        )
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')


# --- USER LOGIN ---
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'invalid username or password'})
    return render(request, 'login.html')


# --- USER LOGOUT ---
def logout_user(request):
    logout(request)
    return redirect('login')


# --- ABOUT PAGE ---
def about(request):
    return render(request, 'about.html')