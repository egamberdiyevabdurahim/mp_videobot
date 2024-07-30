import requests
import json


BASE_URL = 'https://mpvideo.pythonanywhere.com/'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# POSTS

def find_post(code):
    url = f"{BASE_URL}/post/"
    response = requests.get(url=url).text
    dat = json.loads(response)
    for x in dat:
        if x['code'] == code:
            url2 = f"{BASE_URL}/category/"
            response = requests.get(url=url2).text
            dat2 = json.loads(response)
            lis = [li['name'] for li in dat2 if x['category'] == li['id']]
            dat = {
                'id': x['id'],
                'title': x['title'],
                'video': x['video'],
                'code': x['code'],
                'created_date': x['created_date'],
                'language': x['language'],
                'country': x['country'],
                'time_of': x['time_of'],
                'genre': x['genre'],
                'quality': x['quality'],
                'category': lis[0],
            }
            return dat


def create_simple_user(telegram_id, first_name=None, last_name=None, password=None, username=None):
    url = f"{BASE_URL}/user/"
    url2 = f"{BASE_URL}/account/"
    response = requests.get(url=url).text
    dat = json.loads(response)
    d = {}
    for x in dat:
        if x['username'] == username:
            if x['password'] == password:
                d['username'] = x['username']
                d['password'] = x['password']
                d['first_name'] = x['first_name']
                d['last_name'] = x['last_name']
                d['id'] = x['id']
                d['used'] = x['used']
            return 'Sign-In'
    if d == {}:
        url = f"{BASE_URL}/user/"
        requests.post(url=url, data={'password': password,
                                     'first_name': first_name,
                                     'last_name': last_name,
                                     'username': username})
        response = requests.get(url=url).text
        dat = json.loads(response)
        user_id = [x['id'] for x in dat if x['username'] == username]
        idd = None
        for x in user_id:
            idd = x
        requests.post(url=url2, data={
            'user': idd,
            'telegram_id': telegram_id,
        })


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# USER

def check_user(telegram_id):
    url = f"{BASE_URL}/user/"
    url2 = f"{BASE_URL}/account/"
    response = requests.get(url=url).text
    response2 = requests.get(url=url2).text
    dat = json.loads(response)
    dat2 = json.loads(response2)
    d = {}
    for x in dat2:
        if x['telegram_id'] == telegram_id:
            d['id'] = x['user']
    if d == {}:
        return 'Not Signed-in'
    else:
        for i in dat:
            if i['id'] == d['id']:
                use = i['used']
                requests.patch(url=f"{BASE_URL}/user/{str(d['id'])}/", data={'used': int(use) + 1})
                return True


def sign_in(telegram_id, password, username):
    url = f"{BASE_URL}/user/"
    url2 = f"{BASE_URL}/account/"
    response = requests.get(url=url).text
    response2 = requests.get(url=url2).text
    dat = json.loads(response)
    dat2 = json.loads(response2)
    d = {}
    for x in dat:
        if x['username'] == username:
            if x['password'] == password:
                d['username'] = x['username']
                d['password'] = x['password']
                d['id'] = x['id']
                d['used'] = x['used']
            else:
                return "Password is incorrect"
    if d.get('username') is None:
        return 'Not Registered'
    else:
        message = False
        for j in dat2:
            if j['user'] == d['id']:
                if j['telegram_id'] == telegram_id:
                    message = True
                    use = d['used']
                    requests.patch(url=f"{BASE_URL}/user/{str(d['id'])}/", data={'used': int(use) + 1})
        if message is False:
            requests.post(url=url2, data={
                'user': d['id'],
                'telegram_id': telegram_id,
            })
            use = d['used']
            requests.patch(url=f"{BASE_URL}/user/{str(d['id'])}/", data={'used': int(use) + 1})


def id_detector(telegram_id):
    url2 = f"{BASE_URL}/account/"
    response2 = requests.get(url=url2).text
    dat2 = json.loads(response2)
    for x in dat2:
        if x['telegram_id'] == telegram_id:
            return x['user']


def used_adder(telegram_id):
    url = f"{BASE_URL}/user/"
    url2 = f"{BASE_URL}/account/"
    response = requests.get(url=url).text
    response2 = requests.get(url=url2).text
    dat = json.loads(response)
    dat2 = json.loads(response2)
    for x in dat2:
        if x['telegram_id'] == telegram_id:
            for i in dat:
                if i['id'] == x['user']:
                    use = i['used']
                    requests.patch(url=f"{BASE_URL}/user/{str(x['id'])}/", data={'used': int(use) + 1})


def full_id():
    url = f"{BASE_URL}/account/"
    response = requests.get(url=url).text
    dat = json.loads(response)
    print(dat)
    lis = [li['telegram_id'] for li in dat]
    return lis


def about(text):
    url = f"{BASE_URL}/user/"
    url2 = f"{BASE_URL}/account/"
    response = requests.get(url=url).text
    response2 = requests.get(url=url2).text
    dat = json.loads(response)
    dat2 = json.loads(response2)
    for x in dat2:
        if x['telegram_id'] == text:
            for i in dat:
                if i['id'] == x['user']:
                    use = i['used']
                    requests.patch(url=f"{BASE_URL}/user/{str(x['id'])}/", data={'used': int(use) + 1})
                    data = {
                        'first_name': i['first_name'],
                        'last_name': i['last_name'],
                        'username': i['username'],
                        'password': ''.join(['*' for x in range(len(i['password']))]),
                    }
                    return data


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# HISTORY

def history(text, telegram_id):
    url = f"{BASE_URL}/user/"
    url2 = f"{BASE_URL}/account/"
    url3 = f"{BASE_URL}/history/"
    response = requests.get(url=url).text
    response2 = requests.get(url=url2).text
    dat = json.loads(response)
    dat2 = json.loads(response2)
    for x in dat2:
        if x['telegram_id'] == telegram_id:
            for j in dat:
                if j['id'] == x['user']:
                    data = {'code': text, 'user': j['id']}
                    requests.post(url=url3, json=data)


def hidden_history(text, telegram_id):
    url = f"{BASE_URL}/user/"
    url2 = f"{BASE_URL}/account/"
    url3 = f"{BASE_URL}/hidden_history/"
    response = requests.get(url=url).text
    response2 = requests.get(url=url2).text
    dat = json.loads(response)
    dat2 = json.loads(response2)
    for x in dat2:
        if x['telegram_id'] == telegram_id:
            for j in dat:
                if j['id'] == x['user']:
                    data = {'text': text, 'user': j['id']}
                    requests.post(url=url3, json=data)
