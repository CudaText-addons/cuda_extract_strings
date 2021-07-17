import os
import re
from cudatext import *

from cudax_lib import get_translation
_   = get_translation(__file__)  # I18N

fn_ini = 'cuda_filter_lines.ini'


def do_dialog(text, b_re, b_nocase, b_sort, b_save, i_before, i_after, b_number, b_lexer):
    RES_TEXT = 1
    RES_REGEX = 2
    RES_NOCASE = 3
    RES_SORT = 4
    RES_NUM = 5
    RES_LEXER = 6
    RES_SAVE = 7
    RES_BEF = 9
    RES_AFT = 11
    RES_OK = 12
    c1 = chr(1)
    s_re = '1' if b_re else '0'
    s_i = '1' if b_nocase else '0'
    s_sort = '1' if b_sort else '0'
    s_save = '1' if b_save else '0'
    s_number = '1' if b_number else '0'
    s_lexer = '1' if b_lexer else '0'

    res = dlg_custom(_('Filter Lines'), 406, 300,
      '\n'.join([]
         +[c1.join(['type=label',  'pos=6,5,400,0',     'cap='+_('&Text:')])]
         +[c1.join(['type=edit',   'pos=6,23,400,0',    'val='+text])]
         +[c1.join(['type=check',  'pos=6,51,400,0',    'cap='+_('&Reg.ex.'), 'val='+s_re])]
         +[c1.join(['type=check',  'pos=6,76,400,0',    'cap='+_('&Ignore case'), 'val='+s_i])]
         +[c1.join(['type=check',  'pos=6,101,400,0',   'cap='+_('&Sort output'), 'val='+s_sort])]
         +[c1.join(['type=check',  'pos=6,126,400,0',   'cap='+_('Include line &numbers'), 'val='+s_number])]
         +[c1.join(['type=check',  'pos=6,151,400,0',   'cap='+_('Keep &lexer'), 'val='+s_lexer])]
         +[c1.join(['type=check',  'pos=6,176,400,0',   'cap='+_('S&ave options'), 'val='+s_save])]
         +[c1.join(['type=label',  'pos=6,201,400,0',   'cap='+_('Number of lines &before match:')])]
         +[c1.join(['type=edit',   'pos=370,201,400,0', 'val='+i_before])]
         +[c1.join(['type=label',  'pos=6,235,400,0',   'cap='+_('Number of lines a&fter match:')])]
         +[c1.join(['type=edit',   'pos=370,235,400,0', 'val='+i_after])]
         +[c1.join(['type=button', 'pos=194,270,294,0', 'cap='+_('&OK'), 'ex0=1'])]
         +[c1.join(['type=button', 'pos=300,270,400,0', 'cap='+_('Cancel')])]
      ) )
    if res is None: return

    res, s = res
    if res != RES_OK: return
    s = s.splitlines()
    text = s[RES_TEXT]
    if not text: return

    regex = s[RES_REGEX]=='1'
    nocase = s[RES_NOCASE]=='1'
    sort = s[RES_SORT]=='1'
    save = s[RES_SAVE]=='1'
    before = abs(int(s[RES_BEF]))
    after = abs(int(s[RES_AFT]))
    number = s[RES_NUM]=='1'
    lexer = s[RES_LEXER]=='1'
    return (text, regex, nocase, sort, save, before, after, number, lexer)


def is_ok(line, test, b_regex, b_nocase):
    if not b_regex:
        if b_nocase:
            ok = test.lower() in line.lower()
        else:
            ok = test in line
    else:
        flags = re.I if b_nocase else 0
        ok = bool(re.search(test, line, flags=flags))
    return ok


def decor_line(line, b_number, length, x, flag = ' '):
    if b_number:
        s_num = flag + '[' + str(x).rjust(length, ' ') + ']'

        if len(line.strip()) > 0:
            s_num = s_num + ' '

        line = s_num + line

    return line


