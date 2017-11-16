import os
import os.path
import sys
import html.parser
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError


class MyHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (atr, val) in attrs:
                if atr == 'href':
                    self.links.append(val)
        elif tag == 'img':
            for (atr, val) in attrs:
                if atr == 'src':
                    self.links.append(val)


def to_ascii(link):
    link2 = list(urllib.parse.urlsplit(link))
    link2[2] = urllib.parse.quote(link2[2])
    link2 = urllib.parse.urlunsplit(link2)
    return link2


# sprawdza czy linki są aktywne
def check_links(directory):
    myparser = MyHTMLParser()
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.endswith('.html'):
                with open('%s' % (os.path.join(path, name))) as data:
                    myparser.feed(data.read())

    links_list = list(set(myparser.links))

    for link in links_list:
        if link.startswith('http://') or link.startswith('https://'):
            link2 = to_ascii(link)
            try:
                code = urllib.request.urlopen(link2).getcode()
            except HTTPError as e:
                yield (('Fail! Error code %s' % e.code), link)
            except URLError as e:
                yield (('Fail! Reason: %s' % e.reason), link)
            else:
                yield (('OK! Status code: %s' % code), link)


def get_references(filename):
    myparser = MyHTMLParser()
    with open(filename) as data:
        myparser.feed(data.read())

    return myparser.links


# zwraca parę (nazwa pliku html, lista plików)
# w liście plików znajdują się nazwy wszystkich plików które
# zawierają odnośnik do pliku
def check_references(directory):
    reference_dict = {}
    path_dict = {}
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.endswith('.html'):
                path_dict[name] = os.path.join(path, name)
                reference_dict[name] = get_references('%s' % (os.path.join(path, name)))

    for html_file in reference_dict:
        files_with_ref = []
        for html_file2, links_lists in reference_dict.items():
            if html_file in links_lists:
                files_with_ref.append(path_dict[html_file2])
        yield (path_dict[html_file], files_with_ref)


if __name__ == "__main__":
    for i in check_links(sys.argv[1]):
        print(i)

    print('\n')

    for i in check_references(sys.argv[1]):
        print(i)
