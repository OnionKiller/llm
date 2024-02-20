

import copy
import logging
from typing import List


def wc(s:str):
    return len(s.split(' '))

def sc(s:str):
    return len(s.split('.'))-1

template_text = \
"""
A diplomaterv célja földmegfigyelési szegmentációs és változásdetekciós algoritmusok fejlesztése.
A szegmentáció és változásdetekció nagyon fontos részét képezik a földmegfigyelésnek, hiszen az egyik leggyakoribb kérdés a Földdel kapcsolatban, hogy hogyan változik.
Az Európai Űrügynökség (ESA) missziói során folyamatosan, néhány naponta ismétlődve készít műholdképeket a Föld felszínéről, amelyek ingyenesen hozzáférhetőek.
Ezeknek a képeknek a feldolgozása azonban új kihívásokat támaszt a jelenlegi módszerekkel szemben.
A legnagyobb kihívás a mulitspektrális képek kezelése, illetve különböző adatforrások kombinálása.
Erre a feladatra egy kiváló módszer a fúziós Markov Véletlen Mező módszer, amely nemcsak a különböző képtípusok fúzióját teszi lehetővé, de egy hatékony keretrendszert biztosít változásdetekcióra is.
A felgolgozási lépések során a FÖMI adatszettben elhagyták a Sentinel-2 11. képcsatornáját. Ez a csatona jellemzően cirrus felhők detektálására használható, tiszta égbolt esetén azonban nagyon zajos. Az egyszerű fúzió érdekében az összes képet azonos 10x10 méteres felbontásra 
skáláztam Lánczos interpolációval az OpenCV könyvtár cv2.INTER_LANCZOS4 implementációjával. Emellet mindegyik kép esetén az adatokat np.float64 típusra konvertáltam.
A Sentinel-1 műholdképek az adatszettben már előfeldolgozott formátumban szerepelnek. Az adatok a Level-1 szintű adatból egyből H/A/alpha dekompozíció szerint szerepelnek, 20x20 méteres felbontásra korrigálva. 
A H/A/Alpha dekompozíció egy sajátértékeket meghatározó dekompozíció, amely reflektanciát jellemző paraméterekre bontja le az eredeti adatokat. 
Az így kapott komponensekből az Alpha komponens a szóródás domináns típusát jellemzi, míg az entrópia a szóródás mértékét. 
A Sentinel-1 adatok összesen a következő komponenseket tartalmazták: alpha, anizotrópia, Shannon-entrópia, L1, L2.
Az adatszettben szerepelő képek mind ugyanazt a területet fedik
le, jellegét tekintve tehát egy multitemporális adatszettről beszélhetünk.
Mindegyik kép a földrajzi pozíciójával megfelelően össze van
regisztrálva, a pixelek minden esetben ugyanazt a földrajzi pontot és
területet reprezentálják. Ez mind a Sentinel-1 és a Sentinel-2 képek esetén instrumentálisan garantált, a pixelenkénti 
eltolási hiba a csatornák és a multitemporális képek között is elenyészően kicsi.
A 13. ábrán látható az adatszett által lefedett terület, ami magába foglalja a Velencei-tavat, és két nagyobb víztározót,
Székesfehérvár egy részét, és a Velencei-tó fölött található védett erdőterületeket, többek között a Pákozdi ingóköveket.
Ezáltal jól reprezentál több, a földmegfigyelés szempontjából releváns területtípust. A Pátkai- és Zámolyi-víztározók időszakosan kiszáradnak, ezért
változásdetekciós feladatok validálására hasznosak lehetnek.
Az adatszett 2018 áprilisa és 2018 novembere közötti időszakot foglalja magába, és összesen 60 Sentinel-1 és 8 Sentinel-2 képet tartalmaz. A Sentinel-2 képekhez a hozzájuk időpontban legközelebb eső Sentinel-1 képeket párosítottam.
A dolgozatban főleg Sentinel-2 képekkel folgalkoztam, ezért a meghatározó fizikai felbontásnak a Sentinel-2 legjobb felbontását választottam, ami 10 km oldalhosszúságú pixeleket jelent. Az összes képet ennek megfelelően skáláztam.
""".replace('\n','')


import random
import time


def create_random_text(desing_wc:int,overshoot = .1):
    sl = template_text.split('.')[:-1]
    max_wc = desing_wc*(1+overshoot)
    possible_s = [x for x in sl if wc(x) < desing_wc]
    current_wc = 0
    r_ = []
    while current_wc < desing_wc:
        wc_base = current_wc
        random.shuffle(possible_s)
        for i in possible_s:
            if wc(i) + current_wc < max_wc:
                r_.append(i)
                current_wc += wc(i)
        if wc_base == current_wc:
            #no improvement, excape infinite loop
            break
    return '. '.join(r_) + '.'

def timing_decorator(func):
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time,result
  return wrapper

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