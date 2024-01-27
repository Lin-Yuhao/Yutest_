from time import sleep
from PySide6.QtCore import QThread, Signal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.support import expected_conditions as EC, wait, expected_conditions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.ie.options import Options as IEOptions



class UiTest(QThread):
    finished = Signal(str)
    errorrow = Signal(int)
    errorbrowser = Signal(str)

    def __init__(self):
        super().__init__()
        self.datapath = None
        self.driver = None
        self.data = None
        self.config = None

    def run(self):
        if self.datapath:
            for key, value in self.datapath.items():
                try:
                    if key == "Chrome":
                        options = ChromeOptions()
                        if self.config[0]:
                            options.add_argument("--headless")
                        if self.config[1]:
                            options.page_load_strategy = 'eager'
                        service = ChromeService(value)
                        self.driver = webdriver.Chrome(service=service, options=options)
                    elif key == "Edge":
                        options = EdgeOptions()
                        if self.config[0]:
                            options.add_argument("--headless")
                        if self.config[1]:
                            options.page_load_strategy = 'eager'
                        service = EdgeService(value)
                        self.driver = webdriver.Edge(service=service, options=options)
                    elif key == "Firefox":
                        options = FirefoxOptions()
                        if self.config[0]:
                            options.add_argument("--headless")
                        if self.config[1]:
                            options.page_load_strategy = 'eager'
                        service = FirefoxService(value)
                        self.driver = webdriver.Firefox(service=service, options=options)
                    elif key == "IE":
                        options = IEOptions()
                        if self.config[0]:
                            options.add_argument("--headless")
                        if self.config[1]:
                            options.page_load_strategy = 'eager'
                        service = IEService(value)
                        self.driver = webdriver.Ie(service=service, options=options)
                except:
                    self.errorbrowser.emit('浏览器搜索异常')
                    return
            data = self.data
            if data:
                for item in range(len(data)):
                    for key in data[item]:
                        if hasattr(self, key):
                            method = getattr(self, key)
                            if callable(method):
                                try:
                                    method(data[item][key])
                                except Exception as e:
                                    # print(e)
                                    self.driver.quit()
                                    self.driver = None
                                    if self.driver is None:
                                        self.errorrow.emit(item)
                                    return
                            else:
                                print(f"{key} is not a method in this class.")
                        else:
                            print(f"The method {key} does not exist in this class.")
            self.driver.quit()
            self.driver = None
            if self.driver is None:
                self.finished.emit("Selenium operation finished")
        else:
            self.errorbrowser.emit("Selenium operation finished")

    def operationOpen(self, data):
        self.driver.get(data[0])

    def find(self, by, element):
        locator = {
            0: (By.ID, element),
            1: (By.CLASS_NAME, element),
            2: (By.CSS_SELECTOR, element),
            3: (By.NAME, element),
            4: (By.LINK_TEXT, element),
            5: (By.PARTIAL_LINK_TEXT, element),
            6: (By.TAG_NAME, element),
            7: (By.XPATH, element)
        }
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator[by])
        )

    def operationClick(self, data):
        self.find(data[0], data[1]).click()
        sleep(1)

    def operationEdit(self, data):
        self.find(data[0], data[1]).send_keys(data[2])
        sleep(1)

    def operationClear(self, data):
        self.find(data[0], data[1]).clear()
        sleep(1)

    def operationWindow(self, data):
        if data[0] == 0:
            self.driver.switch_to.new_window('tab')
        elif data[0] == 1:
            self.driver.switch_to.new_window('window')
        elif data[0] == 2:
            self.driver.switch_to.window(self.driver.window_handles[data[1]])
        elif data[0] == 3:
            self.driver.close()

    def operationSize(self, data):
        if data[0] == 0:
            self.driver.maximize_window()
        elif data[0] == 1:
            self.driver.fullscreen_window()
        elif data[0] == 2:
            self.driver.minimize_window()

    def operationNav(self, data):
        if data[0] == 0:
            self.driver.back()
        elif data[0] == 1:
            self.driver.refresh()
        elif data[0] == 2:
            self.driver.forward()

    def operationAlert(self, data):
        if data[0] == 0:
            alert = wait.until(expected_conditions.alert_is_present())
            alert.accept()
        elif data[0] == 1:
            alert = wait.until(expected_conditions.alert_is_present())
            alert.dismiss()

    def operationCookie(self, data):
        for key, value in data.items():
            self.driver.add_cookie({'name': key, 'value': value})

    def operationFrames(self, data):
        if data[0] == 0:
            self.driver.switch_to.frame(data[1])
        elif data[0] == 1:
            self.driver.switch_to.frame(data[1])
        elif data[0] == 2:
            iframe = self.driver.find_elements(By.TAG_NAME, 'iframe')[data[2]]
            self.driver.switch_to.frame(iframe)
        elif data[0] == 3:
            self.driver.switch_to.default_content()

    def operationJS(self, data):
        self.driver.execute_script(data[0])
