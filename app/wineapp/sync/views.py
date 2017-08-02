from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
import json,os
from syncdb.tester import func
from syncdb.output import main

location = r'/home/ubuntu/app/data2/'

@login_required
def sync(request):
    return render(request,'syncdb.html')

@login_required
def foundWines(request):
    return render(request,'winesfound.html')

@login_required
def syncoutput(request):
    #data = func()
    records,time_took = main()
    data = {"Records":records,"Time":time_took}
    return HttpResponse(json.dumps(data),content_type="application/json")

@login_required
def getWorkingWines(request):
    path = os.path.join(location,"found_wines.csv")
    data = open(path,"r").read()
    response = HttpResponse(data,content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="working_wines.csv"'
    
    return response

@login_required
def getNotWorkingWines(request):
    path = os.path.join(location,"not_found_wines.csv")
    data = open(path,"r").read()
    response = HttpResponse(data,content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="not_working_wines.csv"'

    return response

