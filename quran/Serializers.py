from rest_framework import serializers 
from .models import (
    Surah,
    Place,
    Aya
)


class IncludedAr_NamePlaceSerial(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['ar_name']



class index_serializer(serializers.ModelSerializer):
    # place = IncludedAr_NamePlaceSerial()
    class Meta:
        model = Surah
        fields = ['id', 'ar_name', 'start_page', 'end_page', 'number', 'place']
    
    def to_representation(self, instance):
        rep = super(index_serializer, self).to_representation(instance)
        rep['place'] = instance.place.ar_name
        return rep


class surah_serializer(serializers.ModelSerializer):
    class Meta:
        model = Aya
        fields = ['id', 'text', 'number']