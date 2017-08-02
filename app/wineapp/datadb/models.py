from django.db import models
from django.utils.encoding import smart_unicode
# Create your models here.
import datetime

class eurhkd(models.Model):
    value = models.CharField(max_length=25,blank=False)
    date = models.CharField(max_length=25,blank=False)
    works = models.CharField(max_length=25)
    class Meta:
        verbose_name = "Currency - EUR to HKD"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.value)
    def eurhkd_dates(self):
        return smart_unicode(self.date)
    def api_works(self):
        return smart_unicode(self.works)
    
class usdhkd(models.Model):
    value = models.CharField(max_length=25,blank=False)
    date = models.CharField(max_length=25,blank=False)
    works = models.CharField(max_length=25)
    class Meta:
        verbose_name = "Currency - USD to HKD"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.value)
    def usdhkd_dates(self):
        return smart_unicode(self.date)
    def api_works(self):
        return smart_unicode(self.works)

class gbphkd(models.Model):
    value = models.CharField(max_length=25,blank=False)
    date = models.CharField(max_length=25,blank=False)
    works = models.CharField(max_length=25)
    class Meta:
        verbose_name = "Currency - GBP to HKD"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return smart_unicode(self.value)
    def usdhkd_dates(self):
        return smart_unicode(self.date)
    def api_works(self):
        return smart_unicode(self.works)

class markup(models.Model):
    price = models.CharField(max_length=25,blank=False)
    mark = models.CharField(max_length=25,blank=False)
    def __unicode__(self):
        return smart_unicode(self.price)
    def marks(self):
        return smart_unicode(self.mark)

class synctable(models.Model):
    wine = models.CharField(max_length=50,blank=False,verbose_name="Wine")
    year = models.CharField(max_length=10,blank=False,verbose_name="Vintage")
    region = models.CharField(max_length=50,blank=False,verbose_name="Region")
    format = models.CharField(max_length=10,blank=False,verbose_name="Format")
    price = models.CharField(max_length=10,blank=False,verbose_name="Cost")
    markup_percentile = models.CharField(max_length=10,blank=False,verbose_name="Markup %")
    markup_price = models.CharField(max_length=10,blank=False,verbose_name="Markup Price")
    ws_merchants = models.CharField(max_length=200,blank=False,verbose_name="WS Merchant")
    ws_price = models.CharField(max_length=10,blank=False,verbose_name="Lowest WS Price")
    recommended_price = models.CharField(max_length=10,blank=False,verbose_name="Recommended Selling Price")
    margin = models.CharField(max_length=10,blank=False,verbose_name="Margin")
    sell = models.CharField(max_length=5,blank=False,verbose_name="Sell")
    negoce = models.CharField(max_length=200,blank=False,verbose_name="Negoce")
    quantity = models.CharField(max_length=10,verbose_name="Quantity",default="N/A")
    a_type = models.CharField(max_length=200,verbose_name="Type",default="N/A")
    vendor = models.CharField(max_length=200,verbose_name="Vendor",default="N/A")
    
    class Meta:
        verbose_name = "Sync Table"
        verbose_name_plural = verbose_name
    def Wine(self):
        return smart_unicode(self.wine)
    def Price(self):
        return smart_unicode(self.price)
    def Year(self):
        return smart_unicode(self.year)
    def Region(self):
        return smart_unicode(self.region)
    def Format(self):
        return smart_unicode(self.format)
    def Markup_Price(self):
        return smart_unicode(self.markup_price)
    def Markup_Percentiles(self):
        return smart_unicode(self.markup_percentile)
    def WS_Merchants(self):
        return smart_unicode(self.ws_merchants)
    def WS_Price(self):
        return smart_unicode(self.ws_price)
    def Recommend_Price(self):
        return smart_unicode(self.recommended_price)
    def Sell(self):
        return smart_unicode(self.sell)
    def Margin(self):
        return smart_unicode(self.margin)
    def Negoce(self):
        return smart_unicode(self.negoce)
    def Quantity(self):
        return smart_unicode(self.quantity)
    def Type(self):
        return smart_unicode(self.a_type)
    def Vendor(self):
        return smart_unicode(self.vendor)

class dictionary(models.Model):

    filename = models.CharField(max_length=200,blank=False,verbose_name="File name")
    uploadingdate = models.DateTimeField(auto_now=True)

    wineid = models.CharField(max_length=200,blank=False,verbose_name="Wine ID")
    rating = models.CharField(max_length=200,blank=True,verbose_name="Rating")
    vintage = models.CharField(max_length=20,blank=True,verbose_name="Vintage")
    growth = models.CharField(max_length=200,blank=True,verbose_name="Growth")

    typeenglish = models.CharField(max_length=200,blank=True,verbose_name="Type (English)")
    wineenglish = models.CharField(max_length=200,blank=True,verbose_name="Wine (English)")
    countryenglish = models.CharField(max_length=200,blank=True,verbose_name="Country (English)")
    regionenglish = models.CharField(max_length=200,blank=True,verbose_name="Region (English)")
    vendorenglish = models.CharField(max_length=200,blank=True,verbose_name="Vendor (English)")

    typechinese = models.CharField(max_length=200,blank=True,verbose_name="Type (Chinese)")
    winechinese = models.CharField(max_length=200,blank=True,verbose_name="Wine (Chinese)")
    countrychinese = models.CharField(max_length=200,blank=True,verbose_name="Country (Chinese)")
    regionchinese = models.CharField(max_length=200,blank=True,verbose_name="Region (Chinese)")
    vendorchinese = models.CharField(max_length=200,blank=True,verbose_name="Vendor (Chinese)")

    class Meta:
        verbose_name = "Dictionary Table"
        verbose_name_plural = verbose_name
    
    def Date(self):
        return smart_unicode(self.uploadingdate)
    def Filename(self):
        return smart_unicode(self.filename)
    def WineID(self):
        return smart_unicode(self.wineid)
    def Vintage(self):
        return smart_unicode(self.vintage)
    def Growth(self):
        return smart_unicode(self.growth)

    def TypeEnglish(self):
        return smart_unicode(self.typeenglish)
    def WineEnglish(self):
        return smart_unicode(self.wineenglish)
    def CountryEnglish(self):
        return smart_unicode(self.countryenglish)
    def RegionEnglish(self):
        return smart_unicode(self.regionenglish)
    def VendorEnglish(self):
        return smart_unicode(self.vendorenglish)

    def TypeChinese(self):
        return smart_unicode(self.typechinese)
    def WineChinese(self):
        return smart_unicode(self.winechinese)
    def CountryChinese(self):
        return smart_unicode(self.countrychinese)
    def RegionChinese(self):
        return smart_unicode(self.regionchinese)
    def VendorChinese(self):
        return smart_unicode(self.vendorchinese)
