from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory 
from .filters import OrderFilter

# Create your views here.
def home(request):
    orders = Orders.objects.all()
    customers = Customer.objects.all()   
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status= 'Pending').count()


    context = {'orders':orders,'customers':customers,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context)

def products(request):
   products  = Product.objects.all()

   return render(request,'accounts/products.html',{'products':products})

def customer(request,pk):
   customer = Customer.objects.get(id=pk)
   orders = customer.orders_set.all()
   order_count = orders.count()

   myfilter = OrderFilter(request.GET,queryset=orders)
   orders = myfilter.qs

   context = {
      'customer':customer,
      'orders': orders,
      'order_count': order_count,
      'myfilter' : myfilter
   }
   return render(request,'accounts/customer.html',context)

def createOrder(request,pk):
   OrderFormSet = inlineformset_factory(Customer,Orders,fields=('product','status'), extra=10)
   customer = Customer.objects.get(id=pk)
   formset = OrderFormSet(queryset=Orders.objects.none(), instance=customer )
   # form = OrderForm(initial={'customer':customer})
   if request.method == 'POST':
      #print('Printing POST:',request.POST)
      formset = OrderFormSet(request.POST,instance=customer )
      if formset.is_valid():
         formset.save()
         return redirect('/')

   context = {
         'formset':formset
   }
   return render(request,'accounts/order_form.html',context)

def updateOrder(request,pk):
   order =Orders.objects.get(id=pk)
   form = OrderForm(instance=order)

   if request.method == 'POST':
      #print('Printing POST:',request.POST)
      form = OrderForm(request.POST,instance=order)
      if form.is_valid():
         form.save()
         return redirect('/')

   context = {
      'form':form
   }
   return render(request,'accounts/order_form.html',context)

def deleteOrder(request, pk):
   order = Orders.objects.get(id=pk)

   if request.method == 'POST':
      order.delete()
      
      return redirect('/')

   context ={
      'item':order
   }
   return render(request,'accounts/delete.html',context)