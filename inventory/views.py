from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # https://docs.djangoproject.com/en/4.2/ref/templates/builtins/
    # https://getbootstrap.com/docs/5.0/examples/navbars/
    # https://thenounproject.com/icon/hacker-1482319/
    return render(request, template_name="inventory/index.html")