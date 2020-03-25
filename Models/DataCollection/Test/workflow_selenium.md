
# from https://gist.github.com/textarcana/5855427

 - install firefow and X et al :
    * sudo apt install firefox
    * sudo apt install xvfb
    * sudo apt install firefox-geckodriver

 - launch windows system : Xvfb :99 -ac -screen 0 1280x1024x24 &
 - redirect display to it : export DISPLAY=:99 (in .bashrc)
 - launch selenium server : java -jar $SELENIUM_SERVER_JAR
 
