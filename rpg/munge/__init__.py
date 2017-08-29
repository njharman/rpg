# vim: set fileencoding=utf-8
'''Parse and reformat PDF's converted to text.
'''
import re
from collections import defaultdict

from . import rst
from . import out


PAGE_BREAK = '\f'

RE_EMPTYLINE = re.compile(r'^\s*$')

# Sort alphabetically 10 after 2,4,8,etc.
alpha_sort = lambda key: [int(t) if t.isdigit() else t for t in re.split('([0-9]+)', key)]


def slurp_re(stopon, i, lines, strip):
    '''Slurp lines until line matches re 'stopon'.'''
    bits = list()
    bits.append(lines[i].rpartition(strip)[2].strip())
    while not stopon.match(lines[i + 1]):
        i += 1
        bits.append(lines[i].strip())
    return i, ' '.join(bits).strip()


## Look for

def lookfor(test, accum, reduce):
    def finder(line):
        accum.append(line)
        if test(line):
            for para in reduce(accum):
                yield para
    return finder


def is_cap(char):
    '''Func lookfor test.'''
    return char == char.upper()


def space_reduce(lines):
    '''Func lookfor reducer.'''
    yield ' '.join(lines)


## Line Oriented

def replace_typography(lines):
    '''Replace weirdo characters.'''
    for line in lines:
        yield line.replace('“', '"') \
                .replace('”', '"') \
                .replace('—', '--') \
                .replace('’', '\'') \
                .replace('\xc2\x92', '\'') \
                .replace('\xc2\x93', '"') \
                .replace('\xc2\x94', '"') \
                .replace('\xe2\x80\x93', '-')


def strip_newlines(lines, strip='\n'):
    '''Remove newlines from end of lines.'''
    for line in lines:
        yield line.strip(strip)


def strip_emptylines(lines):
    '''Remove lines containing only whitespace.'''
    for line in lines:
        if line.strip():
            yield line


def strip_comments(lines):
    '''Remove ## comment line.'''
    for line in lines:
        if not line.startswith('##'):
            yield line


def strip_tt_pagebreaks(lines):
    '''TT has pagenumber preceding pagebreak.'''
    previous = None
    for line in lines:
        if PAGE_BREAK in line:
            line = line.replace(PAGE_BREAK, '')
            previous = None
        if previous is not None:
            yield previous
        previous = line
    if previous:
        yield previous


def strip_aec_pagebreaks(lines):
    '''AEC has pagenumber after pagebreak and page break line is garbage.'''
    skip = False
    for line in lines:
        if PAGE_BREAK in line:
            skip = True
            continue
        if skip:
            skip = False
            continue
        yield line


def dehyphenate(lines):
    '''Combine two lines with hypenated word into one line, removing hypen.'''
    first = ''
    for line in lines:
        line = line.rstrip()
        if len(line) > 1 and line[-1] == '-' and line[-2] != '-':
            first += line[:-1]
            continue
        if first:
            yield first + line.lstrip()
            first = ''
        else:
            yield line


def by_simple_para(lines):
    '''Combine multiple lines into one line, delineated by blank lines.'''
    para = list()
    for l in lines:
        if l.strip():
            para.append(l.strip())
        elif para:
            yield ' '.join(para)
            yield ''
            para = list()
    if para:
        yield ' '.join(para)


def break_base(line, accum):
    # Break on blank line or after line ending with period or colon (if only colon on line)
    if not line or line.endswith('.') or (line.endswith(':') and line.count(':') == 1):
        if line:
            accum.append(line)
        return True


def break_list(line, accum):
    # Break before "List Header:" should be on its own line.
    if accum and line.endswith(':') and line.count(':') == 1 and is_cap(line[0]):
        return line


def break_regex_factory(regex, newline=False):
    matcher = re.compile(regex)
    def break_regex(line, accum):
        # Break when regex matches
        if matcher.search(line):
            if line and newline:
                return line
            if line:
                accum.append(line)
            return True
    return break_regex


