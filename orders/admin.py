from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'total', 'date']
