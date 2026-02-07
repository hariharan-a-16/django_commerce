from django import forms
from .models import Address, Order

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
