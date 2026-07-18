from scripts.validate_publication import Parser


def test_document_title_ignores_svg_titles():
    html = """<!doctype html><html><head><title>Document title</title></head>
    <body><svg><title>Accessible SVG title</title></svg></body></html>"""
    parser = Parser()
    parser.feed(html)
    assert parser.title_count == 1


def test_mermaid_detection_requires_mermaid_markup():
    ordinary = Parser()
    ordinary.feed('<html><head><title>Page</title></head><body><script>const marker="language-mermaid";</script></body></html>')
    assert ordinary.mermaid_blocks == 0

    diagram = Parser()
    diagram.feed('<html><head><title>Page</title></head><body><pre class="language-mermaid"><code class="language-mermaid">graph TD</code></pre></body></html>')
    assert diagram.mermaid_blocks >= 1
