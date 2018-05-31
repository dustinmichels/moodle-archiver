import scrapy
from scrapy.pipelines.files import FilesPipeline


class SaveFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item.get('file_urls', []):
            yield scrapy.Request(file_url, meta={
                'path': item.get('path'),
                'course_name': item.get('course_name'),
                'file_data': item.get('file_data').get(file_url)})

    def file_path(self, request, response=None, info=None):
        path = request.meta.get('path')
        course_name = request.meta.get('course_name')

        file_data = request.meta.get('file_data')
        section = file_data.get('section')
        filename = file_data.get('filename')

        return f'{path}/{course_name}/{section}/{filename}'
