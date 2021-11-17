from bs4 import BeautifulSoup
import requests
import libtorrent as lt
import time
import datetime
def download(link):
  ses = lt.session()
  ses.listen_on(6881, 6891)
  params = {
      'save_path': '/home/becode/Downloads', #dans mon serveur vps
      'storage_mode': lt.storage_mode_t(2)}
     
  print(link)
  handle = lt.add_magnet_uri(ses, link, params)
  ses.start_dht()
  begin = time.time()
  print(datetime.datetime.now())
  print ('Downloading Metadata...')
  while (not handle.has_metadata()):
      time.sleep(1)
  print ('Got Metadata, Starting Torrent Download...')
  print("Starting", handle.name())
  while (handle.status().state != lt.torrent_status.seeding):
      s = handle.status()
      state_str = ['queued', 'checking', 'downloading metadata', \
              'downloading', 'finished', 'seeding', 'allocating']
      print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
              (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
              s.num_peers, state_str[s.state]))
      time.sleep(5)
  end = time.time()
  print(handle.name(), "COMPLETE")
  print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")
  print(datetime.datetime.now())
def scraper():
  choice = input('Which tracker do you want to use ( Choices : [1]piratebay [2]1337) ?')
  search = input('What do you want to download ? : ')
  if choice == '1':
      url = 'https://thepiratebay.party/search/' + search
      page = requests.get(url)
      soup = BeautifulSoup(page.text, 'lxml')
      torrents = soup.find(id="searchResult")
      trs = torrents.find_all("tr")
      # magnets = []
      # for tr in trs[1:3]:
      #     magnets.append(tr.nobr.a['href'])
      # # print(trs[1].nobr.a['href'])
      # for each in magnets:
      #     download(each)
      download(trs[4].nobr.a['href'])
  elif choice == '2':
      url = 'https://www.1377x.to/search/' + search + '/1/'
      page = requests.get(url)
      soup = BeautifulSoup(page.text, 'lxml')
      torrents = soup.find_all('tr')
      magnets = []
      for each in torrents[1:3]:
          url = 'https://www.1377x.to/' + each.findall('a')[1].get('href')
          page = requests.get(url)
          soup = BeautifulSoup(page.text, 'lxml')
          magnet = soup.find(class_='col-9 page-content')
          magnet = magnet.li.a.get('href')
          magnets.append(magnet)
      print(magnets)
scraper()

