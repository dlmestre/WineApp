# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode
from datetime import datetime
# Create your models here.

class negoces(models.Model):
    wine = models.CharField(max_length=50,blank=False,verbose_name="Wine")
    year = models.CharField(max_length=10,blank=False,verbose_name="Vintage")
    region = models.CharField(max_length=50,blank=False,verbose_name="Region")
    format = models.CharField(max_length=10,blank=False,verbose_name="Format")
    negoce_name = models.CharField(max_length=200,blank=False,verbose_name="Negoce")
    price = models.CharField(max_length=10,blank=False,verbose_name="Cost")
    markup_percentile = models.CharField(max_length=10,blank=False,verbose_name="Markup %")
    markup_price = models.CharField(max_length=10,blank=False,verbose_name="Markup Price")
    ws_merchants = models.CharField(max_length=200,blank=False,verbose_name="WS Merchant")
    ws_price = models.CharField(max_length=10,blank=False,verbose_name="Lowest WS Price")
    recommended_price = models.CharField(max_length=10,blank=False,verbose_name="Recommended Selling Price")
    margin = models.CharField(max_length=10,blank=False,verbose_name="Margin")
    sell = models.CharField(max_length=5,blank=False,verbose_name="Sell")
    date = models.CharField(max_length=50,blank=False,verbose_name="Date")    
    quantity = models.CharField(max_length=5,blank=False,verbose_name="Qty")
    a_type = models.CharField(max_length=200,verbose_name="Type",default="N/A")
    vendor = models.CharField(max_length=200,verbose_name="Vendor",default="N/A")

    class Meta:
        verbose_name = "Negoce"
        verbose_name_plural = verbose_name
    def Wine(self):
        return smart_unicode(self.wine)
    def Price(self):
        return smart_unicode(self.price)
    def Date(self):
        return smart_unicode(self.date)
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
    def Negoce_Name(self):
        return smart_unicode(self.negoce_name)
    def Recommend_Price(self):
        return smart_unicode(self.recommended_price)
    def Sell(self):
        return smart_unicode(self.sell)
    def Margin(self):
        return smart_unicode(self.margin)
    def Quantity(self):
        return smart_unicode(self.quantity)
    def Type(self):
        return smart_unicode(self.a_type)
    def Vendor(self):
        return smart_unicode(self.vendor)

