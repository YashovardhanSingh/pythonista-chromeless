import selenium
from selenium.webdriver import Chrome, ChromeOptions
import io
from PIL import Image
try:
    """developer in git env"""
    from apigateway_credentials import awsgateway_url, awsgateway_apikey
    from pypi.chromeless.chromeless import Chromeless, LambdaAlreadyTriggeredException
except Exception as e:
    """general user who downloaded this script"""
    # pip install chromeless
    from chromeless import Chromeless, LambdaAlreadyTriggeredException
    # replace credentials
    awsgateway_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    awsgateway_url = "https://XXXXXXXXXX.execute-api.us-west-2.amazonaws.com/default/chromeless"


def get_title(self, url):
    self.get(url)
    return self.title


def example_of_get_title():
    """basic example"""
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_title)
    result = chrome.get_title("https://google.com")
    print(result, type(result))
    # Google <class 'str'>


def get_list(self):
    self.get("https://stackoverflow.com/")
    question_titles = [e.text for e in self.find_elements_by_xpath(
        "//h3/a[@class='question-hyperlink']")]
    return question_titles


def example_of_get_list():
    """you can get any type if it's picklable. this is <class 'list'> example"""
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_list)
    result = chrome.get_list()
    print(result[:2], type(result))
    # ['JSoup: how to list links from a list?', 'How to Fix PHPSESSID issue in Symfony 3.4'] <class 'list'>


def get_title_letter_num(self, url):
    return len(self.get_title(url))


def example_of_get_title_letter_num():
    """
    you can call only one method,
    but you can bind multiple method and use them all by wrapping.
    """
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_title)
    chrome.attach_method(get_title_letter_num)
    result = chrome.get_title_letter_num("http://github.com")
    print(result, type(result))
    # 58 <class 'int'>


def get_screenshot(self, url, filename):
    self.get(url)
    self.save_screenshot(filename)


def example_of_get_screenshot():
    """
    just use the same local path argument as same as origin Chrome.save_screenshot(path).
    Chromeless will transfer from lambda to your local.
    """
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(get_screenshot)
    result = chrome.get_screenshot("https://github.com/umihico", "screenshot.png")
    print(result, type(result))
    # None <class 'NoneType'>


def example_of_default_method():
    """
    you can also run simple default method on Chrome
    """
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    result = chrome.get("http://aws.amazon.com")
    print(result, type(result))
    # None <class 'NoneType'>


def example_of_twice_called_error():
    """you can't call method more than once"""
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.get("http://github.com")
    try:
        chrome.get("https://google.com")
    except LambdaAlreadyTriggeredException as e:
        print('(expected error)', e)
    # (expected error) If you have multiple methods, please wrap them and call the wrapper instead.


def cause_NoSuchElementException(self):
    self.get("http://github.com")
    self.find_element_by_xpath("//nonexistelement")  # cause NoSuchElementException in lambda


def example_of_cause_NoSuchElementException():
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(cause_NoSuchElementException)
    try:
        chrome.cause_NoSuchElementException()
    except selenium.common.exceptions.NoSuchElementException as e:
        print('(expected error)', e)


def example_of_changing_windowsize():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    # default is "--window-size=1280x1696"
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--homedir=/tmp")
    chrome = Chromeless(awsgateway_url, awsgateway_apikey, chrome_options=chrome_options)
    chrome.attach_method(get_screenshot)
    result = chrome.get_screenshot("https://github.com/umihico", "screenshot.png")
    print(result, type(result))


def resize_screenshot(self):
    self.get("https://github.com/umihico")
    img_png = self.get_screenshot_as_png()
    img_io = io.BytesIO(img_png)
    img = Image.open(img_io)
    image.thumbnail((500, 500), Image.LANCZOS)
    return image


def example_of_resize_screenshot():
    chrome = Chromeless(awsgateway_url, awsgateway_apikey)
    chrome.attach_method(resize_screenshot)
    chrome.activate_library('import io')
    chrome.activate_library('from PIL import Image')
    image = chrome.resize_screenshot()
    image.save("screenshot.png")


if __name__ == '__main__':
    # example_of_get_title()
    # example_of_get_list()
    # example_of_get_title_letter_num()
    # example_of_get_screenshot()
    # example_of_default_method()
    # example_of_twice_called_error()
    # example_of_cause_NoSuchElementException()
    # example_of_changing_windowsize()
    example_of_resize_screenshot()
