# -*- coding: utf-8 -*-
import scrapy
import json
from pymongo import MongoClient



class MuabannetSpider(scrapy.Spider):
    name = 'muabannet'
    allowed_domains = ['muaban.net']
    start_urls = ['https://muaban.net/']

    def start_requests(self):

        # Connect to database

        client = MongoClient('mongodb://localhost:27017')
        db = client['muabannet']
        
        # Crawl from choosen source

        urls = {
            'bds': 'https://muaban.net/mua-ban-nha-dat-cho-thue-toan-quoc-l0-c3', # Bds
            'viec-lam': 'https://muaban.net/viec-lam-tuyen-sinh-toan-quoc-l0-c1', # Viec Lam
            'oto': 'https://muaban.net/o-to-toan-quoc-l0-c4', # Oto
            'xe-may': 'https://muaban.net/xe-may-toan-quoc-l0-c5', # Xe may
            'dich-vu': 'https://muaban.net/dich-vu-toan-quoc-l0-c9', # Dich vu
            'do-dien-tu': 'https://muaban.net/do-dien-tu-toan-quoc-l0-c6', # Do dien tu
            'dien-may-do-gia-dung': 'https://muaban.net/dien-may-do-gia-dung-toan-quoc-l0-c7', # Dien may - Do gia dung
            'khac': 'https://muaban.net/so-thich-mat-hang-khac-toan-quoc-l0-c8', # Khac
            'thoi-trang-my-pham': 'https://muaban.net/thoi-trang-my-pham-toan-quoc-l0-c2', # Thoi trang - my pham
            'doi-tac-cong-dong': 'https://muaban.net/doi-tac-cong-dong-toan-quoc-l0-ca' # Doi tac - cong dong
        }

        collections = db.collection_names()

        # collections = [
        #     'bds',
        #     'viec-lam',
        #     'oto',
        #     'xe-may',
        #     'dich-vu',
        #     'do-dien-tu',
        #     'dien-may-do-gia-dung',
        #     'khac',
        #     'thoi-trang-my-pham',
        #     'doi-tac-cong-dong'
        # ]

        # print(len(collections))

        for index in range(0,len(collections)):
            # print(collections[index])
            # print(urls[collections[index]])
            yield scrapy.Request(url=urls[collections[index]], callback=self.parse, meta={'collection': collections[index], 'db': db[collections[index]]})

    def parse(self, response):

        # Get collection and db need to insert
        collection = response.meta.get('collection')
        db = response.meta.get('db')

        # Get link to go into details of post
        a_selectors = response.xpath('//div[contains(@class, "list-item-container")]/a')
        for selector in a_selectors:
            link = selector.xpath('@href').extract_first()
            title = selector.xpath('@title').extract_first()
            # print(title + "\n" + link)
            if db is not None:
                if [x for x in db.find({"title": title})] == []:
                    yield scrapy.Request(url=link, callback=self.details_parse, meta={'collection': collection, 'db': db})
            else:
                yield scrapy.Request(url=link, callback=self.details_parse, meta={'collection': collection, 'db': db})
                
        next_page = response.xpath('//a[contains(@class, "pagination__link")]/@href').extract()
        # print(next_page[len(next_page) - 1])
        # next_page = response.urljoin(next_page)
        yield scrapy.Request(url=next_page[len(next_page) - 1], callback=self.parse, meta={'collection': collection, 'db': db})
    
    def details_parse(self, response):

        # Get collection and db need to insert
        collection = response.meta.get('collection')
        db = response.meta.get('db')

        # Get post id
        process_url = response.url.split("/")
        post_id = process_url[-1].split("-id")[-1]

        # Get upload position
        upload_location = response.xpath('//div[contains(@class, "location-clock")]/span[contains(@class, "location-clock__location")]/text()').extract()[-1]
        upload_time = response.xpath('//div[contains(@class, "location-clock")]/span[contains(@class, "location-clock__clock")]/text()').extract()[-1]

        # Get images
        imgs = []
        img_selectors = response.xpath('//div[contains(@class, "image__slides")]/img')
        for selector in img_selectors:
            link = selector.xpath('@src').extract_first()
            imgs.append(link)

        # Get videos
        vids = []
        vid_selectors = response.xpath('//div[contains(@class, "image__slides")]').css('iframe')

        if vid_selectors is not None:
            for selector in vid_selectors:
                link = selector.xpath('@src').extract_first()
                vids.append(link)

        title = response.xpath('//h1[contains(@class, "title")]/text()').extract_first()

        price = response.xpath('//div[contains(@class, "price-container__value")]/text()').extract_first()

        user_fullname = response.xpath('//div[contains(@class, "user-info__fullname")]/text()').extract_first()

        mobile = response.xpath('//div[contains(@class, "mobile-container__value")]/span/@mobile').extract_first()

        description = response.xpath('//div[contains(@class, "body-container")]/text()').extract()

        data = {
            'post_id': post_id,
            'upload_time': upload_time.replace("\n", ""),
            'upload_location': upload_location.replace("\n", ""),
            'images': imgs,
            'videos': vids,
            'title': title.replace("\n", ""),  
            'price': price, 
            'user_fullname': user_fullname.replace("\n", ""),
            'mobile': mobile,
            'description': description
        }

        fields = response.xpath('//div[contains(@class, "tect-content-block")]/div[contains(@class, "tech-item")]')

        if fields is not None:
            for field in fields:
                info = field.css('div::text').extract()
                data.update({ info[1].replace(":",""):info[-2] })
        
        with open('muabannet/' + collection + '.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        db.insert_one(data).inserted_id

