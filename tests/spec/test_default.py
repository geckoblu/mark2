# pylint: skip-file
# fmt: off
"""Test spec examples for default HTML rendering.

This file is auto-generated from spec.txt.
Run generate_test_default.py to regenerate.
"""

import pytest
from markdown_it import MarkdownIt


@pytest.mark.spec
def test_example1():
    """Test example 1: foo baz  bim.

    Source: spec.txt lines 355-360
    """
    md = MarkdownIt()

    input_text = '\tfoo\tbaz\t\tbim'
    expected = '<pre><code>foo\tbaz\t\tbim\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example2():
    """Test example 2: foo baz  bim.

    Source: spec.txt lines 362-367
    """
    md = MarkdownIt()

    input_text = '  \tfoo\tbaz\t\tbim'
    expected = '<pre><code>foo\tbaz\t\tbim\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example3():
    """Test example 3: a a      a.

    Source: spec.txt lines 369-376
    """
    md = MarkdownIt()

    input_text = '    a\ta\n    ὐ\ta'
    expected = '<pre><code>a\ta\nὐ\ta\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example4():
    """Test example 4: foo   bar.

    Source: spec.txt lines 382-393
    """
    md = MarkdownIt()

    input_text = '  - foo\n\n\tbar'
    expected = '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example5():
    """Test example 5: foo    bar.

    Source: spec.txt lines 395-407
    """
    md = MarkdownIt()

    input_text = '- foo\n\n\t\tbar'
    expected = '<ul>\n<li>\n<p>foo</p>\n<pre><code>  bar\n</code></pre>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example6():
    """Test example 6: foo.

    Source: spec.txt lines 418-425
    """
    md = MarkdownIt()

    input_text = '>\t\tfoo'
    expected = '<blockquote>\n<pre><code>  foo\n</code></pre>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example7():
    """Test example 7: foo.

    Source: spec.txt lines 427-436
    """
    md = MarkdownIt()

    input_text = '-\t\tfoo'
    expected = '<ul>\n<li>\n<pre><code>  foo\n</code></pre>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example8():
    """Test example 8: foo  bar.

    Source: spec.txt lines 439-446
    """
    md = MarkdownIt()

    input_text = '    foo\n\tbar'
    expected = '<pre><code>foo\nbar\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example9():
    """Test example 9: foo     bar    baz.

    Source: spec.txt lines 448-464
    """
    md = MarkdownIt()

    input_text = ' - foo\n   - bar\n\t - baz'
    expected = '<ul>\n<li>foo\n<ul>\n<li>bar\n<ul>\n<li>baz</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example10():
    """Test example 10: Foo.

    Source: spec.txt lines 466-470
    """
    md = MarkdownIt()

    input_text = '#\tFoo'
    expected = '<h1>Foo</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example11():
    """Test example 11.

    Source: spec.txt lines 472-476
    """
    md = MarkdownIt()

    input_text = '*\t*\t*\t'
    expected = '<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example12():
    """Test example 12.

    Source: spec.txt lines 489-493
    """
    md = MarkdownIt()

    input_text = '\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^\\_\\`\\{\\|\\}\\~'
    expected = "<p>!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~</p>"

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example13():
    """Test example 13: Aa 3.

    Source: spec.txt lines 499-503
    """
    md = MarkdownIt()

    input_text = '\\\t\\A\\a\\ \\3\\φ\\«'
    expected = '<p>\\\t\\A\\a\\ \\3\\φ\\«</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example14():
    """Test example 14: not emphasized br not a tag not a link.

    Source: spec.txt lines 509-529
    """
    md = MarkdownIt()

    input_text = '\\*not emphasized*\n\\<br/> not a tag\n\\[not a link](/foo)\n\\`not code`\n1\\. not a list\n\\* not a list\n\\# not a heading\n\\[foo]: /url "not a reference"\n\\&ouml; not a character entity'
    expected = '<p>*not emphasized*\n&lt;br/&gt; not a tag\n[not a link](/foo)\n`not code`\n1. not a list\n* not a list\n# not a heading\n[foo]: /url &quot;not a reference&quot;\n&amp;ouml; not a character entity</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example15():
    """Test example 15: emphasis.

    Source: spec.txt lines 534-538
    """
    md = MarkdownIt()

    input_text = '\\\\*emphasis*'
    expected = '<p>\\<em>emphasis</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example16():
    """Test example 16: foo bar.

    Source: spec.txt lines 543-549
    """
    md = MarkdownIt()

    input_text = 'foo\\\nbar'
    expected = '<p>foo<br />\nbar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example17():
    """Test example 17.

    Source: spec.txt lines 555-559
    """
    md = MarkdownIt()

    input_text = '`` \\[\\` ``'
    expected = '<p><code>\\[\\`</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example18():
    """Test example 18.

    Source: spec.txt lines 562-567
    """
    md = MarkdownIt()

    input_text = '    \\[\\]'
    expected = '<pre><code>\\[\\]\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example19():
    """Test example 19.

    Source: spec.txt lines 570-577
    """
    md = MarkdownIt()

    input_text = '~~~\n\\[\\]\n~~~'
    expected = '<pre><code>\\[\\]\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example20():
    """Test example 20: httpsexamplecomfind.

    Source: spec.txt lines 580-584
    """
    md = MarkdownIt()

    input_text = '<https://example.com?find=\\*>'
    expected = '<p><a href="https://example.com?find=%5C*">https://example.com?find=\\*</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example21():
    """Test example 21: a hrefbar.

    Source: spec.txt lines 587-591
    """
    md = MarkdownIt()

    input_text = '<a href="/bar\\/)">'
    expected = '<a href="/bar\\/)">'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example22():
    """Test example 22: foobar title.

    Source: spec.txt lines 597-601
    """
    md = MarkdownIt()

    input_text = '[foo](/bar\\* "ti\\*tle")'
    expected = '<p><a href="/bar*" title="ti*tle">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example23():
    """Test example 23: foo  foo bar title.

    Source: spec.txt lines 604-610
    """
    md = MarkdownIt()

    input_text = '[foo]\n\n[foo]: /bar\\* "ti\\*tle"'
    expected = '<p><a href="/bar*" title="ti*tle">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example24():
    """Test example 24: foobar foo.

    Source: spec.txt lines 613-620
    """
    md = MarkdownIt()

    input_text = '``` foo\\+bar\nfoo\n```'
    expected = '<pre><code class="language-foo+bar">foo\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example25():
    """Test example 25: nbsp amp copy AElig Dcaron frac34 Hil.

    Source: spec.txt lines 649-657
    """
    md = MarkdownIt()

    input_text = '&nbsp; &amp; &copy; &AElig; &Dcaron;\n&frac34; &HilbertSpace; &DifferentialD;\n&ClockwiseContourIntegral; &ngE;'
    expected = '<p>\xa0 &amp; © Æ Ď\n¾ ℋ ⅆ\n∲ ≧̸</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example26():
    """Test example 26: 35 1234 992 0.

    Source: spec.txt lines 668-672
    """
    md = MarkdownIt()

    input_text = '&#35; &#1234; &#992; &#0;'
    expected = '<p># Ӓ Ϡ �</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example27():
    """Test example 27: X22 XD06 xcab.

    Source: spec.txt lines 681-685
    """
    md = MarkdownIt()

    input_text = '&#X22; &#XD06; &#xcab;'
    expected = '<p>&quot; ആ ಫ</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example28():
    """Test example 28: nbsp x  x 87654321 abcdef0 ThisIsN.

    Source: spec.txt lines 690-700
    """
    md = MarkdownIt()

    input_text = '&nbsp &x; &#; &#x;\n&#87654321;\n&#abcdef0;\n&ThisIsNotDefined; &hi?;'
    expected = '<p>&amp;nbsp &amp;x; &amp;#; &amp;#x;\n&amp;#87654321;\n&amp;#abcdef0;\n&amp;ThisIsNotDefined; &amp;hi?;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example29():
    """Test example 29: copy.

    Source: spec.txt lines 707-711
    """
    md = MarkdownIt()

    input_text = '&copy'
    expected = '<p>&amp;copy</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example30():
    """Test example 30: MadeUpEntity.

    Source: spec.txt lines 717-721
    """
    md = MarkdownIt()

    input_text = '&MadeUpEntity;'
    expected = '<p>&amp;MadeUpEntity;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example31():
    """Test example 31: a hrefoumloumlhtml.

    Source: spec.txt lines 728-732
    """
    md = MarkdownIt()

    input_text = '<a href="&ouml;&ouml;.html">'
    expected = '<a href="&ouml;&ouml;.html">'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example32():
    """Test example 32: foofoumlouml foumlouml.

    Source: spec.txt lines 735-739
    """
    md = MarkdownIt()

    input_text = '[foo](/f&ouml;&ouml; "f&ouml;&ouml;")'
    expected = '<p><a href="/f%C3%B6%C3%B6" title="föö">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example33():
    """Test example 33: foo  foo foumlouml foumlouml.

    Source: spec.txt lines 742-748
    """
    md = MarkdownIt()

    input_text = '[foo]\n\n[foo]: /f&ouml;&ouml; "f&ouml;&ouml;"'
    expected = '<p><a href="/f%C3%B6%C3%B6" title="föö">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example34():
    """Test example 34: foumlouml foo.

    Source: spec.txt lines 751-758
    """
    md = MarkdownIt()

    input_text = '``` f&ouml;&ouml;\nfoo\n```'
    expected = '<pre><code class="language-föö">foo\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example35():
    """Test example 35: foumlouml.

    Source: spec.txt lines 764-768
    """
    md = MarkdownIt()

    input_text = '`f&ouml;&ouml;`'
    expected = '<p><code>f&amp;ouml;&amp;ouml;</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example36():
    """Test example 36: foumlfouml.

    Source: spec.txt lines 771-776
    """
    md = MarkdownIt()

    input_text = '    f&ouml;f&ouml;'
    expected = '<pre><code>f&amp;ouml;f&amp;ouml;\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example37():
    """Test example 37: 42foo42 foo.

    Source: spec.txt lines 783-789
    """
    md = MarkdownIt()

    input_text = '&#42;foo&#42;\n*foo*'
    expected = '<p>*foo*\n<em>foo</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example38():
    """Test example 38: 42 foo   foo.

    Source: spec.txt lines 791-800
    """
    md = MarkdownIt()

    input_text = '&#42; foo\n\n* foo'
    expected = '<p>* foo</p>\n<ul>\n<li>foo</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example39():
    """Test example 39: foo1010bar.

    Source: spec.txt lines 802-808
    """
    md = MarkdownIt()

    input_text = 'foo&#10;&#10;bar'
    expected = '<p>foo\n\nbar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example40():
    """Test example 40: 9foo.

    Source: spec.txt lines 810-814
    """
    md = MarkdownIt()

    input_text = '&#9;foo'
    expected = '<p>\tfoo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example41():
    """Test example 41: aurl quottitquot.

    Source: spec.txt lines 817-821
    """
    md = MarkdownIt()

    input_text = '[a](url &quot;tit&quot;)'
    expected = '<p>[a](url &quot;tit&quot;)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example42():
    """Test example 42: one  two.

    Source: spec.txt lines 840-848
    """
    md = MarkdownIt()

    input_text = '- `one\n- two`'
    expected = '<ul>\n<li>`one</li>\n<li>two`</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example43():
    """Test example 43.

    Source: spec.txt lines 879-887
    """
    md = MarkdownIt()

    input_text = '***\n---\n___'
    expected = '<hr />\n<hr />\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example44():
    """Test example 44.

    Source: spec.txt lines 892-896
    """
    md = MarkdownIt()

    input_text = '+++'
    expected = '<p>+++</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example45():
    """Test example 45.

    Source: spec.txt lines 899-903
    """
    md = MarkdownIt()

    input_text = '==='
    expected = '<p>===</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example46():
    """Test example 46.

    Source: spec.txt lines 908-916
    """
    md = MarkdownIt()

    input_text = '--\n**\n__'
    expected = '<p>--\n**\n__</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example47():
    """Test example 47.

    Source: spec.txt lines 921-929
    """
    md = MarkdownIt()

    input_text = ' ***\n  ***\n   ***'
    expected = '<hr />\n<hr />\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example48():
    """Test example 48.

    Source: spec.txt lines 934-939
    """
    md = MarkdownIt()

    input_text = '    ***'
    expected = '<pre><code>***\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example49():
    """Test example 49: Foo.

    Source: spec.txt lines 942-948
    """
    md = MarkdownIt()

    input_text = 'Foo\n    ***'
    expected = '<p>Foo\n***</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example50():
    """Test example 50.

    Source: spec.txt lines 953-957
    """
    md = MarkdownIt()

    input_text = '_____________________________________'
    expected = '<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example51():
    """Test example 51.

    Source: spec.txt lines 962-966
    """
    md = MarkdownIt()

    input_text = ' - - -'
    expected = '<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example52():
    """Test example 52.

    Source: spec.txt lines 969-973
    """
    md = MarkdownIt()

    input_text = ' **  * ** * ** * **'
    expected = '<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example53():
    """Test example 53.

    Source: spec.txt lines 976-980
    """
    md = MarkdownIt()

    input_text = '-     -      -      -'
    expected = '<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example54():
    """Test example 54.

    Source: spec.txt lines 985-989
    """
    md = MarkdownIt()

    input_text = '- - - -    '
    expected = '<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example55():
    """Test example 55: a  a  a.

    Source: spec.txt lines 994-1004
    """
    md = MarkdownIt()

    input_text = '_ _ _ _ a\n\na------\n\n---a---'
    expected = '<p>_ _ _ _ a</p>\n<p>a------</p>\n<p>---a---</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example56():
    """Test example 56.

    Source: spec.txt lines 1010-1014
    """
    md = MarkdownIt()

    input_text = ' *-*'
    expected = '<p><em>-</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example57():
    """Test example 57: foo   bar.

    Source: spec.txt lines 1019-1031
    """
    md = MarkdownIt()

    input_text = '- foo\n***\n- bar'
    expected = '<ul>\n<li>foo</li>\n</ul>\n<hr />\n<ul>\n<li>bar</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example58():
    """Test example 58: Foo  bar.

    Source: spec.txt lines 1036-1044
    """
    md = MarkdownIt()

    input_text = 'Foo\n***\nbar'
    expected = '<p>Foo</p>\n<hr />\n<p>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example59():
    """Test example 59: Foo  bar.

    Source: spec.txt lines 1053-1060
    """
    md = MarkdownIt()

    input_text = 'Foo\n---\nbar'
    expected = '<h2>Foo</h2>\n<p>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example60():
    """Test example 60: Foo     Bar.

    Source: spec.txt lines 1066-1078
    """
    md = MarkdownIt()

    input_text = '* Foo\n* * *\n* Bar'
    expected = '<ul>\n<li>Foo</li>\n</ul>\n<hr />\n<ul>\n<li>Bar</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example61():
    """Test example 61: Foo.

    Source: spec.txt lines 1083-1093
    """
    md = MarkdownIt()

    input_text = '- Foo\n- * * *'
    expected = '<ul>\n<li>Foo</li>\n<li>\n<hr />\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example62():
    """Test example 62: foo  foo  foo  foo  foo  foo.

    Source: spec.txt lines 1112-1126
    """
    md = MarkdownIt()

    input_text = '# foo\n## foo\n### foo\n#### foo\n##### foo\n###### foo'
    expected = '<h1>foo</h1>\n<h2>foo</h2>\n<h3>foo</h3>\n<h4>foo</h4>\n<h5>foo</h5>\n<h6>foo</h6>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example63():
    """Test example 63: foo.

    Source: spec.txt lines 1131-1135
    """
    md = MarkdownIt()

    input_text = '####### foo'
    expected = '<p>####### foo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example64():
    """Test example 64: 5 bolt  hashtag.

    Source: spec.txt lines 1146-1153
    """
    md = MarkdownIt()

    input_text = '#5 bolt\n\n#hashtag'
    expected = '<p>#5 bolt</p>\n<p>#hashtag</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example65():
    """Test example 65: foo.

    Source: spec.txt lines 1158-1162
    """
    md = MarkdownIt()

    input_text = '\\## foo'
    expected = '<p>## foo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example66():
    """Test example 66: foo bar baz.

    Source: spec.txt lines 1167-1171
    """
    md = MarkdownIt()

    input_text = '# foo *bar* \\*baz\\*'
    expected = '<h1>foo <em>bar</em> *baz*</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example67():
    """Test example 67: foo.

    Source: spec.txt lines 1176-1180
    """
    md = MarkdownIt()

    input_text = '#                  foo                     '
    expected = '<h1>foo</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example68():
    """Test example 68: foo    foo     foo.

    Source: spec.txt lines 1185-1193
    """
    md = MarkdownIt()

    input_text = ' ### foo\n  ## foo\n   # foo'
    expected = '<h3>foo</h3>\n<h2>foo</h2>\n<h1>foo</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example69():
    """Test example 69: foo.

    Source: spec.txt lines 1198-1203
    """
    md = MarkdownIt()

    input_text = '    # foo'
    expected = '<pre><code># foo\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example70():
    """Test example 70: foo      bar.

    Source: spec.txt lines 1206-1212
    """
    md = MarkdownIt()

    input_text = 'foo\n    # bar'
    expected = '<p>foo\n# bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example71():
    """Test example 71: foo       bar.

    Source: spec.txt lines 1217-1223
    """
    md = MarkdownIt()

    input_text = '## foo ##\n  ###   bar    ###'
    expected = '<h2>foo</h2>\n<h3>bar</h3>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example72():
    """Test example 72: foo   foo.

    Source: spec.txt lines 1228-1234
    """
    md = MarkdownIt()

    input_text = '# foo ##################################\n##### foo ##'
    expected = '<h1>foo</h1>\n<h5>foo</h5>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example73():
    """Test example 73: foo.

    Source: spec.txt lines 1239-1243
    """
    md = MarkdownIt()

    input_text = '### foo ###     '
    expected = '<h3>foo</h3>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example74():
    """Test example 74: foo  b.

    Source: spec.txt lines 1250-1254
    """
    md = MarkdownIt()

    input_text = '### foo ### b'
    expected = '<h3>foo ### b</h3>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example75():
    """Test example 75: foo.

    Source: spec.txt lines 1259-1263
    """
    md = MarkdownIt()

    input_text = '# foo#'
    expected = '<h1>foo#</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example76():
    """Test example 76: foo   foo   foo.

    Source: spec.txt lines 1269-1277
    """
    md = MarkdownIt()

    input_text = '### foo \\###\n## foo #\\##\n# foo \\#'
    expected = '<h3>foo ###</h3>\n<h2>foo ###</h2>\n<h1>foo #</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example77():
    """Test example 77: foo.

    Source: spec.txt lines 1283-1291
    """
    md = MarkdownIt()

    input_text = '****\n## foo\n****'
    expected = '<hr />\n<h2>foo</h2>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example78():
    """Test example 78: Foo bar  baz Bar foo.

    Source: spec.txt lines 1294-1302
    """
    md = MarkdownIt()

    input_text = 'Foo bar\n# baz\nBar foo'
    expected = '<p>Foo bar</p>\n<h1>baz</h1>\n<p>Bar foo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example79():
    """Test example 79.

    Source: spec.txt lines 1307-1315
    """
    md = MarkdownIt()

    input_text = '## \n#\n### ###'
    expected = '<h2></h2>\n<h1></h1>\n<h3></h3>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example80():
    """Test example 80: Foo bar   Foo bar.

    Source: spec.txt lines 1347-1356
    """
    md = MarkdownIt()

    input_text = 'Foo *bar*\n=========\n\nFoo *bar*\n---------'
    expected = '<h1>Foo <em>bar</em></h1>\n<h2>Foo <em>bar</em></h2>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example81():
    """Test example 81: Foo bar baz.

    Source: spec.txt lines 1361-1368
    """
    md = MarkdownIt()

    input_text = 'Foo *bar\nbaz*\n===='
    expected = '<h1>Foo <em>bar\nbaz</em></h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example82():
    """Test example 82: Foo bar baz.

    Source: spec.txt lines 1375-1382
    """
    md = MarkdownIt()

    input_text = '  Foo *bar\nbaz*\t\n===='
    expected = '<h1>Foo <em>bar\nbaz</em></h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example83():
    """Test example 83: Foo   Foo.

    Source: spec.txt lines 1387-1396
    """
    md = MarkdownIt()

    input_text = 'Foo\n-------------------------\n\nFoo\n='
    expected = '<h2>Foo</h2>\n<h1>Foo</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example84():
    """Test example 84: Foo     Foo     Foo.

    Source: spec.txt lines 1402-1415
    """
    md = MarkdownIt()

    input_text = '   Foo\n---\n\n  Foo\n-----\n\n  Foo\n  ==='
    expected = '<h2>Foo</h2>\n<h2>Foo</h2>\n<h1>Foo</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example85():
    """Test example 85: Foo           Foo.

    Source: spec.txt lines 1420-1433
    """
    md = MarkdownIt()

    input_text = '    Foo\n    ---\n\n    Foo\n---'
    expected = '<pre><code>Foo\n---\n\nFoo\n</code></pre>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example86():
    """Test example 86: Foo.

    Source: spec.txt lines 1439-1444
    """
    md = MarkdownIt()

    input_text = 'Foo\n   ----      '
    expected = '<h2>Foo</h2>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example87():
    """Test example 87: Foo.

    Source: spec.txt lines 1449-1455
    """
    md = MarkdownIt()

    input_text = 'Foo\n    ---'
    expected = '<p>Foo\n---</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example88():
    """Test example 88: Foo    Foo.

    Source: spec.txt lines 1460-1471
    """
    md = MarkdownIt()

    input_text = 'Foo\n= =\n\nFoo\n--- -'
    expected = '<p>Foo\n= =</p>\n<p>Foo</p>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example89():
    """Test example 89: Foo.

    Source: spec.txt lines 1476-1481
    """
    md = MarkdownIt()

    input_text = 'Foo  \n-----'
    expected = '<h2>Foo</h2>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example90():
    """Test example 90: Foo.

    Source: spec.txt lines 1486-1491
    """
    md = MarkdownIt()

    input_text = 'Foo\\\n----'
    expected = '<h2>Foo\\</h2>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example91():
    """Test example 91: Foo    a titlea lot  of dashes.

    Source: spec.txt lines 1497-1510
    """
    md = MarkdownIt()

    input_text = '`Foo\n----\n`\n\n<a title="a lot\n---\nof dashes"/>'
    expected = '<h2>`Foo</h2>\n<p>`</p>\n<h2>&lt;a title=&quot;a lot</h2>\n<p>of dashes&quot;/&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example92():
    """Test example 92: Foo.

    Source: spec.txt lines 1516-1524
    """
    md = MarkdownIt()

    input_text = '> Foo\n---'
    expected = '<blockquote>\n<p>Foo</p>\n</blockquote>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example93():
    """Test example 93: foo bar.

    Source: spec.txt lines 1527-1537
    """
    md = MarkdownIt()

    input_text = '> foo\nbar\n==='
    expected = '<blockquote>\n<p>foo\nbar\n===</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example94():
    """Test example 94: Foo.

    Source: spec.txt lines 1540-1548
    """
    md = MarkdownIt()

    input_text = '- Foo\n---'
    expected = '<ul>\n<li>Foo</li>\n</ul>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example95():
    """Test example 95: Foo Bar.

    Source: spec.txt lines 1555-1562
    """
    md = MarkdownIt()

    input_text = 'Foo\nBar\n---'
    expected = '<h2>Foo\nBar</h2>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example96():
    """Test example 96: Foo  Bar  Baz.

    Source: spec.txt lines 1568-1580
    """
    md = MarkdownIt()

    input_text = '---\nFoo\n---\nBar\n---\nBaz'
    expected = '<hr />\n<h2>Foo</h2>\n<h2>Bar</h2>\n<p>Baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example97():
    """Test example 97.

    Source: spec.txt lines 1585-1590
    """
    md = MarkdownIt()

    input_text = '\n===='
    expected = '<p>====</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example98():
    """Test example 98.

    Source: spec.txt lines 1597-1603
    """
    md = MarkdownIt()

    input_text = '---\n---'
    expected = '<hr />\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example99():
    """Test example 99: foo.

    Source: spec.txt lines 1606-1614
    """
    md = MarkdownIt()

    input_text = '- foo\n-----'
    expected = '<ul>\n<li>foo</li>\n</ul>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example100():
    """Test example 100: foo.

    Source: spec.txt lines 1617-1624
    """
    md = MarkdownIt()

    input_text = '    foo\n---'
    expected = '<pre><code>foo\n</code></pre>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example101():
    """Test example 101: foo.

    Source: spec.txt lines 1627-1635
    """
    md = MarkdownIt()

    input_text = '> foo\n-----'
    expected = '<blockquote>\n<p>foo</p>\n</blockquote>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example102():
    """Test example 102: foo.

    Source: spec.txt lines 1641-1646
    """
    md = MarkdownIt()

    input_text = '\\> foo\n------'
    expected = '<h2>&gt; foo</h2>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example103():
    """Test example 103: Foo  bar  baz.

    Source: spec.txt lines 1672-1682
    """
    md = MarkdownIt()

    input_text = 'Foo\n\nbar\n---\nbaz'
    expected = '<p>Foo</p>\n<h2>bar</h2>\n<p>baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example104():
    """Test example 104: Foo bar    baz.

    Source: spec.txt lines 1688-1700
    """
    md = MarkdownIt()

    input_text = 'Foo\nbar\n\n---\n\nbaz'
    expected = '<p>Foo\nbar</p>\n<hr />\n<p>baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example105():
    """Test example 105: Foo bar    baz.

    Source: spec.txt lines 1706-1716
    """
    md = MarkdownIt()

    input_text = 'Foo\nbar\n* * *\nbaz'
    expected = '<p>Foo\nbar</p>\n<hr />\n<p>baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example106():
    """Test example 106: Foo bar  baz.

    Source: spec.txt lines 1721-1731
    """
    md = MarkdownIt()

    input_text = 'Foo\nbar\n\\---\nbaz'
    expected = '<p>Foo\nbar\n---\nbaz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example107():
    """Test example 107: a simple       indented code block.

    Source: spec.txt lines 1749-1756
    """
    md = MarkdownIt()

    input_text = '    a simple\n      indented code block'
    expected = '<pre><code>a simple\n  indented code block\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example108():
    """Test example 108: foo      bar.

    Source: spec.txt lines 1763-1774
    """
    md = MarkdownIt()

    input_text = '  - foo\n\n    bar'
    expected = '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example109():
    """Test example 109: 1  foo       bar.

    Source: spec.txt lines 1777-1790
    """
    md = MarkdownIt()

    input_text = '1.  foo\n\n    - bar'
    expected = '<ol>\n<li>\n<p>foo</p>\n<ul>\n<li>bar</li>\n</ul>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example110():
    """Test example 110: a     hi       one.

    Source: spec.txt lines 1797-1808
    """
    md = MarkdownIt()

    input_text = '    <a/>\n    *hi*\n\n    - one'
    expected = '<pre><code>&lt;a/&gt;\n*hi*\n\n- one\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example111():
    """Test example 111: chunk1      chunk2            chunk3.

    Source: spec.txt lines 1813-1830
    """
    md = MarkdownIt()

    input_text = '    chunk1\n\n    chunk2\n  \n \n \n    chunk3'
    expected = '<pre><code>chunk1\n\nchunk2\n\n\n\nchunk3\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example112():
    """Test example 112: chunk1              chunk2.

    Source: spec.txt lines 1836-1845
    """
    md = MarkdownIt()

    input_text = '    chunk1\n      \n      chunk2'
    expected = '<pre><code>chunk1\n  \n  chunk2\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example113():
    """Test example 113: Foo     bar.

    Source: spec.txt lines 1851-1858
    """
    md = MarkdownIt()

    input_text = 'Foo\n    bar\n'
    expected = '<p>Foo\nbar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example114():
    """Test example 114: foo bar.

    Source: spec.txt lines 1865-1872
    """
    md = MarkdownIt()

    input_text = '    foo\nbar'
    expected = '<pre><code>foo\n</code></pre>\n<p>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example115():
    """Test example 115: Heading     foo Heading      foo.

    Source: spec.txt lines 1878-1893
    """
    md = MarkdownIt()

    input_text = '# Heading\n    foo\nHeading\n------\n    foo\n----'
    expected = '<h1>Heading</h1>\n<pre><code>foo\n</code></pre>\n<h2>Heading</h2>\n<pre><code>foo\n</code></pre>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example116():
    """Test example 116: foo     bar.

    Source: spec.txt lines 1898-1905
    """
    md = MarkdownIt()

    input_text = '        foo\n    bar'
    expected = '<pre><code>    foo\nbar\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example117():
    """Test example 117: foo.

    Source: spec.txt lines 1911-1920
    """
    md = MarkdownIt()

    input_text = '\n    \n    foo\n    \n'
    expected = '<pre><code>foo\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example118():
    """Test example 118: foo.

    Source: spec.txt lines 1925-1930
    """
    md = MarkdownIt()

    input_text = '    foo  '
    expected = '<pre><code>foo  \n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example119():
    """Test example 119.

    Source: spec.txt lines 1980-1989
    """
    md = MarkdownIt()

    input_text = '```\n<\n >\n```'
    expected = '<pre><code>&lt;\n &gt;\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example120():
    """Test example 120.

    Source: spec.txt lines 1994-2003
    """
    md = MarkdownIt()

    input_text = '~~~\n<\n >\n~~~'
    expected = '<pre><code>&lt;\n &gt;\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example121():
    """Test example 121: foo.

    Source: spec.txt lines 2007-2013
    """
    md = MarkdownIt()

    input_text = '``\nfoo\n``'
    expected = '<p><code>foo</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example122():
    """Test example 122: aaa.

    Source: spec.txt lines 2018-2027
    """
    md = MarkdownIt()

    input_text = '```\naaa\n~~~\n```'
    expected = '<pre><code>aaa\n~~~\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example123():
    """Test example 123: aaa.

    Source: spec.txt lines 2030-2039
    """
    md = MarkdownIt()

    input_text = '~~~\naaa\n```\n~~~'
    expected = '<pre><code>aaa\n```\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example124():
    """Test example 124: aaa.

    Source: spec.txt lines 2044-2053
    """
    md = MarkdownIt()

    input_text = '````\naaa\n```\n``````'
    expected = '<pre><code>aaa\n```\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example125():
    """Test example 125: aaa.

    Source: spec.txt lines 2056-2065
    """
    md = MarkdownIt()

    input_text = '~~~~\naaa\n~~~\n~~~~'
    expected = '<pre><code>aaa\n~~~\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example126():
    """Test example 126.

    Source: spec.txt lines 2071-2075
    """
    md = MarkdownIt()

    input_text = '```'
    expected = '<pre><code></code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example127():
    """Test example 127: aaa.

    Source: spec.txt lines 2078-2088
    """
    md = MarkdownIt()

    input_text = '`````\n\n```\naaa'
    expected = '<pre><code>\n```\naaa\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example128():
    """Test example 128: aaa  bbb.

    Source: spec.txt lines 2091-2102
    """
    md = MarkdownIt()

    input_text = '> ```\n> aaa\n\nbbb'
    expected = '<blockquote>\n<pre><code>aaa\n</code></pre>\n</blockquote>\n<p>bbb</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example129():
    """Test example 129.

    Source: spec.txt lines 2107-2116
    """
    md = MarkdownIt()

    input_text = '```\n\n  \n```'
    expected = '<pre><code>\n  \n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example130():
    """Test example 130.

    Source: spec.txt lines 2121-2126
    """
    md = MarkdownIt()

    input_text = '```\n```'
    expected = '<pre><code></code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example131():
    """Test example 131: aaa aaa.

    Source: spec.txt lines 2133-2142
    """
    md = MarkdownIt()

    input_text = ' ```\n aaa\naaa\n```'
    expected = '<pre><code>aaa\naaa\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example132():
    """Test example 132: aaa   aaa aaa.

    Source: spec.txt lines 2145-2156
    """
    md = MarkdownIt()

    input_text = '  ```\naaa\n  aaa\naaa\n  ```'
    expected = '<pre><code>aaa\naaa\naaa\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example133():
    """Test example 133: aaa     aaa   aaa.

    Source: spec.txt lines 2159-2170
    """
    md = MarkdownIt()

    input_text = '   ```\n   aaa\n    aaa\n  aaa\n   ```'
    expected = '<pre><code>aaa\n aaa\naaa\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example134():
    """Test example 134: aaa.

    Source: spec.txt lines 2175-2184
    """
    md = MarkdownIt()

    input_text = '    ```\n    aaa\n    ```'
    expected = '<pre><code>```\naaa\n```\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example135():
    """Test example 135: aaa.

    Source: spec.txt lines 2190-2197
    """
    md = MarkdownIt()

    input_text = '```\naaa\n  ```'
    expected = '<pre><code>aaa\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example136():
    """Test example 136: aaa.

    Source: spec.txt lines 2200-2207
    """
    md = MarkdownIt()

    input_text = '   ```\naaa\n  ```'
    expected = '<pre><code>aaa\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example137():
    """Test example 137: aaa.

    Source: spec.txt lines 2212-2220
    """
    md = MarkdownIt()

    input_text = '```\naaa\n    ```'
    expected = '<pre><code>aaa\n    ```\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example138():
    """Test example 138: aaa.

    Source: spec.txt lines 2226-2232
    """
    md = MarkdownIt()

    input_text = '``` ```\naaa'
    expected = '<p><code> </code>\naaa</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example139():
    """Test example 139: aaa.

    Source: spec.txt lines 2235-2243
    """
    md = MarkdownIt()

    input_text = '~~~~~~\naaa\n~~~ ~~'
    expected = '<pre><code>aaa\n~~~ ~~\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example140():
    """Test example 140: foo  bar  baz.

    Source: spec.txt lines 2249-2260
    """
    md = MarkdownIt()

    input_text = 'foo\n```\nbar\n```\nbaz'
    expected = '<p>foo</p>\n<pre><code>bar\n</code></pre>\n<p>baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example141():
    """Test example 141: foo   bar   baz.

    Source: spec.txt lines 2266-2278
    """
    md = MarkdownIt()

    input_text = 'foo\n---\n~~~\nbar\n~~~\n# baz'
    expected = '<h2>foo</h2>\n<pre><code>bar\n</code></pre>\n<h1>baz</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example142():
    """Test example 142: ruby def foox   return 3 end.

    Source: spec.txt lines 2288-2299
    """
    md = MarkdownIt()

    input_text = '```ruby\ndef foo(x)\n  return 3\nend\n```'
    expected = '<pre><code class="language-ruby">def foo(x)\n  return 3\nend\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example143():
    """Test example 143: ruby startline3  def foox   return.

    Source: spec.txt lines 2302-2313
    """
    md = MarkdownIt()

    input_text = '~~~~    ruby startline=3 $%@#$\ndef foo(x)\n  return 3\nend\n~~~~~~~'
    expected = '<pre><code class="language-ruby">def foo(x)\n  return 3\nend\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example144():
    """Test example 144.

    Source: spec.txt lines 2316-2321
    """
    md = MarkdownIt()

    input_text = '````;\n````'
    expected = '<pre><code class="language-;"></code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example145():
    """Test example 145: aa  foo.

    Source: spec.txt lines 2326-2332
    """
    md = MarkdownIt()

    input_text = '``` aa ```\nfoo'
    expected = '<p><code>aa</code>\nfoo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example146():
    """Test example 146: aa   foo.

    Source: spec.txt lines 2337-2344
    """
    md = MarkdownIt()

    input_text = '~~~ aa ``` ~~~\nfoo\n~~~'
    expected = '<pre><code class="language-aa">foo\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example147():
    """Test example 147: aaa.

    Source: spec.txt lines 2349-2356
    """
    md = MarkdownIt()

    input_text = '```\n``` aaa\n```'
    expected = '<pre><code>``` aaa\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example148():
    """Test example 148: tabletrtd pre Hello  world pre.

    Source: spec.txt lines 2429-2444
    """
    md = MarkdownIt()

    input_text = '<table><tr><td>\n<pre>\n**Hello**,\n\n_world_.\n</pre>\n</td></tr></table>'
    expected = '<table><tr><td>\n<pre>\n**Hello**,\n<p><em>world</em>.\n</pre></p>\n</td></tr></table>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example149():
    """Test example 149: table   tr     td            hi     td.

    Source: spec.txt lines 2458-2477
    """
    md = MarkdownIt()

    input_text = '<table>\n  <tr>\n    <td>\n           hi\n    </td>\n  </tr>\n</table>\n\nokay.'
    expected = '<table>\n  <tr>\n    <td>\n           hi\n    </td>\n  </tr>\n</table>\n<p>okay.</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example150():
    """Test example 150: div   hello          fooa.

    Source: spec.txt lines 2480-2488
    """
    md = MarkdownIt()

    input_text = ' <div>\n  *hello*\n         <foo><a>'
    expected = ' <div>\n  *hello*\n         <foo><a>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example151():
    """Test example 151: div foo.

    Source: spec.txt lines 2493-2499
    """
    md = MarkdownIt()

    input_text = '</div>\n*foo*'
    expected = '</div>\n*foo*'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example152():
    """Test example 152: DIV CLASSfoo  Markdown  DIV.

    Source: spec.txt lines 2504-2514
    """
    md = MarkdownIt()

    input_text = '<DIV CLASS="foo">\n\n*Markdown*\n\n</DIV>'
    expected = '<DIV CLASS="foo">\n<p><em>Markdown</em></p>\n</DIV>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example153():
    """Test example 153: div idfoo   classbar div.

    Source: spec.txt lines 2520-2528
    """
    md = MarkdownIt()

    input_text = '<div id="foo"\n  class="bar">\n</div>'
    expected = '<div id="foo"\n  class="bar">\n</div>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example154():
    """Test example 154: div idfoo classbar   baz div.

    Source: spec.txt lines 2531-2539
    """
    md = MarkdownIt()

    input_text = '<div id="foo" class="bar\n  baz">\n</div>'
    expected = '<div id="foo" class="bar\n  baz">\n</div>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example155():
    """Test example 155: div foo  bar.

    Source: spec.txt lines 2543-2552
    """
    md = MarkdownIt()

    input_text = '<div>\n*foo*\n\n*bar*'
    expected = '<div>\n*foo*\n<p><em>bar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example156():
    """Test example 156: div idfoo hi.

    Source: spec.txt lines 2559-2565
    """
    md = MarkdownIt()

    input_text = '<div id="foo"\n*hi*'
    expected = '<div id="foo"\n*hi*'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example157():
    """Test example 157: div class foo.

    Source: spec.txt lines 2568-2574
    """
    md = MarkdownIt()

    input_text = '<div class\nfoo'
    expected = '<div class\nfoo'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example158():
    """Test example 158: div  foo.

    Source: spec.txt lines 2580-2586
    """
    md = MarkdownIt()

    input_text = '<div *???-&&&-<---\n*foo*'
    expected = '<div *???-&&&-<---\n*foo*'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example159():
    """Test example 159: diva hrefbarfooadiv.

    Source: spec.txt lines 2592-2596
    """
    md = MarkdownIt()

    input_text = '<div><a href="bar">*foo*</a></div>'
    expected = '<div><a href="bar">*foo*</a></div>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example160():
    """Test example 160: tabletrtd foo tdtrtable.

    Source: spec.txt lines 2599-2607
    """
    md = MarkdownIt()

    input_text = '<table><tr><td>\nfoo\n</td></tr></table>'
    expected = '<table><tr><td>\nfoo\n</td></tr></table>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example161():
    """Test example 161: divdiv  c int x  33.

    Source: spec.txt lines 2616-2626
    """
    md = MarkdownIt()

    input_text = '<div></div>\n``` c\nint x = 33;\n```'
    expected = '<div></div>\n``` c\nint x = 33;\n```'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example162():
    """Test example 162: div  not quoted text.

    Source: spec.txt lines 2629-2635
    """
    md = MarkdownIt()

    input_text = '<div\n> not quoted text'
    expected = '<div\n> not quoted text'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example163():
    """Test example 163: a hreffoo bar a.

    Source: spec.txt lines 2642-2650
    """
    md = MarkdownIt()

    input_text = '<a href="foo">\n*bar*\n</a>'
    expected = '<a href="foo">\n*bar*\n</a>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example164():
    """Test example 164: Warning bar Warning.

    Source: spec.txt lines 2655-2663
    """
    md = MarkdownIt()

    input_text = '<Warning>\n*bar*\n</Warning>'
    expected = '<Warning>\n*bar*\n</Warning>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example165():
    """Test example 165: i classfoo bar i.

    Source: spec.txt lines 2666-2674
    """
    md = MarkdownIt()

    input_text = '<i class="foo">\n*bar*\n</i>'
    expected = '<i class="foo">\n*bar*\n</i>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example166():
    """Test example 166: ins bar.

    Source: spec.txt lines 2677-2683
    """
    md = MarkdownIt()

    input_text = '</ins>\n*bar*'
    expected = '</ins>\n*bar*'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example167():
    """Test example 167: del foo del.

    Source: spec.txt lines 2692-2700
    """
    md = MarkdownIt()

    input_text = '<del>\n*foo*\n</del>'
    expected = '<del>\n*foo*\n</del>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example168():
    """Test example 168: del  foo  del.

    Source: spec.txt lines 2707-2717
    """
    md = MarkdownIt()

    input_text = '<del>\n\n*foo*\n\n</del>'
    expected = '<del>\n<p><em>foo</em></p>\n</del>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example169():
    """Test example 169: delfoodel.

    Source: spec.txt lines 2725-2729
    """
    md = MarkdownIt()

    input_text = '<del>*foo*</del>'
    expected = '<p><del><em>foo</em></del></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example170():
    """Test example 170: del classfoo foo del.

    Source: spec.txt lines 2731-2741
    """
    md = MarkdownIt()

    input_text = '<del\nclass="foo">\n*foo*\n</del>'
    expected = '<p><del\nclass="foo">\n<em>foo</em>\n</del></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example171():
    """Test example 171: pre languagehaskellcode import TextHTMLTa.

    Source: spec.txt lines 2753-2769
    """
    md = MarkdownIt()

    input_text = '<pre language="haskell"><code>\nimport Text.HTML.TagSoup\n\nmain :: IO ()\nmain = print $ parseTags tags\n</code></pre>\nokay'
    expected = '<pre language="haskell"><code>\nimport Text.HTML.TagSoup\n\nmain :: IO ()\nmain = print $ parseTags tags\n</code></pre>\n<p>okay</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example172():
    """Test example 172: script typetextjavascript  JavaScript exam.

    Source: spec.txt lines 2774-2788
    """
    md = MarkdownIt()

    input_text = '<script type="text/javascript">\n// JavaScript example\n\ndocument.getElementById("demo").innerHTML = "Hello JavaScript!";\n</script>\nokay'
    expected = '<script type="text/javascript">\n// JavaScript example\n\ndocument.getElementById("demo").innerHTML = "Hello JavaScript!";\n</script>\n<p>okay</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example173():
    """Test example 173: textarea  foo  bar  textarea.

    Source: spec.txt lines 2793-2809
    """
    md = MarkdownIt()

    input_text = '<textarea>\n\n*foo*\n\n_bar_\n\n</textarea>'
    expected = '<textarea>\n\n*foo*\n\n_bar_\n\n</textarea>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example174():
    """Test example 174: style   typetextcss h1 colorred  p colo.

    Source: spec.txt lines 2813-2829
    """
    md = MarkdownIt()

    input_text = '<style\n  type="text/css">\nh1 {color:red;}\n\np {color:blue;}\n</style>\nokay'
    expected = '<style\n  type="text/css">\nh1 {color:red;}\n\np {color:blue;}\n</style>\n<p>okay</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example175():
    """Test example 175: style   typetextcss  foo.

    Source: spec.txt lines 2836-2846
    """
    md = MarkdownIt()

    input_text = '<style\n  type="text/css">\n\nfoo'
    expected = '<style\n  type="text/css">\n\nfoo'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example176():
    """Test example 176: div  foo  bar.

    Source: spec.txt lines 2849-2860
    """
    md = MarkdownIt()

    input_text = '> <div>\n> foo\n\nbar'
    expected = '<blockquote>\n<div>\nfoo\n</blockquote>\n<p>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example177():
    """Test example 177: div  foo.

    Source: spec.txt lines 2863-2873
    """
    md = MarkdownIt()

    input_text = '- <div>\n- foo'
    expected = '<ul>\n<li>\n<div>\n</li>\n<li>foo</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example178():
    """Test example 178: stylepcolorredstyle foo.

    Source: spec.txt lines 2878-2884
    """
    md = MarkdownIt()

    input_text = '<style>p{color:red;}</style>\n*foo*'
    expected = '<style>p{color:red;}</style>\n<p><em>foo</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example179():
    """Test example 179: foo bar baz.

    Source: spec.txt lines 2887-2893
    """
    md = MarkdownIt()

    input_text = '<!-- foo -->*bar*\n*baz*'
    expected = '<!-- foo -->*bar*\n<p><em>baz</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example180():
    """Test example 180: script foo script1 bar.

    Source: spec.txt lines 2899-2907
    """
    md = MarkdownIt()

    input_text = '<script>\nfoo\n</script>1. *bar*'
    expected = '<script>\nfoo\n</script>1. *bar*'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example181():
    """Test example 181: Foo  bar    baz  okay.

    Source: spec.txt lines 2912-2924
    """
    md = MarkdownIt()

    input_text = '<!-- Foo\n\nbar\n   baz -->\nokay'
    expected = '<!-- Foo\n\nbar\n   baz -->\n<p>okay</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example182():
    """Test example 182: php    echo    okay.

    Source: spec.txt lines 2930-2944
    """
    md = MarkdownIt()

    input_text = "<?php\n\n  echo '>';\n\n?>\nokay"
    expected = "<?php\n\n  echo '>';\n\n?>\n<p>okay</p>"

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example183():
    """Test example 183: DOCTYPE html.

    Source: spec.txt lines 2949-2953
    """
    md = MarkdownIt()

    input_text = '<!DOCTYPE html>'
    expected = '<!DOCTYPE html>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example184():
    """Test example 184: CDATA function matchwoab    if a  b  a.

    Source: spec.txt lines 2958-2986
    """
    md = MarkdownIt()

    input_text = '<![CDATA[\nfunction matchwo(a,b)\n{\n  if (a < b && a < 0) then {\n    return 1;\n\n  } else {\n\n    return 0;\n  }\n}\n]]>\nokay'
    expected = '<![CDATA[\nfunction matchwo(a,b)\n{\n  if (a < b && a < 0) then {\n    return 1;\n\n  } else {\n\n    return 0;\n  }\n}\n]]>\n<p>okay</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example185():
    """Test example 185: foo        foo.

    Source: spec.txt lines 2992-3000
    """
    md = MarkdownIt()

    input_text = '  <!-- foo -->\n\n    <!-- foo -->'
    expected = '  <!-- foo -->\n<pre><code>&lt;!-- foo --&gt;\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example186():
    """Test example 186: div      div.

    Source: spec.txt lines 3003-3011
    """
    md = MarkdownIt()

    input_text = '  <div>\n\n    <div>'
    expected = '  <div>\n<pre><code>&lt;div&gt;\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example187():
    """Test example 187: Foo div bar div.

    Source: spec.txt lines 3017-3027
    """
    md = MarkdownIt()

    input_text = 'Foo\n<div>\nbar\n</div>'
    expected = '<p>Foo</p>\n<div>\nbar\n</div>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example188():
    """Test example 188: div bar div foo.

    Source: spec.txt lines 3034-3044
    """
    md = MarkdownIt()

    input_text = '<div>\nbar\n</div>\n*foo*'
    expected = '<div>\nbar\n</div>\n*foo*'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example189():
    """Test example 189: Foo a hrefbar baz.

    Source: spec.txt lines 3049-3057
    """
    md = MarkdownIt()

    input_text = 'Foo\n<a href="bar">\nbaz'
    expected = '<p>Foo\n<a href="bar">\nbaz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example190():
    """Test example 190: div  Emphasized text  div.

    Source: spec.txt lines 3090-3100
    """
    md = MarkdownIt()

    input_text = '<div>\n\n*Emphasized* text.\n\n</div>'
    expected = '<div>\n<p><em>Emphasized</em> text.</p>\n</div>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example191():
    """Test example 191: div Emphasized text div.

    Source: spec.txt lines 3103-3111
    """
    md = MarkdownIt()

    input_text = '<div>\n*Emphasized* text.\n</div>'
    expected = '<div>\n*Emphasized* text.\n</div>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example192():
    """Test example 192: table  tr  td Hi td  tr  table.

    Source: spec.txt lines 3125-3145
    """
    md = MarkdownIt()

    input_text = '<table>\n\n<tr>\n\n<td>\nHi\n</td>\n\n</tr>\n\n</table>'
    expected = '<table>\n<tr>\n<td>\nHi\n</td>\n</tr>\n</table>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example193():
    """Test example 193: table    tr      td       Hi     td.

    Source: spec.txt lines 3152-3173
    """
    md = MarkdownIt()

    input_text = '<table>\n\n  <tr>\n\n    <td>\n      Hi\n    </td>\n\n  </tr>\n\n</table>'
    expected = '<table>\n  <tr>\n<pre><code>&lt;td&gt;\n  Hi\n&lt;/td&gt;\n</code></pre>\n  </tr>\n</table>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example194():
    """Test example 194: foo url title  foo.

    Source: spec.txt lines 3201-3207
    """
    md = MarkdownIt()

    input_text = '[foo]: /url "title"\n\n[foo]'
    expected = '<p><a href="/url" title="title">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example195():
    """Test example 195: foo        url              the title.

    Source: spec.txt lines 3210-3218
    """
    md = MarkdownIt()

    input_text = "   [foo]: \n      /url  \n           'the title'  \n\n[foo]"
    expected = '<p><a href="/url" title="the title">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example196():
    """Test example 196: Foobarmyurl title with parens  Foob.

    Source: spec.txt lines 3221-3227
    """
    md = MarkdownIt()

    input_text = "[Foo*bar\\]]:my_(url) 'title (with parens)'\n\n[Foo*bar\\]]"
    expected = '<p><a href="my_(url)" title="title (with parens)">Foo*bar]</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example197():
    """Test example 197: Foo bar my url title  Foo bar.

    Source: spec.txt lines 3230-3238
    """
    md = MarkdownIt()

    input_text = "[Foo bar]:\n<my url>\n'title'\n\n[Foo bar]"
    expected = '<p><a href="my%20url" title="title">Foo bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example198():
    """Test example 198: foo url  title line1 line2   foo.

    Source: spec.txt lines 3243-3257
    """
    md = MarkdownIt()

    input_text = "[foo]: /url '\ntitle\nline1\nline2\n'\n\n[foo]"
    expected = '<p><a href="/url" title="\ntitle\nline1\nline2\n">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example199():
    """Test example 199: foo url title  with blank line  foo.

    Source: spec.txt lines 3262-3272
    """
    md = MarkdownIt()

    input_text = "[foo]: /url 'title\n\nwith blank line'\n\n[foo]"
    expected = "<p>[foo]: /url 'title</p>\n<p>with blank line'</p>\n<p>[foo]</p>"

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example200():
    """Test example 200: foo url  foo.

    Source: spec.txt lines 3277-3284
    """
    md = MarkdownIt()

    input_text = '[foo]:\n/url\n\n[foo]'
    expected = '<p><a href="/url">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example201():
    """Test example 201: foo  foo.

    Source: spec.txt lines 3289-3296
    """
    md = MarkdownIt()

    input_text = '[foo]:\n\n[foo]'
    expected = '<p>[foo]:</p>\n<p>[foo]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example202():
    """Test example 202: foo   foo.

    Source: spec.txt lines 3301-3307
    """
    md = MarkdownIt()

    input_text = '[foo]: <>\n\n[foo]'
    expected = '<p><a href="">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example203():
    """Test example 203: foo barbaz  foo.

    Source: spec.txt lines 3312-3319
    """
    md = MarkdownIt()

    input_text = '[foo]: <bar>(baz)\n\n[foo]'
    expected = '<p>[foo]: <bar>(baz)</p>\n<p>[foo]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example204():
    """Test example 204: foo urlbarbaz foobarbaz  foo.

    Source: spec.txt lines 3325-3331
    """
    md = MarkdownIt()

    input_text = '[foo]: /url\\bar\\*baz "foo\\"bar\\baz"\n\n[foo]'
    expected = '<p><a href="/url%5Cbar*baz" title="foo&quot;bar\\baz">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example205():
    """Test example 205: foo  foo url.

    Source: spec.txt lines 3336-3342
    """
    md = MarkdownIt()

    input_text = '[foo]\n\n[foo]: url'
    expected = '<p><a href="url">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example206():
    """Test example 206: foo  foo first foo second.

    Source: spec.txt lines 3348-3355
    """
    md = MarkdownIt()

    input_text = '[foo]\n\n[foo]: first\n[foo]: second'
    expected = '<p><a href="first">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example207():
    """Test example 207: FOO url  Foo.

    Source: spec.txt lines 3361-3367
    """
    md = MarkdownIt()

    input_text = '[FOO]: /url\n\n[Foo]'
    expected = '<p><a href="/url">Foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example208():
    """Test example 208.

    Source: spec.txt lines 3370-3376
    """
    md = MarkdownIt()

    input_text = '[ΑΓΩ]: /φου\n\n[αγω]'
    expected = '<p><a href="/%CF%86%CE%BF%CF%85">αγω</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example209():
    """Test example 209: foo url.

    Source: spec.txt lines 3385-3388
    """
    md = MarkdownIt()

    input_text = '[foo]: /url'
    expected = ''

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example210():
    """Test example 210: foo  url bar.

    Source: spec.txt lines 3393-3400
    """
    md = MarkdownIt()

    input_text = '[\nfoo\n]: /url\nbar'
    expected = '<p>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example211():
    """Test example 211: foo url title ok.

    Source: spec.txt lines 3406-3410
    """
    md = MarkdownIt()

    input_text = '[foo]: /url "title" ok'
    expected = '<p>[foo]: /url &quot;title&quot; ok</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example212():
    """Test example 212: foo url title ok.

    Source: spec.txt lines 3415-3420
    """
    md = MarkdownIt()

    input_text = '[foo]: /url\n"title" ok'
    expected = '<p>&quot;title&quot; ok</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example213():
    """Test example 213: foo url title  foo.

    Source: spec.txt lines 3426-3434
    """
    md = MarkdownIt()

    input_text = '    [foo]: /url "title"\n\n[foo]'
    expected = '<pre><code>[foo]: /url &quot;title&quot;\n</code></pre>\n<p>[foo]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example214():
    """Test example 214: foo url   foo.

    Source: spec.txt lines 3440-3450
    """
    md = MarkdownIt()

    input_text = '```\n[foo]: /url\n```\n\n[foo]'
    expected = '<pre><code>[foo]: /url\n</code></pre>\n<p>[foo]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example215():
    """Test example 215: Foo bar baz  bar.

    Source: spec.txt lines 3455-3464
    """
    md = MarkdownIt()

    input_text = 'Foo\n[bar]: /baz\n\n[bar]'
    expected = '<p>Foo\n[bar]: /baz</p>\n<p>[bar]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example216():
    """Test example 216: Foo foo url  bar.

    Source: spec.txt lines 3470-3479
    """
    md = MarkdownIt()

    input_text = '# [Foo]\n[foo]: /url\n> bar'
    expected = '<h1><a href="/url">Foo</a></h1>\n<blockquote>\n<p>bar</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example217():
    """Test example 217: foo url bar  foo.

    Source: spec.txt lines 3481-3489
    """
    md = MarkdownIt()

    input_text = '[foo]: /url\nbar\n===\n[foo]'
    expected = '<h1>bar</h1>\n<p><a href="/url">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example218():
    """Test example 218: foo url  foo.

    Source: spec.txt lines 3491-3498
    """
    md = MarkdownIt()

    input_text = '[foo]: /url\n===\n[foo]'
    expected = '<p>===\n<a href="/url">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example219():
    """Test example 219: foo foourl foo bar barurl   bar baz.

    Source: spec.txt lines 3504-3517
    """
    md = MarkdownIt()

    input_text = '[foo]: /foo-url "foo"\n[bar]: /bar-url\n  "bar"\n[baz]: /baz-url\n\n[foo],\n[bar],\n[baz]'
    expected = '<p><a href="/foo-url" title="foo">foo</a>,\n<a href="/bar-url" title="bar">bar</a>,\n<a href="/baz-url">baz</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example220():
    """Test example 220: foo   foo url.

    Source: spec.txt lines 3525-3533
    """
    md = MarkdownIt()

    input_text = '[foo]\n\n> [foo]: /url'
    expected = '<p><a href="/url">foo</a></p>\n<blockquote>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example221():
    """Test example 221: aaa  bbb.

    Source: spec.txt lines 3547-3554
    """
    md = MarkdownIt()

    input_text = 'aaa\n\nbbb'
    expected = '<p>aaa</p>\n<p>bbb</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example222():
    """Test example 222: aaa bbb  ccc ddd.

    Source: spec.txt lines 3559-3570
    """
    md = MarkdownIt()

    input_text = 'aaa\nbbb\n\nccc\nddd'
    expected = '<p>aaa\nbbb</p>\n<p>ccc\nddd</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example223():
    """Test example 223: aaa   bbb.

    Source: spec.txt lines 3575-3583
    """
    md = MarkdownIt()

    input_text = 'aaa\n\n\nbbb'
    expected = '<p>aaa</p>\n<p>bbb</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example224():
    """Test example 224: aaa  bbb.

    Source: spec.txt lines 3588-3594
    """
    md = MarkdownIt()

    input_text = '  aaa\n bbb'
    expected = '<p>aaa\nbbb</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example225():
    """Test example 225: aaa              bbb.

    Source: spec.txt lines 3600-3608
    """
    md = MarkdownIt()

    input_text = 'aaa\n             bbb\n                                       ccc'
    expected = '<p>aaa\nbbb\nccc</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example226():
    """Test example 226: aaa bbb.

    Source: spec.txt lines 3614-3620
    """
    md = MarkdownIt()

    input_text = '   aaa\nbbb'
    expected = '<p>aaa\nbbb</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example227():
    """Test example 227: aaa bbb.

    Source: spec.txt lines 3623-3630
    """
    md = MarkdownIt()

    input_text = '    aaa\nbbb'
    expected = '<pre><code>aaa\n</code></pre>\n<p>bbb</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example228():
    """Test example 228: aaa      bbb.

    Source: spec.txt lines 3637-3643
    """
    md = MarkdownIt()

    input_text = 'aaa     \nbbb     '
    expected = '<p>aaa<br />\nbbb</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example229():
    """Test example 229: aaa      aaa.

    Source: spec.txt lines 3654-3666
    """
    md = MarkdownIt()

    input_text = '  \n\naaa\n  \n\n# aaa\n\n  '
    expected = '<p>aaa</p>\n<h1>aaa</h1>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example230():
    """Test example 230: Foo  bar  baz.

    Source: spec.txt lines 3722-3732
    """
    md = MarkdownIt()

    input_text = '> # Foo\n> bar\n> baz'
    expected = '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example231():
    """Test example 231: Foo bar  baz.

    Source: spec.txt lines 3737-3747
    """
    md = MarkdownIt()

    input_text = '># Foo\n>bar\n> baz'
    expected = '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example232():
    """Test example 232: Foo     bar   baz.

    Source: spec.txt lines 3752-3762
    """
    md = MarkdownIt()

    input_text = '   > # Foo\n   > bar\n > baz'
    expected = '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example233():
    """Test example 233: Foo      bar      baz.

    Source: spec.txt lines 3767-3776
    """
    md = MarkdownIt()

    input_text = '    > # Foo\n    > bar\n    > baz'
    expected = '<pre><code>&gt; # Foo\n&gt; bar\n&gt; baz\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example234():
    """Test example 234: Foo  bar baz.

    Source: spec.txt lines 3782-3792
    """
    md = MarkdownIt()

    input_text = '> # Foo\n> bar\nbaz'
    expected = '<blockquote>\n<h1>Foo</h1>\n<p>bar\nbaz</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example235():
    """Test example 235: bar baz  foo.

    Source: spec.txt lines 3798-3808
    """
    md = MarkdownIt()

    input_text = '> bar\nbaz\n> foo'
    expected = '<blockquote>\n<p>bar\nbaz\nfoo</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example236():
    """Test example 236: foo.

    Source: spec.txt lines 3822-3830
    """
    md = MarkdownIt()

    input_text = '> foo\n---'
    expected = '<blockquote>\n<p>foo</p>\n</blockquote>\n<hr />'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example237():
    """Test example 237: foo  bar.

    Source: spec.txt lines 3842-3854
    """
    md = MarkdownIt()

    input_text = '> - foo\n- bar'
    expected = '<blockquote>\n<ul>\n<li>foo</li>\n</ul>\n</blockquote>\n<ul>\n<li>bar</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example238():
    """Test example 238: foo     bar.

    Source: spec.txt lines 3860-3870
    """
    md = MarkdownIt()

    input_text = '>     foo\n    bar'
    expected = '<blockquote>\n<pre><code>foo\n</code></pre>\n</blockquote>\n<pre><code>bar\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example239():
    """Test example 239: foo.

    Source: spec.txt lines 3873-3883
    """
    md = MarkdownIt()

    input_text = '> ```\nfoo\n```'
    expected = '<blockquote>\n<pre><code></code></pre>\n</blockquote>\n<p>foo</p>\n<pre><code></code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example240():
    """Test example 240: foo      bar.

    Source: spec.txt lines 3889-3897
    """
    md = MarkdownIt()

    input_text = '> foo\n    - bar'
    expected = '<blockquote>\n<p>foo\n- bar</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example241():
    """Test example 241.

    Source: spec.txt lines 3913-3918
    """
    md = MarkdownIt()

    input_text = '>'
    expected = '<blockquote>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example242():
    """Test example 242.

    Source: spec.txt lines 3921-3928
    """
    md = MarkdownIt()

    input_text = '>\n>  \n> '
    expected = '<blockquote>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example243():
    """Test example 243: foo.

    Source: spec.txt lines 3933-3941
    """
    md = MarkdownIt()

    input_text = '>\n> foo\n>  '
    expected = '<blockquote>\n<p>foo</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example244():
    """Test example 244: foo   bar.

    Source: spec.txt lines 3946-3957
    """
    md = MarkdownIt()

    input_text = '> foo\n\n> bar'
    expected = '<blockquote>\n<p>foo</p>\n</blockquote>\n<blockquote>\n<p>bar</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example245():
    """Test example 245: foo  bar.

    Source: spec.txt lines 3968-3976
    """
    md = MarkdownIt()

    input_text = '> foo\n> bar'
    expected = '<blockquote>\n<p>foo\nbar</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example246():
    """Test example 246: foo   bar.

    Source: spec.txt lines 3981-3990
    """
    md = MarkdownIt()

    input_text = '> foo\n>\n> bar'
    expected = '<blockquote>\n<p>foo</p>\n<p>bar</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example247():
    """Test example 247: foo  bar.

    Source: spec.txt lines 3995-4003
    """
    md = MarkdownIt()

    input_text = 'foo\n> bar'
    expected = '<p>foo</p>\n<blockquote>\n<p>bar</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example248():
    """Test example 248: aaa   bbb.

    Source: spec.txt lines 4009-4021
    """
    md = MarkdownIt()

    input_text = '> aaa\n***\n> bbb'
    expected = '<blockquote>\n<p>aaa</p>\n</blockquote>\n<hr />\n<blockquote>\n<p>bbb</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example249():
    """Test example 249: bar baz.

    Source: spec.txt lines 4027-4035
    """
    md = MarkdownIt()

    input_text = '> bar\nbaz'
    expected = '<blockquote>\n<p>bar\nbaz</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example250():
    """Test example 250: bar  baz.

    Source: spec.txt lines 4038-4047
    """
    md = MarkdownIt()

    input_text = '> bar\n\nbaz'
    expected = '<blockquote>\n<p>bar</p>\n</blockquote>\n<p>baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example251():
    """Test example 251: bar  baz.

    Source: spec.txt lines 4050-4059
    """
    md = MarkdownIt()

    input_text = '> bar\n>\nbaz'
    expected = '<blockquote>\n<p>bar</p>\n</blockquote>\n<p>baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example252():
    """Test example 252: foo bar.

    Source: spec.txt lines 4066-4078
    """
    md = MarkdownIt()

    input_text = '> > > foo\nbar'
    expected = '<blockquote>\n<blockquote>\n<blockquote>\n<p>foo\nbar</p>\n</blockquote>\n</blockquote>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example253():
    """Test example 253: foo  bar baz.

    Source: spec.txt lines 4081-4095
    """
    md = MarkdownIt()

    input_text = '>>> foo\n> bar\n>>baz'
    expected = '<blockquote>\n<blockquote>\n<blockquote>\n<p>foo\nbar\nbaz</p>\n</blockquote>\n</blockquote>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example254():
    """Test example 254: code      not code.

    Source: spec.txt lines 4103-4115
    """
    md = MarkdownIt()

    input_text = '>     code\n\n>    not code'
    expected = '<blockquote>\n<pre><code>code\n</code></pre>\n</blockquote>\n<blockquote>\n<p>not code</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example255():
    """Test example 255: A paragraph with two lines      indented code.

    Source: spec.txt lines 4157-4172
    """
    md = MarkdownIt()

    input_text = 'A paragraph\nwith two lines.\n\n    indented code\n\n> A block quote.'
    expected = '<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example256():
    """Test example 256: 1  A paragraph     with two lines          inden.

    Source: spec.txt lines 4179-4198
    """
    md = MarkdownIt()

    input_text = '1.  A paragraph\n    with two lines.\n\n        indented code\n\n    > A block quote.'
    expected = '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example257():
    """Test example 257: one   two.

    Source: spec.txt lines 4212-4221
    """
    md = MarkdownIt()

    input_text = '- one\n\n two'
    expected = '<ul>\n<li>one</li>\n</ul>\n<p>two</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example258():
    """Test example 258: one    two.

    Source: spec.txt lines 4224-4235
    """
    md = MarkdownIt()

    input_text = '- one\n\n  two'
    expected = '<ul>\n<li>\n<p>one</p>\n<p>two</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example259():
    """Test example 259: one       two.

    Source: spec.txt lines 4238-4248
    """
    md = MarkdownIt()

    input_text = ' -    one\n\n     two'
    expected = '<ul>\n<li>one</li>\n</ul>\n<pre><code> two\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example260():
    """Test example 260: one        two.

    Source: spec.txt lines 4251-4262
    """
    md = MarkdownIt()

    input_text = ' -    one\n\n      two'
    expected = '<ul>\n<li>\n<p>one</p>\n<p>two</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example261():
    """Test example 261: 1  one       two.

    Source: spec.txt lines 4273-4288
    """
    md = MarkdownIt()

    input_text = '   > > 1.  one\n>>\n>>     two'
    expected = '<blockquote>\n<blockquote>\n<ol>\n<li>\n<p>one</p>\n<p>two</p>\n</li>\n</ol>\n</blockquote>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example262():
    """Test example 262: one       two.

    Source: spec.txt lines 4300-4313
    """
    md = MarkdownIt()

    input_text = '>>- one\n>>\n  >  > two'
    expected = '<blockquote>\n<blockquote>\n<ul>\n<li>one</li>\n</ul>\n<p>two</p>\n</blockquote>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example263():
    """Test example 263: one  2two.

    Source: spec.txt lines 4319-4326
    """
    md = MarkdownIt()

    input_text = '-one\n\n2.two'
    expected = '<p>-one</p>\n<p>2.two</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example264():
    """Test example 264: foo     bar.

    Source: spec.txt lines 4332-4344
    """
    md = MarkdownIt()

    input_text = '- foo\n\n\n  bar'
    expected = '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example265():
    """Test example 265: 1  foo           bar           baz       b.

    Source: spec.txt lines 4349-4371
    """
    md = MarkdownIt()

    input_text = '1.  foo\n\n    ```\n    bar\n    ```\n\n    baz\n\n    > bam'
    expected = '<ol>\n<li>\n<p>foo</p>\n<pre><code>bar\n</code></pre>\n<p>baz</p>\n<blockquote>\n<p>bam</p>\n</blockquote>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example266():
    """Test example 266: Foo        bar         baz.

    Source: spec.txt lines 4377-4395
    """
    md = MarkdownIt()

    input_text = '- Foo\n\n      bar\n\n\n      baz'
    expected = '<ul>\n<li>\n<p>Foo</p>\n<pre><code>bar\n\n\nbaz\n</code></pre>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example267():
    """Test example 267: 123456789 ok.

    Source: spec.txt lines 4399-4405
    """
    md = MarkdownIt()

    input_text = '123456789. ok'
    expected = '<ol start="123456789">\n<li>ok</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example268():
    """Test example 268: 1234567890 not ok.

    Source: spec.txt lines 4408-4412
    """
    md = MarkdownIt()

    input_text = '1234567890. not ok'
    expected = '<p>1234567890. not ok</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example269():
    """Test example 269: 0 ok.

    Source: spec.txt lines 4417-4423
    """
    md = MarkdownIt()

    input_text = '0. ok'
    expected = '<ol start="0">\n<li>ok</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example270():
    """Test example 270: 003 ok.

    Source: spec.txt lines 4426-4432
    """
    md = MarkdownIt()

    input_text = '003. ok'
    expected = '<ol start="3">\n<li>ok</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example271():
    """Test example 271: 1 not ok.

    Source: spec.txt lines 4437-4441
    """
    md = MarkdownIt()

    input_text = '-1. not ok'
    expected = '<p>-1. not ok</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example272():
    """Test example 272: foo        bar.

    Source: spec.txt lines 4460-4472
    """
    md = MarkdownIt()

    input_text = '- foo\n\n      bar'
    expected = '<ul>\n<li>\n<p>foo</p>\n<pre><code>bar\n</code></pre>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example273():
    """Test example 273: 10  foo             bar.

    Source: spec.txt lines 4477-4489
    """
    md = MarkdownIt()

    input_text = '  10.  foo\n\n           bar'
    expected = '<ol start="10">\n<li>\n<p>foo</p>\n<pre><code>bar\n</code></pre>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example274():
    """Test example 274: indented code  paragraph      more code.

    Source: spec.txt lines 4496-4508
    """
    md = MarkdownIt()

    input_text = '    indented code\n\nparagraph\n\n    more code'
    expected = '<pre><code>indented code\n</code></pre>\n<p>paragraph</p>\n<pre><code>more code\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example275():
    """Test example 275: 1     indented code     paragraph         more co.

    Source: spec.txt lines 4511-4527
    """
    md = MarkdownIt()

    input_text = '1.     indented code\n\n   paragraph\n\n       more code'
    expected = '<ol>\n<li>\n<pre><code>indented code\n</code></pre>\n<p>paragraph</p>\n<pre><code>more code\n</code></pre>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example276():
    """Test example 276: 1      indented code     paragraph         more c.

    Source: spec.txt lines 4533-4549
    """
    md = MarkdownIt()

    input_text = '1.      indented code\n\n   paragraph\n\n       more code'
    expected = '<ol>\n<li>\n<pre><code> indented code\n</code></pre>\n<p>paragraph</p>\n<pre><code>more code\n</code></pre>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example277():
    """Test example 277: foo  bar.

    Source: spec.txt lines 4560-4567
    """
    md = MarkdownIt()

    input_text = '   foo\n\nbar'
    expected = '<p>foo</p>\n<p>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example278():
    """Test example 278: foo    bar.

    Source: spec.txt lines 4570-4579
    """
    md = MarkdownIt()

    input_text = '-    foo\n\n  bar'
    expected = '<ul>\n<li>foo</li>\n</ul>\n<p>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example279():
    """Test example 279: foo     bar.

    Source: spec.txt lines 4587-4598
    """
    md = MarkdownIt()

    input_text = '-  foo\n\n   bar'
    expected = '<ul>\n<li>\n<p>foo</p>\n<p>bar</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example280():
    """Test example 280: foo       bar           baz.

    Source: spec.txt lines 4614-4635
    """
    md = MarkdownIt()

    input_text = '-\n  foo\n-\n  ```\n  bar\n  ```\n-\n      baz'
    expected = '<ul>\n<li>foo</li>\n<li>\n<pre><code>bar\n</code></pre>\n</li>\n<li>\n<pre><code>baz\n</code></pre>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example281():
    """Test example 281: foo.

    Source: spec.txt lines 4640-4647
    """
    md = MarkdownIt()

    input_text = '-   \n  foo'
    expected = '<ul>\n<li>foo</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example282():
    """Test example 282: foo.

    Source: spec.txt lines 4654-4663
    """
    md = MarkdownIt()

    input_text = '-\n\n  foo'
    expected = '<ul>\n<li></li>\n</ul>\n<p>foo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example283():
    """Test example 283: foo   bar.

    Source: spec.txt lines 4668-4678
    """
    md = MarkdownIt()

    input_text = '- foo\n-\n- bar'
    expected = '<ul>\n<li>foo</li>\n<li></li>\n<li>bar</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example284():
    """Test example 284: foo      bar.

    Source: spec.txt lines 4683-4693
    """
    md = MarkdownIt()

    input_text = '- foo\n-   \n- bar'
    expected = '<ul>\n<li>foo</li>\n<li></li>\n<li>bar</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example285():
    """Test example 285: 1 foo 2 3 bar.

    Source: spec.txt lines 4698-4708
    """
    md = MarkdownIt()

    input_text = '1. foo\n2.\n3. bar'
    expected = '<ol>\n<li>foo</li>\n<li></li>\n<li>bar</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example286():
    """Test example 286.

    Source: spec.txt lines 4713-4719
    """
    md = MarkdownIt()

    input_text = '*'
    expected = '<ul>\n<li></li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example287():
    """Test example 287: foo   foo 1.

    Source: spec.txt lines 4723-4734
    """
    md = MarkdownIt()

    input_text = 'foo\n*\n\nfoo\n1.'
    expected = '<p>foo\n*</p>\n<p>foo\n1.</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example288():
    """Test example 288: 1  A paragraph      with two lines           in.

    Source: spec.txt lines 4745-4764
    """
    md = MarkdownIt()

    input_text = ' 1.  A paragraph\n     with two lines.\n\n         indented code\n\n     > A block quote.'
    expected = '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example289():
    """Test example 289: 1  A paragraph       with two lines.

    Source: spec.txt lines 4769-4788
    """
    md = MarkdownIt()

    input_text = '  1.  A paragraph\n      with two lines.\n\n          indented code\n\n      > A block quote.'
    expected = '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example290():
    """Test example 290: 1  A paragraph        with two lines.

    Source: spec.txt lines 4793-4812
    """
    md = MarkdownIt()

    input_text = '   1.  A paragraph\n       with two lines.\n\n           indented code\n\n       > A block quote.'
    expected = '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example291():
    """Test example 291: 1  A paragraph         with two lines.

    Source: spec.txt lines 4817-4832
    """
    md = MarkdownIt()

    input_text = '    1.  A paragraph\n        with two lines.\n\n            indented code\n\n        > A block quote.'
    expected = '<pre><code>1.  A paragraph\n    with two lines.\n\n        indented code\n\n    &gt; A block quote.\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example292():
    """Test example 292: 1  A paragraph with two lines            inden.

    Source: spec.txt lines 4847-4866
    """
    md = MarkdownIt()

    input_text = '  1.  A paragraph\nwith two lines.\n\n          indented code\n\n      > A block quote.'
    expected = '<ol>\n<li>\n<p>A paragraph\nwith two lines.</p>\n<pre><code>indented code\n</code></pre>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example293():
    """Test example 293: 1  A paragraph     with two lines.

    Source: spec.txt lines 4871-4879
    """
    md = MarkdownIt()

    input_text = '  1.  A paragraph\n    with two lines.'
    expected = '<ol>\n<li>A paragraph\nwith two lines.</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example294():
    """Test example 294: 1  Blockquote continued here.

    Source: spec.txt lines 4884-4898
    """
    md = MarkdownIt()

    input_text = '> 1. > Blockquote\ncontinued here.'
    expected = '<blockquote>\n<ol>\n<li>\n<blockquote>\n<p>Blockquote\ncontinued here.</p>\n</blockquote>\n</li>\n</ol>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example295():
    """Test example 295: 1  Blockquote  continued here.

    Source: spec.txt lines 4901-4915
    """
    md = MarkdownIt()

    input_text = '> 1. > Blockquote\n> continued here.'
    expected = '<blockquote>\n<ol>\n<li>\n<blockquote>\n<p>Blockquote\ncontinued here.</p>\n</blockquote>\n</li>\n</ol>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example296():
    """Test example 296: foo    bar      baz        boo.

    Source: spec.txt lines 4929-4950
    """
    md = MarkdownIt()

    input_text = '- foo\n  - bar\n    - baz\n      - boo'
    expected = '<ul>\n<li>foo\n<ul>\n<li>bar\n<ul>\n<li>baz\n<ul>\n<li>boo</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example297():
    """Test example 297: foo   bar    baz     boo.

    Source: spec.txt lines 4955-4967
    """
    md = MarkdownIt()

    input_text = '- foo\n - bar\n  - baz\n   - boo'
    expected = '<ul>\n<li>foo</li>\n<li>bar</li>\n<li>baz</li>\n<li>boo</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example298():
    """Test example 298: 10 foo      bar.

    Source: spec.txt lines 4972-4983
    """
    md = MarkdownIt()

    input_text = '10) foo\n    - bar'
    expected = '<ol start="10">\n<li>foo\n<ul>\n<li>bar</li>\n</ul>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example299():
    """Test example 299: 10 foo     bar.

    Source: spec.txt lines 4988-4998
    """
    md = MarkdownIt()

    input_text = '10) foo\n   - bar'
    expected = '<ol start="10">\n<li>foo</li>\n</ol>\n<ul>\n<li>bar</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example300():
    """Test example 300: foo.

    Source: spec.txt lines 5003-5013
    """
    md = MarkdownIt()

    input_text = '- - foo'
    expected = '<ul>\n<li>\n<ul>\n<li>foo</li>\n</ul>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example301():
    """Test example 301: 1  2 foo.

    Source: spec.txt lines 5016-5030
    """
    md = MarkdownIt()

    input_text = '1. - 2. foo'
    expected = '<ol>\n<li>\n<ul>\n<li>\n<ol start="2">\n<li>foo</li>\n</ol>\n</li>\n</ul>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example302():
    """Test example 302: Foo  Bar      baz.

    Source: spec.txt lines 5035-5049
    """
    md = MarkdownIt()

    input_text = '- # Foo\n- Bar\n  ---\n  baz'
    expected = '<ul>\n<li>\n<h1>Foo</h1>\n</li>\n<li>\n<h2>Bar</h2>\nbaz</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example303():
    """Test example 303: foo  bar  baz.

    Source: spec.txt lines 5271-5283
    """
    md = MarkdownIt()

    input_text = '- foo\n- bar\n+ baz'
    expected = '<ul>\n<li>foo</li>\n<li>bar</li>\n</ul>\n<ul>\n<li>baz</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example304():
    """Test example 304: 1 foo 2 bar 3 baz.

    Source: spec.txt lines 5286-5298
    """
    md = MarkdownIt()

    input_text = '1. foo\n2. bar\n3) baz'
    expected = '<ol>\n<li>foo</li>\n<li>bar</li>\n</ol>\n<ol start="3">\n<li>baz</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example305():
    """Test example 305: Foo  bar  baz.

    Source: spec.txt lines 5305-5315
    """
    md = MarkdownIt()

    input_text = 'Foo\n- bar\n- baz'
    expected = '<p>Foo</p>\n<ul>\n<li>bar</li>\n<li>baz</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example306():
    """Test example 306: The number of windows in my house is 14  The numb.

    Source: spec.txt lines 5382-5388
    """
    md = MarkdownIt()

    input_text = 'The number of windows in my house is\n14.  The number of doors is 6.'
    expected = '<p>The number of windows in my house is\n14.  The number of doors is 6.</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example307():
    """Test example 307: The number of windows in my house is 1  The numbe.

    Source: spec.txt lines 5392-5400
    """
    md = MarkdownIt()

    input_text = 'The number of windows in my house is\n1.  The number of doors is 6.'
    expected = '<p>The number of windows in my house is</p>\n<ol>\n<li>The number of doors is 6.</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example308():
    """Test example 308: foo   bar    baz.

    Source: spec.txt lines 5406-5425
    """
    md = MarkdownIt()

    input_text = '- foo\n\n- bar\n\n\n- baz'
    expected = '<ul>\n<li>\n<p>foo</p>\n</li>\n<li>\n<p>bar</p>\n</li>\n<li>\n<p>baz</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example309():
    """Test example 309: foo    bar      baz         bim.

    Source: spec.txt lines 5427-5449
    """
    md = MarkdownIt()

    input_text = '- foo\n  - bar\n    - baz\n\n\n      bim'
    expected = '<ul>\n<li>foo\n<ul>\n<li>bar\n<ul>\n<li>\n<p>baz</p>\n<p>bim</p>\n</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example310():
    """Test example 310: foo  bar      baz  bim.

    Source: spec.txt lines 5457-5475
    """
    md = MarkdownIt()

    input_text = '- foo\n- bar\n\n<!-- -->\n\n- baz\n- bim'
    expected = '<ul>\n<li>foo</li>\n<li>bar</li>\n</ul>\n<!-- -->\n<ul>\n<li>baz</li>\n<li>bim</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example311():
    """Test example 311: foo      notcode     foo         code.

    Source: spec.txt lines 5478-5501
    """
    md = MarkdownIt()

    input_text = '-   foo\n\n    notcode\n\n-   foo\n\n<!-- -->\n\n    code'
    expected = '<ul>\n<li>\n<p>foo</p>\n<p>notcode</p>\n</li>\n<li>\n<p>foo</p>\n</li>\n</ul>\n<!-- -->\n<pre><code>code\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example312():
    """Test example 312: a   b    c     d    e   f  g.

    Source: spec.txt lines 5509-5527
    """
    md = MarkdownIt()

    input_text = '- a\n - b\n  - c\n   - d\n  - e\n - f\n- g'
    expected = '<ul>\n<li>a</li>\n<li>b</li>\n<li>c</li>\n<li>d</li>\n<li>e</li>\n<li>f</li>\n<li>g</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example313():
    """Test example 313: 1 a    2 b     3 c.

    Source: spec.txt lines 5530-5548
    """
    md = MarkdownIt()

    input_text = '1. a\n\n  2. b\n\n   3. c'
    expected = '<ol>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n<li>\n<p>c</p>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example314():
    """Test example 314: a   b    c     d      e.

    Source: spec.txt lines 5554-5568
    """
    md = MarkdownIt()

    input_text = '- a\n - b\n  - c\n   - d\n    - e'
    expected = '<ul>\n<li>a</li>\n<li>b</li>\n<li>c</li>\n<li>d\n- e</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example315():
    """Test example 315: 1 a    2 b      3 c.

    Source: spec.txt lines 5574-5591
    """
    md = MarkdownIt()

    input_text = '1. a\n\n  2. b\n\n    3. c'
    expected = '<ol>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n</ol>\n<pre><code>3. c\n</code></pre>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example316():
    """Test example 316: a  b   c.

    Source: spec.txt lines 5597-5614
    """
    md = MarkdownIt()

    input_text = '- a\n- b\n\n- c'
    expected = '<ul>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n<li>\n<p>c</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example317():
    """Test example 317: a    c.

    Source: spec.txt lines 5619-5634
    """
    md = MarkdownIt()

    input_text = '* a\n*\n\n* c'
    expected = '<ul>\n<li>\n<p>a</p>\n</li>\n<li></li>\n<li>\n<p>c</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example318():
    """Test example 318: a  b    c  d.

    Source: spec.txt lines 5641-5660
    """
    md = MarkdownIt()

    input_text = '- a\n- b\n\n  c\n- d'
    expected = '<ul>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n<p>c</p>\n</li>\n<li>\n<p>d</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example319():
    """Test example 319: a  b    ref url  d.

    Source: spec.txt lines 5663-5681
    """
    md = MarkdownIt()

    input_text = '- a\n- b\n\n  [ref]: /url\n- d'
    expected = '<ul>\n<li>\n<p>a</p>\n</li>\n<li>\n<p>b</p>\n</li>\n<li>\n<p>d</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example320():
    """Test example 320: a     b       c.

    Source: spec.txt lines 5686-5705
    """
    md = MarkdownIt()

    input_text = '- a\n- ```\n  b\n\n\n  ```\n- c'
    expected = '<ul>\n<li>a</li>\n<li>\n<pre><code>b\n\n\n</code></pre>\n</li>\n<li>c</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example321():
    """Test example 321: a    b      c  d.

    Source: spec.txt lines 5712-5730
    """
    md = MarkdownIt()

    input_text = '- a\n  - b\n\n    c\n- d'
    expected = '<ul>\n<li>a\n<ul>\n<li>\n<p>b</p>\n<p>c</p>\n</li>\n</ul>\n</li>\n<li>d</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example322():
    """Test example 322: a    b     c.

    Source: spec.txt lines 5736-5750
    """
    md = MarkdownIt()

    input_text = '* a\n  > b\n  >\n* c'
    expected = '<ul>\n<li>a\n<blockquote>\n<p>b</p>\n</blockquote>\n</li>\n<li>c</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example323():
    """Test example 323: a    b      c     d.

    Source: spec.txt lines 5756-5774
    """
    md = MarkdownIt()

    input_text = '- a\n  > b\n  ```\n  c\n  ```\n- d'
    expected = '<ul>\n<li>a\n<blockquote>\n<p>b</p>\n</blockquote>\n<pre><code>c\n</code></pre>\n</li>\n<li>d</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example324():
    """Test example 324: a.

    Source: spec.txt lines 5779-5785
    """
    md = MarkdownIt()

    input_text = '- a'
    expected = '<ul>\n<li>a</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example325():
    """Test example 325: a    b.

    Source: spec.txt lines 5788-5799
    """
    md = MarkdownIt()

    input_text = '- a\n  - b'
    expected = '<ul>\n<li>a\n<ul>\n<li>b</li>\n</ul>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example326():
    """Test example 326: 1     foo         bar.

    Source: spec.txt lines 5805-5819
    """
    md = MarkdownIt()

    input_text = '1. ```\n   foo\n   ```\n\n   bar'
    expected = '<ol>\n<li>\n<pre><code>foo\n</code></pre>\n<p>bar</p>\n</li>\n</ol>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example327():
    """Test example 327: foo    bar    baz.

    Source: spec.txt lines 5824-5839
    """
    md = MarkdownIt()

    input_text = '* foo\n  * bar\n\n  baz'
    expected = '<ul>\n<li>\n<p>foo</p>\n<ul>\n<li>bar</li>\n</ul>\n<p>baz</p>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example328():
    """Test example 328: a    b    c   d    e    f.

    Source: spec.txt lines 5842-5867
    """
    md = MarkdownIt()

    input_text = '- a\n  - b\n  - c\n\n- d\n  - e\n  - f'
    expected = '<ul>\n<li>\n<p>a</p>\n<ul>\n<li>b</li>\n<li>c</li>\n</ul>\n</li>\n<li>\n<p>d</p>\n<ul>\n<li>e</li>\n<li>f</li>\n</ul>\n</li>\n</ul>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example329():
    """Test example 329: hilo.

    Source: spec.txt lines 5876-5880
    """
    md = MarkdownIt()

    input_text = '`hi`lo`'
    expected = '<p><code>hi</code>lo`</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example330():
    """Test example 330: foo.

    Source: spec.txt lines 5908-5912
    """
    md = MarkdownIt()

    input_text = '`foo`'
    expected = '<p><code>foo</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example331():
    """Test example 331: foo  bar.

    Source: spec.txt lines 5919-5923
    """
    md = MarkdownIt()

    input_text = '`` foo ` bar ``'
    expected = '<p><code>foo ` bar</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example332():
    """Test example 332.

    Source: spec.txt lines 5929-5933
    """
    md = MarkdownIt()

    input_text = '` `` `'
    expected = '<p><code>``</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example333():
    """Test example 333.

    Source: spec.txt lines 5937-5941
    """
    md = MarkdownIt()

    input_text = '`  ``  `'
    expected = '<p><code> `` </code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example334():
    """Test example 334: a.

    Source: spec.txt lines 5946-5950
    """
    md = MarkdownIt()

    input_text = '` a`'
    expected = '<p><code> a</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example335():
    """Test example 335: b.

    Source: spec.txt lines 5955-5959
    """
    md = MarkdownIt()

    input_text = '`\xa0b\xa0`'
    expected = '<p><code>\xa0b\xa0</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example336():
    """Test example 336.

    Source: spec.txt lines 5963-5969
    """
    md = MarkdownIt()

    input_text = '`\xa0`\n`  `'
    expected = '<p><code>\xa0</code>\n<code>  </code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example337():
    """Test example 337: foo bar   baz.

    Source: spec.txt lines 5974-5982
    """
    md = MarkdownIt()

    input_text = '``\nfoo\nbar  \nbaz\n``'
    expected = '<p><code>foo bar   baz</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example338():
    """Test example 338: foo.

    Source: spec.txt lines 5984-5990
    """
    md = MarkdownIt()

    input_text = '``\nfoo \n``'
    expected = '<p><code>foo </code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example339():
    """Test example 339: foo   bar  baz.

    Source: spec.txt lines 5995-6000
    """
    md = MarkdownIt()

    input_text = '`foo   bar \nbaz`'
    expected = '<p><code>foo   bar  baz</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example340():
    """Test example 340: foobar.

    Source: spec.txt lines 6012-6016
    """
    md = MarkdownIt()

    input_text = '`foo\\`bar`'
    expected = '<p><code>foo\\</code>bar`</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example341():
    """Test example 341: foobar.

    Source: spec.txt lines 6023-6027
    """
    md = MarkdownIt()

    input_text = '``foo`bar``'
    expected = '<p><code>foo`bar</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example342():
    """Test example 342: foo  bar.

    Source: spec.txt lines 6029-6033
    """
    md = MarkdownIt()

    input_text = '` foo `` bar `'
    expected = '<p><code>foo `` bar</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example343():
    """Test example 343: foo.

    Source: spec.txt lines 6041-6045
    """
    md = MarkdownIt()

    input_text = '*foo`*`'
    expected = '<p>*foo<code>*</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example344():
    """Test example 344: not a linkfoo.

    Source: spec.txt lines 6050-6054
    """
    md = MarkdownIt()

    input_text = '[not a `link](/foo`)'
    expected = '<p>[not a <code>link](/foo</code>)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example345():
    """Test example 345: a href.

    Source: spec.txt lines 6060-6064
    """
    md = MarkdownIt()

    input_text = '`<a href="`">`'
    expected = '<p><code>&lt;a href=&quot;</code>&quot;&gt;`</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example346():
    """Test example 346: a href.

    Source: spec.txt lines 6069-6073
    """
    md = MarkdownIt()

    input_text = '<a href="`">`'
    expected = '<p><a href="`">`</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example347():
    """Test example 347: httpsfoobarbaz.

    Source: spec.txt lines 6078-6082
    """
    md = MarkdownIt()

    input_text = '`<https://foo.bar.`baz>`'
    expected = '<p><code>&lt;https://foo.bar.</code>baz&gt;`</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example348():
    """Test example 348: httpsfoobarbaz.

    Source: spec.txt lines 6087-6091
    """
    md = MarkdownIt()

    input_text = '<https://foo.bar.`baz>`'
    expected = '<p><a href="https://foo.bar.%60baz">https://foo.bar.`baz</a>`</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example349():
    """Test example 349: foo.

    Source: spec.txt lines 6097-6101
    """
    md = MarkdownIt()

    input_text = '```foo``'
    expected = '<p>```foo``</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example350():
    """Test example 350: foo.

    Source: spec.txt lines 6104-6108
    """
    md = MarkdownIt()

    input_text = '`foo'
    expected = '<p>`foo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example351():
    """Test example 351: foobar.

    Source: spec.txt lines 6113-6117
    """
    md = MarkdownIt()

    input_text = '`foo``bar``'
    expected = '<p>`foo<code>bar</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example352():
    """Test example 352: foo bar.

    Source: spec.txt lines 6330-6334
    """
    md = MarkdownIt()

    input_text = '*foo bar*'
    expected = '<p><em>foo bar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example353():
    """Test example 353: a  foo bar.

    Source: spec.txt lines 6340-6344
    """
    md = MarkdownIt()

    input_text = 'a * foo bar*'
    expected = '<p>a * foo bar*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example354():
    """Test example 354: afoo.

    Source: spec.txt lines 6351-6355
    """
    md = MarkdownIt()

    input_text = 'a*"foo"*'
    expected = '<p>a*&quot;foo&quot;*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example355():
    """Test example 355: a.

    Source: spec.txt lines 6360-6364
    """
    md = MarkdownIt()

    input_text = '*\xa0a\xa0*'
    expected = '<p>*\xa0a\xa0*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example356():
    """Test example 356: alpha  bravo  charlie  delta.

    Source: spec.txt lines 6369-6382
    """
    md = MarkdownIt()

    input_text = '*$*alpha.\n\n*£*bravo.\n\n*€*charlie.\n\n*𞋿*delta.'
    expected = '<p>*$*alpha.</p>\n<p>*£*bravo.</p>\n<p>*€*charlie.</p>\n<p>*𞋿*delta.</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example357():
    """Test example 357: foobar.

    Source: spec.txt lines 6387-6391
    """
    md = MarkdownIt()

    input_text = 'foo*bar*'
    expected = '<p>foo<em>bar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example358():
    """Test example 358: 5678.

    Source: spec.txt lines 6394-6398
    """
    md = MarkdownIt()

    input_text = '5*6*78'
    expected = '<p>5<em>6</em>78</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example359():
    """Test example 359: foo bar.

    Source: spec.txt lines 6403-6407
    """
    md = MarkdownIt()

    input_text = '_foo bar_'
    expected = '<p><em>foo bar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example360():
    """Test example 360: foo bar.

    Source: spec.txt lines 6413-6417
    """
    md = MarkdownIt()

    input_text = '_ foo bar_'
    expected = '<p>_ foo bar_</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example361():
    """Test example 361: afoo.

    Source: spec.txt lines 6423-6427
    """
    md = MarkdownIt()

    input_text = 'a_"foo"_'
    expected = '<p>a_&quot;foo&quot;_</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example362():
    """Test example 362: foobar.

    Source: spec.txt lines 6432-6436
    """
    md = MarkdownIt()

    input_text = 'foo_bar_'
    expected = '<p>foo_bar_</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example363():
    """Test example 363: 5678.

    Source: spec.txt lines 6439-6443
    """
    md = MarkdownIt()

    input_text = '5_6_78'
    expected = '<p>5_6_78</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example364():
    """Test example 364.

    Source: spec.txt lines 6446-6450
    """
    md = MarkdownIt()

    input_text = 'пристаням_стремятся_'
    expected = '<p>пристаням_стремятся_</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example365():
    """Test example 365: aabbcc.

    Source: spec.txt lines 6456-6460
    """
    md = MarkdownIt()

    input_text = 'aa_"bb"_cc'
    expected = '<p>aa_&quot;bb&quot;_cc</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example366():
    """Test example 366: foobar.

    Source: spec.txt lines 6467-6471
    """
    md = MarkdownIt()

    input_text = 'foo-_(bar)_'
    expected = '<p>foo-<em>(bar)</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example367():
    """Test example 367: foo.

    Source: spec.txt lines 6479-6483
    """
    md = MarkdownIt()

    input_text = '_foo*'
    expected = '<p>_foo*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example368():
    """Test example 368: foo bar.

    Source: spec.txt lines 6489-6493
    """
    md = MarkdownIt()

    input_text = '*foo bar *'
    expected = '<p>*foo bar *</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example369():
    """Test example 369: foo bar.

    Source: spec.txt lines 6498-6504
    """
    md = MarkdownIt()

    input_text = '*foo bar\n*'
    expected = '<p>*foo bar\n*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example370():
    """Test example 370: foo.

    Source: spec.txt lines 6511-6515
    """
    md = MarkdownIt()

    input_text = '*(*foo)'
    expected = '<p>*(*foo)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example371():
    """Test example 371: foo.

    Source: spec.txt lines 6521-6525
    """
    md = MarkdownIt()

    input_text = '*(*foo*)*'
    expected = '<p><em>(<em>foo</em>)</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example372():
    """Test example 372: foobar.

    Source: spec.txt lines 6530-6534
    """
    md = MarkdownIt()

    input_text = '*foo*bar'
    expected = '<p><em>foo</em>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example373():
    """Test example 373: foo bar.

    Source: spec.txt lines 6543-6547
    """
    md = MarkdownIt()

    input_text = '_foo bar _'
    expected = '<p>_foo bar _</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example374():
    """Test example 374: foo.

    Source: spec.txt lines 6553-6557
    """
    md = MarkdownIt()

    input_text = '_(_foo)'
    expected = '<p>_(_foo)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example375():
    """Test example 375: foo.

    Source: spec.txt lines 6562-6566
    """
    md = MarkdownIt()

    input_text = '_(_foo_)_'
    expected = '<p><em>(<em>foo</em>)</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example376():
    """Test example 376: foobar.

    Source: spec.txt lines 6571-6575
    """
    md = MarkdownIt()

    input_text = '_foo_bar'
    expected = '<p>_foo_bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example377():
    """Test example 377.

    Source: spec.txt lines 6578-6582
    """
    md = MarkdownIt()

    input_text = '_пристаням_стремятся'
    expected = '<p>_пристаням_стремятся</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example378():
    """Test example 378: foobarbaz.

    Source: spec.txt lines 6585-6589
    """
    md = MarkdownIt()

    input_text = '_foo_bar_baz_'
    expected = '<p><em>foo_bar_baz</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example379():
    """Test example 379: bar.

    Source: spec.txt lines 6596-6600
    """
    md = MarkdownIt()

    input_text = '_(bar)_.'
    expected = '<p><em>(bar)</em>.</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example380():
    """Test example 380: foo bar.

    Source: spec.txt lines 6605-6609
    """
    md = MarkdownIt()

    input_text = '**foo bar**'
    expected = '<p><strong>foo bar</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example381():
    """Test example 381: foo bar.

    Source: spec.txt lines 6615-6619
    """
    md = MarkdownIt()

    input_text = '** foo bar**'
    expected = '<p>** foo bar**</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example382():
    """Test example 382: afoo.

    Source: spec.txt lines 6626-6630
    """
    md = MarkdownIt()

    input_text = 'a**"foo"**'
    expected = '<p>a**&quot;foo&quot;**</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example383():
    """Test example 383: foobar.

    Source: spec.txt lines 6635-6639
    """
    md = MarkdownIt()

    input_text = 'foo**bar**'
    expected = '<p>foo<strong>bar</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example384():
    """Test example 384: foo bar.

    Source: spec.txt lines 6644-6648
    """
    md = MarkdownIt()

    input_text = '__foo bar__'
    expected = '<p><strong>foo bar</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example385():
    """Test example 385: foo bar.

    Source: spec.txt lines 6654-6658
    """
    md = MarkdownIt()

    input_text = '__ foo bar__'
    expected = '<p>__ foo bar__</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example386():
    """Test example 386: foo bar.

    Source: spec.txt lines 6662-6668
    """
    md = MarkdownIt()

    input_text = '__\nfoo bar__'
    expected = '<p>__\nfoo bar__</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example387():
    """Test example 387: afoo.

    Source: spec.txt lines 6674-6678
    """
    md = MarkdownIt()

    input_text = 'a__"foo"__'
    expected = '<p>a__&quot;foo&quot;__</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example388():
    """Test example 388: foobar.

    Source: spec.txt lines 6683-6687
    """
    md = MarkdownIt()

    input_text = 'foo__bar__'
    expected = '<p>foo__bar__</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example389():
    """Test example 389: 5678.

    Source: spec.txt lines 6690-6694
    """
    md = MarkdownIt()

    input_text = '5__6__78'
    expected = '<p>5__6__78</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example390():
    """Test example 390.

    Source: spec.txt lines 6697-6701
    """
    md = MarkdownIt()

    input_text = 'пристаням__стремятся__'
    expected = '<p>пристаням__стремятся__</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example391():
    """Test example 391: foo bar baz.

    Source: spec.txt lines 6704-6708
    """
    md = MarkdownIt()

    input_text = '__foo, __bar__, baz__'
    expected = '<p><strong>foo, <strong>bar</strong>, baz</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example392():
    """Test example 392: foobar.

    Source: spec.txt lines 6715-6719
    """
    md = MarkdownIt()

    input_text = 'foo-__(bar)__'
    expected = '<p>foo-<strong>(bar)</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example393():
    """Test example 393: foo bar.

    Source: spec.txt lines 6728-6732
    """
    md = MarkdownIt()

    input_text = '**foo bar **'
    expected = '<p>**foo bar **</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example394():
    """Test example 394: foo.

    Source: spec.txt lines 6741-6745
    """
    md = MarkdownIt()

    input_text = '**(**foo)'
    expected = '<p>**(**foo)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example395():
    """Test example 395: foo.

    Source: spec.txt lines 6751-6755
    """
    md = MarkdownIt()

    input_text = '*(**foo**)*'
    expected = '<p><em>(<strong>foo</strong>)</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example396():
    """Test example 396: Gomphocarpus Gomphocarpus physocarpus syn.

    Source: spec.txt lines 6758-6764
    """
    md = MarkdownIt()

    input_text = '**Gomphocarpus (*Gomphocarpus physocarpus*, syn.\n*Asclepias physocarpa*)**'
    expected = '<p><strong>Gomphocarpus (<em>Gomphocarpus physocarpus</em>, syn.\n<em>Asclepias physocarpa</em>)</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example397():
    """Test example 397: foo bar foo.

    Source: spec.txt lines 6767-6771
    """
    md = MarkdownIt()

    input_text = '**foo "*bar*" foo**'
    expected = '<p><strong>foo &quot;<em>bar</em>&quot; foo</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example398():
    """Test example 398: foobar.

    Source: spec.txt lines 6776-6780
    """
    md = MarkdownIt()

    input_text = '**foo**bar'
    expected = '<p><strong>foo</strong>bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example399():
    """Test example 399: foo bar.

    Source: spec.txt lines 6788-6792
    """
    md = MarkdownIt()

    input_text = '__foo bar __'
    expected = '<p>__foo bar __</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example400():
    """Test example 400: foo.

    Source: spec.txt lines 6798-6802
    """
    md = MarkdownIt()

    input_text = '__(__foo)'
    expected = '<p>__(__foo)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example401():
    """Test example 401: foo.

    Source: spec.txt lines 6808-6812
    """
    md = MarkdownIt()

    input_text = '_(__foo__)_'
    expected = '<p><em>(<strong>foo</strong>)</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example402():
    """Test example 402: foobar.

    Source: spec.txt lines 6817-6821
    """
    md = MarkdownIt()

    input_text = '__foo__bar'
    expected = '<p>__foo__bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example403():
    """Test example 403.

    Source: spec.txt lines 6824-6828
    """
    md = MarkdownIt()

    input_text = '__пристаням__стремятся'
    expected = '<p>__пристаням__стремятся</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example404():
    """Test example 404: foobarbaz.

    Source: spec.txt lines 6831-6835
    """
    md = MarkdownIt()

    input_text = '__foo__bar__baz__'
    expected = '<p><strong>foo__bar__baz</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example405():
    """Test example 405: bar.

    Source: spec.txt lines 6842-6846
    """
    md = MarkdownIt()

    input_text = '__(bar)__.'
    expected = '<p><strong>(bar)</strong>.</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example406():
    """Test example 406: foo barurl.

    Source: spec.txt lines 6854-6858
    """
    md = MarkdownIt()

    input_text = '*foo [bar](/url)*'
    expected = '<p><em>foo <a href="/url">bar</a></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example407():
    """Test example 407: foo bar.

    Source: spec.txt lines 6861-6867
    """
    md = MarkdownIt()

    input_text = '*foo\nbar*'
    expected = '<p><em>foo\nbar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example408():
    """Test example 408: foo bar baz.

    Source: spec.txt lines 6873-6877
    """
    md = MarkdownIt()

    input_text = '_foo __bar__ baz_'
    expected = '<p><em>foo <strong>bar</strong> baz</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example409():
    """Test example 409: foo bar baz.

    Source: spec.txt lines 6880-6884
    """
    md = MarkdownIt()

    input_text = '_foo _bar_ baz_'
    expected = '<p><em>foo <em>bar</em> baz</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example410():
    """Test example 410: foo bar.

    Source: spec.txt lines 6887-6891
    """
    md = MarkdownIt()

    input_text = '__foo_ bar_'
    expected = '<p><em><em>foo</em> bar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example411():
    """Test example 411: foo bar.

    Source: spec.txt lines 6894-6898
    """
    md = MarkdownIt()

    input_text = '*foo *bar**'
    expected = '<p><em>foo <em>bar</em></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example412():
    """Test example 412: foo bar baz.

    Source: spec.txt lines 6901-6905
    """
    md = MarkdownIt()

    input_text = '*foo **bar** baz*'
    expected = '<p><em>foo <strong>bar</strong> baz</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example413():
    """Test example 413: foobarbaz.

    Source: spec.txt lines 6907-6911
    """
    md = MarkdownIt()

    input_text = '*foo**bar**baz*'
    expected = '<p><em>foo<strong>bar</strong>baz</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example414():
    """Test example 414: foobar.

    Source: spec.txt lines 6931-6935
    """
    md = MarkdownIt()

    input_text = '*foo**bar*'
    expected = '<p><em>foo**bar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example415():
    """Test example 415: foo bar.

    Source: spec.txt lines 6944-6948
    """
    md = MarkdownIt()

    input_text = '***foo** bar*'
    expected = '<p><em><strong>foo</strong> bar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example416():
    """Test example 416: foo bar.

    Source: spec.txt lines 6951-6955
    """
    md = MarkdownIt()

    input_text = '*foo **bar***'
    expected = '<p><em>foo <strong>bar</strong></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example417():
    """Test example 417: foobar.

    Source: spec.txt lines 6958-6962
    """
    md = MarkdownIt()

    input_text = '*foo**bar***'
    expected = '<p><em>foo<strong>bar</strong></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example418():
    """Test example 418: foobarbaz.

    Source: spec.txt lines 6969-6973
    """
    md = MarkdownIt()

    input_text = 'foo***bar***baz'
    expected = '<p>foo<em><strong>bar</strong></em>baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example419():
    """Test example 419: foobarbaz.

    Source: spec.txt lines 6975-6979
    """
    md = MarkdownIt()

    input_text = 'foo******bar*********baz'
    expected = '<p>foo<strong><strong><strong>bar</strong></strong></strong>***baz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example420():
    """Test example 420: foo bar baz bim bop.

    Source: spec.txt lines 6984-6988
    """
    md = MarkdownIt()

    input_text = '*foo **bar *baz* bim** bop*'
    expected = '<p><em>foo <strong>bar <em>baz</em> bim</strong> bop</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example421():
    """Test example 421: foo barurl.

    Source: spec.txt lines 6991-6995
    """
    md = MarkdownIt()

    input_text = '*foo [*bar*](/url)*'
    expected = '<p><em>foo <a href="/url"><em>bar</em></a></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example422():
    """Test example 422: is not an empty emphasis.

    Source: spec.txt lines 7000-7004
    """
    md = MarkdownIt()

    input_text = '** is not an empty emphasis'
    expected = '<p>** is not an empty emphasis</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example423():
    """Test example 423: is not an empty strong emphasis.

    Source: spec.txt lines 7007-7011
    """
    md = MarkdownIt()

    input_text = '**** is not an empty strong emphasis'
    expected = '<p>**** is not an empty strong emphasis</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example424():
    """Test example 424: foo barurl.

    Source: spec.txt lines 7020-7024
    """
    md = MarkdownIt()

    input_text = '**foo [bar](/url)**'
    expected = '<p><strong>foo <a href="/url">bar</a></strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example425():
    """Test example 425: foo bar.

    Source: spec.txt lines 7027-7033
    """
    md = MarkdownIt()

    input_text = '**foo\nbar**'
    expected = '<p><strong>foo\nbar</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example426():
    """Test example 426: foo bar baz.

    Source: spec.txt lines 7039-7043
    """
    md = MarkdownIt()

    input_text = '__foo _bar_ baz__'
    expected = '<p><strong>foo <em>bar</em> baz</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example427():
    """Test example 427: foo bar baz.

    Source: spec.txt lines 7046-7050
    """
    md = MarkdownIt()

    input_text = '__foo __bar__ baz__'
    expected = '<p><strong>foo <strong>bar</strong> baz</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example428():
    """Test example 428: foo bar.

    Source: spec.txt lines 7053-7057
    """
    md = MarkdownIt()

    input_text = '____foo__ bar__'
    expected = '<p><strong><strong>foo</strong> bar</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example429():
    """Test example 429: foo bar.

    Source: spec.txt lines 7060-7064
    """
    md = MarkdownIt()

    input_text = '**foo **bar****'
    expected = '<p><strong>foo <strong>bar</strong></strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example430():
    """Test example 430: foo bar baz.

    Source: spec.txt lines 7067-7071
    """
    md = MarkdownIt()

    input_text = '**foo *bar* baz**'
    expected = '<p><strong>foo <em>bar</em> baz</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example431():
    """Test example 431: foobarbaz.

    Source: spec.txt lines 7074-7078
    """
    md = MarkdownIt()

    input_text = '**foo*bar*baz**'
    expected = '<p><strong>foo<em>bar</em>baz</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example432():
    """Test example 432: foo bar.

    Source: spec.txt lines 7081-7085
    """
    md = MarkdownIt()

    input_text = '***foo* bar**'
    expected = '<p><strong><em>foo</em> bar</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example433():
    """Test example 433: foo bar.

    Source: spec.txt lines 7088-7092
    """
    md = MarkdownIt()

    input_text = '**foo *bar***'
    expected = '<p><strong>foo <em>bar</em></strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example434():
    """Test example 434: foo bar baz bim bop.

    Source: spec.txt lines 7097-7103
    """
    md = MarkdownIt()

    input_text = '**foo *bar **baz**\nbim* bop**'
    expected = '<p><strong>foo <em>bar <strong>baz</strong>\nbim</em> bop</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example435():
    """Test example 435: foo barurl.

    Source: spec.txt lines 7106-7110
    """
    md = MarkdownIt()

    input_text = '**foo [*bar*](/url)**'
    expected = '<p><strong>foo <a href="/url"><em>bar</em></a></strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example436():
    """Test example 436: is not an empty emphasis.

    Source: spec.txt lines 7115-7119
    """
    md = MarkdownIt()

    input_text = '__ is not an empty emphasis'
    expected = '<p>__ is not an empty emphasis</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example437():
    """Test example 437: is not an empty strong emphasis.

    Source: spec.txt lines 7122-7126
    """
    md = MarkdownIt()

    input_text = '____ is not an empty strong emphasis'
    expected = '<p>____ is not an empty strong emphasis</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example438():
    """Test example 438: foo.

    Source: spec.txt lines 7132-7136
    """
    md = MarkdownIt()

    input_text = 'foo ***'
    expected = '<p>foo ***</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example439():
    """Test example 439: foo.

    Source: spec.txt lines 7139-7143
    """
    md = MarkdownIt()

    input_text = 'foo *\\**'
    expected = '<p>foo <em>*</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example440():
    """Test example 440: foo.

    Source: spec.txt lines 7146-7150
    """
    md = MarkdownIt()

    input_text = 'foo *_*'
    expected = '<p>foo <em>_</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example441():
    """Test example 441: foo.

    Source: spec.txt lines 7153-7157
    """
    md = MarkdownIt()

    input_text = 'foo *****'
    expected = '<p>foo *****</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example442():
    """Test example 442: foo.

    Source: spec.txt lines 7160-7164
    """
    md = MarkdownIt()

    input_text = 'foo **\\***'
    expected = '<p>foo <strong>*</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example443():
    """Test example 443: foo.

    Source: spec.txt lines 7167-7171
    """
    md = MarkdownIt()

    input_text = 'foo **_**'
    expected = '<p>foo <strong>_</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example444():
    """Test example 444: foo.

    Source: spec.txt lines 7178-7182
    """
    md = MarkdownIt()

    input_text = '**foo*'
    expected = '<p>*<em>foo</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example445():
    """Test example 445: foo.

    Source: spec.txt lines 7185-7189
    """
    md = MarkdownIt()

    input_text = '*foo**'
    expected = '<p><em>foo</em>*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example446():
    """Test example 446: foo.

    Source: spec.txt lines 7192-7196
    """
    md = MarkdownIt()

    input_text = '***foo**'
    expected = '<p>*<strong>foo</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example447():
    """Test example 447: foo.

    Source: spec.txt lines 7199-7203
    """
    md = MarkdownIt()

    input_text = '****foo*'
    expected = '<p>***<em>foo</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example448():
    """Test example 448: foo.

    Source: spec.txt lines 7206-7210
    """
    md = MarkdownIt()

    input_text = '**foo***'
    expected = '<p><strong>foo</strong>*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example449():
    """Test example 449: foo.

    Source: spec.txt lines 7213-7217
    """
    md = MarkdownIt()

    input_text = '*foo****'
    expected = '<p><em>foo</em>***</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example450():
    """Test example 450: foo.

    Source: spec.txt lines 7223-7227
    """
    md = MarkdownIt()

    input_text = 'foo ___'
    expected = '<p>foo ___</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example451():
    """Test example 451: foo.

    Source: spec.txt lines 7230-7234
    """
    md = MarkdownIt()

    input_text = 'foo _\\__'
    expected = '<p>foo <em>_</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example452():
    """Test example 452: foo.

    Source: spec.txt lines 7237-7241
    """
    md = MarkdownIt()

    input_text = 'foo _*_'
    expected = '<p>foo <em>*</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example453():
    """Test example 453: foo.

    Source: spec.txt lines 7244-7248
    """
    md = MarkdownIt()

    input_text = 'foo _____'
    expected = '<p>foo _____</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example454():
    """Test example 454: foo.

    Source: spec.txt lines 7251-7255
    """
    md = MarkdownIt()

    input_text = 'foo __\\___'
    expected = '<p>foo <strong>_</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example455():
    """Test example 455: foo.

    Source: spec.txt lines 7258-7262
    """
    md = MarkdownIt()

    input_text = 'foo __*__'
    expected = '<p>foo <strong>*</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example456():
    """Test example 456: foo.

    Source: spec.txt lines 7265-7269
    """
    md = MarkdownIt()

    input_text = '__foo_'
    expected = '<p>_<em>foo</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example457():
    """Test example 457: foo.

    Source: spec.txt lines 7276-7280
    """
    md = MarkdownIt()

    input_text = '_foo__'
    expected = '<p><em>foo</em>_</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example458():
    """Test example 458: foo.

    Source: spec.txt lines 7283-7287
    """
    md = MarkdownIt()

    input_text = '___foo__'
    expected = '<p>_<strong>foo</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example459():
    """Test example 459: foo.

    Source: spec.txt lines 7290-7294
    """
    md = MarkdownIt()

    input_text = '____foo_'
    expected = '<p>___<em>foo</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example460():
    """Test example 460: foo.

    Source: spec.txt lines 7297-7301
    """
    md = MarkdownIt()

    input_text = '__foo___'
    expected = '<p><strong>foo</strong>_</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example461():
    """Test example 461: foo.

    Source: spec.txt lines 7304-7308
    """
    md = MarkdownIt()

    input_text = '_foo____'
    expected = '<p><em>foo</em>___</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example462():
    """Test example 462: foo.

    Source: spec.txt lines 7314-7318
    """
    md = MarkdownIt()

    input_text = '**foo**'
    expected = '<p><strong>foo</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example463():
    """Test example 463: foo.

    Source: spec.txt lines 7321-7325
    """
    md = MarkdownIt()

    input_text = '*_foo_*'
    expected = '<p><em><em>foo</em></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example464():
    """Test example 464: foo.

    Source: spec.txt lines 7328-7332
    """
    md = MarkdownIt()

    input_text = '__foo__'
    expected = '<p><strong>foo</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example465():
    """Test example 465: foo.

    Source: spec.txt lines 7335-7339
    """
    md = MarkdownIt()

    input_text = '_*foo*_'
    expected = '<p><em><em>foo</em></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example466():
    """Test example 466: foo.

    Source: spec.txt lines 7345-7349
    """
    md = MarkdownIt()

    input_text = '****foo****'
    expected = '<p><strong><strong>foo</strong></strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example467():
    """Test example 467: foo.

    Source: spec.txt lines 7352-7356
    """
    md = MarkdownIt()

    input_text = '____foo____'
    expected = '<p><strong><strong>foo</strong></strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example468():
    """Test example 468: foo.

    Source: spec.txt lines 7363-7367
    """
    md = MarkdownIt()

    input_text = '******foo******'
    expected = '<p><strong><strong><strong>foo</strong></strong></strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example469():
    """Test example 469: foo.

    Source: spec.txt lines 7372-7376
    """
    md = MarkdownIt()

    input_text = '***foo***'
    expected = '<p><em><strong>foo</strong></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example470():
    """Test example 470: foo.

    Source: spec.txt lines 7379-7383
    """
    md = MarkdownIt()

    input_text = '_____foo_____'
    expected = '<p><em><strong><strong>foo</strong></strong></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example471():
    """Test example 471: foo bar baz.

    Source: spec.txt lines 7388-7392
    """
    md = MarkdownIt()

    input_text = '*foo _bar* baz_'
    expected = '<p><em>foo _bar</em> baz_</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example472():
    """Test example 472: foo bar baz bim bam.

    Source: spec.txt lines 7395-7399
    """
    md = MarkdownIt()

    input_text = '*foo __bar *baz bim__ bam*'
    expected = '<p><em>foo <strong>bar *baz bim</strong> bam</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example473():
    """Test example 473: foo bar baz.

    Source: spec.txt lines 7404-7408
    """
    md = MarkdownIt()

    input_text = '**foo **bar baz**'
    expected = '<p>**foo <strong>bar baz</strong></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example474():
    """Test example 474: foo bar baz.

    Source: spec.txt lines 7411-7415
    """
    md = MarkdownIt()

    input_text = '*foo *bar baz*'
    expected = '<p>*foo <em>bar baz</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example475():
    """Test example 475: barurl.

    Source: spec.txt lines 7420-7424
    """
    md = MarkdownIt()

    input_text = '*[bar*](/url)'
    expected = '<p>*<a href="/url">bar*</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example476():
    """Test example 476: foo barurl.

    Source: spec.txt lines 7427-7431
    """
    md = MarkdownIt()

    input_text = '_foo [bar_](/url)'
    expected = '<p>_foo <a href="/url">bar_</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example477():
    """Test example 477: img srcfoo title.

    Source: spec.txt lines 7434-7438
    """
    md = MarkdownIt()

    input_text = '*<img src="foo" title="*"/>'
    expected = '<p>*<img src="foo" title="*"/></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example478():
    """Test example 478: a href.

    Source: spec.txt lines 7441-7445
    """
    md = MarkdownIt()

    input_text = '**<a href="**">'
    expected = '<p>**<a href="**"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example479():
    """Test example 479: a href.

    Source: spec.txt lines 7448-7452
    """
    md = MarkdownIt()

    input_text = '__<a href="__">'
    expected = '<p>__<a href="__"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example480():
    """Test example 480: a.

    Source: spec.txt lines 7455-7459
    """
    md = MarkdownIt()

    input_text = '*a `*`*'
    expected = '<p><em>a <code>*</code></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example481():
    """Test example 481: a.

    Source: spec.txt lines 7462-7466
    """
    md = MarkdownIt()

    input_text = '_a `_`_'
    expected = '<p><em>a <code>_</code></em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example482():
    """Test example 482: ahttpsfoobarq.

    Source: spec.txt lines 7469-7473
    """
    md = MarkdownIt()

    input_text = '**a<https://foo.bar/?q=**>'
    expected = '<p>**a<a href="https://foo.bar/?q=**">https://foo.bar/?q=**</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example483():
    """Test example 483: ahttpsfoobarq.

    Source: spec.txt lines 7476-7480
    """
    md = MarkdownIt()

    input_text = '__a<https://foo.bar/?q=__>'
    expected = '<p>__a<a href="https://foo.bar/?q=__">https://foo.bar/?q=__</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example484():
    """Test example 484: linkuri title.

    Source: spec.txt lines 7564-7568
    """
    md = MarkdownIt()

    input_text = '[link](/uri "title")'
    expected = '<p><a href="/uri" title="title">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example485():
    """Test example 485: linkuri.

    Source: spec.txt lines 7574-7578
    """
    md = MarkdownIt()

    input_text = '[link](/uri)'
    expected = '<p><a href="/uri">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example486():
    """Test example 486: targetmd.

    Source: spec.txt lines 7580-7584
    """
    md = MarkdownIt()

    input_text = '[](./target.md)'
    expected = '<p><a href="./target.md"></a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example487():
    """Test example 487: link.

    Source: spec.txt lines 7587-7591
    """
    md = MarkdownIt()

    input_text = '[link]()'
    expected = '<p><a href="">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example488():
    """Test example 488: link.

    Source: spec.txt lines 7594-7598
    """
    md = MarkdownIt()

    input_text = '[link](<>)'
    expected = '<p><a href="">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example489():
    """Test example 489.

    Source: spec.txt lines 7601-7605
    """
    md = MarkdownIt()

    input_text = '[]()'
    expected = '<p><a href=""></a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example490():
    """Test example 490: linkmy uri.

    Source: spec.txt lines 7610-7614
    """
    md = MarkdownIt()

    input_text = '[link](/my uri)'
    expected = '<p>[link](/my uri)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example491():
    """Test example 491: linkmy uri.

    Source: spec.txt lines 7616-7620
    """
    md = MarkdownIt()

    input_text = '[link](</my uri>)'
    expected = '<p><a href="/my%20uri">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example492():
    """Test example 492: linkfoo bar.

    Source: spec.txt lines 7625-7631
    """
    md = MarkdownIt()

    input_text = '[link](foo\nbar)'
    expected = '<p>[link](foo\nbar)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example493():
    """Test example 493: linkfoo bar.

    Source: spec.txt lines 7633-7639
    """
    md = MarkdownIt()

    input_text = '[link](<foo\nbar>)'
    expected = '<p>[link](<foo\nbar>)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example494():
    """Test example 494: abc.

    Source: spec.txt lines 7644-7648
    """
    md = MarkdownIt()

    input_text = '[a](<b)c>)'
    expected = '<p><a href="b)c">a</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example495():
    """Test example 495: linkfoo.

    Source: spec.txt lines 7652-7656
    """
    md = MarkdownIt()

    input_text = '[link](<foo\\>)'
    expected = '<p>[link](&lt;foo&gt;)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example496():
    """Test example 496: abc abc abc.

    Source: spec.txt lines 7661-7669
    """
    md = MarkdownIt()

    input_text = '[a](<b)c\n[a](<b)c>\n[a](<b>c)'
    expected = '<p>[a](&lt;b)c\n[a](&lt;b)c&gt;\n[a](<b>c)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example497():
    """Test example 497: linkfoo.

    Source: spec.txt lines 7673-7677
    """
    md = MarkdownIt()

    input_text = '[link](\\(foo\\))'
    expected = '<p><a href="(foo)">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example498():
    """Test example 498: linkfooandbar.

    Source: spec.txt lines 7682-7686
    """
    md = MarkdownIt()

    input_text = '[link](foo(and(bar)))'
    expected = '<p><a href="foo(and(bar))">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example499():
    """Test example 499: linkfooandbar.

    Source: spec.txt lines 7691-7695
    """
    md = MarkdownIt()

    input_text = '[link](foo(and(bar))'
    expected = '<p>[link](foo(and(bar))</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example500():
    """Test example 500: linkfooandbar.

    Source: spec.txt lines 7698-7702
    """
    md = MarkdownIt()

    input_text = '[link](foo\\(and\\(bar\\))'
    expected = '<p><a href="foo(and(bar)">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example501():
    """Test example 501: linkfooandbar.

    Source: spec.txt lines 7705-7709
    """
    md = MarkdownIt()

    input_text = '[link](<foo(and(bar)>)'
    expected = '<p><a href="foo(and(bar)">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example502():
    """Test example 502: linkfoo.

    Source: spec.txt lines 7715-7719
    """
    md = MarkdownIt()

    input_text = '[link](foo\\)\\:)'
    expected = '<p><a href="foo):">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example503():
    """Test example 503: linkfragment  linkhttpsexamplecomfrag.

    Source: spec.txt lines 7724-7734
    """
    md = MarkdownIt()

    input_text = '[link](#fragment)\n\n[link](https://example.com#fragment)\n\n[link](https://example.com?foo=3#frag)'
    expected = '<p><a href="#fragment">link</a></p>\n<p><a href="https://example.com#fragment">link</a></p>\n<p><a href="https://example.com?foo=3#frag">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example504():
    """Test example 504: linkfoobar.

    Source: spec.txt lines 7740-7744
    """
    md = MarkdownIt()

    input_text = '[link](foo\\bar)'
    expected = '<p><a href="foo%5Cbar">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example505():
    """Test example 505: linkfoo20bauml.

    Source: spec.txt lines 7756-7760
    """
    md = MarkdownIt()

    input_text = '[link](foo%20b&auml;)'
    expected = '<p><a href="foo%20b%C3%A4">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example506():
    """Test example 506: linktitle.

    Source: spec.txt lines 7767-7771
    """
    md = MarkdownIt()

    input_text = '[link]("title")'
    expected = '<p><a href="%22title%22">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example507():
    """Test example 507: linkurl title linkurl title link.

    Source: spec.txt lines 7776-7784
    """
    md = MarkdownIt()

    input_text = '[link](/url "title")\n[link](/url \'title\')\n[link](/url (title))'
    expected = '<p><a href="/url" title="title">link</a>\n<a href="/url" title="title">link</a>\n<a href="/url" title="title">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example508():
    """Test example 508: linkurl title quot.

    Source: spec.txt lines 7790-7794
    """
    md = MarkdownIt()

    input_text = '[link](/url "title \\"&quot;")'
    expected = '<p><a href="/url" title="title &quot;&quot;">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example509():
    """Test example 509: linkurltitle.

    Source: spec.txt lines 7801-7805
    """
    md = MarkdownIt()

    input_text = '[link](/url\xa0"title")'
    expected = '<p><a href="/url%C2%A0%22title%22">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example510():
    """Test example 510: linkurl title and title.

    Source: spec.txt lines 7810-7814
    """
    md = MarkdownIt()

    input_text = '[link](/url "title "and" title")'
    expected = '<p>[link](/url &quot;title &quot;and&quot; title&quot;)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example511():
    """Test example 511: linkurl title and title.

    Source: spec.txt lines 7819-7823
    """
    md = MarkdownIt()

    input_text = '[link](/url \'title "and" title\')'
    expected = '<p><a href="/url" title="title &quot;and&quot; title">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example512():
    """Test example 512: link   uri   title.

    Source: spec.txt lines 7844-7849
    """
    md = MarkdownIt()

    input_text = '[link](   /uri\n  "title"  )'
    expected = '<p><a href="/uri" title="title">link</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example513():
    """Test example 513: link uri.

    Source: spec.txt lines 7855-7859
    """
    md = MarkdownIt()

    input_text = '[link] (/uri)'
    expected = '<p>[link] (/uri)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example514():
    """Test example 514: link foo baruri.

    Source: spec.txt lines 7865-7869
    """
    md = MarkdownIt()

    input_text = '[link [foo [bar]]](/uri)'
    expected = '<p><a href="/uri">link [foo [bar]]</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example515():
    """Test example 515: link baruri.

    Source: spec.txt lines 7872-7876
    """
    md = MarkdownIt()

    input_text = '[link] bar](/uri)'
    expected = '<p>[link] bar](/uri)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example516():
    """Test example 516: link baruri.

    Source: spec.txt lines 7879-7883
    """
    md = MarkdownIt()

    input_text = '[link [bar](/uri)'
    expected = '<p>[link <a href="/uri">bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example517():
    """Test example 517: link baruri.

    Source: spec.txt lines 7886-7890
    """
    md = MarkdownIt()

    input_text = '[link \\[bar](/uri)'
    expected = '<p><a href="/uri">link [bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example518():
    """Test example 518: link foo bar uri.

    Source: spec.txt lines 7895-7899
    """
    md = MarkdownIt()

    input_text = '[link *foo **bar** `#`*](/uri)'
    expected = '<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example519():
    """Test example 519: moonmoonjpguri.

    Source: spec.txt lines 7902-7906
    """
    md = MarkdownIt()

    input_text = '[![moon](moon.jpg)](/uri)'
    expected = '<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example520():
    """Test example 520: foo baruriuri.

    Source: spec.txt lines 7911-7915
    """
    md = MarkdownIt()

    input_text = '[foo [bar](/uri)](/uri)'
    expected = '<p>[foo <a href="/uri">bar</a>](/uri)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example521():
    """Test example 521: foo bar bazuriuriuri.

    Source: spec.txt lines 7918-7922
    """
    md = MarkdownIt()

    input_text = '[foo *[bar [baz](/uri)](/uri)*](/uri)'
    expected = '<p>[foo <em>[bar <a href="/uri">baz</a>](/uri)</em>](/uri)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example522():
    """Test example 522: foouri1uri2uri3.

    Source: spec.txt lines 7925-7929
    """
    md = MarkdownIt()

    input_text = '![[[foo](uri1)](uri2)](uri3)'
    expected = '<p><img src="uri3" alt="[foo](uri2)" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example523():
    """Test example 523: foouri.

    Source: spec.txt lines 7935-7939
    """
    md = MarkdownIt()

    input_text = '*[foo*](/uri)'
    expected = '<p>*<a href="/uri">foo*</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example524():
    """Test example 524: foo barbaz.

    Source: spec.txt lines 7942-7946
    """
    md = MarkdownIt()

    input_text = '[foo *bar](baz*)'
    expected = '<p><a href="baz*">foo *bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example525():
    """Test example 525: foo bar baz.

    Source: spec.txt lines 7952-7956
    """
    md = MarkdownIt()

    input_text = '*foo [bar* baz]'
    expected = '<p><em>foo [bar</em> baz]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example526():
    """Test example 526: foo bar attrbaz.

    Source: spec.txt lines 7962-7966
    """
    md = MarkdownIt()

    input_text = '[foo <bar attr="](baz)">'
    expected = '<p>[foo <bar attr="](baz)"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example527():
    """Test example 527: foouri.

    Source: spec.txt lines 7969-7973
    """
    md = MarkdownIt()

    input_text = '[foo`](/uri)`'
    expected = '<p>[foo<code>](/uri)</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example528():
    """Test example 528: foohttpsexamplecomsearchuri.

    Source: spec.txt lines 7976-7980
    """
    md = MarkdownIt()

    input_text = '[foo<https://example.com/?search=](uri)>'
    expected = '<p>[foo<a href="https://example.com/?search=%5D(uri)">https://example.com/?search=](uri)</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example529():
    """Test example 529: foobar  bar url title.

    Source: spec.txt lines 8014-8020
    """
    md = MarkdownIt()

    input_text = '[foo][bar]\n\n[bar]: /url "title"'
    expected = '<p><a href="/url" title="title">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example530():
    """Test example 530: link foo barref  ref uri.

    Source: spec.txt lines 8029-8035
    """
    md = MarkdownIt()

    input_text = '[link [foo [bar]]][ref]\n\n[ref]: /uri'
    expected = '<p><a href="/uri">link [foo [bar]]</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example531():
    """Test example 531: link barref  ref uri.

    Source: spec.txt lines 8038-8044
    """
    md = MarkdownIt()

    input_text = '[link \\[bar][ref]\n\n[ref]: /uri'
    expected = '<p><a href="/uri">link [bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example532():
    """Test example 532: link foo bar ref  ref uri.

    Source: spec.txt lines 8049-8055
    """
    md = MarkdownIt()

    input_text = '[link *foo **bar** `#`*][ref]\n\n[ref]: /uri'
    expected = '<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example533():
    """Test example 533: moonmoonjpgref  ref uri.

    Source: spec.txt lines 8058-8064
    """
    md = MarkdownIt()

    input_text = '[![moon](moon.jpg)][ref]\n\n[ref]: /uri'
    expected = '<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example534():
    """Test example 534: foo baruriref  ref uri.

    Source: spec.txt lines 8069-8075
    """
    md = MarkdownIt()

    input_text = '[foo [bar](/uri)][ref]\n\n[ref]: /uri'
    expected = '<p>[foo <a href="/uri">bar</a>]<a href="/uri">ref</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example535():
    """Test example 535: foo bar bazrefref  ref uri.

    Source: spec.txt lines 8078-8084
    """
    md = MarkdownIt()

    input_text = '[foo *bar [baz][ref]*][ref]\n\n[ref]: /uri'
    expected = '<p>[foo <em>bar <a href="/uri">baz</a></em>]<a href="/uri">ref</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example536():
    """Test example 536: fooref  ref uri.

    Source: spec.txt lines 8093-8099
    """
    md = MarkdownIt()

    input_text = '*[foo*][ref]\n\n[ref]: /uri'
    expected = '<p>*<a href="/uri">foo*</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example537():
    """Test example 537: foo barref  ref uri.

    Source: spec.txt lines 8102-8108
    """
    md = MarkdownIt()

    input_text = '[foo *bar][ref]*\n\n[ref]: /uri'
    expected = '<p><a href="/uri">foo *bar</a>*</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example538():
    """Test example 538: foo bar attrref  ref uri.

    Source: spec.txt lines 8114-8120
    """
    md = MarkdownIt()

    input_text = '[foo <bar attr="][ref]">\n\n[ref]: /uri'
    expected = '<p>[foo <bar attr="][ref]"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example539():
    """Test example 539: fooref  ref uri.

    Source: spec.txt lines 8123-8129
    """
    md = MarkdownIt()

    input_text = '[foo`][ref]`\n\n[ref]: /uri'
    expected = '<p>[foo<code>][ref]</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example540():
    """Test example 540: foohttpsexamplecomsearchref  ref.

    Source: spec.txt lines 8132-8138
    """
    md = MarkdownIt()

    input_text = '[foo<https://example.com/?search=][ref]>\n\n[ref]: /uri'
    expected = '<p>[foo<a href="https://example.com/?search=%5D%5Bref%5D">https://example.com/?search=][ref]</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example541():
    """Test example 541: fooBaR  bar url title.

    Source: spec.txt lines 8143-8149
    """
    md = MarkdownIt()

    input_text = '[foo][BaR]\n\n[bar]: /url "title"'
    expected = '<p><a href="/url" title="title">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example542():
    """Test example 542: SS url.

    Source: spec.txt lines 8154-8160
    """
    md = MarkdownIt()

    input_text = '[ẞ]\n\n[SS]: /url'
    expected = '<p><a href="/url">ẞ</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example543():
    """Test example 543: Foo   bar url  BazFoo bar.

    Source: spec.txt lines 8166-8173
    """
    md = MarkdownIt()

    input_text = '[Foo\n  bar]: /url\n\n[Baz][Foo bar]'
    expected = '<p><a href="/url">Baz</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example544():
    """Test example 544: foo bar  bar url title.

    Source: spec.txt lines 8179-8185
    """
    md = MarkdownIt()

    input_text = '[foo] [bar]\n\n[bar]: /url "title"'
    expected = '<p>[foo] <a href="/url" title="title">bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example545():
    """Test example 545: foo bar  bar url title.

    Source: spec.txt lines 8188-8196
    """
    md = MarkdownIt()

    input_text = '[foo]\n[bar]\n\n[bar]: /url "title"'
    expected = '<p>[foo]\n<a href="/url" title="title">bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example546():
    """Test example 546: foo url1  foo url2  barfoo.

    Source: spec.txt lines 8229-8237
    """
    md = MarkdownIt()

    input_text = '[foo]: /url1\n\n[foo]: /url2\n\n[bar][foo]'
    expected = '<p><a href="/url1">bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example547():
    """Test example 547: barfoo  foo url.

    Source: spec.txt lines 8244-8250
    """
    md = MarkdownIt()

    input_text = '[bar][foo\\!]\n\n[foo!]: /url'
    expected = '<p>[bar][foo!]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example548():
    """Test example 548: fooref  ref uri.

    Source: spec.txt lines 8256-8263
    """
    md = MarkdownIt()

    input_text = '[foo][ref[]\n\n[ref[]: /uri'
    expected = '<p>[foo][ref[]</p>\n<p>[ref[]: /uri</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example549():
    """Test example 549: foorefbar  refbar uri.

    Source: spec.txt lines 8266-8273
    """
    md = MarkdownIt()

    input_text = '[foo][ref[bar]]\n\n[ref[bar]]: /uri'
    expected = '<p>[foo][ref[bar]]</p>\n<p>[ref[bar]]: /uri</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example550():
    """Test example 550: foo  foo url.

    Source: spec.txt lines 8276-8283
    """
    md = MarkdownIt()

    input_text = '[[[foo]]]\n\n[[[foo]]]: /url'
    expected = '<p>[[[foo]]]</p>\n<p>[[[foo]]]: /url</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example551():
    """Test example 551: fooref  ref uri.

    Source: spec.txt lines 8286-8292
    """
    md = MarkdownIt()

    input_text = '[foo][ref\\[]\n\n[ref\\[]: /uri'
    expected = '<p><a href="/uri">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example552():
    """Test example 552: bar uri  bar.

    Source: spec.txt lines 8297-8303
    """
    md = MarkdownIt()

    input_text = '[bar\\\\]: /uri\n\n[bar\\\\]'
    expected = '<p><a href="/uri">bar\\</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example553():
    """Test example 553: uri.

    Source: spec.txt lines 8309-8316
    """
    md = MarkdownIt()

    input_text = '[]\n\n[]: /uri'
    expected = '<p>[]</p>\n<p>[]: /uri</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example554():
    """Test example 554: uri.

    Source: spec.txt lines 8319-8330
    """
    md = MarkdownIt()

    input_text = '[\n ]\n\n[\n ]: /uri'
    expected = '<p>[\n]</p>\n<p>[\n]: /uri</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example555():
    """Test example 555: foo  foo url title.

    Source: spec.txt lines 8342-8348
    """
    md = MarkdownIt()

    input_text = '[foo][]\n\n[foo]: /url "title"'
    expected = '<p><a href="/url" title="title">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example556():
    """Test example 556: foo bar  foo bar url title.

    Source: spec.txt lines 8351-8357
    """
    md = MarkdownIt()

    input_text = '[*foo* bar][]\n\n[*foo* bar]: /url "title"'
    expected = '<p><a href="/url" title="title"><em>foo</em> bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example557():
    """Test example 557: Foo  foo url title.

    Source: spec.txt lines 8362-8368
    """
    md = MarkdownIt()

    input_text = '[Foo][]\n\n[foo]: /url "title"'
    expected = '<p><a href="/url" title="title">Foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example558():
    """Test example 558: foo    foo url title.

    Source: spec.txt lines 8375-8383
    """
    md = MarkdownIt()

    input_text = '[foo] \n[]\n\n[foo]: /url "title"'
    expected = '<p><a href="/url" title="title">foo</a>\n[]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example559():
    """Test example 559: foo  foo url title.

    Source: spec.txt lines 8395-8401
    """
    md = MarkdownIt()

    input_text = '[foo]\n\n[foo]: /url "title"'
    expected = '<p><a href="/url" title="title">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example560():
    """Test example 560: foo bar  foo bar url title.

    Source: spec.txt lines 8404-8410
    """
    md = MarkdownIt()

    input_text = '[*foo* bar]\n\n[*foo* bar]: /url "title"'
    expected = '<p><a href="/url" title="title"><em>foo</em> bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example561():
    """Test example 561: foo bar  foo bar url title.

    Source: spec.txt lines 8413-8419
    """
    md = MarkdownIt()

    input_text = '[[*foo* bar]]\n\n[*foo* bar]: /url "title"'
    expected = '<p>[<a href="/url" title="title"><em>foo</em> bar</a>]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example562():
    """Test example 562: bar foo  foo url.

    Source: spec.txt lines 8422-8428
    """
    md = MarkdownIt()

    input_text = '[[bar [foo]\n\n[foo]: /url'
    expected = '<p>[[bar <a href="/url">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example563():
    """Test example 563: Foo  foo url title.

    Source: spec.txt lines 8433-8439
    """
    md = MarkdownIt()

    input_text = '[Foo]\n\n[foo]: /url "title"'
    expected = '<p><a href="/url" title="title">Foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example564():
    """Test example 564: foo bar  foo url.

    Source: spec.txt lines 8444-8450
    """
    md = MarkdownIt()

    input_text = '[foo] bar\n\n[foo]: /url'
    expected = '<p><a href="/url">foo</a> bar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example565():
    """Test example 565: foo  foo url title.

    Source: spec.txt lines 8456-8462
    """
    md = MarkdownIt()

    input_text = '\\[foo]\n\n[foo]: /url "title"'
    expected = '<p>[foo]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example566():
    """Test example 566: foo url  foo.

    Source: spec.txt lines 8468-8474
    """
    md = MarkdownIt()

    input_text = '[foo*]: /url\n\n*[foo*]'
    expected = '<p>*<a href="/url">foo*</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example567():
    """Test example 567: foobar  foo url1 bar url2.

    Source: spec.txt lines 8480-8487
    """
    md = MarkdownIt()

    input_text = '[foo][bar]\n\n[foo]: /url1\n[bar]: /url2'
    expected = '<p><a href="/url2">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example568():
    """Test example 568: foo  foo url1.

    Source: spec.txt lines 8489-8495
    """
    md = MarkdownIt()

    input_text = '[foo][]\n\n[foo]: /url1'
    expected = '<p><a href="/url1">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example569():
    """Test example 569: foo  foo url1.

    Source: spec.txt lines 8499-8505
    """
    md = MarkdownIt()

    input_text = '[foo]()\n\n[foo]: /url1'
    expected = '<p><a href="">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example570():
    """Test example 570: foonot a link  foo url1.

    Source: spec.txt lines 8507-8513
    """
    md = MarkdownIt()

    input_text = '[foo](not a link)\n\n[foo]: /url1'
    expected = '<p><a href="/url1">foo</a>(not a link)</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example571():
    """Test example 571: foobarbaz  baz url.

    Source: spec.txt lines 8518-8524
    """
    md = MarkdownIt()

    input_text = '[foo][bar][baz]\n\n[baz]: /url'
    expected = '<p>[foo]<a href="/url">bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example572():
    """Test example 572: foobarbaz  baz url1 bar url2.

    Source: spec.txt lines 8530-8537
    """
    md = MarkdownIt()

    input_text = '[foo][bar][baz]\n\n[baz]: /url1\n[bar]: /url2'
    expected = '<p><a href="/url2">foo</a><a href="/url1">baz</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example573():
    """Test example 573: foobarbaz  baz url1 foo url2.

    Source: spec.txt lines 8543-8550
    """
    md = MarkdownIt()

    input_text = '[foo][bar][baz]\n\n[baz]: /url1\n[foo]: /url2'
    expected = '<p>[foo]<a href="/url1">bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example574():
    """Test example 574: foourl title.

    Source: spec.txt lines 8566-8570
    """
    md = MarkdownIt()

    input_text = '![foo](/url "title")'
    expected = '<p><img src="/url" alt="foo" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example575():
    """Test example 575: foo bar  foo bar trainjpg train  trac.

    Source: spec.txt lines 8573-8579
    """
    md = MarkdownIt()

    input_text = '![foo *bar*]\n\n[foo *bar*]: train.jpg "train & tracks"'
    expected = '<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example576():
    """Test example 576: foo barurlurl2.

    Source: spec.txt lines 8582-8586
    """
    md = MarkdownIt()

    input_text = '![foo ![bar](/url)](/url2)'
    expected = '<p><img src="/url2" alt="foo bar" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example577():
    """Test example 577: foo barurlurl2.

    Source: spec.txt lines 8589-8593
    """
    md = MarkdownIt()

    input_text = '![foo [bar](/url)](/url2)'
    expected = '<p><img src="/url2" alt="foo bar" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example578():
    """Test example 578: foo bar  foo bar trainjpg train  tr.

    Source: spec.txt lines 8603-8609
    """
    md = MarkdownIt()

    input_text = '![foo *bar*][]\n\n[foo *bar*]: train.jpg "train & tracks"'
    expected = '<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example579():
    """Test example 579: foo barfoobar  FOOBAR trainjpg train.

    Source: spec.txt lines 8612-8618
    """
    md = MarkdownIt()

    input_text = '![foo *bar*][foobar]\n\n[FOOBAR]: train.jpg "train & tracks"'
    expected = '<p><img src="train.jpg" alt="foo bar" title="train &amp; tracks" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example580():
    """Test example 580: footrainjpg.

    Source: spec.txt lines 8621-8625
    """
    md = MarkdownIt()

    input_text = '![foo](train.jpg)'
    expected = '<p><img src="train.jpg" alt="foo" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example581():
    """Test example 581: My foo barpathtotrainjpg  title.

    Source: spec.txt lines 8628-8632
    """
    md = MarkdownIt()

    input_text = 'My ![foo bar](/path/to/train.jpg  "title"   )'
    expected = '<p>My <img src="/path/to/train.jpg" alt="foo bar" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example582():
    """Test example 582: foourl.

    Source: spec.txt lines 8635-8639
    """
    md = MarkdownIt()

    input_text = '![foo](<url>)'
    expected = '<p><img src="url" alt="foo" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example583():
    """Test example 583: url.

    Source: spec.txt lines 8642-8646
    """
    md = MarkdownIt()

    input_text = '![](/url)'
    expected = '<p><img src="/url" alt="" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example584():
    """Test example 584: foobar  bar url.

    Source: spec.txt lines 8651-8657
    """
    md = MarkdownIt()

    input_text = '![foo][bar]\n\n[bar]: /url'
    expected = '<p><img src="/url" alt="foo" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example585():
    """Test example 585: foobar  BAR url.

    Source: spec.txt lines 8660-8666
    """
    md = MarkdownIt()

    input_text = '![foo][bar]\n\n[BAR]: /url'
    expected = '<p><img src="/url" alt="foo" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example586():
    """Test example 586: foo  foo url title.

    Source: spec.txt lines 8671-8677
    """
    md = MarkdownIt()

    input_text = '![foo][]\n\n[foo]: /url "title"'
    expected = '<p><img src="/url" alt="foo" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example587():
    """Test example 587: foo bar  foo bar url title.

    Source: spec.txt lines 8680-8686
    """
    md = MarkdownIt()

    input_text = '![*foo* bar][]\n\n[*foo* bar]: /url "title"'
    expected = '<p><img src="/url" alt="foo bar" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example588():
    """Test example 588: Foo  foo url title.

    Source: spec.txt lines 8691-8697
    """
    md = MarkdownIt()

    input_text = '![Foo][]\n\n[foo]: /url "title"'
    expected = '<p><img src="/url" alt="Foo" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example589():
    """Test example 589: foo    foo url title.

    Source: spec.txt lines 8703-8711
    """
    md = MarkdownIt()

    input_text = '![foo] \n[]\n\n[foo]: /url "title"'
    expected = '<p><img src="/url" alt="foo" title="title" />\n[]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example590():
    """Test example 590: foo  foo url title.

    Source: spec.txt lines 8716-8722
    """
    md = MarkdownIt()

    input_text = '![foo]\n\n[foo]: /url "title"'
    expected = '<p><img src="/url" alt="foo" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example591():
    """Test example 591: foo bar  foo bar url title.

    Source: spec.txt lines 8725-8731
    """
    md = MarkdownIt()

    input_text = '![*foo* bar]\n\n[*foo* bar]: /url "title"'
    expected = '<p><img src="/url" alt="foo bar" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example592():
    """Test example 592: foo  foo url title.

    Source: spec.txt lines 8736-8743
    """
    md = MarkdownIt()

    input_text = '![[foo]]\n\n[[foo]]: /url "title"'
    expected = '<p>![[foo]]</p>\n<p>[[foo]]: /url &quot;title&quot;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example593():
    """Test example 593: Foo  foo url title.

    Source: spec.txt lines 8748-8754
    """
    md = MarkdownIt()

    input_text = '![Foo]\n\n[foo]: /url "title"'
    expected = '<p><img src="/url" alt="Foo" title="title" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example594():
    """Test example 594: foo  foo url title.

    Source: spec.txt lines 8760-8766
    """
    md = MarkdownIt()

    input_text = '!\\[foo]\n\n[foo]: /url "title"'
    expected = '<p>![foo]</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example595():
    """Test example 595: foo  foo url title.

    Source: spec.txt lines 8772-8778
    """
    md = MarkdownIt()

    input_text = '\\![foo]\n\n[foo]: /url "title"'
    expected = '<p>!<a href="/url" title="title">foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example596():
    """Test example 596: httpfoobarbaz.

    Source: spec.txt lines 8805-8809
    """
    md = MarkdownIt()

    input_text = '<http://foo.bar.baz>'
    expected = '<p><a href="http://foo.bar.baz">http://foo.bar.baz</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example597():
    """Test example 597: httpsfoobarbaztestqhelloid22boolean.

    Source: spec.txt lines 8812-8816
    """
    md = MarkdownIt()

    input_text = '<https://foo.bar.baz/test?q=hello&id=22&boolean>'
    expected = '<p><a href="https://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean">https://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example598():
    """Test example 598: ircfoobar2233baz.

    Source: spec.txt lines 8819-8823
    """
    md = MarkdownIt()

    input_text = '<irc://foo.bar:2233/baz>'
    expected = '<p><a href="irc://foo.bar:2233/baz">irc://foo.bar:2233/baz</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example599():
    """Test example 599: MAILTOFOOBARBAZ.

    Source: spec.txt lines 8828-8832
    """
    md = MarkdownIt()

    input_text = '<MAILTO:FOO@BAR.BAZ>'
    expected = '<p><a href="MAILTO:FOO@BAR.BAZ">MAILTO:FOO@BAR.BAZ</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example600():
    """Test example 600: abcd.

    Source: spec.txt lines 8840-8844
    """
    md = MarkdownIt()

    input_text = '<a+b+c:d>'
    expected = '<p><a href="a+b+c:d">a+b+c:d</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example601():
    """Test example 601: madeupschemefoobar.

    Source: spec.txt lines 8847-8851
    """
    md = MarkdownIt()

    input_text = '<made-up-scheme://foo,bar>'
    expected = '<p><a href="made-up-scheme://foo,bar">made-up-scheme://foo,bar</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example602():
    """Test example 602: https.

    Source: spec.txt lines 8854-8858
    """
    md = MarkdownIt()

    input_text = '<https://../>'
    expected = '<p><a href="https://../">https://../</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example603():
    """Test example 603: localhost5001foo.

    Source: spec.txt lines 8861-8865
    """
    md = MarkdownIt()

    input_text = '<localhost:5001/foo>'
    expected = '<p><a href="localhost:5001/foo">localhost:5001/foo</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example604():
    """Test example 604: httpsfoobarbaz bim.

    Source: spec.txt lines 8870-8874
    """
    md = MarkdownIt()

    input_text = '<https://foo.bar/baz bim>'
    expected = '<p>&lt;https://foo.bar/baz bim&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example605():
    """Test example 605: httpsexamplecom.

    Source: spec.txt lines 8879-8883
    """
    md = MarkdownIt()

    input_text = '<https://example.com/\\[\\>'
    expected = '<p><a href="https://example.com/%5C%5B%5C">https://example.com/\\[\\</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example606():
    """Test example 606: foobarexamplecom.

    Source: spec.txt lines 8901-8905
    """
    md = MarkdownIt()

    input_text = '<foo@bar.example.com>'
    expected = '<p><a href="mailto:foo@bar.example.com">foo@bar.example.com</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example607():
    """Test example 607: foospecialBarbazbar0com.

    Source: spec.txt lines 8908-8912
    """
    md = MarkdownIt()

    input_text = '<foo+special@Bar.baz-bar0.com>'
    expected = '<p><a href="mailto:foo+special@Bar.baz-bar0.com">foo+special@Bar.baz-bar0.com</a></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example608():
    """Test example 608: foobarexamplecom.

    Source: spec.txt lines 8917-8921
    """
    md = MarkdownIt()

    input_text = '<foo\\+@bar.example.com>'
    expected = '<p>&lt;foo+@bar.example.com&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example609():
    """Test example 609.

    Source: spec.txt lines 8926-8930
    """
    md = MarkdownIt()

    input_text = '<>'
    expected = '<p>&lt;&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example610():
    """Test example 610: httpsfoobar.

    Source: spec.txt lines 8933-8937
    """
    md = MarkdownIt()

    input_text = '< https://foo.bar >'
    expected = '<p>&lt; https://foo.bar &gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example611():
    """Test example 611: mabc.

    Source: spec.txt lines 8940-8944
    """
    md = MarkdownIt()

    input_text = '<m:abc>'
    expected = '<p>&lt;m:abc&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example612():
    """Test example 612: foobarbaz.

    Source: spec.txt lines 8947-8951
    """
    md = MarkdownIt()

    input_text = '<foo.bar.baz>'
    expected = '<p>&lt;foo.bar.baz&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example613():
    """Test example 613: httpsexamplecom.

    Source: spec.txt lines 8954-8958
    """
    md = MarkdownIt()

    input_text = 'https://example.com'
    expected = '<p>https://example.com</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example614():
    """Test example 614: foobarexamplecom.

    Source: spec.txt lines 8961-8965
    """
    md = MarkdownIt()

    input_text = 'foo@bar.example.com'
    expected = '<p>foo@bar.example.com</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example615():
    """Test example 615: ababc2c.

    Source: spec.txt lines 9041-9045
    """
    md = MarkdownIt()

    input_text = '<a><bab><c2c>'
    expected = '<p><a><bab><c2c></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example616():
    """Test example 616: ab2.

    Source: spec.txt lines 9050-9054
    """
    md = MarkdownIt()

    input_text = '<a/><b2/>'
    expected = '<p><a/><b2/></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example617():
    """Test example 617: a  b2 datafoo.

    Source: spec.txt lines 9059-9065
    """
    md = MarkdownIt()

    input_text = '<a  /><b2\ndata="foo" >'
    expected = '<p><a  /><b2\ndata="foo" ></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example618():
    """Test example 618: a foobar bam  baz emem boolean zoop.

    Source: spec.txt lines 9070-9076
    """
    md = MarkdownIt()

    input_text = '<a foo="bar" bam = \'baz <em>"</em>\'\n_boolean zoop:33=zoop:33 />'
    expected = '<p><a foo="bar" bam = \'baz <em>"</em>\'\n_boolean zoop:33=zoop:33 /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example619():
    """Test example 619: Foo responsiveimage srcfoojpg.

    Source: spec.txt lines 9081-9085
    """
    md = MarkdownIt()

    input_text = 'Foo <responsive-image src="foo.jpg" />'
    expected = '<p>Foo <responsive-image src="foo.jpg" /></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example620():
    """Test example 620: 33.

    Source: spec.txt lines 9090-9094
    """
    md = MarkdownIt()

    input_text = '<33> <__>'
    expected = '<p>&lt;33&gt; &lt;__&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example621():
    """Test example 621: a hrefhi.

    Source: spec.txt lines 9099-9103
    """
    md = MarkdownIt()

    input_text = '<a h*#ref="hi">'
    expected = '<p>&lt;a h*#ref=&quot;hi&quot;&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example622():
    """Test example 622: a hrefhi a hrefhi.

    Source: spec.txt lines 9108-9112
    """
    md = MarkdownIt()

    input_text = '<a href="hi\'> <a href=hi\'>'
    expected = "<p>&lt;a href=&quot;hi'&gt; &lt;a href=hi'&gt;</p>"

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example623():
    """Test example 623: a foobar  foo barbaz bimbop.

    Source: spec.txt lines 9117-9127
    """
    md = MarkdownIt()

    input_text = '< a><\nfoo><bar/ >\n<foo bar=baz\nbim!bop />'
    expected = '<p>&lt; a&gt;&lt;\nfoo&gt;&lt;bar/ &gt;\n&lt;foo bar=baz\nbim!bop /&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example624():
    """Test example 624: a hrefbartitletitle.

    Source: spec.txt lines 9132-9136
    """
    md = MarkdownIt()

    input_text = "<a href='bar'title=title>"
    expected = "<p>&lt;a href='bar'title=title&gt;</p>"

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example625():
    """Test example 625: afoo.

    Source: spec.txt lines 9141-9145
    """
    md = MarkdownIt()

    input_text = '</a></foo >'
    expected = '<p></a></foo ></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example626():
    """Test example 626: a hreffoo.

    Source: spec.txt lines 9150-9154
    """
    md = MarkdownIt()

    input_text = '</a href="foo">'
    expected = '<p>&lt;/a href=&quot;foo&quot;&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example627():
    """Test example 627: foo  this is a  comment  with hyphens.

    Source: spec.txt lines 9159-9165
    """
    md = MarkdownIt()

    input_text = 'foo <!-- this is a --\ncomment - with hyphens -->'
    expected = '<p>foo <!-- this is a --\ncomment - with hyphens --></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
