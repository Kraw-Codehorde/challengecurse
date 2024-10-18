from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'total', 'date']
