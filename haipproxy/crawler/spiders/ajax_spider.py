"""
Ajax proxy ip crawler with scrapy-splash
"""
from haipproxy.config.settings import SPIDER_AJAX_TASK
from ..redis_spiders import RedisAjaxSpider
from ..items import ProxyUrlItem
from .base import BaseSpider


class AjaxSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax'
    task_queue = SPIDER_AJAX_TASK

    def __init__(self):
        super().__init__()
        self.parser_maps.setdefault('goubanjia', self.parse_goubanjia)
        self.parser_maps.setdefault('cnproxy', self.parse_cnproxy)

    def parse_goubanjia(self, response):
        infos = response.xpath('//tr')[1:]
        items = list()
        for info in infos:
            proxy_detail = info.xpath('td[1]//*[name(.)!="p"]/text()').extract()
            ip = "".join(proxy_detail[:-1])
            port = proxy_detail[-1]
            protocols = self.procotol_extractor(info.extract())
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items

    def parse_cnproxy(self, response):
        items = list()
        infos = response.xpath('//tr')[2:]
        for info in infos:
            info_str = info.extract()
            proxy_detail = info.css('td::text').extract()
            ip = proxy_detail[0].strip()
            port = proxy_detail[1][1:].strip()
            cur_protocols = self.procotol_extractor(info_str)
            for protocol in cur_protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))

        return items



