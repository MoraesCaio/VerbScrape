from bs4 import BeautifulSoup
import requests


sites = [
    'https://www.conjugacao.com.br/verbos-regulares/',
    'https://www.conjugacao.com.br/verbos-irregulares/',
]

# remover 3 do final de cada
vr = []
vi = []

verb_lists = [
    vr,
    vi
]


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


# GETTING URLS FOR VERBS
for site, verb_list in zip(sites, verb_lists):

    source = requests.get(site).text
    soup = BeautifulSoup(source, 'lxml')

    site = site[:find_nth(site, '/', 3)]

    # print(soup.prettify())

    # for div in soup.find_all('div', class_='wrapper'):
    for div in soup.find_all(lambda tag:
                             tag.name == 'div' and
                             tag.get('class') == ['wrapper']
                             ):
        for ul in div.find_all('ul'):
            for li in ul:
                verb_list.append(site + li.a['href'])

    # print('\n'.join(verb_list))
verbs_urls = verb_lists[0] + verb_lists[1]

# GET VERB'S CONJUGATIONS
conj_file = open('conjugacoes.txt', 'w')
for verb_url in verbs_urls:
    source = requests.get(verb_url).text
    soup = BeautifulSoup(source, 'lxml')

    print(verb_url)

    skip_line = True

    for main_div in soup.find_all('div', {'id': 'conjugacao'}):
        for div in main_div.find_all(lambda tag:
                                     tag.name == 'div' and
                                     tag.get('class') == ['tempo-conjugacao']
                                     ):
            for p in div.find_all('p'):
                for modo in p.find_all('span'):
                    for span in modo.find_all('span'):
                        for conjugacao in span.find_all('span'):
                            conj_file.write(conjugacao.text + ' ')
                        conj_file.write('\n')
conj_file.close()

# CLEANING OUTPUT FILE
conj_file = open('conjugacoes.txt', 'r')
conj_clean = open('conjugacoes_clean.txt', 'w')
conj_3p = open('conjugacoes_3p.txt', 'w')

not_verb = ['eles', 'que', 'se', 'quando', 'por']

for l in conj_file:
    text_line = l.strip()
    words = text_line.split(' ')
    if text_line and 'eles' in words:
        conj_3p.write(text_line + '\n')
        for word in words:
            if word not in not_verb:
                conj_clean.write(word + '\n')
                if not word.endswith('ão') and not word.endswith('m'):
                    print(word)

conj_file.close()
conj_clean.close()
conj_3p.close()
