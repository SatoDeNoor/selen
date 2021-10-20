from selen.client.driver import Operations
from selen.client.helper import Tools


def test_web_element(driver):
    driver.get('https://www.google.com/')
    search_button = Operations.web_element('(//input[@*[contains(.,"Google")]])[2]').get_attribute('value')
    assert 'oogle' in search_button, 'Web element check FAILED'


def test_send_keys(driver):
    driver.get('https://www.google.com/')
    input_el = Operations.web_element('//input[@role="combobox"]')
    Operations.send_data(input_el, 'selenium download')
    Operations.keyboard('enter')
    link = Operations.web_element('((//div[@class="g"])[1]//a)[1]').get_attribute('href')
    assert 'selenium' in link, 'Send Keys check FAILED'


def test_validator():
    eq_1 = Tools.text_validation(actual_text='equal', expected_text='equal', condition='==')
    eq_2 = Tools.text_validation(actual_text='equal', expected_text='NOTequal', condition='==')
    in_1 = Tools.text_validation(actual_text='words', expected_text='word', condition='in')
    in_2 = Tools.text_validation(actual_text='word', expected_text='words', condition='in')
    neq_1 = Tools.text_validation(actual_text='equal', expected_text='NOTequal', condition='!=')
    neq_2 = Tools.text_validation(actual_text='equal', expected_text='equal', condition='!=')
    assert (eq_1 and in_1 and neq_1) is None, 'Positive validation FAILED'
    assert isinstance((eq_2 and in_2 and neq_2), str), 'Negative validation FAILED'


def test_style(driver):
    driver.get('https://www.google.com/')
    input_el = Operations.web_element('//input[@role="combobox"]')
    style = Operations.style(input_el, 'cursor')
    assert style == 'text', 'Style check FAILED'


def test_attribute(driver):
    driver.get('https://www.google.com/')
    input_el = Operations.web_element('//input[@role="combobox"]')
    attribute = Operations.attribute(input_el, 'role')
    assert attribute == 'combobox', 'Attribute check FAILED'
