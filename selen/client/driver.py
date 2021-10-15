import os
import time
import allure
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

_driver_instance = None


class DriverInstance:
    def __init__(self, driver=None):
        self.driver = driver

    @staticmethod
    def get_driver():
        return _driver_instance

    def set_driver(self):
        global _driver_instance
        _driver_instance = self.driver


class Driver:
    @staticmethod
    def chrome(size='1920x1080', headless=True, download_path=None, driver_path=None):
        chrome_options = ChromeOptions()
        if headless is True:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--window-size={size}')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        if download_path:
            download_preference = {"download.default_directory": download_path,
                                   "download.directory_upgrade": True,
                                   "download.prompt_for_download": False,
                                   "safebrowsing.enabled": True}
            chrome_options.add_experimental_option("prefs", download_preference)
        if driver_path:
            driver = Chrome(executable_path=driver_path, options=chrome_options)
        else:
            driver = Chrome(options=chrome_options)
        return driver

    @staticmethod
    def create_screenshot(driver, sc_name, option):
        if option == 'allure':
            # allure screenshot, will be attached with allure test case
            allure.attach(driver.get_screenshot_as_png(), name=sc_name, attachment_type=AttachmentType.PNG)


class Operations:
    @staticmethod
    def web_element(xpath: str, timer=3, attempts=3, elements=False, visibility=True):
        while attempts > 0:
            try:
                if elements is False:
                    if visibility is True:
                        element = WebDriverWait(DriverInstance().get_driver(), timer).\
                            until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    else:
                        element = DriverInstance().get_driver().find_element_by_xpath(xpath)
                else:
                    if visibility is True:
                        element = WebDriverWait(DriverInstance().get_driver(), timer).\
                            until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
                    else:
                        element = DriverInstance().get_driver().find_elements_by_xpath(xpath)
                return element
            except Exception as e:
                attempts -= 1
                if attempts == 0:
                    print(e)

    @staticmethod
    def shadow_element(shadow_root: str, selector: str, option: str, data=None, timer=10, waiting=0.25):
        # shadow root works with css selector
        scripts = {
            'basic': f'return document.querySelector(\'{shadow_root}\').shadowRoot.querySelector(\'{selector}\');',
            'text': f'return Array.from(document.querySelector(\'{shadow_root}\').shadowRoot.querySelectorAll'
                    f'(\'{selector}\')).find(el => el.textContent.includes(\'{data}\'));',
            'elements': f'return Array.from(document.querySelector(\'{shadow_root}\').shadowRoot.'
                        f'querySelectorAll(\'{selector}\'));'
        }.get(option)
        while timer > 0:
            try:
                shadow_element = DriverInstance().get_driver().execute_script(scripts)
                return shadow_element
            except Exception as e:
                timer -= waiting
                if timer == 0:
                    print(e)
                time.sleep(waiting)

    @staticmethod
    def js_click(element, option: str):
        if option == 'element':
            DriverInstance().get_driver().execute_script("arguments[0].click();", element)
        elif option == 'xpath':
            script = "function getElementByXpath(path) {" \
                     "return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)." \
                     "singleNodeValue;}" \
                     f"getElementByXpath('{element}').click();"
            DriverInstance().get_driver().execute_script(script)

    @staticmethod
    def drag_n_drop(source: object, destination: object, option, offset=None):
        if option == 'classic':
            # classic selenium drag and drop
            ActionChains(DriverInstance().get_driver()).drag_and_drop(source, destination).perform()
        elif option == 'offset':
            # drag by offset
            ActionChains(DriverInstance().get_driver()).click_and_hold(source).move_by_offset(offset[0], offset[1]).\
                release().perform()
        elif option == 'mr':
            # move to and release
            ActionChains(DriverInstance().get_driver()).click_and_hold(source).move_to_element(destination).\
                release(destination).perform()
        elif option == 'js':
            # drag and drop via javascript
            with open(os.path.join(os.path.dirname(__file__), 'dnd.js'), 'r') as f:
                drag_and_drop_js = f.read()
            DriverInstance().get_driver().execute_script(drag_and_drop_js + "executeDnD(arguments[0], arguments[1])",
                                                         source, destination)

    @staticmethod
    def send_data(web_element: object, data, click=False, clear=True):
        if click is True:
            web_element.click()
        if clear is True:
            web_element.clear()
        web_element.send_keys(data)

    @staticmethod
    def zoom(web_element: object, zoom):
        DriverInstance().get_driver().execute_script("arguments[0].style.zoom = arguments[1]", web_element, f'{zoom}%')

    @staticmethod
    def attribute(web_element: object, attribute: str):
        # returns value of attribute
        return web_element.get_attribute(attribute)

    @staticmethod
    def style(web_element: object, css_property: str):
        # returns value of css property
        return web_element.value_of_css_property(css_property)

    @staticmethod
    def element_state(web_element: object):
        # returns enabled/disabled element state
        flag = web_element.get_attribute('disabled')
        if flag == 'true':
            return True
        else:
            return False

    @staticmethod
    def scroll(web_element: object, width, height):
        DriverInstance().get_driver().execute_script('window.scrollBy(arguments[1],arguments[2])',
                                                     web_element, width, height)

    @staticmethod
    def right_click(web_element: object):
        ActionChains(DriverInstance().get_driver()).context_click(web_element).perform()

    @staticmethod
    def double_click(web_element: object):
        ActionChains(DriverInstance().get_driver()).double_click(web_element).perform()

    @staticmethod
    def switch_to_active_element():
        return DriverInstance().get_driver().switch_to.active_element

    @staticmethod
    def move_to_element(web_element: object):
        ActionChains(DriverInstance().get_driver()).move_to_element(web_element).perform()

    @staticmethod
    def click_on_demand(self):
        ActionChains(self.get_driver()).click().perform()

    @staticmethod
    def keyboard(command: str):
        commands = {
            'enter': Keys.ENTER,
            'alt': Keys.ALT,
            'shift': Keys.SHIFT,
            'ctrl': Keys.CONTROL,
            'escape': Keys.ESCAPE,
            'backspace': Keys.BACKSPACE,
            'tab': Keys.TAB,
            'command': Keys.COMMAND,
            'up': Keys.UP,
            'down': Keys.DOWN,
            'left': Keys.LEFT,
            'right': Keys.RIGHT
        }.get(command)
        ActionChains(DriverInstance().get_driver()).send_keys(commands).perform()
