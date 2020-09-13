# pylint: disable=import-error
# pylint: disable=anomalous-backslash-in-string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from tqdm import tqdm

from navs.search import Search