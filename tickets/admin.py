from django.contrib import admin
from .models import Guest,Movie,Reservation, post
# Register your models here.
admin.site.register(Guest)
admin.site.register(Movie)
admin.site.register(Reservation)
admin.site.register(post)