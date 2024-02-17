

import copy
import logging
from typing import List


def preprocess_text_list(in_text_list:List[str],allowed_word_count:int = 320):
    text_list = copy.deepcopy(in_text_list)
    def wc(t:str):
        return len(t.split(' '))
    modification_list = []
    for id,text in enumerate(text_list):
        #assume we want to have around 1k kontext length, and on average hungarian words translate to 3 token
        if wc(text)> allowed_word_count:
            index = text.find('.',len(text)//2-40)
            if index == -1:
                #TODO log missing punktuation
                logging.warning("No punctuation found!")
                continue
            modification_list.append(id)
            index += 1
            t1 = text[0:index]
            t2 = text[index:]
            text_list[id] = t1
            text_list.append(t2)
    return text_list,modification_list

def postprocess_text_list(text_list:List[str],mod_list:List[int]):
    orig_list_len = len(text_list)-len(mod_list)
    for extra_index,orig_index in enumerate(mod_list):
        if orig_index > orig_list_len:
            #TODO handle recursive splitting
            continue
        text_list[orig_index] = text_list[orig_index] + text_list[orig_list_len+extra_index]
    
    return text_list[:orig_list_len]