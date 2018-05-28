import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['https://moodle.carleton.edu/auth/shibboleth/index.php']

    def parse(self, response):
        # 1. Press continue on initial form
        return scrapy.FormRequest.from_response(
            response, callback=self.login)

    def login(self, response):
        # 2. Enter login information
        username = self.settings.attributes['MOODLE_USERNAME'].value
        password = self.settings.attributes['MOODLE_PASSWORD'].value
        return scrapy.FormRequest.from_response(
            response,
            formdata={'j_username': username, 'j_password': password},
            callback=self.press_continue)

    def press_continue(self, response):
        # 3. Press continue again
        return scrapy.FormRequest.from_response(
            response, callback=self.after_logged_in)

    def after_logged_in(self, response):
        # 4. Get all the links to courses
        with open('homepage.html', 'wb') as f:
            self.logger.info('Writing %s', response.url)
            f.write(response.body)

        if "The password you entered was incorrect" in response.text:
            self.logger.error("Login failed")
            return

        self.logger.info("Login successful")
        course_tree = response.css('ol.tree')
        terms = course_tree.xpath('li/ol/li[not(@class)]')
        t = terms[0]  # temporary-- just take first course
        course_urls = t.xpath('ol/li/a/@href').extract()
        for url in course_urls:
            yield scrapy.Request(url=url, callback=self.parse_course)

    def parse_course(self, response):
        # 5. Parse individual courses
        course_id = response.url.split("id=")[1]
        filename = 'course-%s.html' % course_id
        with open(filename, 'wb') as f:
            self.logger.info('Writing %s', filename)
            f.write(response.body)

        main = response.xpath('//section[@id="region-main"]')
        resource_urls = main.xpath('.//a/@href[contains(.,"resource")]').extract()
        print(resource_urls)
