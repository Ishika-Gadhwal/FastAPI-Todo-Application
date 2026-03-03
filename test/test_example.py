import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 5
    
    
def test_isInstance():
    assert isinstance("Hello", str)
    assert not isinstance("1", int)
    
    
def test_booleans():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False
    

def test_types():
    assert type("hello") == str
    assert type("1" is not int)
    
    
def test_greater_and_less_than():
    assert 7 > 3
    assert 3 < 11
    
    
def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)
    
    
class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
        
        
@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'Computer Science', 3)
    
def test_person_initialization(default_employee):
    assert default_employee.first_name == "John"
    assert default_employee.last_name == "Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3