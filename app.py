import os
from PIL import Image
import urllib.parse
from flask import Flask, send_file, abort
from time import sleep

from selenium import webdriver
from selenium.webdriver import ChromeOptions

app = Flask(__name__)

options = ChromeOptions()
options.headless=True
options.add_argument('--ignore-certificate-errors')
options.binary_location = "/app/.apt/usr/bin/google-chrome"
driver = webdriver.Chrome(chrome_options=options)

@app.route('/')
def view_landing():
    return "Welcome to the screenshot service!"


@app.route('/image/<path:encoded_url>.png')
def generate_image(encoded_url):
    """
    Returns an image (PNG) of a URL. The URL is encoded in the path of the image being requested.
    """
    url_to_fetch = urllib.parse.unquote_plus(encoded_url)
    # domain = os.environ.get('DOMAIN', 'https://casparwre.de')
    # if not url_to_fetch.startswith(domain):
    #     app.logger.info(f'Not allowed to generate preview for this domain: {url_to_fetch}')
    #     abort(405)
    app.logger.debug(f'Generating preview for {url_to_fetch}')
    driver.get(url_to_fetch)
    sleep(2)
    driver.set_window_size(1100, 600)

    screenshot_path = '/tmp/image.png'
    driver.save_screenshot(screenshot_path)
    output_size = (550,300)
    i = Image.open(screenshot_path)
    i.thumbnail(output_size)
    i.save(screenshot_path)
    # driver.quit()
    return send_file(screenshot_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(port=5001, debug=True)