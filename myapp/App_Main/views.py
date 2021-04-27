from django.shortcuts import render
from . import models,forms
from App_Login.models import Merchant
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.urls import reverse,reverse_lazy
import uuid

# Create your views here.
def order(request):
    orders=models.Order.objects.filter(orderer=request.user,ordered=True)
    return render(request,'App_Main/Orders.html',context={'orders':orders,'title':'Your Orders'})

def insidedhaka(weight):
    if weight >= 0.5 and weight <= 2:
        cost=60 
    elif weight== 3:
        cost=70 
    elif weight== 4:
        cost=80 
    elif weight== 5:
        cost=90 
    else:
        cost=0
    cod_charge=cost*0
    return_charge=cost*0
    return cost,cod_charge,return_charge

def dhaka(weight):
    if weight >= 0.5 and weight <= 2:
        cost=110 
    elif weight== 3:
        cost=130 
    elif weight== 4:
        cost=150 
    elif weight== 5:
        cost=170
    else:
        cost=0
    cod_charge=cost*0.1
    return_charge=cost*0.5
    return cost,cod_charge,return_charge

def outsidedhaka(weight):
    if weight >= 0.5 and weight <= 2:
        cost=130 
    elif weight== 3:
        cost=150 
    elif weight== 4:
        cost=170 
    elif weight== 5:
        cost=190
    else:
        cost=0
    cod_charge=cost*0.1
    return_charge=cost*0.5
    return cost,cod_charge,return_charge



def create_parcel(request):
    form=forms.ParcelForm()
    parcels=models.Parcel.objects.filter(added_for_delivery=False)
    cod_charge=0
    return_charge=0
    cost=0
    if request.method=='POST':
        form=forms.ParcelForm(request.POST)
        if form.is_valid():
            parcel_weight=form.cleaned_data.get('parcel_weight')
            print(parcel_weight)
            parcel_deliver_to=form.cleaned_data.get('parcel_deliver_to')
            parcel_deliver_to=str(parcel_deliver_to)
            parcel_weight=int(parcel_weight)
            form=form.save(commit=False)
            if parcel_deliver_to=='Inside Dhaka':
               cost,cod_charge,return_charge=insidedhaka(parcel_weight)
            elif parcel_deliver_to=='Dhaka':
                cost,cod_charge,return_charge=dhaka(parcel_weight)
            elif parcel_deliver_to=='Outside Dhaka':
                cost,cod_charge,return_charge=outsidedhaka(parcel_weight)
            form.parcel_cod_charge=cod_charge
            form.parcel_return_charge=return_charge
            form.parcel_cost=cost+cod_charge+return_charge
            form.save()
            messages.success(request,'Parcel Created Successfully')
            return HttpResponseRedirect(reverse('App_Main:parcel'))
    return render(request,'App_Main/CreateParcel.html',context={'form':form,'title':'Create a New Parcel','parcels':parcels})

def deliver_parcel(request,pk):
    form=forms.OrderForm()
    user=request.user
    parcels=models.Parcel.objects.filter(added_for_delivery=False,pk=pk)
    if request.method=='POST':
        form=forms.OrderForm(request.POST)
        if form.is_valid():
            merchant_invoice_id=form.cleaned_data.get('merchant_invoice_id')
            verify_merchant=Merchant.objects.filter(invoice_id=merchant_invoice_id)
            if verify_merchant.exists():
                print(verify_merchant)
                form=form.save(commit=False)
                if parcels.exists():
                    parcel=parcels[0]
                    parcel.added_for_delivery=True
                    parcel.save()
                    print(parcel.added_for_delivery)
                    form.parcel=parcel
                    print(parcel.added_for_delivery)
                if user.is_superuser:
                    form.orderer=user
                form.ordered=True
                form.order_id=str(uuid.uuid4())[:10]
                form.save()
                messages.success(request,'Parcel Created Successfully')
            else:
                messages.warning(request,'Unable To Verify Merchant. Please Check Merchants Invoice id')    
            return HttpResponseRedirect(reverse('App_Main:parcel'))
    return render(request,'App_Main/DeliverParcel.html',context={'form':form,'title':'Deliver This Parcel','parcels':parcels})



def merchant_orders(request):
    merchant=Merchant.objects.get(user=request.user)
    orders=models.Order.objects.filter(merchant=merchant,ordered=True)
    return render(request,'App_Main/MerchantOrders.html',context={'title':'My Orders','orders':orders})