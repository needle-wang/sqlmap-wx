## sqlmap-wx
sqlmap GUI, using wxpython4.0  

此GUI(wxpython太难控制了, 真想弃了...)虽然跨平台, 但主要在win使用.  
如果想在linux下使用, 建议使用[sqlmap-gtk](https://github.com/needle-wang/sqlmap-gtk), 体验更好!  
欢迎使用, 反馈!  

sqlmap已经移植到了python3!  
来自sqlmap's FAQ:  
"Both Python 2 and 3 are supported from May of 2019"  

#### 截图
![screenshot](https://github.com/needle-wang/sqlmap-wx/blob/master/screenshots/sqlmap-wx1.png)

#### 安装及使用
1. **要求**  
  - python3.5+
  - wxpython4.0+:  
     win: `pip3 install wxPython`  
     linux: 到[wxPython官方下载页](https://wxpython.org/pages/downloads/index.html)下载, 有的  
  - requests: `pip3 install requests`  
  - 最新的 [sqlmap](https://github.com/sqlmapproject/sqlmap): `git clone` it.  
2. **下载本GUI**
  - `git clone https://github.com/needle-wang/sqlmap-wx.git`  
  或 从这下载: [releases](https://github.com/needle-wang/sqlmap-wx/releases)(不一定最新)  
3. **运行**  
  - `./sqlmap_wx.py`  

#### 功能
1. 包含sqlmap(1.3.10.7#dev)所有选项(除了-d, 不定时更新sqlmap选项)  
2. 支持sqlmapapi客户端(API区)  
3. 会话功能, 自动保存和载入上一次的选项  
4. 将手册的内容全部集成进tooltip中

#### 关于
1. V0.3.3  
   2019年 10月 16日 星期三 06:54:46 CST  
   作者: needle wang ( needlewang2011@gmail.com )  
2. 使用wxPthon4重写sqlmap-wx(using PyGObject)  
5. 感谢[sqm](https://github.com/kxcode/gui-for-sqlmap)带来的灵感, 其作者: [KINGX](https://github.com/kxcode) (sqm UI 使用的是python2 + tkinter)  

#### 参考文献
1. wxpython教程: https://wiki.wxpython.org/ , http://zetcode.com/wxpython/  
2. wxpython API: https://wxpython.org/Phoenix/docs/html/index.html  
