from django.contrib import admin

# Register your models here.

from .models import eurhkd, usdhkd, gbphkd, markup, synctable, dictionary

class eurhkdAdmin(admin.ModelAdmin):
    class Meta:
        model = eurhkd
    list_display = ["__unicode__","eurhkd_dates","api_works"]
    #verbose_name = "Currency - EUR to HKD"

class usdhkdAdmin(admin.ModelAdmin):
    class Meta:
        model = usdhkd
    list_display = ["__unicode__","usdhkd_dates","api_works"]

class gbphkdAdmin(admin.ModelAdmin):
    class Meta:
        model = gbphkd
    list_display = ["__unicode__","usdhkd_dates","api_works"]

class markupAdmin(admin.ModelAdmin):
    class Meta:
        model = markup
    list_display = ["__unicode__","marks"]

class syncdbAdmin(admin.ModelAdmin):
    class Meta:
        model = synctable
    list_display = ["Wine","Price","Year","Region","Format","Markup_Price","Markup_Percentiles","WS_Merchants",
                    "WS_Price","Recommend_Price","Sell","Margin","Negoce","Quantity","Type","Vendor"]

class dictionaryAdmin(admin.ModelAdmin):
    class Meta:
        model = dictionary
    list_display = ["Date","Filename","WineID","Vintage","Growth","TypeEnglish","WineEnglish", 
                    "CountryEnglish","RegionEnglish","VendorEnglish","TypeChinese","WineChinese",
                    "CountryChinese","RegionChinese","VendorChinese"]

admin.site.register(eurhkd,eurhkdAdmin)
admin.site.register(usdhkd,usdhkdAdmin)
admin.site.register(gbphkd,gbphkdAdmin)
admin.site.register(markup,markupAdmin)
admin.site.register(synctable,syncdbAdmin)
admin.site.register(dictionary,dictionaryAdmin)