def dlg_filter():

    b_save = ini_read(fn_ini, 'op', 'save', '0')=='1'
    if b_save:
        text = ini_read(fn_ini, 'op', 'text', '')
        b_regex = ini_read(fn_ini, 'op', 'regex', '0')=='1'
        b_nocase = ini_read(fn_ini, 'op', 'nocase', '0')=='1'
        b_sort = ini_read(fn_ini, 'op', 'sort', '0')=='1'
        i_before = ini_read(fn_ini, 'op', 'before', '0')
        i_after = ini_read(fn_ini, 'op', 'after', '0')
        b_number = ini_read(fn_ini, 'op', 'number', '0')=='1'
        b_lexer = ini_read(fn_ini, 'op', 'lexer', '0')=='1'
    else:
        text = ''
        b_regex = False
        b_nocase = False
        b_sort = False
        i_before = '0'
        i_after = '0'
        b_number = False
        b_lexer = False

    res = do_dialog(text, b_regex, b_nocase, b_sort, b_save, i_before, i_after,
                    b_number, b_lexer)
    if res is None: return
    text, b_regex, b_nocase, b_sort, b_save, i_before, i_after, b_number, b_lexer = res

    #save options
    ini_write(fn_ini, 'op', 'save', '1' if b_save else '0')
    if b_save:
        ini_write(fn_ini, 'op', 'text', text)
        ini_write(fn_ini, 'op', 'regex', '1' if b_regex else '0')
        ini_write(fn_ini, 'op', 'nocase', '1' if b_nocase else '0')
        ini_write(fn_ini, 'op', 'sort', '1' if b_sort else '0')
        ini_write(fn_ini, 'op', 'before', str(i_before))
        ini_write(fn_ini, 'op', 'after', str(i_after))
        ini_write(fn_ini, 'op', 'number', '1' if b_number else '0')
        ini_write(fn_ini, 'op', 'lexer', '1' if b_lexer else '0')

    res = []
    last_match = -1
    num_lines = ed.get_line_count()
    length = len(str(num_lines))

    for i in range(num_lines):
        line = ed.get_text_line(i)

        if is_ok(line, text, b_regex, b_nocase):

            # If the option to include lines after the match is on: i_after > 0
            # This code prints the lines after the previous match:
            # last_match != -1
            i_prev_max_line = -1
            if i_after > 0 and last_match != -1:
                for j in range(last_match + 1, min(i, last_match + i_after + 1)):
                    line_tmp = ed.get_text_line(j)
                    res.append(decor_line(line_tmp, b_number, length, j + 1))
                i_prev_max_line = min(i, last_match + i_after)

            # If the option to include lines before the match is on: i_before > 0
            # Continue just if the match happens at least in the second line of
            # the file i > 0
            if i_before > 0 and i > 0:
                # Correct considering a previous match
                i_start = max(i - i_before, 0, i_prev_max_line + 1, last_match + 1)

                # Shows dots meaning "many lines"
                if i_start - 1 > max(i_prev_max_line, last_match) and b_number:
                    res.append('  ' + '.' * length)

                for j in range(i_start, i):
                    line_tmp = ed.get_text_line(j)
                    res.append(decor_line(line_tmp, b_number, length, j + 1))

            # Shows dots meaning "many lines" when i_before = 0
            if i_before == 0:
                if i - 1 > max(i_prev_max_line, last_match) and b_number:
                    res.append('  ' + '.' * length)

            res.append(decor_line(line, b_number, length, i + 1, '*'))
            last_match = i

    # After loop through the lines
    if last_match != -1:
        # Validate for the last match if is necessary to print
        if i_after > 0:
            for j in range(last_match + 1,
                           min(num_lines, last_match + i_after + 1)):
                line_tmp = ed.get_text_line(j)
                res.append(decor_line(line_tmp, b_number, length, j + 1))

            if num_lines - 1 > min(num_lines, last_match + i_after) and b_number:
                res.append('  ' + '.' * length)
        else:
            if num_lines - 1 > last_match and b_number:
                res.append('  ' + '.' * length)

    if not res:
        msg_status(_('Cannot find lines: ')+text)
        return

    if b_sort:
        res = sorted(res)

    # Get current file lexer
    s_lexer = ed.get_prop(PROP_LEXER_FILE)
    file_open('')
    flag = 'r' if b_regex else ''
    flag += 'i' if b_nocase else ''
    flag += 's' if b_sort else ''

    ed.set_prop(PROP_TAB_TITLE, 'Filter['+flag+']: '+text)
    if b_lexer: ed.set_prop(PROP_LEXER_FILE, s_lexer)
    ed.set_text_all('\n'.join(res))
    msg_status(_('Found %d matching lines') % len(res))

