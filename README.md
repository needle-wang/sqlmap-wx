## sqlmap-wx
sqlmap GUI, using wxPython4.0

此GUI(wxPython太难控制了~)虽然跨平台, 但主要在win使用.  
linux下建议使用[sqlmap-gtk](https://github.com/needle-wang/sqlmap-gtk).   
sqlmap已经移植到了python3. 来自sqlmap的FAQ:  
"Both Python 2 and 3 are supported from May of 2019"

#### SCREENSHOT
![screenshot](https://github.com/needle-wang/sqlmap-wx/blob/master/screenshots/sqlmap-wx1.png)

#### HOW-TO
1. **Prerequisites**
  - python3.6+
  - [sqlmap](https://github.com/sqlmapproject/sqlmap): (choose one)
    - `pip3 install sqlmap`(suggestion)
    - `git clone https://github.com/sqlmapproject/sqlmap.git`
  - wxPython4.0+:
     - windows: `pip3 install wxPython`
     - linux: 到[wxPython官方](https://wxpython.org/pages/downloads/index.html)下载, 有的
  - requests: `pip3 install requests`
2. **Download**
  - `git clone https://github.com/needle-wang/sqlmap-wx.git`
3. **Run**
  - `./sqlmap_wx.py`

#### FUNCTION
- all sqlmap(1.3.10.7#dev) options(except -d, 不定时更新sqlmap选项)
- sqlmapapi client
- built-in mini wiki(tooltip and placeholder)
- session: autosave current options before quit, autoload last used options

#### ABOUT
- V0.3.3.1  
   2021-01-31 05:12:52
- use wxPython4 to recode sqlmap-gtk(driven by PyGObject)
- thanks to the idea from sqm <https://github.com/kxcode/gui-for-sqlmap>  
  author: [KINGX](https://github.com/kxcode)(sqm UI using python2 + tkinter)

#### REFERENCE
- wxPython教程: https://wiki.wxpython.org/, http://zetcode.com/wxpython/
- wxPython API: https://wxpython.org/Phoenix/docs/html/index.html
