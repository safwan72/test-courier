from django.shortcuts import render
from . import models,forms
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse,reverse_lazy
from django.contrib import messages
import uuid
from django.views.generic import  TemplateView,UpdateView,CreateView,DetailView,DeleteView,ListView
# Create your views here.
class HomeView(TemplateView):
     template_name = "home.html"
     
     
     
def signupview(request):
    form=forms.MerchantRegForm()
    if request.method=='POST':
        form=forms.MerchantRegForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_merchant=True
            user.save()
            merchant=models.Merchant(user=user)
            merchant.invoice_id=str(uuid.uuid4())[:10]
            merchant.save()
            messages.success(request,'Account Created Successfully')
            return HttpResponseRedirect(reverse('App_Login:home'))
    return render(request,'App_Login/Signup.html',context={'form':form,'title':'Signup as a Merchant'})





def login_view(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('App_Login:home'))
            messages.success(request,'Logged in Successfully')
        else:
            messages.warning(request,'Log In Failed. Check Proper Inputs')
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request,'App_Login/Login.html',context={'title':'Login Page','form':form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:home'))

def merchant_profile_change(request):
    user=request.user
    profile=models.Merchant.objects.get(user=user)
    form=forms.MerchantChangeForm(instance=profile)
    if request.method=='POST':
        form=forms.MerchantChangeForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Updated Successfully')
            # form=forms.MerchantRegForm(instance=profile)
            return HttpResponseRedirect(reverse('App_Login:profile_update'))
    
    return render(request,'App_Login/ProfileChange.html',context={'form':form})
