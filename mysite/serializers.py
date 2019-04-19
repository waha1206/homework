from django.conf import settings
from rest_framework import serializers
from mysite.models import Profit, Music, MyoSupplier, MaterialLevelThree, MaterialLevelTwo, MaterialLevelOne


class ProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profit
        fields = '__all__'
        #fields = ('id', 'song', 'singer', 'last_modify_date', 'created')

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        # fields = '__all__'
        fields = ('id', 'song', 'singer', 'last_modify_date', 'created')

class MyoSupplierSerializerDT(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)
    class Meta:
        model = MyoSupplier
        fields = '__all__'
        #fields = ('id', 'create_time', 'name', 'company_tax_id', 'contact_sales', 'contact_sales_phone', 'contact_sales_mob', 'address')

class MyoSupplierSerializerEx(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)
    class Meta:
        model = MyoSupplier
        fields = '__all__'
        #fields = ('create_time', 'name', 'company_tax_id', 'contact_sales', 'contact_sales_phone', 'contact_sales_mob', 'email', 'address')
        
class MaterialLevelOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialLevelOne
        fields = '__all__'
        
class MaterialLevelTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialLevelTwo
        fields = '__all__'
        
class MaterialLevelThreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialLevelThree
        fields = '__all__'
        
        