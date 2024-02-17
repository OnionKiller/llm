
import copy
import tools

def create_test_text(wc:int):
    _r = []
    for _ in range(wc):
        _r += ["test"]
    return " ".join(_r)

def insert_punkt_after_wc(text:str,wc:int):
    l = text.split(' ')
    l.insert(wc,".")
    return ' '.join(l)

def wc(t:str):
    return len(t.split(' '))

def test_end2end_processing():
    test_list = [
        create_test_text(20),
        insert_punkt_after_wc(create_test_text(300),149),
        insert_punkt_after_wc(create_test_text(300),151),
    ]
    check_list = copy.deepcopy(test_list)

    new_list,mod = tools.preprocess_text_list(test_list,200)
    reverted_list = tools.postprocess_text_list(new_list,mod)

    #check if outpput matches input
    assert reverted_list == check_list
    
def test_immutability():
    test_list = [
        create_test_text(20),
        insert_punkt_after_wc(create_test_text(300),149),
    ]

    new_list,mod = tools.preprocess_text_list(test_list,200)
    reverted_list = tools.postprocess_text_list(new_list,mod)
    #check if immutable for input
    assert reverted_list == test_list

def test_preprocessing_split_check():
    test_list = [
        create_test_text(20),
        insert_punkt_after_wc(create_test_text(99),50),
        insert_punkt_after_wc(create_test_text(100),50),
        " ".join(["test."]*130),
    ]
    assert [wc(t) for t in test_list] == [20,100,101,130]
    new_list,mod = tools.preprocess_text_list(test_list,100)

    assert len(new_list) == 6
    assert mod == [2,3]
    assert [wc(t) for t in new_list] == [20,100,51,59,51,72]


