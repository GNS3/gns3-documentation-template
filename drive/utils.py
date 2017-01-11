import urllib
import lxml
import re


def process_link(url, root=''):
    purl = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(purl.query)

    if url.startswith('https://www.google.com/url'):
        redirect_url = qs['q'][0]

        if redirect_url.startswith('https://docs.google.com/document/d/'):
            url = redirect_url.replace('https://docs.google.com/document/d/', '')
            doc_id = re.sub(r'/.*', '', url)
            url = root + '/' + doc_id + '/index.html'
        else:
            url = redirect_url

    purl = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(purl.query)
    if purl.hostname == 'drive.google.com':
        if 'id' in qs:
            url = root + '/' + qs['id'][0] + '/index.html'
    return url


def html_to_text(html):
    """
    Transform an HTML soup to a plain text with the correct
    carriage return.
    """
    if isinstance(html, bytes):
        html = html.decode()
    html = re.sub('[\r\n]', '', html)
    html = re.sub('[\t]', ' ', html)
    html = lxml.html.fromstring(html)
    lxml.etree.strip_elements(html, ['script', 'style', 'svg'])
    try:
        body = html.xpath('//body')[0]
    except IndexError:
        return ""

    for elem in body.xpath('//li'):
        if elem.text:
            elem.text = '* ' + elem.text

    elements = list(body.xpath('//node()'))
    elements.reverse()
    blob = ''
    out = ''
    for elem in elements:
        if isinstance(elem, str):
            blob = elem + blob
        elif elem.tag == 'br':
            blob = '\n' + blob
        else:
            if elem.tag in ['h1', 'h2', 'h3', 'div', 'hr']:
                out = '{}\n\n{}'.format(blob.strip(), out)
                blob = ''
            elif elem.tag in ['p', 'li']:
                out = '{}\n{}'.format(blob.strip(), out)
                blob = ''
    out = '{}{}'.format(blob.strip(), out)
    return out.strip()
