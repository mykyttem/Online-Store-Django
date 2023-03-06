from django.http import HttpResponse
from django.template import loader
from .models import Items

# Create your views here.
def items(request):
    myitems = Items.objects.all().values
    template = loader.get_template('all_items.html')
    context = {
        'myitems': myitems,
    }

    return HttpResponse(template.render(context, request))
