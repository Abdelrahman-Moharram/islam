from django.db import models
from project.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator

class Part(BaseModel):
    name        = models.CharField(max_length=40)
    number      = models.IntegerField(validators=[MaxValueValidator(30), MinValueValidator(1)])

    def __str__(self):
        return self.number
class Place(BaseModel):
    ar_name     = models.CharField(max_length=50)    
    en_name     = models.CharField(max_length=50)

class Surah(BaseModel):
    ar_name     = models.CharField(max_length=40)
    en_name     = models.CharField(max_length=40)
    # part        = models.ForeignKey(Part, null=True, on_delete=models.SET_NULL)
    start_page  = models.IntegerField(blank=True, null=True)
    end_page    = models.IntegerField(blank=True, null=True)
    place       = models.ForeignKey(Place, blank=True, null=True, on_delete=models.SET_NULL)
    order       = models.IntegerField(validators=[MinValueValidator(1)])
    ayat_count  = models.IntegerField(validators=[MinValueValidator(1)])
    number      = models.IntegerField(validators=[MinValueValidator(1)], unique=True)
    # @property
    # def ayat_count(self):
    #     return Aya.objects.filter(surah=self).count()
    
    class Meta:
        db_table = 'Surah'
class Aya(BaseModel):
    number      = models.IntegerField()
    text        = models.TextField()
    surah       = models.ForeignKey(Surah, null=True, on_delete=models.SET_NULL)

    
    class Meta:
        db_table = 'Ayat'

class Reader(BaseModel):
    def imagesave(instance,filename):
        extension = filename.split(".")[-1]
        return "readers/%s.%s"%(instance.id, extension)
    
    name        = models.CharField(max_length=255)
    image       = models.FileField(upload_to=imagesave, max_length=100)

class Aya_Audio(BaseModel):
    def imagesave(instance,filename):
        extension = filename.split(".")[-1]
        return "ayat/%s.%s"%(instance.id, extension)
    
    aya         = models.ForeignKey(Aya, null=True, on_delete=models.SET_NULL)
    audio       = models.FileField(upload_to=imagesave, max_length=100)