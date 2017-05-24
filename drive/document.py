import urllib.request
import lxml.html.clean
import lxml.html.builder
import lxml.html
import lxml.etree
import urllib
import hashlib
import os
import re


from drive.utils import process_link, html_to_text
from drive.theme import Theme


import logging
log = logging.getLogger(__name__)


class DriveDocument:
    def __init__(self, id, title, data, export_dir, authors=[], modifiedTime=None, theme=None, editable_by_anyone=False, template='document', appliances=None, config={}):
        log.info('Process document %s %s', id, title)
        if theme is None:
            self._theme = Theme(export_dir)
        else:
            self._theme = theme

        self._template = template
        self._config = config
        self._export_dir = export_dir
        self._authors = authors
        self._modifiedTime = modifiedTime
        self._data = data
        self._title = title
        self._appliances = appliances
        self._id = id
        self._html = lxml.html.fromstring(self._data)
        text = html_to_text(self._data)
        text = re.sub('\n\n+', '\n\n', text)
        self._text = text.replace('\n', '<br/>')
        self._editable_by_anyone = editable_by_anyone

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def modifiedTime(self):
        return self._modifiedTime

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, val):
        self._authors = val

    @property
    def text(self):
        return self._text

    @property
    def html(self):
        return self._html

    @property
    def content(self):
        """
        HTML content of the page
        """
        return self._content.decode("utf-8")

    @property
    def editable_by_anyone(self):
        return self._editable_by_anyone

    @property
    def toc(self):
        return self._toc

    def _get_toc(self):
        """
        Return the table of content
        [
            {'id': 'l1', 'text': 'Header 1', 'level': 1},
            {'id': 'l2', 'text': 'Header 2', 'level': 2},
            {'id': 'l3', 'text': 'Header 3', 'level': 3}
        ]
        """
        toc = []
        for element in self._html.iter(['h1', 'h2', 'h3']):
            if element.attrib.get('id') and element.text:
                toc.append({
                    'id': element.attrib['id'],
                    'text': element.text.strip(),
                    'level': int(element.tag.lstrip('h'))
                })
        return toc

    def export(self):
        output_dir = os.path.join(self._export_dir, self._id)
        root = ".."
        os.makedirs(output_dir, exist_ok=True)
        data, files = self._process(root=root)

        with open(os.path.join(output_dir, 'index.html'), 'wb+') as f:
            f.write(data.encode('utf-8'))

        for url, file in files:
            self._download_url(url, os.path.join(output_dir, file))

    def _download_url(self, url, path):
        """
        Download a file to this path
        """
        if not os.path.exists(path):
            log.debug("Download %s", url)
            u = urllib.request.urlopen(url)
            with open(path, 'wb+') as f:
                f.write(u.read())

    def _process(self, root='..'):
        files = []
        self._clean_html()
        self._annotate()

        for (element, attr, url, _) in self._html.iterlinks():
            if element.tag == 'a' and attr == 'href' and url.startswith('https://www.google.com/url'):
                element.set('href', process_link(url, root=root))
            elif element.tag == 'img' and attr == 'src':
                filetitle = hashlib.md5(url.encode()).hexdigest()
                filetitle += '.jpg'
                element.set('src', '../' +  self._id + '/' + filetitle) # We go to top level to handle when the document is use as appliance
                files.append((url, filetitle))

        self._toc = self._get_toc()
        self._add_anchors()
        self._wrap_images()
        self._replace_youtube_videos()

        # Wrap the original body
        try:
            body = self._html.xpath('//body')[0]
        except (IndexError):
            body = lxml.html.Element('body')
        body.tag = 'div'

        if 'style' in body.attrib:
            del body.attrib['style']

        self._content = lxml.etree.tostring(body, pretty_print=True, method="html")
        return self._theme.render(self._template + '.html', document=self, root=root, config=self._config, appliances=self._appliances), files

    def _wrap_images(self):
        """
        Wrap images in a target blank
        """
        for img in self._html.iter('img'):
            img.attrib.pop('style', None)
            a = img
            a.attrib["href"] = img.attrib.pop("src", None)
            a.attrib["target"] = "_blank"
            a.tag = "a"
            img = lxml.html.builder.IMG()
            img.attrib["src"] = a.attrib["href"]
            a.append(img)

    def _annotate(self):
        """
        Special block like NOTE, WARNING

        If we have a block like:
        <p><strong>WARNING:</strong></p>
        <p>This is a warning</p>

        We replace by:
        <p class="badge warning"><strong>WARNING:</strong> This is a warning</p>
        """
        for element in self._html.iter('strong'):
            if element.text:
                text = element.text.strip(' ')
                if text.endswith(':'):
                    text = text.strip(':').replace(' ', '_')
                    element.text = text
                    if text.isupper():
                        parent = element.getparent()
                        parent.attrib["class"] = "badge " + text.lower()
                        following = parent.getnext()
                        if following.text:
                            parent.append(lxml.html.builder.SPAN(following.text))
                        parent.extend(list(following))
                        following.drop_tree()

    def _clean_html(self):
        # Strip footnotes
        for element in self._html.iter('sup'):
            element.drop_tree()
        for a in self._html.iter('a'):
            if a.attrib.get('href', '').startswith('#cmnt_ref'):
                parent = a
                while parent.tag != 'div':
                    parent = parent.getparent()
                parent.drop_tree()

        # If we have this style we replace by a CSS class or a tag
        # Order is important
        default_styles = (
            ('font-weight:700', '<strong>'),
            ('font-family:"Courier New"', 'code'),
            ('font-size:26pt', 'title'),
            ('padding-top:10pt;margin:0;', 'toc1'),
            ('padding-top:4pt;margin:0', 'toc1'),
            ('margin-left:18pt', 'toc2'),
            ('transform: rotate(0.00rad) translateZ(0px)', 'image'),
            ('color:#1155cc;text-decoration:underline', None),
            ('color:inherit;text-decoration:inherit', None),
            ('border-spacing:0;border-collapse:collapse', None), # table
            ('height:0pt', None), # tr
            ('border-right-style:solid', None), # td
            ('padding:0;margin:0', None), # reset ul style
            ('background-color:#ffffff', None), # p
            ('font-size:10pt', None), # p
            ('font-size:10.5pt', None), # p
            ('font-size:11pt', None), # p
            ('font-size:12pt', None), # p
            ('orphans:2;widows:2', None), # p
            ('font-size:20pt', None), # h1
            ('font-size:16pt', None), # h2
            ('font-size:14pt', None) # h3
        )
        for element in self._html.iter():
            element_style = element.attrib.get('style', '').replace(' ', '')
            if len(element_style) == 0:
                continue
            for style, replace in default_styles:
                if style.replace(' ', '') in element_style:
                    if replace:
                        if replace.startswith('<'):
                            element.tag = replace.strip('<>')
                        else:
                            element.attrib['class'] = replace
                    element.attrib.pop('style', None)

        #Empty <span><br><br></span> should be merge with previous span block
        for span in list(self._html.iter('span')):
            if span.text is None and set([ e.tag for e in span ]) == set(('br', )):
                previous = span.getprevious()
                if previous is not None and previous.tag == 'span':
                    previous.extend(list(span))
                    span.drop_tree()

        # Drop empty <p> full of unbreakable spaces
        for p in list(self._html.iter('p')):
            if p.text:
                if re.match("^\u00A0+$", p.text):
                    p.drop_tree()
                elif re.match("^(&#160;[ ]?)+$", p.text):
                    p.drop_tree()
                else:
                    p.text = p.text.lstrip(" ^\u00A0\r\n")

        # Merge all code block to a single
        for p in list(self._html.iter('p')):
            code_class = False
            for child in p:
                if child.attrib.get('class', '') == 'code':
                    code_class = True
                else:
                    code_class = False
                    break
            if code_class:
                p.attrib['class'] = 'code'
                for child in list(p):
                    child.attrib.pop('class', None)
                previous = p.getprevious()
                if previous is not None and previous.tag == 'p' and previous.attrib.get('class') == 'code':
                    previous.append(lxml.html.builder.BR())
                    if p.text:
                        previous.append(lxml.html.builder.SPAN(p.text))
                    previous.extend(list(p))
                    p.getparent().remove(p)

        # Remove useless span <p><span>Hello</span></p>
        for element in self._html.iter():
            if element.tag == "span" and len(element.attrib) == 0:
                if len([e for e in element if e.tag != 'br']) == 0:
                    element.drop_tag()

    def _add_anchors(self):
        """
        Add anchors link to h1, h2, h3
        """
        for element in self._html.iter('h1', 'h2', 'h3'):
            if len(element) == 0 and element.attrib.get('id') is not None:
                a = lxml.html.builder.A()
                a.attrib['href'] = "#" + element.attrib.get('id')
                a.text = element.text
                element.text = None
                element.append(a)

    def _replace_youtube_videos(self):
        for (element, attr, url, _) in list(self._html.iterlinks()):
            if element.tag == 'a' and attr == 'href' and 'youtube.com/watch' in url:
                purl = urllib.parse.urlparse(url)
                qs = urllib.parse.parse_qs(purl.query)
                url = "https://www.youtube.com/embed/" + qs["v"][0]

                element.tag = 'iframe'
                element.set('src', url)
                element.set('width', '560')
                element.set('height', '315')
                element.set('frameborder', '0')
                element.set('allowfullscreen', '1')
                element.set('style', 'display:block')
                element.text = None
                del element.attrib['href']


def main():
    """
    Run a test
    """
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        document = DriveDocument("42", "test", "<html><body style=\"test\"><h1>Hello</h1></body></html>", editable_by_anyone=True)
        document.export(tmpdir)
        with open(os.path.join(tmpdir, "42", "index.html")) as f:
            print(f.read())

if __name__ == '__main__':
    main()
