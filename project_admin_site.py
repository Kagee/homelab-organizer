import logging
from django.contrib import admin as a

#for model, model_admin in admin.site._registry.items():
#    print(model)
#from django.contrib import admin

logger = logging.getLogger(__name__)

class HLOProjectAdminSite(a.AdminSite):
    site_header = "Monty Python administration"

    #def get_app_list(self, request):
        #"""
        #Return a sorted list of all the installed apps that have been
        #registered in this site.
        #"""
        #ordering = {
        #    "Event heros": 1,
        #    "Event villains": 2,
        #    "Epics": 3,
        #    "Events": 4
        #}
        #app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        #app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        #for app in app_list:
        #    app['models'].sort(key=lambda x: ordering[x['name']])
    #    app_list = super().get_app_list(request)
    #    logger.error(app_list)
    #    return app_list

#my_admin = HLOAdminSite()