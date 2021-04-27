from django import forms
from django.forms import ModelForm
from App_Login.models import Merchant
from . import models


class OrderForm(forms.ModelForm):
    query_list = Merchant.objects.all()
    merchant = forms.ModelChoiceField(
        queryset=query_list,
        label="Select Merchant:",
        required=True,
        to_field_name='user',
        empty_label="Select Merchant",
        widget=forms.Select(attrs={"class": "form-control mb-3"}),
    )
    merchant_invoice_id = forms.CharField(
        required=True,
        label='Enter The InVoice Id For your Merchant:',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Merchant InVoice Id to Confirm Order",
                "class": "form-control mb-3",
            }
        ),
    )

    class Meta:
        model = models.Order
        fields = (
            "merchant",
            "merchant_invoice_id",
        )


class ParcelForm(forms.ModelForm):
    TYPE = (
        ("F", "Fragile"),
        ("L", "Liquid"),
    )
    parcel_weight = forms.IntegerField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Your Parcels Weight(In Kg, 2,3,4,5)",
                "class": "form-control mb-3",
            }
        ),
    )
    parcel_type = forms.ChoiceField(
        required=True,
        choices=TYPE,
        widget=forms.Select(attrs={"class": "form-control mb-3"}),
    )
    parcel_deliver_to = forms.ModelChoiceField(
        queryset=models.Location.objects.all(),
        label="Select Delivery Place:",
        required=True,
        to_field_name='location',
        empty_label="Select Delivery Place",
        widget=forms.Select(attrs={"class": "form-control mb-3"}),
    )

    class Meta:
        model = models.Parcel
        exclude = ("added_for_delivery",'parcel_cost','parcel_cod_charge','parcel_return_charge',)