@pytest.mark.xfail(reason='failing')
def test_example628():
    """Test example 628: foo  foo   foo  foo.

    Source: spec.txt lines 9167-9174
    """
    md = MarkdownIt()

    input_text = 'foo <!--> foo -->\n\nfoo <!---> foo -->'
    expected = '<p>foo <!--> foo --&gt;</p>\n<p>foo <!---> foo --&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example629():
    """Test example 629: foo php echo a.

    Source: spec.txt lines 9179-9183
    """
    md = MarkdownIt()

    input_text = 'foo <?php echo $a; ?>'
    expected = '<p>foo <?php echo $a; ?></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example630():
    """Test example 630: foo ELEMENT br EMPTY.

    Source: spec.txt lines 9188-9192
    """
    md = MarkdownIt()

    input_text = 'foo <!ELEMENT br EMPTY>'
    expected = '<p>foo <!ELEMENT br EMPTY></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example631():
    """Test example 631: foo CDATA.

    Source: spec.txt lines 9197-9201
    """
    md = MarkdownIt()

    input_text = 'foo <![CDATA[>&<]]>'
    expected = '<p>foo <![CDATA[>&<]]></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example632():
    """Test example 632: foo a hrefouml.

    Source: spec.txt lines 9207-9211
    """
    md = MarkdownIt()

    input_text = 'foo <a href="&ouml;">'
    expected = '<p>foo <a href="&ouml;"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example633():
    """Test example 633: foo a href.

    Source: spec.txt lines 9216-9220
    """
    md = MarkdownIt()

    input_text = 'foo <a href="\\*">'
    expected = '<p>foo <a href="\\*"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example634():
    """Test example 634: a href.

    Source: spec.txt lines 9223-9227
    """
    md = MarkdownIt()

    input_text = '<a href="\\"">'
    expected = '<p>&lt;a href=&quot;&quot;&quot;&gt;</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example635():
    """Test example 635: a  quoted text.

    Source: spec.txt lines 9233-9241
    """
    md = MarkdownIt()

    input_text = '<a\n> quoted text'
    expected = '<p>&lt;a</p>\n<blockquote>\n<p>quoted text</p>\n</blockquote>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example636():
    """Test example 636: foo   baz.

    Source: spec.txt lines 9251-9257
    """
    md = MarkdownIt()

    input_text = 'foo  \nbaz'
    expected = '<p>foo<br />\nbaz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example637():
    """Test example 637: foo baz.

    Source: spec.txt lines 9263-9269
    """
    md = MarkdownIt()

    input_text = 'foo\\\nbaz'
    expected = '<p>foo<br />\nbaz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example638():
    """Test example 638: foo        baz.

    Source: spec.txt lines 9274-9280
    """
    md = MarkdownIt()

    input_text = 'foo       \nbaz'
    expected = '<p>foo<br />\nbaz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example639():
    """Test example 639: foo        bar.

    Source: spec.txt lines 9285-9291
    """
    md = MarkdownIt()

    input_text = 'foo  \n     bar'
    expected = '<p>foo<br />\nbar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example640():
    """Test example 640: foo      bar.

    Source: spec.txt lines 9294-9300
    """
    md = MarkdownIt()

    input_text = 'foo\\\n     bar'
    expected = '<p>foo<br />\nbar</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example641():
    """Test example 641: foo   bar.

    Source: spec.txt lines 9306-9312
    """
    md = MarkdownIt()

    input_text = '*foo  \nbar*'
    expected = '<p><em>foo<br />\nbar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example642():
    """Test example 642: foo bar.

    Source: spec.txt lines 9315-9321
    """
    md = MarkdownIt()

    input_text = '*foo\\\nbar*'
    expected = '<p><em>foo<br />\nbar</em></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example643():
    """Test example 643: code   span.

    Source: spec.txt lines 9326-9331
    """
    md = MarkdownIt()

    input_text = '`code  \nspan`'
    expected = '<p><code>code   span</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example644():
    """Test example 644: code span.

    Source: spec.txt lines 9334-9339
    """
    md = MarkdownIt()

    input_text = '`code\\\nspan`'
    expected = '<p><code>code\\ span</code></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example645():
    """Test example 645: a hreffoo   bar.

    Source: spec.txt lines 9344-9350
    """
    md = MarkdownIt()

    input_text = '<a href="foo  \nbar">'
    expected = '<p><a href="foo  \nbar"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example646():
    """Test example 646: a hreffoo bar.

    Source: spec.txt lines 9353-9359
    """
    md = MarkdownIt()

    input_text = '<a href="foo\\\nbar">'
    expected = '<p><a href="foo\\\nbar"></p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example647():
    """Test example 647: foo.

    Source: spec.txt lines 9366-9370
    """
    md = MarkdownIt()

    input_text = 'foo\\'
    expected = '<p>foo\\</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example648():
    """Test example 648: foo.

    Source: spec.txt lines 9373-9377
    """
    md = MarkdownIt()

    input_text = 'foo  '
    expected = '<p>foo</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example649():
    """Test example 649: foo.

    Source: spec.txt lines 9380-9384
    """
    md = MarkdownIt()

    input_text = '### foo\\'
    expected = '<h3>foo\\</h3>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example650():
    """Test example 650: foo.

    Source: spec.txt lines 9387-9391
    """
    md = MarkdownIt()

    input_text = '### foo  '
    expected = '<h3>foo</h3>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example651():
    """Test example 651: foo baz.

    Source: spec.txt lines 9402-9408
    """
    md = MarkdownIt()

    input_text = 'foo\nbaz'
    expected = '<p>foo\nbaz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example652():
    """Test example 652: foo   baz.

    Source: spec.txt lines 9414-9420
    """
    md = MarkdownIt()

    input_text = 'foo \n baz'
    expected = '<p>foo\nbaz</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example653():
    """Test example 653: hello there.

    Source: spec.txt lines 9434-9438
    """
    md = MarkdownIt()

    input_text = "hello $.;'there"
    expected = "<p>hello $.;'there</p>"

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example654():
    """Test example 654: Foo.

    Source: spec.txt lines 9441-9445
    """
    md = MarkdownIt()

    input_text = 'Foo χρῆν'
    expected = '<p>Foo χρῆν</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


@pytest.mark.spec
def test_example655():
    """Test example 655: Multiple     spaces.

    Source: spec.txt lines 9450-9454
    """
    md = MarkdownIt()

    input_text = 'Multiple     spaces'
    expected = '<p>Multiple     spaces</p>'

    result = md.render(input_text).rstrip('\n')
    assert result == expected


