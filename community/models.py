from django.db import models
from django.conf import settings
import os


class MyUser(models.Model):
    ID = models.EmailField(primary_key=True)
    PassWords = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    SN = models.CharField(max_length=20)
    Identifier = models.CharField(max_length=20)
    Grade = models.CharField(max_length=20, null=True)
    tutor = models.ForeignKey('self', null= True, default = None,on_delete=models.SET_NULL)

    def __str__(self):
        return self.Name+"/"+self.ID

class Board(models.Model):
    b_purpose = models.CharField(max_length=200,unique=True)
    identifier = models.AutoField(primary_key=True)
    
    def __str__(self):
        return self.b_purpose

class BoardCategory(models.Model):
    c_name = models.CharField(max_length=200, unique=True, default="a")
    refer = models.ForeignKey(Board, to_field='identifier', db_column='refer', null = False, blank=False,on_delete = models.CASCADE)
    identifier = models.AutoField(primary_key=True)

    def __str__(self):
        return self.c_name

class BoardCon(models.Model):
    m_title = models.CharField(max_length=200)
    m_WriterID = models.ForeignKey(MyUser,null = False, blank=False,on_delete = models.CASCADE)
    m_WriterName = models.CharField(max_length=30)
    m_create_date = models.DateTimeField('date created')
    m_update_date = models.DateTimeField('date updated')
    m_content = models.TextField()
    refer = models.ForeignKey(BoardCategory,null = False, blank=False,on_delete = models.CASCADE)
    identifier = models.AutoField(primary_key=True)
    file_path = models.FileField(upload_to = 'files/%Y/%m/%d', blank=True, null=True)
    file_desc = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.m_title
