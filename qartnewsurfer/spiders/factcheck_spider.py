import scrapy


def strip_html(string):
    tag_end_index = string.index('>')
    if '=' in string[:tag_end_index]:
        html_tag_length = string.index(' ') - 1
    else:
        html_tag_length = tag_end_index - 1

    return string[tag_end_index+1:-(html_tag_length+3)]

class FactCheckSpider(scrapy.Spider):
    name = 'factcheck'

    def start_requests(self):
        urls = [
            # 'https://factcheck.ge/ka/story/39584-პენსია-არის-ბევრად-უფრო-ნაკლები-ვიდრე-მაშინ-როდესაც-ქართულმა-ოცნებამ-გადმოიბარა-ხელისუფლება'
            'https://factcheck.ge/ka/story/39592-დეზინფორმაცია-ვაქცინაციის-შედეგად-სხეულში-შეყვანილი-თხევადი-კრისტალების-საშუალებით-ადამიანის-ზომბებად-ქცევაა-შესაძლებელი',
            # 'https://factcheck.ge/ka/story/256-qethevan-tsikhelashvili-ganrideba-artserthi-utskhoeli-moqalaqis-an-moqalaqeobis-armqone-piris-mimarth-ar-gankhortsielebula'
            # 'https://factcheck.ge/ka/story/39359-2019-2020-წლებში-გასამმაგდა-ოკუპირებული-რეგიონებიდან-სტუდენტების-რაოდენობა'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Get elements content
        title = response.xpath('/html/body/main/div/div/div/div[1]/div/div[1]/div[2]/h3/text()').get()
        title_img = response.xpath('/html/body/main/div/div/div/div[1]/div/div[1]/div[1]/img/@src').get()
        verdict_text_full = response.xpath('/html/body/main/div/div/div/div[1]/div/div[1]/div[2]/p/text()').get()
        verdict_text_short = response.xpath('/html/body/main/div/div/div/div[1]/div/div[1]/div[2]/div/div[2]/div[1]/text()').get()
        verdict_text_popup = response.xpath('/html/body/main/div/div/div/div[1]/div/div[1]/div[2]/div/div[2]/div[2]/div/div/text()').get()
        verdict_percentage = response.xpath('/html/body/main/div/div/div/div[1]/div/div[1]/div[2]/div/div[2]/div[2]/div/i/@style').get()
        # text_intro = strip_html(response.xpath('//*[@id="article-text"]/p[2]').get())
        full_text = response.xpath('//*[@id="article-text"]/*').getall()
        author_name = response.xpath('/html/body/main/div/div/div/div[1]/div/div[3]/div[4]/a/div[2]/text()').get()
        tags = response.xpath('/html/body/main/div/div/div/div[1]/div/div[3]/div[3]/div/h5/a/text()').getall()
        person_tag = response.xpath('/html/body/main/div/div/div/div[2]/div[1]/div[2]/div/div/div/h4/a/text()').get()

        date = response.xpath('/html/body/main/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/text()').get()
        url = response.request.url

        # Modify elements content
        verdict_percentage = verdict_percentage[verdict_percentage.index("left")+5:verdict_percentage[verdict_percentage.index("left"):].index(";")]
        if verdict_percentage == "-10%":
            verdict_converted_percentage = 0
        else:
            verdict_converted_percentage = int((int(verdict_percentage.replace('%', '')) / 90) * 100)

        tags = [tag.replace('\n', '') for tag in tags]
        author_name = author_name.replace('\n', '')
        full_text = "\n".join([strip_html(paragraph) for paragraph in full_text])

        # Return
        yield {
            'article_title': title,
            'title_image': title_img,
            'verdict_text_full': verdict_text_full,
            'verdict_text_short': verdict_text_short,
            'verdict_text_popup': verdict_text_popup,
            'verdict_percentage': verdict_percentage,
            'verdict_converted_percentage': verdict_converted_percentage,
            'full_text': full_text,
            'author_name': author_name,
            'tags': tags,
            'person_tag': person_tag,
            'date': date,
            'url': url,
        }
