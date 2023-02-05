This project makes use of Scweet which requires selenium-4.2.0 to run properly.

To install requirements for the external packages used (sgnlp and scweet-modified_ver), run:
<pre><code>pip install -r requirements.txt</code></pre>
Note: Chrome/Firefox must be installed for windows and linux, support for safari is available for macos. 
For Macos users, you may need to enable remote control for safari, otherwise, set the headless boolean in Twitter::scraper::DEFAULT_SETTING to False to enable scraping from twitter. 
