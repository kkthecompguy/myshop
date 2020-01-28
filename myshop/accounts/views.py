from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .filters import OrderFilter
from .forms import OrderForm, UserAuthForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@unauthenticated_user
def registerPage(request):

  form = UserAuthForm()
  if request.method == 'POST':
    form = UserAuthForm(request.POST)
    if form.is_valid():
      user = form.save()
      return redirect('login')
    else:
      messages.info(request, 'The two passwords did not match')

  context = {
    'form': form
  }

  return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        return redirect('home')
      else:
        messages.info(request, 'Invalid credentials')

  context = {}

  return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutPage(request):
  logout(request)
  return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
  customers = Customer.objects.all().order_by('-id')
  orders = Order.objects.all().order_by('-created_at')
  total_orders = orders.count()
  delivered = orders.filter(status='Delivered').count()
  pending = orders.filter(status='Pending').count()

  context = {
    'customers': customers,
    'orders': orders,
    'total_orders': total_orders,
    'delivered': delivered,
    'pending': pending
  }

  return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
  products = Product.objects.all()

  context = {
    'products': products
  }

  return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
  customer = Customer.objects.get(id=pk)
  orders = customer.order_set.all()
  total_orders = orders.count()

  myFilter = OrderFilter(request.GET, queryset=orders)
  orders = myFilter.qs

  context = {
    'customer': customer,
    'orders': orders,
    'total_orders': total_orders,
    'myFilter': myFilter
  }

  return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
  orders = request.user.customer.order_set.all().order_by('-created_at')
  total_orders = orders.count()
  delivered = orders.filter(status='Delivered').count()
  pending = orders.filter(status='Pending').count()

  context = {
    'orders': orders,
    'total_orders': total_orders,
    'delivered': delivered,
    'pending': pending
  }
  return render(request, 'accounts/users.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
  customer = request.user.customer
  form = CustomerForm(instance=customer)

  if request.method == 'POST':
    form = CustomerForm(request.POST, request.FILES, instance=customer)
    if form.is_valid():
      form.save()

  context = {
    'form': form
  }

  return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
  OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
  customer = Customer.objects.get(id=pk)
  #form = OrderForm(initial={'customer': customer})
  formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)

  if request.method == 'POST':
    formset = OrderFormSet(request.POST, instance=customer)
    #form = OrderForm(request.POST)
    if formset.is_valid():
      formset.save()
      return redirect('/')
  
  context = {
    'formset': formset,
    'title': 'Create a new order (s)'
  }

  return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
  order = Order.objects.get(id=pk)
  form = OrderForm(instance=order)

  if request.method == 'POST':
    form = OrderForm(request.POST, instance=order)
    if form.is_valid():
      form.save()
      return redirect('/')

  context = {
    'form': form,
    'title': 'Update Order'
  }
  
  return render(request, 'accounts/update_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
  order = Order.objects.get(id=pk)


  context = {
    'item': order
  }

  if request.method == 'POST':
    order.delete()
    return redirect('/')
  
  return render(request, 'accounts/delete.html', context)