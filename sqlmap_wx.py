#!/usr/bin/env python3
#
# 2019年 05月 05日 星期日 14:50:15 CST

from subprocess import Popen, PIPE, STDOUT
from threading import Thread

from widgets import wx, Panel, btn, cb, cbb, nb, st, tc
from widgets import VERTICAL, EXPAND, ALL, ALIGN_CENTER

from page1_notebook import Page1Notebook
from handlers import Handler

BoxSizer = wx.BoxSizer
GridSizer = wx.GridSizer
StaticBoxSizer = wx.StaticBoxSizer

SizerFlags = wx.SizerFlags
EVT_BUTTON = wx.EVT_BUTTON


class Window(wx.Frame):
  def __init__(self, parent):
    super().__init__(parent, title = 'sqlmap-wx', size = (300, 400))
    self._handlers = Handler(self)  # 需要先设置handler, Bind需要它

    self.initUI()
    # self.make_accels()  # 要先初始化完后, 才能设全局键

  # @profile
  def initUI(self):
    vbox = BoxSizer(VERTICAL)
    self.build_page_target()

    self.main_notebook = nb(self)
    page1 = self.build_page1(self.main_notebook)
    page2 = self.build_page2(self.main_notebook)
    page3 = self.build_page3(self.main_notebook)
    page4 = self.build_page4(self.main_notebook)
    page5 = self.build_page5(self.main_notebook)
    page6 = self.build_page6(self.main_notebook)

    self.main_notebook.AddPage(page1, '选项区(&1)')
    self.main_notebook.AddPage(page2, '输出区(&2)')
    self.main_notebook.AddPage(page3, '日志区(&3)')
    self.main_notebook.AddPage(page4, 'API区(&4)')
    self.main_notebook.AddPage(page5, '帮助(&H)')
    self.main_notebook.AddPage(page6, '关于')

    vbox.Add(self._target_notebook, flag = EXPAND)
    vbox.Add(self.main_notebook, proportion = 1, flag = EXPAND)
    # 很重要! Fit重新校正布局(包括子页面)
    self.SetSizerAndFit(vbox)

  def make_accels(self):
    '''
    https://www.blog.pythonlibrary.org/2017/09/28/wxpython-all-about-accelerators/
    只有最后一次的SetAcceleratorTable会生效
    '''
    self.Bind(wx.EVT_MENU, self.onExit, id = wx.ID_EXIT)
    self.accel_entries = [(wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
                          (wx.ACCEL_CTRL, ord('W'), wx.ID_EXIT)]

    main_note_ks = ['1', '2', '3', '4', 'H']
    for i in range(len(main_note_ks)):
      pageid = self.main_notebook.GetPage(i).GetId()

      self.accel_entries.append((wx.ACCEL_ALT, ord(main_note_ks[i]), pageid))
      self.Bind(
        wx.EVT_MENU,
        lambda evt, page = i: self.main_notebook.ChangeSelection(page),
        id = pageid)

    _note_keys = ['Q', 'W', 'E', 'R', 'T']
    for i in range(len(_note_keys)):
      pageid = self._notebook.GetPage(i).GetId()

      self.accel_entries.append((wx.ACCEL_ALT, ord(_note_keys[i]), pageid))
      self.Bind(
        wx.EVT_MENU,
        lambda evt, page = i:
          self._notebook.ChangeSelection(page)
            if self.main_notebook.GetSelection() == 0 else evt.Skip(),
        id = pageid)

    accel_tbl = wx.AcceleratorTable(self.accel_entries)
    self.SetAcceleratorTable(accel_tbl)

  def clear_all_entry(self, event):
    m = self._notebook
    for _i in dir(m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(m, _i)
        if isinstance(_tmp_entry, tc):
          _tmp_entry.SetValue('')

  def unselect_all_ckbtn(self, event):
    m = self._notebook
    for _i in dir(m):
      if _i.endswith('ckbtn'):
        _tmp_ckbtn = getattr(m, _i)
        if isinstance(_tmp_ckbtn, cb):
          _tmp_ckbtn.SetValue(False)
    for _i in m._enum_area_opts_ckbtns:
      for _j in _i:
        _j.SetValue(False)

  def onExit(self, event):
    # https://stackoverflow.com/questions/49454737/how-can-i-exit-out-of-a-wxpython-application-cleanly
    wx.CallAfter(self.Close)

  def build_page_target(self):
    # gtk3下的正确的高度!
    # self.a = nb(self, size = (400, 68))
    # b = tc(a, size = (-1, 36))
    self._target_notebook = nb(self)

    self._url_combobox = cbb(self._target_notebook, choices = ['http://www.site.com/vuln.php?id=1'])   # style = wx.CB_DROPDOWN

    p2 = Panel(self._target_notebook)
    hbox2 = BoxSizer()
    self._burp_logfile = tc(p2)
    self._burp_logfile_chooser = btn(p2, label = '打开')
    self._burp_logfile_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [self._burp_logfile]:
        self._handlers.set_file_entry_text(evt, data))

    hbox2.Add(self._burp_logfile, proportion = 1, flag = EXPAND)
    hbox2.Add(self._burp_logfile_chooser, flag = EXPAND)
    p2.SetSizer(hbox2)

    p3 = Panel(self._target_notebook)
    hbox3 = BoxSizer()
    self._request_file = tc(p3)
    self._request_file_chooser = btn(p3, label = '打开')
    self._request_file_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [self._request_file]:
        self._handlers.set_file_entry_text(evt, data))

    hbox3.Add(self._request_file, proportion = 1, flag = EXPAND)
    hbox3.Add(self._request_file_chooser, flag = EXPAND)
    p3.SetSizer(hbox3)

    p4 = Panel(self._target_notebook)
    hbox4 = BoxSizer()
    self._bulkfile = tc(p4)
    self._bulkfile_chooser = btn(p4, label = '打开')
    self._bulkfile_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [self._bulkfile]:
        self._handlers.set_file_entry_text(evt, data))

    hbox4.Add(self._bulkfile, proportion = 1, flag = EXPAND)
    hbox4.Add(self._bulkfile_chooser, flag = EXPAND)
    p4.SetSizer(hbox4)

    p5 = Panel(self._target_notebook)
    hbox5 = BoxSizer()
    self._configfile = tc(p5)
    self._configfile_chooser = btn(p5, label = '打开')
    self._configfile_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [self._configfile]:
        self._handlers.set_file_entry_text(evt, data))

    hbox5.Add(self._configfile, proportion = 1, flag = EXPAND)
    hbox5.Add(self._configfile_chooser, flag = EXPAND)
    p5.SetSizerAndFit(hbox5)

    self._sitemap_url = tc(self._target_notebook)
    self._google_dork = tc(self._target_notebook)

    self._target_notebook.AddPage(self._url_combobox, '目标url')
    self._target_notebook.AddPage(p2, 'burp日志')
    self._target_notebook.AddPage(p3, 'HTTP请求')
    self._target_notebook.AddPage(p4, 'BULKFILE')
    self._target_notebook.AddPage(p5, 'ini文件')
    self._target_notebook.AddPage(self._sitemap_url, 'xml_url')
    self._target_notebook.AddPage(self._google_dork, 'GOOGLEDORK')

  def build_page1(self, parent):
    p = Panel(parent)
    vbox = BoxSizer(VERTICAL)

    # sqlmap命令语句
    cmd_area = StaticBoxSizer(VERTICAL, p, 'A.收集选项 的结果显示在这:')
    _cmd_area = cmd_area.GetStaticBox()

    self._cmd_entry = tc(_cmd_area)

    cmd_area.Add(self._cmd_entry, flag = EXPAND)

    # 主构造区
    self._notebook = Page1Notebook(p, self._handlers)

    # 构造与执行
    grid = GridSizer(1, 4, 0, 0)
    _build_button = btn(p, label = 'A.收集选项(&A)')
    _build_button.Bind(EVT_BUTTON, self._handlers.build_all)
    # 用于改善ui的使用体验
    _unselect_all_btn = btn(p, label = '反选所有复选框(&S)')
    _unselect_all_btn.Bind(EVT_BUTTON, self.unselect_all_ckbtn)
    _clear_all_entry = btn(p, label = '清空所有输入框(&D)')
    _clear_all_entry.Bind(EVT_BUTTON, self.clear_all_entry)
    _run_button = btn(p, label = 'B.开始(&F)')
    _run_button.Bind(EVT_BUTTON, self._handlers.run_cmdline)

    grid.Add(_build_button, flag = ALIGN_CENTER)
    grid.Add(_unselect_all_btn, flag = ALIGN_CENTER)
    grid.Add(_clear_all_entry, flag = ALIGN_CENTER)
    grid.Add(_run_button, flag = ALIGN_CENTER)

    vbox.Add(cmd_area, flag = EXPAND)
    vbox.Add(self._notebook, proportion = 1, flag = EXPAND)
    vbox.Add(grid, flag = EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page2(self, parent):
    p = Panel(parent)
    return p

  def build_page3(self, parent):
    p = Panel(parent)
    vbox = BoxSizer(VERTICAL)
    # 多行文本框的默认size太小了
    # 默认高度太低, 不指定个高度, 会报 滚动条相关的size 警告
    self._page3_log_view = tc(p,
                              size = (-1, 300),
                              style = wx.TE_MULTILINE | wx.TE_READONLY)
    self._handlers.clear_log_view_buffer(None)

    grid = GridSizer(1, 3, 0, 0)
    _page3_read_target_btn = btn(p, label = '查看target文件')
    _page3_clear_btn = btn(p, label = '清空(&C)')
    _page3_read_log_btn = btn(p, label = '查看log文件')

    _page3_read_target_btn.Bind(EVT_BUTTON, self._handlers.read_target_file)
    _page3_clear_btn.Bind(EVT_BUTTON, self._handlers.clear_log_view_buffer)
    _page3_read_log_btn.Bind(EVT_BUTTON, self._handlers.read_log_file)

    grid.Add(_page3_read_target_btn, flag = ALIGN_CENTER)
    grid.Add(_page3_clear_btn, flag = ALIGN_CENTER)
    grid.Add(_page3_read_log_btn, flag = ALIGN_CENTER)

    vbox.Add(self._page3_log_view, proportion = 1, flag = EXPAND | ALL, border = 10)
    vbox.Add(grid, flag = EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page4(self, parent):
    p = Panel(parent)

    return p

  def build_page5(self, parent):
    p = Panel(parent)
    vbox = BoxSizer(VERTICAL)
    # 多行文本框的默认size太小了
    # 默认高度太低, 不指定个高度, 会报 滚动条相关的size 警告
    self._page5_manual_view = tc(p,
                                 size = (-1, 300),
                                 style = wx.TE_MULTILINE | wx.TE_READONLY)
    vbox.Add(self._page5_manual_view, proportion = 1, flag = EXPAND | ALL, border = 10)

    # 使用线程 填充 帮助标签, 加快启动速度
    t = Thread(target = self._set_manual_view,
               args = (self._page5_manual_view,))
    # t.daemon = True   # 死了也会存在
    t.start()

    p.SetSizerAndFit(vbox)
    return p

  def _set_manual_view(self, textbuffer):
    '''
    不用多线程能行嘛? 想要获得输出结果就一定会有阻塞的可能!
    https://www.jianshu.com/p/11090e197648
    https://wiki.gnome.org/Projects/PyGObject/Threading
    '''
    # _manual_hh = '/home/needle/bin/output_interval.sh'
    # WIN下不能用此行
    # _manual_hh = ['/usr/bin/env', 'sqlmap', '-hh']
    _manual_hh = 'echo y|sqlmap -hh'
    try:
      _subprocess = Popen(_manual_hh, stdout=PIPE, stderr=STDOUT, bufsize=1, shell = True)

      for _an_bytes_line_tmp in iter(_subprocess.stdout.readline, b''):
        wx.CallAfter(textbuffer.write, _an_bytes_line_tmp.decode('utf8'))
      _subprocess.stdout.close()
      _subprocess.wait()
    except FileNotFoundError as e:
      wx.CallAfter(textbuffer.write, str(e))
    finally:
      wx.CallAfter(textbuffer.ShowPosition, 0)

  def build_page6(self, parent):
    p = Panel(parent)
    vbox = BoxSizer(VERTICAL)

    _about_str = '''
    1. VERSION: 0.1
       2019年 05月 08日 星期三 20:59:42 CST
       required: python3.5+, wxPython4.0+, sqlmap(require: python2.6+)
       作者: needle wang ( needlewang2011@gmail.com )\n
    2. 使用wxPython重写sqlmap-ui(using PyGObject)\n
    3. wxpython教程: https://wiki.wxpython.org/
                     http://zetcode.com/wxpython/
    4. wxpython API: https://wxpython.org/Phoenix/docs/html/index.html\n\n
    5. 感谢sqm带来的灵感, 其作者: KINGX ( https://github.com/kxcode ), sqm UI 使用的是python2 + tkinter
    '''
    hbox = BoxSizer()
    _page6_about = st(p, label = _about_str)
    # 完全居中!
    hbox.Add(_page6_about, flag = ALIGN_CENTER)
    vbox.Add(hbox, proportion = 1, flag = ALIGN_CENTER)

    p.SetSizerAndFit(vbox)
    return p


def main():
  app = wx.App()

  win = Window(None)
  win.Centre()
  win.Show()

  app.MainLoop()


if __name__ == '__main__':
  main()
