from django.db import models


class Person(models.Model):
    color = models.ForeignKey('Color', on_delete = models.CASCADE,null=True, blank=True, related_name='color')
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField(max_length=254, unique=True)
   
class Color(models.Model):
    color_name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.color_name
     