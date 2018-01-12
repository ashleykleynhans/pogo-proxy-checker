import requests
from random import randrange


def get_proxies():
    f = open('proxies.txt', 'r')
    proxies = f.read()
    f.close()

    return proxies.split('\n')


def test_proxy(proxy):
    proxy = proxy.strip()
    if len(proxy) == 0: return

    proxies = {
        'http': proxy,
        'https': proxy,
    }

    headers = {
        'Accept': '*/*',
        'User-Agent': 'pokemongo/0 CFNetwork/811.5.4 Darwin/16.7.0',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'gzip, deflate',
        'X-Unity-Version': '2017.1.2f1'
    }

    url = 'https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize&locale=en_US'

    try:
        r = requests.get(url, proxies=proxies, timeout=1.0, headers=headers)

        if r.status_code == 200:
            print('PROXY [%s] : HTTP 200: Proxy is OK' % proxy)

            headers = {
                'User-Agent': 'Niantic App'
            }

            url = 'https://pgorelease.nianticlabs.com/plfe/version'

            r = requests.get(url, proxies=proxies, timeout=1.0, headers=headers)

            if r.status_code == 200:
                out = open('good-proxies.txt', 'a')
                out.write(proxy)
                out.close()

        elif r.status_code == 409:
            print('PROXY [%s] : HTTP 409: Proxy is banned' % proxy)
        elif r.status_code == 403:
            print('PROXY [%s] : HTTP 403: Proxy is banned' % proxy)
        elif r.status_code == 503:
            print('PROXY [%s] : HTTP 503: Proxy is throttled' % proxy)
        else:
            print('PROXY [%s] : HTTP %s' % (proxy, r.status_code))
    except:
        print('PROXY [%s] : Connect timed out' % proxy)


for proxy in get_proxies():
    test_proxy(proxy)