class negoces2(models.Model):
    wineid = models.CharField(max_length=80,blank=False,verbose_name="Wine ID")
    wine = models.CharField(max_length=50,blank=False,verbose_name="Wine (English)")
    wine_chinese = models.CharField(max_length=200,default="",verbose_name="Wine (Chinese)")
    year = models.CharField(max_length=10,blank=False,verbose_name="Vintage")
    region_english = models.CharField(max_length=50,blank=False,verbose_name="Region English")
    region_chinese = models.CharField(max_length=50,blank=False,verbose_name="Region Chinese")
    a_format = models.CharField(max_length=10,blank=False,verbose_name="Format")
    negoce_name = models.CharField(max_length=200,blank=False,verbose_name="Negoce")
    price = models.CharField(max_length=10,blank=False,verbose_name="Cost")
    markup_percentile = models.CharField(max_length=10,blank=False,verbose_name="Markup %")
    markup_price = models.CharField(max_length=10,blank=False,verbose_name="Markup Price")
    ws_merchants = models.CharField(max_length=200,blank=False,verbose_name="WS Merchant")
    ws_price = models.CharField(max_length=10,blank=False,verbose_name="Lowest WS Price")
    recommended_price = models.CharField(max_length=10,blank=False,verbose_name="Recommended Selling Price")
    margin = models.CharField(max_length=10,blank=False,verbose_name="Margin")
    sell = models.CharField(max_length=5,blank=False,verbose_name="Sell")
    date = models.CharField(max_length=50,blank=False,verbose_name="Date")    
    quantity = models.CharField(max_length=5,blank=False,verbose_name="Qty")
    a_type_english = models.CharField(max_length=180,verbose_name="Type English",default="N/A")
    a_type_chinese = models.CharField(max_length=180,verbose_name="Type Chinese",default="N/A")
    vendor_english = models.CharField(max_length=180,verbose_name="Vendor English",default="N/A")
    vendor_chinese = models.CharField(max_length=180,verbose_name="Vendor Chinese",default="N/A")
    rating = models.CharField(max_length=200,verbose_name="Rating",default="N/A")
    growth = models.CharField(max_length=200,verbose_name="Growth",default="N/A")
    country_english = models.CharField(max_length=180,verbose_name="Country English",default="N/A")
    country_chinese = models.CharField(max_length=180,verbose_name="Country Chinese",default="N/A")
    cheapest_percent = models.CharField(max_length=10,verbose_name="Cheapest Percent",default="N/A")

    class Meta:
        verbose_name = "Negoce 2"
        verbose_name_plural = verbose_name
    def WineID(self):
        return smart_unicode(self.wineid)
    def Wine(self):
        return smart_unicode(self.wine)
    Wine.short_description = "Wine (English)"
    def WineChinese(self):
        return u"%s" %(self.wine_chinese)
    WineChinese.short_description = "Wine (Chinese)"
    def Price(self):
        return smart_unicode(self.price)
    def Date(self):
        return smart_unicode(self.date)
    def Year(self):
        return smart_unicode(self.year)
    def RegionEnglish(self):
        return smart_unicode(self.region_english)
    RegionEnglish.short_description = "Region (English)"
    def RegionChinese(self):
        return u'%s' %(self.region_chinese)
    RegionChinese.short_description = "Region (Chinese)"
    def Format(self):
        return smart_unicode(self.a_format)
    def Markup_Price(self):
        return smart_unicode(self.markup_price)
    def Markup_Percentiles(self):
        return smart_unicode(self.markup_percentile)
    def WS_Merchants(self):
        return smart_unicode(self.ws_merchants)
    def WS_Price(self):
        return smart_unicode(self.ws_price)
    def Negoce_Name(self):
        return smart_unicode(self.negoce_name)
    def Recommend_Price(self):
        return smart_unicode(self.recommended_price)
    def Sell(self):
        return smart_unicode(self.sell)
    def Margin(self):
        return smart_unicode(self.margin)
    def Quantity(self):
        return smart_unicode(self.quantity)
    def TypeEnglish(self):
        return smart_unicode(self.a_type_english)
    def TypeChinese(self):
        return smart_unicode(self.a_type_chinese)
    def VendorEnglish(self):
        return smart_unicode(self.vendor_english)
    def VendorChinese(self):
        return smart_unicode(self.vendor_chinese)
    def Rating(self):
        return smart_unicode(self.rating)
    def Growth(self):
        return smart_unicode(self.growth)
    def CountryEnglish(self):
        return smart_unicode(self.country_english)
    def CountryChinese(self):
        return smart_unicode(self.country_chinese)
    def CheapestPercent(self):
        return smart_unicode(self.cheapest_percent)

class manual(models.Model):
    wine = models.CharField(max_length=50,blank=False,verbose_name="Wine")
    price = models.CharField(max_length=10,blank=False,verbose_name="Cost")
    year = models.CharField(max_length=10,blank=False,verbose_name="Vintage")
    region = models.CharField(max_length=50,blank=False,verbose_name="Region")
    format = models.CharField(max_length=10,blank=False,verbose_name="Format")
    negoce = models.CharField(max_length=200,blank=False,verbose_name="Negoce")
    markup_price = models.CharField(max_length=10,blank=False,verbose_name="Markup Price")
    markup_percentile = models.CharField(max_length=10,blank=False,verbose_name="Markup %")
    quantity = models.CharField(max_length=5,blank=False,verbose_name="Qty")

    class Meta:
        verbose_name = "Manual"
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
    def Negoce(self):
        return smart_unicode(self.negoce)
    def MarkupPrice(self):
        return smart_unicode(self.markup_price)
    def MarkupPercentile(self):
        return smart_unicode(self.markup_percentile)
    def Quantity(self):
        return smart_unicode(self.quantity)
