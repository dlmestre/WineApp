from django.db import models
from django.utils.encoding import smart_unicode
# Create your models here.

class costs(models.Model):
    name = models.CharField(max_length=250,blank=False)
    value = models.CharField(max_length=25,blank=False)
    valuetype = models.CharField(max_length=6,blank=False)
    comments = models.CharField(max_length=250,blank=True)
    date = models.DateTimeField(auto_now=True,blank=True)
    class Meta:
        verbose_name = "Unit Costs"
        verbose_name_plural = verbose_name
    def Name(self):
        return smart_unicode(self.name)
    Name.short_description = "Title"
    def percentageValue(self):
        return smart_unicode(self.value)
    percentageValue.short_description = "Cost"
    def Type(self):
        return smart_unicode(self.valuetype)
    Type.short_description = "Value Type"
    def Comments(self):
        return smart_unicode(self.comments)
    Comments.short_description = "Comments"
    def Dates(self):
        return smart_unicode(self.date)
    Dates.short_description = "Date"

class markup(models.Model):
    name = models.CharField(max_length=250,blank=False)
    value = models.CharField(max_length=25,blank=False)
    comments = models.CharField(max_length=250,blank=True)
    date = models.DateTimeField(auto_now=True,blank=True)
    class Meta:
        verbose_name = "Markup"
        verbose_name_plural = verbose_name
    def Name(self):
        return smart_unicode(self.name)
    Name.short_description = "Title"
    def percentageValue(self):
        return smart_unicode(self.value)
    percentageValue.short_description = "Percentage Value"
    def Comments(self):
        return smart_unicode(self.comments)
    Comments.short_description = "Comments"
    def Dates(self):
        return smart_unicode(self.date)
    Dates.short_description = "Date"
