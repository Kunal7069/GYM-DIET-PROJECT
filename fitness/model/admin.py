from django.contrib import admin


from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display=('name','rollno')
admin.site.register(Person,PersonAdmin)
