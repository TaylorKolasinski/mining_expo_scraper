import scrapy
from scrapy.http import Request
from miner.items import MinerItem

class MinerSpider(scrapy.Spider):

  name = 'minerspider'

  start_urls = ['http://minexpo-365.ascendeventmedia.com/page/%s' % page for page in xrange(2,192)]
  start_urls.append('http://minexpo-365.ascendeventmedia.com')

  item = MinerItem()

  def parse(self, response):
    for page_link in response.css('article.row > div.exhibitorslist__primary > h3 a::attr("href")').extract():
      request = Request(page_link, callback=self.getCompanyInfo)

      yield request


  def getCompanyInfo(self, response):
    name_l = response.css('h1.entry-title::text').extract()

    self.item['name'] = name_l[0].encode('utf-8') if len(name_l) > 0 else 'None'
   

    if len(response.css('div.exhibitor__email a::text').extract()) > 0:
      self.item['email'] = response.css('div.exhibitor__email a::text').extract()[0].encode('utf-8')
    else:
      self.item['email'] = 'None'

    if len(response.css('div.exhibitor__description::text').extract()) > 0:
      self.item['description'] = response.css('div.exhibitor__description::text').extract()[0].encode('utf-8')
    else:
      self.item['description'] = 'None'

    if len(response.css('div.exhibitor__website a::text').extract()) > 0:
      self.item['website'] = response.css('div.exhibitor__website a::text').extract()[0].encode('utf-8')
    else:
      self.item['website'] = 'None'

    if len(response.css('span.exhibitor__country::text').extract()) > 0:
      self.item['country'] = response.css('span.exhibitor__country::text').extract()[0].encode('utf-8')
    else:
      self.item['country'] = 'None'

    yield self.item
