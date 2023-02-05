This project requires Python 3.8+ and requires selenium-4.2.0 to run properly.

To install requirements for the external packages used (sgnlp and scweet-modified_ver), run:
<pre><code>pip install -r requirements.txt</code></pre>

To run the code:
<pre><code>python dashboard.py</code></pre>

Note: Chrome/Firefox must be installed for windows and linux, support for safari is available for Macos. 

It is recommended to use a windows system to test our code.  For Macos users, you may need to enable remote control for safari as discussed  [here](https://stackoverflow.com/questions/63927063/selenium-not-connecting-to-safari-web-driver) and change the driver_type in runner instance to be "safari", otherwise, set the headless boolean in Twitter::scraper::DEFAULT_SETTING to False to allow chrome driver to scrape from twitter. 
