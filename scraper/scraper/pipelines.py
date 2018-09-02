import scrapy
from scrapy.pipelines.files import FilesPipeline


class SaveFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):

        # print("in get_media_requests!!!!")
        # print(self)
        # print(item)
        # print(info)
        # print('-----------')
        # print('----IN GET MEDIA REQ----')

        for file_url in item.get('file_urls', []):
            yield scrapy.Request(file_url, meta={
                'path': item.get('path'),
                'course_name': item.get('course_name'),
                'file_data': item.get('file_data').get(file_url)})

    def file_path(self, request, response=None, info=None):

        # print('----IN FILE PATH----')
        # print("in file path!!!")
        # print("Self:", self)
        # print("Req:", request)
        # print("Res:", response)

        path = request.meta.get('path')
        course_name = request.meta.get('course_name')

        file_data = request.meta.get('file_data')
        section = file_data.get('section')
        # filename = file_data.get('filename')
        filename = "NOT_NAMED"

        if response:
            filename = response.url.split('/')[-1]
            filename = filename.replace('%2', ' ')

        return f'{path}/{course_name}/{section}/{filename}'
