import requests
import codecs
from bs4 import BeautifulSoup
from random import randint

__all__ = ['head_hunter', 'superjob']

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def head_hunter(url):
    domain = get_domain_name(url)
    jobs = []
    errors = []
    try:
        response = requests.get(url, headers=headers[randint(0, len(headers) - 1)])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'serp-item serp-item_link'})
                for div in div_list:
                    # vacancy
                    href = div.find('a')
                    url = domain + href['href'].replace(domain, '')
                    title = href.span.text

                    # company
                    div_company = div.find('div', attrs={'class': 'vacancy-serp-item-company'})
                    company_name = div_company.a.text

                    jobs.append({'title': title, 'url': url, 'company': company_name})
            else:
                errors.append({'url': url, 'error': 'div does not exist'})
        else:
            errors.append({'url': url, f'error': f'page do not response. Status code: <{response.status_code}>'})

    except requests.exceptions.ConnectionError:
        errors.append({'url': url, 'error': 'no connection'})
    finally:
        return jobs, errors


def superjob(url):
    domain = get_domain_name(url)
    jobs = []
    errors = []
    try:
        response = requests.get(url, headers=headers[randint(0, len(headers) - 1)])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': '_17PZ- _1NA5V'})
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': '_1MxfQ _2ZP2D'})
                for div in div_list:
                    # vacancy
                    href = div.find('a')
                    url = domain + href['href'].replace(domain, '')
                    title = href.text

                    # company
                    div_company = div.find('span', attrs={
                        'class': '_3nMqD f-test-text-vacancy-item-company-name _1trBE _2C8nO _2KJeO _3B9u2 _3nGEP'})
                    company_name = div_company.a.text

                    jobs.append({'title': title, 'url': url, 'company': company_name})
            else:
                errors.append({'url': url, 'error': 'div does not exist'})
        else:
            errors.append({'url': url, f'error': f'page do not response. Status code: <{response.status_code}>'})

    except requests.exceptions.ConnectionError:
        errors.append({'url': url, 'error': 'no connection'})
    finally:
        return jobs, errors


def get_domain_name(url):
    oc_num = 3
    index = -1
    for _ in range(oc_num):
        index = url.find('/', index + 1)
    if index != -1 and url[:index].count('/') == 2:
        return url[:index]
    return ''


if __name__ == '__main__':
    print('import file')
