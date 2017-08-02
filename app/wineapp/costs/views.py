from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import costs,markup
# Create your views here.

def costsHelper(costvalue,costtype):
    msg = None
    if costtype == "%":
        try:
            float(costvalue.replace("%","").replace(",","."))
        except Exception as e:
            msg = "A value inserted is not valid."
    elif costtype == "HK$":
        try:
            float(costvalue.replace("HK$","").replace(",","."))
        except Exception as e:
            msg = "A value inserted is not valid."
    return msg

@login_required
def getCosts(request):
    #3 possible actions: add, delete, or update
    posted = {}
    msg = None
    if request.method == "POST":
        posted["title"] = request.POST.get('costname')
        posted["type"] = request.POST.get('costtype')
        posted["value"] = request.POST.get('costvalue')
        posted["action"] = request.POST.get('action')
        posted["id"] = request.POST.get('costid')
        posted["markup"] = request.POST.get('markupvalue')
        if posted["action"] == "add":
            msg = costsHelper(posted["value"],posted["type"])
            if not msg:
                cost_obj = costs(name=posted["title"],valuetype=posted["type"],value=posted["value"].replace(",","."))
                cost_obj.save()
        elif posted["action"] == "delete":
            cost_obj = costs.objects.get(id=posted["id"])
            cost_obj.delete()
        elif posted["action"] == "update":
            msg = costsHelper(posted["value"],posted["type"])
            if not msg:
                cost_obj = costs.objects.get(id=posted["id"])
                cost_obj.name = posted["title"]
                cost_obj.valuetype = posted["type"]
                cost_obj.value = posted["value"].replace(",",".")
                cost_obj.save()
        elif posted["action"] == "markup":
            msg = costsHelper(posted["markup"],"%")
            if not msg:
                cost_obj = markup.objects.get(id=1)
                cost_obj.value = posted["markup"].replace(",",".")
                cost_obj.save()
    else:
        posted["title"] = None
        posted["type"] = None
        posted["value"] = None
        posted["action"] = None
    data = costs.objects.all()
    ids = [item.__dict__['id'] for item in data]
    titles = [item.__dict__['name'] for item in data]
    types = [item.__dict__['valuetype'] for item in data]
    values = [item.__dict__['value'] for item in data]
    positions = range(len(values))

    ids += ["no_id"]
    titles += ["Add New Cost"]
    types += ["HK$ / %"]
    values += ["XXX"]
    positions += ["100"]

    markup_dict = {}
    markup_data = markup.objects.get(id=1)
    markup_dict["name"] = markup_data.__dict__["name"]
    markup_dict["value"] = markup_data.__dict__["value"]
    markup_dict["position"] = range(len(values))[-1]

    if msg:
        if posted["action"] == "markup":
            msg += """ You have inserted:\nMarkup : {0}""".format(posted["markup"])
        else:
            msg += """ You have inserted:\nTitle : {0}\nType : {1}\nValue : {2}""".format(posted["title"],posted["type"],posted["value"])

    return render(request,'costs.html',{"data":zip(ids,titles,types,values,positions),"posted":posted,"msg":msg,"markup":markup_dict})
