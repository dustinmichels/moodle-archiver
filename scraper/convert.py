import html2text
import os


def get_html():
    path = "output/html/2017-2018/Winter '18/course-Computability and Complexity.html"
    with open(path) as f:
        html = f.read()
    return html


def convert_html(html):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    text_maker.bypass_tables = False
    return text_maker.handle(html)


def html_to_text():
    html = get_html()
    text = convert_html(html)
    return text


if __name__ == '__main__':
    text = html_to_text()
    print(text)