from django.db import models

# Create your models here.

from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=255)  # varchar 类型的名字
    timestamp = models.DateTimeField(auto_now_add=True)  # 时间字段
    number = models.IntegerField()  # 数字字段
    text = models.TextField()  # 字符串文本字段


