import pytest
from selen.client.driver import Driver, DriverInstance
from selen.client.helper import Tool


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def driver(request):
    chrome_driver = Driver.chrome()
    driver_instance = DriverInstance(driver=chrome_driver)
    driver_instance.set_driver()
    driver = driver_instance.get_driver()
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(30)
    yield driver
    if request.node.rep_call.failed:
        Driver.create_screenshot(driver, Tool.time_stamp(request.function.__name__ + '--'), 'allure')
    driver.quit()
