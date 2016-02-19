from scrapy.exceptions import DropItem

class DubizzlePipeline(object):
    def process_item(self, item, spider):
        return item
