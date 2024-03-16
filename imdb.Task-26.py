import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class IMDbSearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.imdb.com/search/name/"

    def open(self):
        self.driver.get(self.url)

    def enter_text_in_search_box(self, text):
        search_box = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "suggestion-search")))
        search_box.clear()
        search_box.send_keys(text)

    def select_option_in_dropdown(self, option):
        # Wait for the dropdown options to be visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//ul[@role='listbox']")))

        # Now select the option
        dropdown = Select(self.driver.find_element(By.ID, "quicksearch-suggestion"))
        dropdown.select_by_visible_text(option)

    def click_search_button(self):
        search_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "suggestion-search-button")))
        search_button.click()

@pytest.fixture
def browser():
    driver = webdriver.Chrome()  # You can change this to your preferred browser driver
    yield driver
    driver.quit()

def test_imdb_search(browser):
    imdb_search_page = IMDbSearchPage(browser)
    imdb_search_page.open()

    # Enter text in search box
    imdb_search_page.enter_text_in_search_box("Tom Hanks")

    # Select an option in the dropdown
    imdb_search_page.select_option_in_dropdown("Actors")

    # Click search button
    imdb_search_page.click_search_button()

    # Wait for search results to load
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "findHeader")))

    # Assertions can be added to verify search results
    assert "Results for 'Tom Hanks'" in browser.title

    # Additional assertions or verifications can be added as per requirements
