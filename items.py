# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime


def date_convert(value):
    value=value.replace('-', '')
    try:
        create_date = datetime.datetime.strptime(value,"%Y%m%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def watchNum_conver(value):
    return int(value)


def return_value(value):
    return value

class csdnItemloader(ItemLoader):
    default_output_processor = TakeFirst()


class CsdnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field(
        output_processor=Join(",")
    )
    time = scrapy.Field(
        output_processor=MapCompose(date_convert)
    )
    watch_num = scrapy.Field(
        output_processor=MapCompose(watchNum_conver)
    )
    URL = scrapy.Field()
    image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )

    def get_inser_sql(self):
        insert_sql="""
        insert into tencentCloudBigData(title,URL,tag,time,watch_num,image_url)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE title=VALUES(title), URL=VALUES(URL)
        """
        params=(self["title"], self["URL"], self["tag"], self["time"], self["watch_num"], self["image_url"])
        return insert_sql, params

    pass
