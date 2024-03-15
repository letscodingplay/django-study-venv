from django.db import models

class Books(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    stock = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return "{'title':'" , self.title, "','isbn':'", self.isbn, "','stock':'",self.stock, "'}"
    
class License(models.Model):
    student_name = models.CharField(max_length = 100)
    score = models.IntegerField(default=0)
    student_birth = models.CharField(max_length = 8)
    student_id = models.CharField(max_length = 7)
    grade = models.CharField(max_length = 2, default=None, null=True)