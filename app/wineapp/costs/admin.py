from django.contrib import admin

# Register your models here.

from .models import costs,markup

class costsAdmin(admin.ModelAdmin):
    class Meta:
        model = costs
    list_display = ["Name","percentageValue","Type","Comments","Dates"]

class markupAdmin(admin.ModelAdmin):
    class Meta:
        model = markup
    list_display = ["Name","percentageValue","Comments","Dates"]

admin.site.register(costs,costsAdmin)
admin.site.register(markup,markupAdmin)
