This project requires Python 3.8+ and selenium-4.2.0 to run properly.

To install requirements for the external packages used ([sgnlp](https://github.com/aisingapore/sgnlp) and [scweet](https://github.com/Altimis/Scweet)(modified_ver)), run:
<pre><code>pip install -r requirements.txt</code></pre>

To run the code:
<pre><code>python dashboard.py</code></pre>

Note: Chrome/Firefox must be installed for windows and linux, support for safari is available for Macos. 

It is recommended to use a windows system to test our code.  For Macos users, you may need to enable remote control for safari as discussed  [here](https://stackoverflow.com/questions/63927063/selenium-not-connecting-to-safari-web-driver) and change the driver_type in runner instance to be "safari", otherwise, set the headless boolean in Twitter::scraper::DEFAULT_SETTING to False to allow chrome driver to scrape from twitter. 

Common Issues:

- There may be firewall issues while installing chromedriver. If you find the search page freezes for a long time, please try to connect to other networks and try again.
  Otherwise, please refer to the instructions in the TODO comment in runner.py
- [Link](https://github.com/SergeyPirogov/webdriver_manager/issues) to webdriver-manager for troubleshoots on chromedriver installation. 
