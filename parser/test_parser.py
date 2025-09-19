from parser import preprocess

def test_1():
    assert preprocess("hello hassan") == ['hello', 'hassan']
    
def test_2():
    assert preprocess("hello 1 hassan") == ['hello', 'hassan']

def test_3():
    assert preprocess("hello 1 . hassan") == ['hello', 'hassan']

def test_4():
    assert preprocess("Hello 1 ., haSSan") == ['hello', 'hassan']