import scrapy
import re


class MoodleSpider(scrapy.Spider):
    name = 'moodle'
    start_urls = ['https://moodle.carleton.edu/auth/shibboleth/index.php']

    # 1. Press continue on initial form
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response, callback=self.login)

    # 2. Enter login information
    def login(self, response):
        username = self.settings.attributes['MOODLE_USERNAME'].value
        password = self.settings.attributes['MOODLE_PASSWORD'].value
        return scrapy.FormRequest.from_response(
            response,
            formdata={'j_username': username, 'j_password': password},
            callback=self.press_continue)

    # 3. Press continue again
    def press_continue(self, response):
        return scrapy.FormRequest.from_response(
            response, callback=self.after_logged_in)

    # 4. Get all the links to courses
    def after_logged_in(self, response):
        with open('html/homepage.html', 'wb') as f:
            self.logger.info('Writing %s', response.url)
            f.write(response.body)

        if "The password you entered was incorrect" in response.text:
            self.logger.error("Login failed")
            return

        self.logger.info("Login successful")

        course_tree = response.css('ol.tree')
        terms = course_tree.xpath('li/ol/li[not(@class)]')

        t = terms[0]  # temp: just take first term
        for term in [t]:
            term_name = term.xpath('./label/text()').extract_first()
            course_urls = term.xpath('ol/li/a/@href').extract()

            u = course_urls[0]  # temp: just use first course
            for url in [u]:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_course,
                    meta={'term': term_name})

    # 5. Parse individual courses
    def parse_course(self, response):

        course_name = response.xpath('//h1/text()').extract_first()
        term_name = response.meta.get('term')

        self.logger.info("Parsing {}".format(course_name))

        # course_id = response.url.split("id=")[1]
        filename = 'course-%s.html' % course_name
        with open(f'html/{filename}', 'wb') as f:
            self.logger.info('Writing %s', course_name)
            f.write(response.body)

        main_selector = response.xpath('//section[@id="region-main"]')

        with open(f'html/{course_name}-main.html', 'w') as f:
            self.logger.info('Writing main %s', course_name)
            f.write(main_selector.extract_first())

        files_selector = main_selector.xpath('.//a[contains(@href,"resource")]')
        file_urls = files_selector.xpath('.//@href[contains(.,"resource")]').extract()
        file_data_dicts = self.get_files_metadata(files_selector)
        return dict(course_name=course_name, term_name=term_name, file_urls=file_urls, file_data=file_data_dicts)

    @staticmethod
    def get_files_metadata(files_sel):
        """Takes list of file selectors, returns dict of metadata keyed by file URL."""

        # Define query paths to get data fields about each file
        link_path = ' .//@href'
        name_path = './span/text()'
        ext_path = 'substring-after( ./img/@src, "/f/" )'
        sect_id_path = 'ancestor::li[contains(@class, "section")]/@id'
        sect_name_path = 'ancestor::li[contains(@class, "section")]/@aria-label'

        # Combine query paths together into single xpath query string
        delim = '||'
        joiner = f', "{delim}", '
        query = 'concat(' + joiner.join([link_path, name_path, ext_path, sect_id_path, sect_name_path]) + ')'

        # Extract data from query (string of values, seperated by `delim`)
        file_data_strings = files_sel.xpath(query).extract()

        # Convert string data into list, then into dictionary
        file_data_lists = [x.split(delim) for x in file_data_strings]

        # convert list of lists into dict of metadata
        file_data_dicts = {}
        for file in file_data_lists:
            # Separate out data fields values
            url, name, ext, sect_id, sect_name = file

            # clean extension (ie, pdf-24 -> .pdf)
            # If ext is just '.' or '.unknown', replace with empty string
            ext = '.' + re.sub('-.*', '', ext)
            ext = '' if ext in ['.', '.unknown'] else ext

            # clean name (replace '/' with '-' file name not reach as folder/file)
            name = name.replace('/', '-')

            # combine name and extension
            filename = name + ext

            # clean id (ie, section-1 -> 1)
            # combine section name and id
            sect_id = sect_id.replace('section-', '')
            section = f'{sect_id}. {sect_name}'

            # add to dict
            file_data_dicts[url] = {'filename': filename, 'section': section}
        return file_data_dicts

