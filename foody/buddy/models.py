from django.db import models

class Books(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    stock = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return "{'title':'" , self.title, "','isbn':'", self.isbn, "','stock':'",self.stock, "'}"