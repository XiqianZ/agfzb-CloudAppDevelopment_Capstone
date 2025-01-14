from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.






# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
    
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'dealer_id', 'type', 'year']
    list_display = ('name', 'dealer_id', 'type', 'year')
    search_fields = ['name', 'dealer_id', 'type', 'year']
    
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    fields = ['name', 'description']
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
    
# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)