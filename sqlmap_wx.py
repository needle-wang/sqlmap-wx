#!/usr/bin/env python3
#
# 2019年 05月 05日 星期日 14:50:15 CST

from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from time import sleep

from widgets import wx, Panel, Scroll, SplitterWindow, btn, cb, cbb, nb, st, tc
from widgets import VERTICAL, EXPAND, ALL, TOP, BOTTOM, LEFT, RIGHT, ALIGN_CENTER

from page1_notebook import Page1Notebook
from handlers import Handler, IS_POSIX
from session import Session
from tooltips import Widget_Mesg as INIT_MESG

BoxSizer = wx.BoxSizer
GridSizer = wx.GridSizer
StaticBoxSizer = wx.StaticBoxSizer

SizerFlags = wx.SizerFlags
EVT_BUTTON = wx.EVT_BUTTON


class Window(wx.Frame):
  def __init__(self, parent):
    super().__init__(parent, title = 'sqlmap-wx')
    self._handlers = Handler(self)  # 需要先设置handler, Bind需要它

    self.initUI()
    self.make_accelerators()  # 要先初始化完成后, 才能设全局键

    # 添加tooltips, placeholders等
    INIT_MESG(self)

    # 读取 上次所有选项
    self.session = Session(self)
    self.session.load_from_tmp()

  # @profile
  def initUI(self):
    p = Panel(self)
    vbox = BoxSizer(VERTICAL)

    self._target_notebook = nb(p)
    self.build_target_notebook(self._target_notebook)

    self.main_notebook = nb(p)
    page1 = self.build_page1(self.main_notebook)
    page2 = self.build_page2(self.main_notebook)
    page3 = self.build_page3(self.main_notebook)
    page4 = self.build_page4(self.main_notebook)
    page5 = self.build_page5(self.main_notebook)
    page6 = self.build_page6(self.main_notebook)

    self.main_notebook.AddPage(page1, '选项区(1)')
    self.main_notebook.AddPage(page2, '输出区(2)')
    self.main_notebook.AddPage(page3, '日志区(3)')
    self.main_notebook.AddPage(page4, 'API区(4)')
    self.main_notebook.AddPage(page5, '帮助(H)')
    self.main_notebook.AddPage(page6, '关于')

    vbox.Add(self._target_notebook, flag = EXPAND)
    vbox.Add(self.main_notebook, proportion = 1, flag = EXPAND)
    p.SetSizer(vbox)

    _frame_sz = BoxSizer()
    _frame_sz.Add(p, proportion = 1, flag = EXPAND)
    # 使用SetSizerAndFit方法使frame拥有最小size
    self.SetSizerAndFit(_frame_sz)

  def make_accelerators(self):
    '''
    https://www.blog.pythonlibrary.org/2017/09/28/wxpython-all-about-accelerators/
    只有最后一次的SetAcceleratorTable会生效
    '''
    self.Bind(wx.EVT_CLOSE, self.onExit)
    self.Bind(wx.EVT_MENU, self.onCloseByAccel, id = wx.ID_EXIT)
    self.accel_entries = [(wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
                          (wx.ACCEL_CTRL, ord('W'), wx.ID_EXIT)]

    main_note_ks = ['1', '2', '3', '4', 'H']
    for i in range(len(main_note_ks)):
      pageid = self.main_notebook.GetPage(i).GetId()

      self.accel_entries.append((wx.ACCEL_ALT, ord(main_note_ks[i]), pageid))
      self.Bind(
        wx.EVT_MENU,
        lambda evt, page = i: self.main_notebook.SetSelection(page),
        id = pageid)

    _note_keys = ['Q', 'W', 'E', 'R', 'T']
    for i in range(len(_note_keys)):
      pageid = self._notebook.GetPage(i).GetId()

      self.accel_entries.append((wx.ACCEL_ALT, ord(_note_keys[i]), pageid))
      self.Bind(
        wx.EVT_MENU,
        lambda evt, page = i:
          self._notebook.SetSelection(page)
            if self.main_notebook.GetSelection() == 0 else evt.Skip(),
        id = pageid)
    # win下, 若焦点没有按钮上, 则不响应mnemonic, 只能在这里实现了
    _btn_keys = ['A', 'S', 'D', 'F']
    btns = self.btn_grid.GetChildren()
    for i in range(len(btns)):
      btn = btns[i].GetWindow()
      btnid = btn.GetId()

      self.accel_entries.append((wx.ACCEL_ALT, ord(_btn_keys[i]), btnid))
      self.Bind(
        wx.EVT_MENU,
        lambda evt, _btn = btn:  # 防止闭包: btn这个变量名跟lambda绑定成一体
          self.make_btn_accel(_btn)
            if self.main_notebook.GetSelection() == 0 else evt.Skip(),
        id = btnid)

    accel_tbl = wx.AcceleratorTable(self.accel_entries)
    self.SetAcceleratorTable(accel_tbl)

  def make_btn_accel(self, btn):
    '''
    https://stackoverflow.com/questions/12786471/invoking-a-wxpython-evt-button-event-programmatically
    '''
    evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, btn.GetId())
    # print(evt)
    wx.PostEvent(btn, evt)

  def clear_all_entry(self, event):
    m = self._notebook
    for _i in dir(m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(m, _i)
        if isinstance(_tmp_entry, tc) and _tmp_entry is not self._notebook.sqlmap_path_entry:
          _tmp_entry.SetValue('')

    m.SetFocus()

  def unselect_all_ckbtn(self, event):
    m = self._notebook
    for _i in dir(m):
      if _i.endswith('ckbtn'):
        _tmp_ckbtn = getattr(m, _i)
        if isinstance(_tmp_ckbtn, cb) and _tmp_ckbtn.IsChecked():
          _tmp_ckbtn.SetValue(False)
    for _i in m._enum_area_opts_ckbtns:
      for _j in _i:
        if _j.IsChecked():
          _j.SetValue(False)

    m.SetFocus()

  def onCloseByAccel(self, event):
    '''
    https://stackoverflow.com/questions/49454737/how-can-i-exit-out-of-a-wxpython-application-cleanly
    '''
    # print('by accelerator.')
    wx.CallAfter(self.Close)

  def onExit(self, event):
    '''
    https://www.daniweb.com/programming/software-development/code/216760/verify-exit-dialog-wxpython
    '''
    # print('by ALT-<F4> or click close button.')
    # 保存 此次所有选项
    self.session.save_to_tmp()

    event.Skip()

  def build_target_notebook(self, parent):
    self._url_combobox = cbb(parent, choices = ['http://www.site.com/vuln.php?id=1'])   # style = wx.CB_DROPDOWN

    p2 = Panel(parent)
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

    p3 = Panel(parent)
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

    p4 = Panel(parent)
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

    p5 = Panel(parent)
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

    self._sitemap_url = tc(parent)
    self._google_dork = tc(parent)

    parent.AddPage(self._url_combobox, '目标url')
    parent.AddPage(p2, 'burp日志')
    parent.AddPage(p3, 'HTTP请求')
    parent.AddPage(p4, 'BULKFILE')
    parent.AddPage(p5, 'ini文件')
    parent.AddPage(self._sitemap_url, 'xml_url')
    parent.AddPage(self._google_dork, 'GOOGLEDORK')

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
    self.btn_grid = GridSizer(1, 4, 0, 0)
    _build_button = btn(p, label = 'A.收集选项(A)')
    _build_button.Bind(EVT_BUTTON, self._handlers.build_all)
    # 用于改善ui的使用体验
    _unselect_all_btn = btn(p, label = '反选所有复选框(S)')
    _unselect_all_btn.Bind(EVT_BUTTON, self.unselect_all_ckbtn)

    _clear_all_entry = btn(p, label = '清空所有输入框(D)')
    _clear_all_entry.Bind(EVT_BUTTON, self.clear_all_entry)

    _run_button = btn(p, label = 'B.开始(F)')
    _run_button.Bind(EVT_BUTTON, self._handlers.run_cmdline)

    self.btn_grid.Add(_build_button, flag = ALIGN_CENTER)
    self.btn_grid.Add(_unselect_all_btn, flag = ALIGN_CENTER)
    self.btn_grid.Add(_clear_all_entry, flag = ALIGN_CENTER)
    self.btn_grid.Add(_run_button, flag = ALIGN_CENTER)

    vbox.Add(cmd_area, flag = EXPAND)
    vbox.Add(self._notebook, proportion = 1, flag = EXPAND)
    vbox.Add(self.btn_grid, flag = EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page2(self, parent):
    p = Panel(parent)
    st(p, label = 'TODO')
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
    self._page3_clear_btn = btn(p, label = '清空(&C)')
    _page3_read_log_btn = btn(p, label = '查看log文件')

    _page3_read_target_btn.Bind(EVT_BUTTON, self._handlers.read_target_file)
    self._page3_clear_btn.Bind(EVT_BUTTON, self._handlers.clear_log_view_buffer)
    _page3_read_log_btn.Bind(EVT_BUTTON, self._handlers.read_log_file)

    grid.Add(_page3_read_target_btn, flag = ALIGN_CENTER)
    grid.Add(self._page3_clear_btn, flag = ALIGN_CENTER)
    grid.Add(_page3_read_log_btn, flag = ALIGN_CENTER)

    vbox.Add(self._page3_log_view, proportion = 1, flag = EXPAND | ALL, border = 10)
    vbox.Add(grid, flag = EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page4(self, parent):
    p = Panel(parent)
    vbox = BoxSizer(VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    row1 = BoxSizer()
    self._page4_api_server_label = st(p, label = 'REST-JSON API server:')
    self._page4_api_server_entry = tc(p, value = '127.0.0.1:8775')
    self._page4_admin_token_label = st(p, label = 'Admin (secret) token:')
    self._page4_admin_token_entry = tc(p)
    self._page4_admin_token_entry.SetMaxLength(32)

    row1.Add(self._page4_api_server_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    row1.Add(self._page4_api_server_entry, proportion_border)
    row1.Add(self._page4_admin_token_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    row1.Add(self._page4_admin_token_entry, proportion_border)

    row2 = BoxSizer()
    _arrow_down = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_BUTTON)
    self._page4_task_new_btn = btn(p, label = '创建任务')
    self._page4_admin_list_btn = btn(p, label = '显示任务')
    self._page4_admin_list_btn.SetBitmap(_arrow_down, dir = RIGHT)
    self._page4_admin_flush_btn = btn(p, label = '删除所有任务')
    self._page4_clear_task_view_btn = btn(p, label = '清空反馈的结果')

    self._page4_task_new_btn.Bind(EVT_BUTTON, self._handlers.api_task_new)
    self._page4_admin_list_btn.Bind(EVT_BUTTON, self._handlers.api_admin_list)
    self._page4_admin_flush_btn.Bind(EVT_BUTTON, self._handlers.api_admin_flush)
    self._page4_clear_task_view_btn.Bind(EVT_BUTTON, self._handlers.clear_task_view_buffer)

    row2.Add(self._page4_task_new_btn, flag = LEFT | RIGHT, border = 5)
    row2.Add(self._page4_admin_list_btn, flag = LEFT | RIGHT, border = 5)
    row2.Add(self._page4_admin_flush_btn, flag = LEFT | RIGHT, border = 5)
    row2.Add(self._page4_clear_task_view_btn, flag = LEFT | RIGHT, border = 5)

    row3 = SplitterWindow(p, style = wx.SP_LIVE_UPDATE | wx.BORDER_SUNKEN)
    # 不能放在SplitVertically后面, 不然gravity会无效
    row3.SetMinimumPaneSize(400)
    row3.SetSashGravity(0.7)

    lpane = Scroll(row3)
    self._api_admin_list_rows = lpane

    lpane.SetSizer(BoxSizer(VERTICAL))

    rpane = Panel(row3)
    _rbox = BoxSizer(VERTICAL)

    self._page4_option_get_entry = tc(rpane, value = 'url risk level')
    _options_example = ("{\n"
                        "  'url': 'http://www.site.com/vuln.php?id=1',\n"
                        "  'level': 1, 'risk': 1,\n\n"
                        "}\n# 所有选项见sqlmap目录中的optiondict.py\n")
    self._page4_option_set_view = tc(rpane,
                                     value = _options_example,
                                     style = wx.TE_MULTILINE)
    _rbox.Add(self._page4_option_get_entry, flag = EXPAND | ALL, border = 2)
    _rbox.Add(self._page4_option_set_view, proportion = 1, flag = EXPAND | ALL, border = 2)
    rpane.SetSizer(_rbox)

    row3.SplitVertically(lpane, rpane)

    self._page4_task_view = tc(p, value = '此处显示反馈的结果:\n', style = wx.TE_MULTILINE | wx.TE_READONLY)

    vbox.Add(row1, flag = EXPAND | ALL, border = 5)
    vbox.Add(row2, flag = EXPAND | ALL, border = 5)
    vbox.Add(row3, proportion = 1, flag = EXPAND | LEFT | RIGHT, border = 10)
    vbox.Add(self._page4_task_view, proportion = 1, flag = EXPAND | ALL, border = 10)

    p.SetSizerAndFit(vbox)
    return p

  def build_page5(self, parent):
    p = Panel(parent)
    vbox = BoxSizer(VERTICAL)

    self._get_sqlmap_path_btn = btn(p, label = '获取帮助')
    # 多行文本框的默认size太小了
    # 默认高度太低, 不指定个高度, gtk会报 滚动条相关的size 警告
    self._page5_manual_view = tc(p,
                                 size = (-1, 300),
                                 style = wx.TE_MULTILINE | wx.TE_READONLY)

    self._get_sqlmap_path_btn.Bind(EVT_BUTTON, self._make_help_thread)

    vbox.Add(self._get_sqlmap_path_btn, flag = TOP | LEFT | BOTTOM, border = 10)
    vbox.Add(self._page5_manual_view, proportion = 1, flag = EXPAND | LEFT | RIGHT, border = 10)

    self._make_help_thread(None)

    p.SetSizerAndFit(vbox)
    return p

  def _make_help_thread(self, event):
    isClick = True if event else False
    # 使用线程 填充 帮助标签, 加快启动速度
    t = Thread(target = self._set_manual_view,
               args = (self._page5_manual_view, isClick))
    # t.daemon = True   # 死了也会存在
    t.start()

  def _set_manual_view(self, view, isClick):
    '''
    不用多线程能行嘛? 想要获得输出结果就一定会有阻塞的可能!
    https://www.jianshu.com/p/11090e197648
    https://wiki.gnome.org/Projects/PyGObject/Threading
    needle注: 跟sqlamp-gtk版本的代码可不一样, 操作的共享对象有两个,
              不过原则一样, 所有对共用对象的操作都要用CallAfter
              这样写是不是很丑?
    '''
    if isClick:
      wx.CallAfter(self._get_sqlmap_path_btn.Disable)
      wx.CallAfter(view.SetValue, '')

    byte_coding = 'utf8' if IS_POSIX else 'gbk'

    # _manual_hh = '/home/needle/bin/output_interval.sh'
    # win下的sqlmap -hh有Enter阻塞
    _manual_hh = 'echo y|%s -hh' % self._handlers.get_sqlmap_path()
    try:
      _subprocess = Popen(_manual_hh, stdout=PIPE, stderr=STDOUT, bufsize=1, shell = True)

      for _an_bytes_line_tmp in iter(_subprocess.stdout.readline, b''):
        wx.CallAfter(view.write, _an_bytes_line_tmp.decode(byte_coding))
      _subprocess.wait()
    except FileNotFoundError as e:
      wx.CallAfter(view.write, str(e))
    finally:
      _subprocess.stdout.close()

    if isClick:
      # 用gtk时, 如果view不在屏幕上可见, ShowPosition会报错
      wx.CallAfter(view.ShowPosition, 0)
      wx.CallAfter(self._get_sqlmap_path_btn.Enable)
      wx.CallAfter(self._get_sqlmap_path_btn.SetFocus)

  def build_page6(self, parent):
    p = Panel(parent)
    vbox = BoxSizer(VERTICAL)

    _about_str = '''
    1. VERSION: 0.2
       2019-05-12 16:58
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
