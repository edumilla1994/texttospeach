from ebooklib import epub

book = epub.EpubBook()
book.set_identifier('id123456')
book.set_title('Sample EPUB')
book.set_language('es')

c1 = epub.EpubHtml(title='Introducción', file_name='intro.xhtml', lang='es')
c1.content = '<h1>Introducción</h1><p>Este es el texto de la introducción.</p>'

c2 = epub.EpubHtml(title='Capítulo 1', file_name='chap1.xhtml', lang='es')
c2.content = '<h1>Capítulo 1</h1><p>Texto del capítulo 1.</p>'

book.add_item(c1)
book.add_item(c2)

book.toc = (epub.Link('intro.xhtml', 'Introducción', 'intro'),
            (epub.Section('Capítulos'), (c2,)))

book.spine = ['nav', c1, c2]

# Add default NCX and Nav files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

epub.write_epub('tests/sample.epub', book)
print('Sample EPUB creado en tests/sample.epub')
