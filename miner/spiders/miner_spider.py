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
    name_l  = response.css('h1.entry-title::text').extract()
    emal_l  = response.css('div.exhibitor__email a::text').extract()
    desc_l  = response.css('div.exhibitor__description::text').extract()
    webs_l  = response.css('div.exhibitor__website a::text').extract()
    cont_l  = response.css('span.exhibitor__country::text').extract()

    self.item['name']         = name_l[0].encode('utf-8') if len(name_l) > 0 else 'None'
    self.item['email']        = emal_l[0].encode('utf-8') if len(emal_l) > 0 else 'None'
    self.item['description']  = desc_l[0].encode('utf-8') if len(desc_l) > 0 else 'None'
    self.item['website']      = webs_l[0].encode('utf-8') if len(webs_l) > 0 else 'None'
    self.item['country']      = cont_l[0].encode('utf-8') if len(cont_l) > 0 else 'None'  

    yield self.item
