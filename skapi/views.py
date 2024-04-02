
from django.shortcuts import render, HttpResponse
from . import utils
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def cheker(request):
    if request.method == 'POST':
        cc = request.POST.get('cc')
        sk = request.POST.get('sk')
        resp = utils.charge(cc, sk)
        return HttpResponse(f'{resp}')
    return HttpResponse('resp')
