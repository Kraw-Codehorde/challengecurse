from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    search_fields = ['name', 'description']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
