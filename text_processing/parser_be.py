import requests
from bs4 import BeautifulSoup
import logging
import json
import lxml


class ParsBeesona:
    def __init__(self, songs_downloaded=False):
        self.base_url = 'https://www.beesona.ru'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
        self.logs = 'file_logs.log'
        logging.basicConfig(level=logging.INFO, filename=self.logs, filemode="w")
        self.flag = songs_downloaded

    def get_page(self, add_url):
        website_url = requests.get(self.base_url + add_url, headers=self.headers).text
        return BeautifulSoup(website_url, 'lxml')

    def find_elem(self, part, type, how='', value=''):
        if how == '':
            return part.find_all(type)
        else:
            return part.find_all(type, {how: value})

    def get_elements(self, urls, id_name):
        elements = []
        for url in urls:
            try:
                div = self.find_elem(self.get_page(url), 'div', 'id', id_name)
                li = self.find_elem(div[0], 'a')
                for l in li:
                    r = l.get('href').strip()
                    elements.append(r)
            except Exception as e:
                logging.error("While getting info from page:" + str(e) + ", on " + str(url))
                continue
        return elements

    def get_all_letters(self):
        div = self.find_elem(self.get_page('/songs'), 'div', 'id', 'ClipsAlpha')
        li = self.find_elem(div[0], 'a')
        url_letters = []
        for l in li:
            r = l.get('href').strip()
            url_letters.append(r)
        logging.info("Finished get_all_users")
        return url_letters

    def get_all_songs(self):
        all_authors = self.get_elements(self.get_all_letters(), 'ClipsFirst')
        logging.info("Finished get_all_authors")
        all_songs = self.get_elements(all_authors, 'grid-1')
        logging.info("Finished get_all_songs")
        return all_songs

    def write_to_file(self, songs_url, file_name='all_songs.txt'):
        file = open(file_name, 'w')
        for elem in songs_url:
            file.write(elem)
            file.write('\n')
        file.close()
        logging.info("File " + file_name + " created")
        return file_name

    def read_url_from_file(self, file_name='all_songs.txt'):
        songs = open(file_name, 'r', encoding="utf8")
        lines = songs.read().split('\n')
        return lines

    def get_all_info(self, song_urls):
        songs_info = []
        for url in song_urls:
            print(url)
            try:
                div = self.find_elem(self.get_page(url), 'span', 'id', 'editors')
                li = self.find_elem(div[0], 'strong')
                name = li[0].text
                author = li[1].text
                div2 = self.find_elem(self.get_page(url), 'div', 'class', 'copys')
                li_text = self.find_elem(div2[0], 'div')[0]
                for a in self.find_elem(li_text, 'br'):
                    a.replaceWith(a.text + '\n')
                info = {'author_name': author, 'name': name, 'text': li_text.text}
                songs_info.append(info)
            except Exception as e:
                logging.error("While creating json: " + str(e) + ", on " + str(url))
                continue
        return songs_info

    def run_parser(self):
        if self.flag:
            songs_urls = self.read_url_from_file()
        else:
            songs_urls = self.get_all_songs()
            self.write_to_file(songs_urls)

        all_info = {}
        all_info['songs_info'] = self.get_all_info(songs_urls)
        with open('songs_info.json', 'w', encoding="utf8") as file:
            json.dump(all_info, file, ensure_ascii=False)