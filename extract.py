import re
from cudatext import *

RES_OPT_TEXT = 1
RES_OPT_CASE = 2
RES_BTN_EMAIL = 3
RES_FIND = 7
RES_COPY_CLIP = 9
RES_COPY_TAB = 10

SIZE_X = 600
SIZE_Y = 400
SIZE_BTN = 150

REGEX_EMAIL = r'\b[a-zA-Z0-9][\w\.\-_]*@\w[\w\.\-]*\.[a-zA-Z]{2,}\b'


def do_find(text, case_sens):
    l = re.findall(text, 
          ed.get_text_all(), 
          0 if case_sens else re.IGNORECASE)
    l = sorted(list(set(l)))
    return l


def do_dialog(text, case_sens, items):
    c1 = chr(1)
    s_en = '1' if items else '0'
    s_case = '1' if case_sens else '0'
    
    while True:
        res = dlg_custom('Extract Strings', SIZE_X, SIZE_Y, 
        '\n'.join([]
         +[c1.join(['type=label', 'pos=6,5,300,0', 'cap=&Regular expression:'])]
         +[c1.join(['type=edit', 'pos=6,23,%d,0'%(SIZE_X-SIZE_BTN-12), 'val='+text])]
         +[c1.join(['type=check', 'pos=6,51,%d,0'%(SIZE_X-SIZE_BTN-12), 'cap=Case &sensitive', 'val='+s_case])]
         +[c1.join(['type=button', 'pos=6,78,156,0', 'cap=Reg.ex. for e-mail'])]
            
         +[c1.join(['type=label', 'pos=6,108,400,0', 'cap=F&ound strings:'])]
         +[c1.join(['type=listbox', 'pos=6,126,%d,%d'%(SIZE_X-SIZE_BTN-12, SIZE_Y-22), 'items='+'\t'.join(items)])]
         +[c1.join(['type=label', 'pos=6,%d,300,0'%(SIZE_Y-20), 'cap=Found: %d'%len(items)])]
             
         +[c1.join(['type=button', 'pos=%d,25,%d,0'%(SIZE_X-SIZE_BTN-6, SIZE_X-6), 'cap=&Find', 'props=1'])]
         +[c1.join(['type=button', 'pos=%d,55,%d,0'%(SIZE_X-SIZE_BTN-6, SIZE_X-6), 'cap=Cancel'])]
         +[c1.join(['type=button', 'pos=%d,126,%d,0'%(SIZE_X-SIZE_BTN-6, SIZE_X-6), 'cap=Copy to &clipboard', 'en='+s_en])]
         +[c1.join(['type=button', 'pos=%d,156,%d,0'%(SIZE_X-SIZE_BTN-6, SIZE_X-6), 'cap=Copy to &new tab', 'en='+s_en])]
          ),
          get_dict=True
          )

        if res is None: return

        action = res['clicked']
        text = res[RES_OPT_TEXT]
        case_sens = res[RES_OPT_CASE]=='1'
        
        if action == RES_BTN_EMAIL:
            #show dlg again
            text = REGEX_EMAIL
        else:
            return (action, text, case_sens)
    

def get_emails():
    text = ed.get_text_all()
    return re.findall(REGEX_EMAIL, text)


def dlg_extract():
    text = r'\w+'
    case_sens = False
    items = []
    while True:
        res = do_dialog(text, case_sens, items)
        if res is None: return
        res, text, case_sens = res
                
        if res==RES_FIND:
            #print('find:', text)
            items = do_find(text, case_sens)
            continue
                
        elif res==RES_COPY_CLIP:
            app_proc(PROC_SET_CLIP, '\n'.join(items))
            msg_status('Copied to clipboard')
            ed.focus()
            return
                
        elif res==RES_COPY_TAB:
            file_open('')
            text = '\n'.join(items)+'\n'
            ed.set_text_all(text)
            msg_status('Copied to tab')
            ed.focus()
            return
                
        else:
            msg_status('Unknown code of dlg')
            return
    
