from django.contrib import admin
from .models import negoces, manual, negoces2
# Register your models here.

class negocesAdmin(admin.ModelAdmin):
    class Meta:
        model = negoces
    list_display = ["Wine","Year","Region","Format","Negoce_Name","Price","Markup_Percentiles","Markup_Price",
                    "WS_Merchants","WS_Price","Recommend_Price","Margin","Sell","Date","Quantity","Type","Vendor"]

class negoces2Admin(admin.ModelAdmin):
    class Meta:
        model = negoces2
    list_display = ["WineID","Wine","WineChinese","Year","RegionEnglish","RegionChinese","Format","Negoce_Name","Price","Markup_Percentiles","Markup_Price",
                    "WS_Merchants","WS_Price","Recommend_Price","Margin","Sell","Date","Quantity","TypeEnglish","TypeChinese","VendorEnglish",
                    "VendorChinese","Rating","Growth","CountryEnglish","CountryChinese","CheapestPercent"]

class manualAdmin(admin.ModelAdmin):
    class Meta:
        model = manual
    list_display = ["Wine","Price","Year","Region","Format","Negoce","MarkupPrice","MarkupPercentile","Quantity"]

admin.site.register(negoces,negocesAdmin)
admin.site.register(negoces2,negoces2Admin)
admin.site.register(manual,manualAdmin)
