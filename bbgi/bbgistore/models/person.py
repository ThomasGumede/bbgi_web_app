from django.db import models
class Person(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    biography=models.TextField(blank=True)
    @property
    def full_name(self): return f'{self.first_name} {self.last_name}'
