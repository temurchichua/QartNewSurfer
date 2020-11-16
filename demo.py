from qartnewsurfer.page_setup import OnGe

page_setup = OnGe
onge = page_setup()
url = onge.get_url(category=0, page=1)
print(url)
# https://on.ge/category/პოლიტიკა?page=150
title = response.css('title::text').getall()



pages = response.css("a.overlay-link.link.js-link")
for page in pages:
     title = page.css("a::text").get()
     url = page.css("a::attr(href)").get()
     link = dict(title=title, url=url)
     print(link)

pages = response.css("a.overlay-link.link.js-link")

page = pages_on_page[index]

title = page.css("a::text").get()
link = page.css("a::attr(href)").get()
