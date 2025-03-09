from selenium import webdriver
import json
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Enroll:
    def __init__(self, config_file) -> None:
        with open(config_file, "r") as file:
            self.config = json.load(file)
            file.close()
        self.driver = webdriver.Firefox()
        self.driver.get(self.config["target"]["url"])

    def abort(self):
        self.driver.close()

    def login(self):
        username_space = self.driver.find_element(
            By.NAME, self.config["login_elem"]["username"]
        )
        password_space = self.driver.find_element(
            By.NAME, self.config["login_elem"]["password"]
        )

        username_space.send_keys(self.config["auth"]["username"])
        password_space.send_keys(self.config["auth"]["password"])

        time.sleep(1)

        self.driver.find_element(By.ID, self.config["login_elem"]["submit"]).submit()

    def get_each_course_page(self):
        i = 0
        conf = self.config["course_elem"]
        while True:
            current_page = conf["current_url"] + str(i)
            self.driver.get(current_page)

            if i > conf["oob"]:
                break

            if self.enroll_valid(conf):
                # self.driver.find_element(By.NAME, conf["submit"])
                print("Valid enroll: ", current_page)
            else:
                print("Invalid enroll: ", current_page)

            self.leave_course(conf)

            time.sleep(0.3)
            i += 1

    def enroll_valid(self, conf):
        try:
            self.driver.find_element(By.NAME, conf["submit"])
        except NoSuchElementException:
            return False
        return True

    def leave_course(self, conf):
        # TODO: Fix this function, there is a confirm page.
        # (post request of unrolling is same as the href id after partial_url)
        partial_url = conf["unroll_url"]
        try:
            leave_course = self.driver.find_element(
                By.XPATH,
                f"//a[contains(@href, '{partial_url}')]",
            )
            # leave_course.click()
        except NoSuchElementException:
            pass


script = Enroll("config.json")
script.login()
time.sleep(3)
script.get_each_course_page()
time.sleep(5)
script.abort()
