
# from https://gist.github.com/textarcana/5855427

 - install firefow and X et al :
    * sudo apt install firefox
    * sudo apt install xvfb
    * sudo apt install firefox-geckodriver
    libXfont Xorg "X Window System" "Desktop" "Fonts" "General Purpose Desktop"

 - launch windows system : Xvfb :99 -ac -screen 0 1280x1024x24 &
 - redirect display to it : export DISPLAY=:99 (in .bashrc)
 - launch selenium server : java -jar $SELENIUM_SERVER_JAR

# for multiple instances :
 - launch torpool
 - use parrunnum to launch parallel instances of test.py (each using a port of torpool) : ./parrunnum "python test.py " $portmin $portmax
NOTE : max 15-20 firefox instances - due to memory ? pb bad ip request -> ipv6 ?
-> can not be used as an attack with these capabilities.
