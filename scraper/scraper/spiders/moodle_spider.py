import scrapy
import re
import os
import errno
import shutil
import html2text


def safe_makedir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def safe_rmdir(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def html_to_markdown(html):
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_links = True
    return h.handle(html)


class MoodleSpider(scrapy.Spider):
    name = 'moodle'
    start_urls = ['https://moodle.carleton.edu/auth/shibboleth/index.php']
    # write_path = 'output/html/'

    # remove output folder
    safe_rmdir('output/')

    # Make folders for output
    safe_makedir('output/')
    # safe_makedir('output/html')

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

        if "The password you entered was incorrect" in response.text:
            self.logger.error("Login failed!")
            return
        self.logger.info("Login successful!")

        # with open('output/html/homepage.html', 'wb') as f:
        #     self.logger.info('Writing HTML: homepage')
        #     f.write(response.body)

        course_tree = response.css('ol.tree')

        # with open('output/html/tree.html', 'w') as f:
        #     self.logger.info('Writing HTML: course tree')
        #     f.write(course_tree.extract_first())

        courses = course_tree.xpath('.//li[@class="course"]')

        # courses = courses[6:9]  # TEMP
        for c in courses:
            term_and_or_year = c.xpath('ancestor::li/label/@title').extract()
            path = '/'.join(term_and_or_year)
            url = c.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_course, meta={'path': path})

    # 5. Parse individual courses
    def parse_course(self, response):

        course_name = response.xpath('//h1/text()').extract_first()
        path = response.meta.get('path')
        url = response.url

        print('URL:', url)

        self.logger.info("Parsing {}".format(course_name))

        safe_makedir(f'output/{path}/{course_name}')
        # safe_makedir(f'output/html/{path}/{course_name}')

        main_selector = response.xpath('//section[@id="region-main"]')

        # Write markdown course summary
        course_html = main_selector.extract_first()
        course_markdown = html_to_markdown(course_html)
        with open(f'output/{path}/{course_name}/{course_name} Outline.txt', 'w') as f:
            f.write(course_markdown)
        # with open(f'output/html/{path}/{course_name}/{course_name}.html', 'w') as f:
        #     f.write(course_html)

        files_selector = main_selector.xpath('.//a[contains(@href,"resource")]')
        file_urls = files_selector.xpath('.//@href[contains(.,"resource")]').extract()
        file_data_dicts = self.get_files_metadata(files_selector)
        return dict(
            course_name=course_name, path=path, url=url,
            file_urls=file_urls, file_data=file_data_dicts)

    @staticmethod
    def get_files_metadata(files_sel):
        """Takes list of file selectors, returns dict of metadata keyed by file URL."""

        # Define query paths to get data fields about each file
        link_path = ' .//@href'
        name_path = './span/text()'
        ext_path = 'substring-after( ./img/@src, "/f/" )'
        sect_id_path = 'ancestor::li[contains(@class, "section")]/@id'
        sect_name_path = 'ancestor::li[contains(@class, "section")]/@aria-label'
        queries = [link_path, name_path, ext_path, sect_id_path, sect_name_path]

        # Combine query paths together into single xpath query string
        delim = '||'
        joiner = f', "{delim}", '
        query = 'concat(' + joiner.join(queries) + ')'

        # Extract data from query (string of values, separated by `delim`)
        file_data_strings = files_sel.xpath(query).extract()

        # Convert string data into list, then into dictionary
        file_data_lists = [x.split(delim) for x in file_data_strings]

        # convert list of lists into dict of metadata
        file_data_dicts = {}
        for file in file_data_lists:
            # Separate output data fields values
            url, name, ext, sect_id, sect_name = file

            # clean extension (ie, pdf-24 -> .pdf)
            # If ext is just '.' or '.unknown', replace with empty string
            # ext = '.' + re.sub('-.*', '', ext)
            # ext = '' if ext in ['.', '.unknown'] else ext

            # clean name (replace '/' with '-' file name not reach as folder/file)
            # name = name.replace('/', '-')
            # name = name.replace('%20', ' ')

            # combine name and extension
            # filename = name + ext

            # clean id (ie, section-1 -> 1)
            # combine section name and id
            sect_id = sect_id.replace('section-', '')
            section = f'{sect_id}. {sect_name}'

            # add to dict
            file_data_dicts[url] = {'section': section}

        return file_data_dicts
