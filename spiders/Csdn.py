# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from CSDN.items import csdnItemloader,CsdnItem
import requests
from urllib import parse


class CsdnSpider(scrapy.Spider):
    name = 'Csdn'
    allowed_domains = ['cloud.tencent.com']
    start_urls = ['https://cloud.tencent.com/community/tag/73']

    userAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    header = {
        "User-Agent": userAgent,
    }
    session = requests.session()


    def parse(self, response):
        post_nodes = response.css('.main-content .unit-box .article-item')

        for post_node in post_nodes:
            image_url = post_node.css('.article-figure img::attr(src)').extract_first("")
            post_url = post_node.css('a::attr(href)').extract_first("")
            yield scrapy.Request(parse.urljoin('https://cloud.tencent.com', post_url), meta={"image_url": image_url}, headers=self.header, callback=self.parse_detail)

        next_url = response.xpath('//*[@id="J-main"]/div/div[2]/div/div[1]/div/div[11]/a[10]/@href').extract_first("")
        if next_url:
            yield scrapy.Request(parse.urljoin('https://cloud.tencent.com', next_url), headers=self.header, callback=self.parse)
        pass


    def parse_detail(self, response):
        item_loader = csdnItemloader(item=CsdnItem(), response=response)
        item_loader.add_value("URL", response.url)
        item_loader.add_css("title", '.article-header h3::text')
        item_loader.add_css("tag", '.infos .tags a::text')
        item_loader.add_xpath("time", '//*[@id="J-main"]/div/div[2]/div/div[1]/div/div[1]/div/span[2]/text()')
        item_loader.add_xpath("watch_num", '//*[@id="J-main"]/div/div[2]/div/div[1]/div/div[1]/div/span[3]/text()')
        Get_image_url = response.meta.get("image_url", "")
        if Get_image_url:
            item_loader.add_value("image_url", [Get_image_url])
        else:
            item_loader.add_value("image_url", "NO image url")
        csdn_item = item_loader.load_item()
        yield csdn_item

