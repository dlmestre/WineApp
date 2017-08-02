from django.contrib import admin
import csv
from django.utils.encoding import smart_str
from django.http import HttpResponse

def export_csv(modeladmin,request,queryset):
    #
    response = HttpResponse(mimetype="text/csv")
