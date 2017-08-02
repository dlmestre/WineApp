from django.conf.urls import include, url, handler404
from django.contrib import admin
from django.contrib.auth.views import login

urlpatterns = [
    # Examples:
    # url(r'^$', 'wineapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'datadb.views.home',name='home'),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^logged_in/$', 'datadb.views.logged_in'),
    url(r'^upload/$','datadb.views.upload'),

    url(r'^uploaddictionary/$', 'datadb.views.upload_dictionary'),
    url(r'^uploadeddictionary/$','datadb.views.uploaded_dictionary'),
    url(r'^uploadsmallerfile/$', 'datadb.views.upload_smallerfile'),
    url(r'^uploadedsmallerfile/$','datadb.views.uploaded_smallerfile'),

    url(r'^uploaddictionary2/$', 'datadb.upload_files_views.upload_dictionary_copy',name="dictionary"),
    url(r'^uploadeddictionary2/$','datadb.upload_files_views.uploaded_dictionary_copy'),
    url(r'^uploadsmallerfile2/$', 'datadb.upload_files_views.upload_smallerfile_copy',name="database"),
    url(r'^uploadedsmallerfile2/$','datadb.upload_files_views.uploaded_smallerfile_copy'),

    url(r'^results/$','datadb.views.results'),
    url(r'^wine/$','datadb.views.wine'),
    url(r'^getwine/$','merchants.views.wine',name='wine'),
    url(r'^testingPage/$','datadb.views.testingPage'),

    url(r'^database/$','merchants.views.database'),
    url(r'^remover/$','merchants.views.remover'),
    url(r'^remover2/$','merchants.views.remover_copy',name='remover'),
    url(r'^table/$','merchants.views.showtable'),
    url(r'^table2/$','merchants.views.showtable2'),
    url(r'^download/$','merchants.views.download'),
    url(r'^manual/$','merchants.views.manual_table'),
    url(r'^download2/$','merchants.views.download2'),
    url(r'^percent/$','merchants.views.percents'),
    url(r'^gettable/$','merchants.views.getTable',name='table'),

    url(r'^costs/$','costs.views.getCosts',name='costs'),
    url(r'^sync/$','sync.views.sync',name='sync'),
    url(r'^syncoutput/$','sync.views.syncoutput',name='output'),
    url(r'^workingwines/$','sync.views.getWorkingWines',name='workingwwines'),
    url(r'^notworkingwines/$','sync.views.getNotWorkingWines',name='notworkingwines'),
    url(r'^foundwines/$','sync.views.foundWines',name='foundwines'),
]

handler404 = 'datadb.views.error404'