def by_para(lines, tests=(), override=()):
    '''Splits into paragraphs.

    Splits on
      - blank lines
      - lines ending with .
      - lines ending with : (if only one colon on line)

    Dehyphenates.
    Understand ReST orders, titles and tables. marks them with <order>, <title> <table>.

    :param tests: break when func(line, accum) returns True
    :param override: break when func(line, accum) returns True
    :return: single line (with possible newlines embedded (for tables))
    '''

    breakfuncs = list(override)
    breakfuncs.extend(list(tests))
    if not override:
        breakfuncs.append(break_base)
        breakfuncs.append(break_list)
    in_table = 0
    in_order = 0
    accumulate = list()
    for line in lines:
        # ReST directive. Must be first, sucks all lines until unindent.
        if line.startswith('.. '):
            yield ' '.join(accumulate)
            accumulate = list()
            line = '<order>' + line
            in_order = True
        if in_order:
            if line.startswith(' ') or not line:
                accumulate.append(line)
                continue
            else:
                in_order = False
                yield '\n'.join(accumulate)
                accumulate = list()

        # ReST title
        if line and line[0] in rst.TITLES and len(accumulate) == 1 and len(accumulate[0]) == len(line):
            yield '<title>%s\n%s' % (accumulate[0], line)
            accumulate = list()
            continue

        # ReST table
        if line.startswith('==='):
            if in_table == 0:  # End previous para, start table.
                yield ' '.join(accumulate)
                line = '<table>' + line
                accumulate = list()
            if in_table < 2:  # Tables, have three === seperator lines.
                in_table += 1
            else:  # End table.
                in_table = 0
                accumulate.append(line.rstrip())
                yield '\n'.join(accumulate)
                accumulate = list()
                continue
        if in_table:
            accumulate.append(line.rstrip())
            continue

        for test in breakfuncs:
            foo = test(line, accumulate)
            if foo:
                yield ' '.join(dehyphenate(accumulate))
                accumulate = list()
                if foo is not True:
                    accumulate.append(foo)
                break
        else:
            accumulate.append(line)

    # TODO: might need '\n'.join
    if accumulate:
        yield ' '.join(dehyphenate(accumulate))


## Page Oriented

def detwocolumn(lines):
    for page in by_page(lines):
        for line in twocolumn_page_to_onecolumn_lines(page):
            yield line


def by_page(lines):
    '''Split into groups of lines by PAGE_BREAK. Remove page break, page numbers, etc.'''
    page = list()
    for line in lines:
        if PAGE_BREAK in line:
            page.pop()  # The pagenumber/footer
            yield page
            page = list()
        else:
            page.append(line)
    if page:
        yield page


def twocolumn_page_to_onecolumn_lines(page):
    '''Convert one "page" of pdftotext 2 column output to list of 1 column lines.'''
    # Find the most common start column.
    lengths = defaultdict(int)
    for l in page:
        if not l.strip():
            continue
        found_three = False
        for halfsie in range(0, max(0, len(l) - 3)):
            if l[halfsie:halfsie + 4] == '    ':
                found_three = True
            if not found_three:
                continue
            if l[halfsie] != ' ':
                break
        if not found_three:
            continue
        else:
            lengths[halfsie] += 1
    if lengths:
        winnar = sorted(lengths.items(), key=lambda x: x[1])[-1][0]
    else:
        winnar = 0
    one = list()
    two = list()
    for l in page:
        if not l.strip():
            one.append(l)
            continue
        # Find column of first non space after three spaces.
        found_three = False
        for halfsie in range(0, max(0, len(l) - 3)):
            if l[halfsie:halfsie + 4] == '    ':
                found_three = True
            if not found_three:
                continue
            if l[halfsie] != ' ':
                break
        if not found_three:
            one.append(l)
        else:
            one.append(l[:halfsie])
            # If second column is winnar+3 or winnar+2 assume it's paragraph leading indent.
            if halfsie == winnar + 3 and l[halfsie - 3:halfsie] == '   ':
                two.append(l[halfsie - 3:])
            elif halfsie == winnar + 2 and l[halfsie - 2:halfsie] == '  ':
                two.append(l[halfsie - 2:])
            else:
                two.append(l[halfsie:])
    return one + two
