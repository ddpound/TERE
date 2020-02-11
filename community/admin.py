from django.contrib import admin
from .models import MyUser
from .models import BoardCategory
from .models import BoardCon
from .models import Board

admin.site.register(MyUser)
admin.site.register(BoardCategory)
admin.site.register(BoardCon)
admin.site.register(Board)      
# Register your models here.
