from selen.client.driver import Operations


def test_web_element(driver):
    driver.get('https://www.google.com/')
    search_button = Operations.web_element('(//input[@*[contains(.,"Google")]])[2]').get_attribute('value')
    assert 'oogle' in search_button, 'Web element check FAILED'


def test_send_keys(driver):
    driver.get('https://www.google.com/')
    input = Operations.web_element('//input[@role="combobox"]')
    Operations.send_data(input, 'selenium download')
    Operations.keyboard('enter')
    link = Operations.web_element('((//div[@class="g"])[1]//a)[1]').get_attribute('href')
    assert 'selenium' in link, 'Send Keys check FAILED'

