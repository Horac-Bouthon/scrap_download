import os
import urllib
import requests
from bs4 import BeautifulSoup
from crawl_obj.crawler_obj import CrawlerObject

import logging
import convert_http


class HttpConverter:

    def __init__(self):
        self.logger = logging.getLogger(convert_http.LOGGER_NAME)
        self.url = ""
        self.page = ""
        self.work_file = ""
        self.soup = None

    def load_site(self, add_url):
        self.url = add_url
        self.page = requests.get(self.url)
        self.page.encoding = "utf-8"
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.logger.debug('Load site {} ...done'.format(self.url))

    def get_object(self):
        return self.soup

    def prettify_to_file(self, file_name):
        with open(file_name, 'w') as outf:
            outf.write(self.soup.prettify())
        self.logger.debug('Prettify in file {}'.format(file_name))

    def st_download_file(self):
        ref = self.soup.find_all('a')
        ret_val = 'None'
        for anchor in ref:
            if 'Ke stáhnutí v XLS' in anchor.text:
                if 'href' in anchor.attrs:
                    base = os.path.split(self.url)[0]
                    file_name = os.path.join(base, anchor.attrs['href'])
                    ret_val = os.path.abspath(self.work_file)
                    urllib.request.urlretrieve(file_name, ret_val)
                    break
        self.logger.debug('File {} downloaded.'.format(self.work_file))
        return ret_val

    def analyze_pattex_de(self):
        co = CrawlerObject.from_none()
        classifications = self.soup.find_all('span', class_='breadcrumb__linkTitle')
        co.classification = classifications[-2].string
        co.product_name = classifications[-1].string
        co.product_url = self.url
        galery = self.soup.find('div', class_='product__images-container')
        co.image_url = galery.find('picture').img.get('src')
        co.description = ""
        section = self.soup.find('div', class_='product__description')
        add_nl = False
        feature_text = section.find('div', class_='product__featureText')
        if feature_text is not None:
            for paragraph in feature_text.find_all('p'):
                if add_nl:
                    co.description += '\n'
                else:
                    add_nl = True
                co.description += paragraph.text
        description_text = section.find('div', class_='product__descriptionText')
        if description_text is not None:
            for paragraph in description_text.find_all('p'):
                if add_nl:
                    co.description += '\n'
                else:
                    add_nl = True
                co.description += paragraph.text
        co.features.clear()
        feat_lis = section.find('div', class_='product__benefitsList').find_all('li')
        for f_o in feat_lis:
            co.features.append(f_o.text)
        co.tech_url.clear()
        co.security_url.clear()
        for paragraph in section.find('div', class_='product__benefitsList').find_all('p'):
            if add_nl:
                co.description += '\n'
            else:
                add_nl = True
            co.description += paragraph.text

        prod_doc = self.soup.find('section', class_='product__documents')
        if prod_doc is not None:
            objs_tech = prod_doc.find_all('a')
            for tech_obj in objs_tech:
                title = tech_obj.get('title')
                if 'Technisches Merkblatt' in title:
                    co.tech_url.append(tech_obj.get('href'))
                if 'Sicherheitsdatenblatt' in title:
                    co.security_url.append(tech_obj.get('href'))
        self.logger.debug('Generated object: {}'.format(repr(co)))
        return co

    @classmethod
    def from_url(cls, new_url):
        new = cls()
        new.load_site(new_url)
        return new

    def __repr__(self):
        return "HttpConverter.from_url('{}')".format(self.url)

    def __str__(self):
        return self.url

