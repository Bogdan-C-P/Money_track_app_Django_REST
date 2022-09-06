
from re import search
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['title','ammount','user']
        
class MySerializer(serializers.Serializer):
    title =serializers.CharField(max_length=200)
    ammount = serializers.DecimalField(max_digits=8,decimal_places=2)

