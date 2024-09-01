from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Surah, Aya, Place
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .Serializers import index_serializer, surah_serializer
from .data import data
from django.db.models import Q

@api_view(['GET'])
@permission_classes((AllowAny,))
def index(request):
    return Response(data={'message':'working ...'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_index_surah(request):
    search = request.GET.get('search')
    if search:
        data = Surah.objects.filter(Q(ar_name__contains=search)|Q(en_name__contains=search)).order_by('number').only('id', 'ar_name', 'start_page', 'end_page', 'number', 'place')
    
    else:
        data = Surah.objects.all().order_by('number').only('id', 'ar_name', 'start_page', 'end_page', 'number', 'place')

    indexs_serial = index_serializer(data=data, many=True)

    if not indexs_serial.is_valid():
        pass
    return Response(
            {
                'indexes': indexs_serial.data
            },
            status=status.HTTP_200_OK
        )
    

@api_view(['GET'])
@permission_classes((AllowAny,))    
def get_surah_by_id(request, id):
    ayat    = Aya.objects.filter(surah__id=id).order_by('number').all().only('text', 'number')

    ayat_serial     = surah_serializer(data=ayat, many=True)

    if ayat_serial.is_valid():
        pass

    return Response(
        data={
            'surah':Surah.objects.filter(id=id).first().ar_name,
            'ayat': ayat_serial.data,
        }
    )

# @api_view(['GET'])
# @permission_classes((AllowAny,))    
# def search_surah_by_name(request, id):
#     ayat    = Aya.objects.filter(surah__id=id).order_by('number').all().only('text', 'number')

#     ayat_serial     = surah_serializer(data=ayat, many=True)

#     if ayat_serial.is_valid():
#         pass

#     return Response(
#         data={
#             'surah':Surah.objects.filter(id=id).first().ar_name,
#             'ayat': ayat_serial.data,
#         }
#     )

# @api_view(['GET'])
# @permission_classes((AllowAny,))
# def seed_data(request):
    print(data)
    surah_count = 1
    makkah_obj = Place.objects.get(id='ddf335dd-7144-4a48-a1a1-21f176f0519a')
    madinah_obj = Place.objects.get(id='437b8e02-a8f8-4d1c-be6d-5645de95f78a')
    for surah in data['chapters']:
        Surah.objects.create(
            ar_name=surah['name_arabic'],
            en_name=surah['name_complex'],
            start_page=surah['pages'][0],
            end_page=surah['pages'][-1],
            place= makkah_obj if surah['revelation_place'] == 'makkah' else madinah_obj,
            order=surah['revelation_order'],
            ayat_count=surah['verses_count'],
            number=surah_count
        )
        surah_count += 1

    for aya in data['verses']:
        surah_num, ayah_num = aya['verse_key'].split(':')
        Aya.objects.create(
            number = ayah_num,
            text = aya['text_indopak'].replace('‏', ''),
            surah = Surah.objects.get(number=surah_num),
        )

    return Response(data={'message':'Data Seeded Successfully!'}, status=status.HTTP_201_CREATED)