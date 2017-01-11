from drive.utils import process_link, html_to_text


def test_process_link_external():
    assert process_link('https://www.google.com/url?q=https://example.com') == 'https://example.com'


def test_process_link_google_doc():
    assert process_link('https://www.google.com/url?q=https://docs.google.com/document/d/3BAA5rVGCNN-aaaaaaa/edit&sa=D&ust=xxxxxxx&usg=xxxxxxxxxx') == '/3BAA5rVGCNN-aaaaaaa/index.html'
    assert process_link('https://drive.google.com/open?id=6775678645356765678567afgb') == '/6775678645356765678567afgb/index.html'
    assert process_link('https://www.google.com/url?q=https://example.org') == 'https://example.org'


def test_html_to_text():
    text = html_to_text(
        """
        <html>
            <body>
                <h1>Hello</h1>
                <h2>World</h2>
                <p>Bonjour</p>
                <p>Le monde</p>
        </body>
        </html>
        """)
    assert text == 'Hello\n\nWorld\n\nBonjour\nLe monde'

    text = html_to_text(
        """
        <html>
            <body>
                <h1>Hello</h1>
                <p>World</p><div>Mister <a>Bond</a> and miss<br>Penny</div>
                <script>alert("Hello")</script>
                <ul>
                    <li>One</li>
                    <li>Two</li>
                </ul>
            </body>
        </html>
        """)
    assert text == 'Hello\n\nWorld\nMister Bond and miss\nPenny\n\n* One\n* Two'
