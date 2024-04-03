
from django.shortcuts import render, HttpResponse
from . import utils
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.


@csrf_exempt
def cheker(request):
    if request.method == 'GET':
        try:
            cc = request.GET.get('cc')
            sk = request.GET.get('sk')
            client_ip = request.META.get('REMOTE_ADDR', '')
            try:
                cvv1 = request.GET.get('cvv1')
            except:
                cvv1 = None
            resp = utils.charge(cc, sk, cvv1)

            return HttpResponse(f"<font size=2 color='white' margin-bottom='5'><i>  <font class='badge badge-danger'>{resp['resp'][:50]} ⇝ {resp['cc']} </span></i></font> <br> <font size=2 color='red'><font class='badge badge-light'>{resp['code']}  IP ⇝ {client_ip} </i></font><br>")
        except Exception as e:
            # Catching the specific exception raised, if any
            return HttpResponse(r"{'cc': 'none', 'resp': 'Error', 'code': 'none', 'time': '1.7', 'bypass': 0}")
    else:
        return HttpResponse(r'Invalid request method')
