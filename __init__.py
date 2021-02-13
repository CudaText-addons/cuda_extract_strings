from cudatext import *
from . import extract
from . import filtering

from cudax_lib import get_translation
_   = get_translation(__file__)  # I18N

class Command:

    def dlg_extract(self):
    
        extract.dlg_extract()
        
    def dlg_filter(self):
    
        filtering.dlg_filter()

    def emails(self):
    
        res = extract.get_emails()
        if not res:
            msg_status(_('No strings found'))
            return

        #del dups
        res = list(set(res))

        file_open('')
        ed.set_prop(PROP_TAB_TITLE, 'e-mails')
        for s in res:
            ed.set_text_line(-1, s)
