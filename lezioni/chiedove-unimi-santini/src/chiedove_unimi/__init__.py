from sys import argv, exit

import requests
from bs4 import BeautifulSoup

SEARCH_URL = 'https://www.unimi.it/it/chi-e-dove'
DETAIL_URL = 'https://www.unimi.it/it/ugov/person/'

def persone(cognome):
  soup = BeautifulSoup(
    requests.get(
      SEARCH_URL,
      params = {
        'cognome': cognome,
        'nome': '',
        'ur_tipi_ruoli_target_id': 'All',
    },
    headers = {'User-Agent': 'Mozilla/5.0'}
  ).text, 'html.parser')
  return [a['href'].split('/')[-1] for a in soup.select('a[href^="/it/ugov/person/"]')]

def dettaglio(persona):
  soup = BeautifulSoup(requests.get(DETAIL_URL + persona, headers = {'User-Agent': 'Mozilla/5.0'}).text, 'html.parser')
  nome_e_cognome = soup.select_one('h1.page-header').text.strip()
  indirizzo = soup.select_one('p.ugov-indirizzo').text.strip()
  telefono = soup.select_one('div.phone + div').text.strip()
  email = decode_cfemail(soup.select_one('span[data-cfemail]')['data-cfemail'])
  return f'{nome_e_cognome}, sede: {indirizzo}, tel: {telefono}, email: {email}'

def decode_cfemail(encoded):
  key, text = int(encoded[:2], 16), bytes.fromhex(encoded[2:])
  return ''.join(chr(b ^ key) for b in text)

def main():
  if len(argv) != 2:
    print('chiedove-unimi <cognome>')
    exit(1)
  for persona in persone(argv[1]):
    print(dettaglio(persona))