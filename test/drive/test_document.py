import lxml
import pytest
import pathlib
from unittest.mock import patch

from drive import DriveDocument


@pytest.fixture
def document(tmpdir):
    return DriveDocument('42', 'Test', "<html><body></body></html>", str(tmpdir))


def test_text(tmpdir):
    doc = DriveDocument('42', 'Test', "<html><body><p><b>hello</b> world</p></html>", str(tmpdir))
    assert doc.text == 'hello world'


def test_editable_by_anyone(tmpdir):
    doc = DriveDocument('42', 'Test', "<html><body><p><b>hello</b> world</p></html>",str(tmpdir), editable_by_anyone=True)
    html, files = doc._process()
    assert 'Edit on Google Doc' in html


def test_title(tmpdir):
    doc = DriveDocument('42', 'Test', "<html><body><p><b>hello</b> world</p></html>", str(tmpdir), config={"title": "My doc"})
    html, files = doc._process()
    assert '<title>\nMy doc\n- Test\n</title>' in html


def test_strip_blank_line(tmpdir):
    """
    Sometimes we have a line of unbreakable space
    """
    doc = DriveDocument('42', 'Test', "<html><body><p>hello</p><p>                     </p></body></html>", str(tmpdir))
    html, files = doc._process()
    assert '<p>\u00A0\u00A0\u00A0</p>' not in html
    assert '<p>hello</p>' in html


def test_process_replace_link(tmpdir):
    data = """
<html>
    <head></head>
    <body>
        <a href="https://www.google.com/url?q=https://docs.google.com/document/d/3BAA5rVGCNN-aaaaaaa/edit&sa=D&ust=xxxxxxx&usg=xxxxxxxxxx">Test link</a>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert 'href="../3BAA5rVGCNN-aaaaaaa/index.html' in html


def test_process_embed_images(tmpdir):
    data = """
<html>
    <head></head>
    <body>
        <img src="http:/example.com/test.jpg">
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert files == [('http:/example.com/test.jpg', '5781900d18096b6717b559024a5fe1e6.jpg')]
    assert '<img src="5781900d18096b6717b559024a5fe1e6.jpg"' in html


def test_process_youtube_embed(tmpdir):
    data = """
<html>
    <head>
    </head>
    <body>
        <p>Hello</p>
        <p><span><a href="https://www.youtube.com/watch?v=qIRGcKs_MRE">https://www.youtube.com/watch?v=qIRGcKs_MRE</a></span></p>
        <p>World</p>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<body>' in html
    assert '<p>Hello</p>' in html
    assert '<iframe src="https://www.youtube.com/embed/qIRGcKs_MRE" width="560" height="315" frameborder="0" allowfullscreen="1" style="display:block"></iframe>' in html
    assert '<p>World</p>' in html


def test_clean_html_span(tmpdir):
    """
    Remove useless spans
    """
    data = """
<html>
    <body>
        <p><span>Hello</span></p>
        <p><span class="world">World</span></p>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<p>Hello</p>' in html
    assert '<p><span class="world">World</span></p>' in html


def test_clean_default_style(tmpdir):
    data = """
<html>
    <body>
        <h2 style='padding-top:18pt;margin:0;color:#000000;padding-left:0;font-size:16pt;padding-bottom:6pt;line-height:1.15;page-break-after:avoid;font-family:"Arial";orphans:2;widows:2;text-align:left;padding-right:0'>Test</h2>
        <p style='padding:0;margin:0;color:#000000;font-size:11pt;font-family:"Arial";orphans:2;widows:2'><span>Hello</span></p>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<h2>Test</h2>' in html
    assert '<p>Hello</p>' in html


def test_add_anchors(tmpdir):
    data = """
<html>
    <body>
        <h2 id="anchor1">Test</h2>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<h2 id="anchor1"><a href="#anchor1">Test</a></h2>' in html


def test_clean_bold(tmpdir):
    data = """
<html>
    <body>
        <p><span>Hello</span> <span style="font-weight: 700">World</span></p>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<p>Hello <strong>World</strong></p>' in html


def test_warning(tmpdir):
    data = """
<html>
    <body>
        <p><strong>WARNING:</strong></p>
        <p>This is a warning</p>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<p class="badge warning"><strong>WARNING</strong><span>This is a warning</span></p>' in html


def test_clean_merge_code_block(tmpdir):
    data = """
<html>
    <body>
        <p><em class="code">Hello</em> <strong class="code">World</strong></p>
        <p class="code">42 <em class="code">test</em> root</p>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<p class="code"><em>Hello</em> <strong>World</strong><br>42 <em>test</em> root</p>' in html


def test_clean_merge_code_block_follow_br(tmpdir):
    """
    Empty <span><br><br></span> should be merge with previous block
    """
    data = """
<html>
    <body>
        <p><span class="code">Hello</span><span><br><br></span><span class="code">World</span></p>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<p class="code">Hello<br><br>World</p>' in html


def test_clean_strip_footnotes(tmpdir):
    """
    Comments are exported as footnotes we strip them
    """
    data = """
<html>
    <body>
        <p>Test<sup>a</sup></p>
        <div style="border:1px solid black;margin:5px">
            <p><a href="#cmnt_ref1" id="cmnt1">[a]</a>correct?</p>
        </div>
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert not '<sup>' in html
    assert not '<div style="border:1px solid black;margin:5px">' in html


def test_wrap_image(tmpdir):
    """
    Image have no style and transform to a link
    """
    data = """
<html>
    <body>
        <img src="test.html" style="test">
    </body>
</html>"""
    d = DriveDocument("42", "Test", data, str(tmpdir))
    html, files = d._process()
    assert '<a href="eac0a7ec83537763d3ba7671828d0989.jpg" target="_blank"><img src="eac0a7ec83537763d3ba7671828d0989.jpg"></a>' in html


def test_toc(tmpdir):
    data = """
<html>
<body>
<h1 id="l1">Header 1</h1>
<h2 id="l2">Header 2</h2>
<h3 id="l3">Header 3</h3>
</body>
</html>
    """
    document = DriveDocument('42', 'Test', data, str(tmpdir))
    assert document._get_toc() == [
        {'id': 'l1', 'text': 'Header 1', 'level': 1},
        {'id': 'l2', 'text': 'Header 2', 'level': 2},
        {'id': 'l3', 'text': 'Header 3', 'level': 3}
    ]


def test_export(tmpdir):
    data = """<html><body></body></html>"""
    document = DriveDocument('42', 'Test', data, str(tmpdir))
    document.export()
    assert pathlib.Path.exists(tmpdir / '42' / 'index.html')


def test_export_with_images(tmpdir):
    data = """<html>
    <body>
        <img src="http://example.org/test.jpg">
    </body>
    </html>"""
    with patch('drive.DriveDocument._download_url') as mock:
        document = DriveDocument('42', 'Test', data, str(tmpdir))
        document.export()
    assert pathlib.Path.exists(tmpdir / '42' / 'index.html')
    mock.assert_called_with('http://example.org/test.jpg', tmpdir / '42' / 'bd4e4a2bb655d3b56dc4a4e32dab2003.jpg')


