from django.db import models
from App_Login.models import  User,Merchant

# Create your models here.

class Location(models.Model):
    location=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural='Location'
        db_table = 'Location'
    
    def __str__(self):
        return self.location    



class Parcel(models.Model):
    TYPE = (
        ('F', 'Fragile'),
        ('L', 'Liquid'),
    )
    parcel_weight=models.IntegerField(default=0)
    parcel_type=models.CharField(max_length=1,choices=TYPE)
    parcel_cost=models.IntegerField(default=0)
    parcel_cod_charge=models.IntegerField(default=0)
    parcel_return_charge=models.IntegerField(default=0)
    parcel_deliver_to=models.ForeignKey(Location,on_delete=models.CASCADE,related_name='deliver_to')
    added_for_delivery=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='Parcel'
        db_table = 'Parcel'

    
    
    

class Order(models.Model):
    orderer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_orderer')
    merchant=models.ForeignKey(Merchant,on_delete=models.CASCADE,related_name='merchant')
    parcel=models.ForeignKey(Parcel,on_delete=models.CASCADE,related_name='parcel')
    merchant_invoice_id=models.CharField(max_length=10)
    order_id=models.CharField(unique=True,max_length=10)
    ordered=models.BooleanField(default=False)   
    class Meta:
        verbose_name_plural='Order Table'
        db_table = 'Order Table'

    def __str__(self):
        return self.orderer.username+'   Ordered   '+ self.merchant.user.username +" "+self.order_id