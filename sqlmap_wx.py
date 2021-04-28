#!/usr/bin/env python3
#
# 2019-05-05 14:50:15

from subprocess import Popen, PIPE, STDOUT
from threading import Thread

from widgets import wx, Panel, Scroll, SplitterWindow, btn, cb, nb, st, tc
from widgets import BoxSizer, GridSizer, StaticBoxSizer, SizerFlags, EVT_BUTTON
from widgets import VERTICAL, EXPAND, ALL, TOP, BOTTOM, LEFT, RIGHT, ALIGN_CENTER

from model import Model
from opts_wx import Notebook
from handlers import Handler, IS_POSIX
from session import Session
from tooltips import Widget_Mesg as INIT_MESG


class Window(wx.Frame):
  def __init__(self, parent):
    super().__init__(parent, title = 'sqlmap-wx')
    self.SetIcon(wx.Icon('static/title.ico'))

    self.m = Model()
    self._handlers = Handler(self, self.m)  # 需要先设置handler, Bind需要它
    self.initUI()
    self.make_accelerators()  # 要先初始化完成后, 才能设全局键
    # add tooltips, placeholders
    INIT_MESG(self.m)

    self.session = Session(self.m)
    self.session.load_from_tmp()

  # @profile
  def initUI(self):
    p = Panel(self)

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

    vbox = BoxSizer(VERTICAL)
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

    main_note_ks = list('1234H')
    for i in range(len(main_note_ks)):
      pageid = self.main_notebook.GetPage(i).GetId()

      self.accel_entries.append((wx.ACCEL_ALT, ord(main_note_ks[i]), pageid))
      self.Bind(
        wx.EVT_MENU,
        lambda evt, page = i: self.main_notebook.SetSelection(page),
        id = pageid)

    _note_keys = list('QWERTY')
    for i in range(len(_note_keys)):
      pageid = self._notebook.GetPage(i).GetId()

      self.accel_entries.append((wx.ACCEL_ALT, ord(_note_keys[i]), pageid))
      self.Bind(
        wx.EVT_MENU,
        lambda evt, page = i:
          self._notebook.SetSelection(page)
            if self.main_notebook.GetSelection() == 0 else evt.Skip(),
        id = pageid)
    # win下, 若焦点没按钮上, 则不响应mnemonic, 只能在这里实现了
    _btn_keys = list('ASDF')
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
    https://stackoverflow.com/questions/9765718/wxpython-trigger-checkbox-event-while-setting-its-value-in-the-code
    '''
    # 手动emit事件
    # evt = wx.CommandEvent(wx.EVT_CHECKBOX.typeId)
    # evt.SetEventObject(cb)  # 将该evt绑定给cb
    # wx.PostEvent(cb, evt)
    evt = wx.PyCommandEvent(EVT_BUTTON.typeId, btn.GetId())
    # print(evt)
    wx.PostEvent(btn, evt)

  def clear_all_entry(self, event):
    m = self.m
    for _i in dir(m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(m, _i)
        if isinstance(_tmp_entry, tc) and _tmp_entry is not m.sqlmap_path_entry:
          _tmp_entry.SetValue('')

    self._notebook.SetFocus()

  def unselect_all_ckbtn(self, event):
    m = self.m
    for _i in dir(m):
      if _i.endswith('ckbtn'):
        _tmp_ckbtn = getattr(m, _i)
        if isinstance(_tmp_ckbtn, cb) and _tmp_ckbtn.IsChecked():
          _tmp_ckbtn.SetValue(False)
    for _i in m._enum_area_opts_ckbtns:
      for _j in _i:
        if _j.IsChecked():
          _j.SetValue(False)

    self._notebook.SetFocus()

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
    try:
      self.session.save_to_tmp()
    except Exception as e:
      raise e
    finally:
      event.Skip()

  def build_target_notebook(self, parent):
    m = self.m

    m._url_combobox.Create(parent, choices = ['http://www.site.com/vuln.php?id=1'])   # style = wx.CB_DROPDOWN

    p2 = Panel(parent)
    hbox2 = BoxSizer()
    m._burp_logfile.Create(p2)
    m._burp_logfile_chooser.Create(p2, label = '打开')
    m._burp_logfile_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._burp_logfile]:
        self._handlers.set_file_entry_text(evt, data))

    hbox2.Add(m._burp_logfile, proportion = 1, flag = EXPAND)
    hbox2.Add(m._burp_logfile_chooser, flag = EXPAND)
    p2.SetSizer(hbox2)

    p3 = Panel(parent)
    hbox3 = BoxSizer()
    m._request_file.Create(p3)
    m._request_file_chooser.Create(p3, label = '打开')
    m._request_file_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._request_file]:
        self._handlers.set_file_entry_text(evt, data))

    hbox3.Add(m._request_file, proportion = 1, flag = EXPAND)
    hbox3.Add(m._request_file_chooser, flag = EXPAND)
    p3.SetSizer(hbox3)

    p4 = Panel(parent)
    hbox4 = BoxSizer()
    m._bulkfile.Create(p4)
    m._bulkfile_chooser.Create(p4, label = '打开')
    m._bulkfile_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._bulkfile]:
        self._handlers.set_file_entry_text(evt, data))

    hbox4.Add(m._bulkfile, proportion = 1, flag = EXPAND)
    hbox4.Add(m._bulkfile_chooser, flag = EXPAND)
    p4.SetSizer(hbox4)

    p5 = Panel(parent)
    hbox5 = BoxSizer()
    m._configfile.Create(p5)
    m._configfile_chooser.Create(p5, label = '打开')
    m._configfile_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._configfile]:
        self._handlers.set_file_entry_text(evt, data))

    hbox5.Add(m._configfile, proportion = 1, flag = EXPAND)
    hbox5.Add(m._configfile_chooser, flag = EXPAND)
    p5.SetSizer(hbox5)

    m._google_dork.Create(parent)
    m._direct_connect.Create(parent,
                             value = 'mysql://USER:PASSWORD@DBMS_IP:DBMS_PORT/DATABASE_NAME or '
                                     'access://DATABASE_FILEPATH')

    parent.AddPage(m._url_combobox, '目标url')
    parent.AddPage(p2, 'burp日志')
    parent.AddPage(p3, 'HTTP请求')
    parent.AddPage(p4, 'BULKFILE')
    parent.AddPage(p5, 'ini文件')
    parent.AddPage(m._google_dork, 'GOOGLEDORK')
    parent.AddPage(m._direct_connect, '-d DIRECT')

  def build_page1(self, parent):
    p = Panel(parent)
    m = self.m

    # sqlmap命令语句
    cmd_area = StaticBoxSizer(VERTICAL, p, 'A.收集选项 的结果显示在这:')
    _cmd_area = cmd_area.GetStaticBox()

    m._cmd_entry.Create(_cmd_area)

    cmd_area.Add(m._cmd_entry, flag = EXPAND)

    # 主构造区
    self._notebook = Notebook(p, m, self._handlers)

    # 构造与执行
    self.btn_grid = GridSizer(1, 4, 0, 0)

    _build_button = btn(p, label = 'A.收集选项(A)')
    _unselect_all_btn = btn(p, label = '反选所有复选框(S)')
    _clear_all_entry = btn(p, label = '清空所有输入框(D)')

    _build_button.Bind(EVT_BUTTON, self._handlers.build_all)
    _unselect_all_btn.Bind(EVT_BUTTON, self.unselect_all_ckbtn)
    _clear_all_entry.Bind(EVT_BUTTON, self.clear_all_entry)

    _run_button = btn(p, label = 'B.开始(F)')
    _run_button.Bind(EVT_BUTTON, self._handlers.run_cmdline)

    self.btn_grid.Add(_build_button, flag = ALIGN_CENTER)
    self.btn_grid.Add(_unselect_all_btn, flag = ALIGN_CENTER)
    self.btn_grid.Add(_clear_all_entry, flag = ALIGN_CENTER)
    self.btn_grid.Add(_run_button, flag = ALIGN_CENTER)

    vbox = BoxSizer(VERTICAL)
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
    m = self.m

    # 多行文本框的默认size太小了
    # 默认高度太低, 不指定个高度, 会报 滚动条相关的size 警告
    m._page3_log_view.Create(p,
                             size = (-1, 300),
                             style = wx.TE_MULTILINE | wx.TE_READONLY)
    self._handlers.clear_log_view_buffer(None)

    grid = GridSizer(1, 3, 0, 0)
    m._page3_read_target_btn.Create(p, label = '查看target文件')
    m._page3_clear_btn.Create(p, label = '清空(&C)')
    m._page3_read_log_btn.Create(p, label = '查看log文件')

    m._page3_read_target_btn.Bind(EVT_BUTTON, self._handlers.read_target_file)
    m._page3_clear_btn.Bind(EVT_BUTTON, self._handlers.clear_log_view_buffer)
    m._page3_read_log_btn.Bind(EVT_BUTTON, self._handlers.read_log_file)

    grid.Add(m._page3_read_target_btn, flag = ALIGN_CENTER)
    grid.Add(m._page3_clear_btn, flag = ALIGN_CENTER)
    grid.Add(m._page3_read_log_btn, flag = ALIGN_CENTER)

    vbox = BoxSizer(VERTICAL)
    vbox.Add(m._page3_log_view, proportion = 1, flag = EXPAND | ALL, border = 10)
    vbox.Add(grid, flag = EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page4(self, parent):
    p = Panel(parent)
    m = self.m

    border = SizerFlags().Border(LEFT | RIGHT, 5).Align(ALIGN_CENTER)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5).Align(ALIGN_CENTER)

    row1, row2 = (BoxSizer() for _ in range(2))
    m._page4_api_server_label.Create(p, label = 'REST-JSON API server:')
    m._page4_api_server_entry.Create(p, value = '127.0.0.1:8775')
    m._page4_admin_token_label.Create(p, label = 'Admin (secret) token:')
    m._page4_admin_token_entry.Create(p)
    m._page4_admin_token_entry.SetMaxLength(32)
    row1.Add(m._page4_api_server_label, border)
    row1.Add(m._page4_api_server_entry, proportion_border)
    row1.Add(m._page4_admin_token_label, border)
    row1.Add(m._page4_admin_token_entry, proportion_border)

    m._page4_task_new_btn.Create(p, label = '创建任务')
    m._page4_admin_list_btn.Create(p, label = '显示任务')
    m._page4_admin_flush_btn.Create(p, label = '删除所有任务')
    m._page4_clear_task_view_btn.Create(p, label = '清空反馈的结果')
    m._page4_username_label.Create(p, label = '用户名:')
    m._page4_username_entry.Create(p)
    m._page4_password_label.Create(p, label = '密码:')
    m._page4_password_entry.Create(p)

    _arrow_down = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_BUTTON)
    m._page4_admin_list_btn.SetBitmap(_arrow_down, dir = RIGHT)

    m._page4_task_new_btn.Bind(EVT_BUTTON, self._handlers.api.task_new)
    m._page4_admin_list_btn.Bind(EVT_BUTTON, self._handlers.api.admin_list)
    m._page4_admin_flush_btn.Bind(EVT_BUTTON, self._handlers.api.admin_flush)
    m._page4_clear_task_view_btn.Bind(EVT_BUTTON, self._handlers.clear_task_view_buffer)

    row2.Add(m._page4_task_new_btn, border)
    row2.Add(m._page4_admin_list_btn, border)
    row2.Add(m._page4_admin_flush_btn, border)
    row2.Add(m._page4_clear_task_view_btn, border)
    row2.Add(m._page4_username_label, flag = ALIGN_CENTER | LEFT, border = 200)
    row2.Add(m._page4_username_entry, proportion_border)
    row2.Add(m._page4_password_label, border)
    row2.Add(m._page4_password_entry, proportion_border)

    row3 = SplitterWindow(p, style = wx.SP_LIVE_UPDATE | wx.BORDER_SUNKEN)
    # 不能放在SplitVertically后面, 不然gravity会无效
    # row3.SetSashGravity(0.5)
    row3.SetMinimumPaneSize(400)

    lpane = Scroll(row3)
    self._api_admin_list_rows = lpane

    lpane.SetSizer(BoxSizer(VERTICAL))

    rpane = Panel(row3)
    _rbox = BoxSizer(VERTICAL)

    m._page4_option_get_entry.Create(rpane, value = 'url risk level')
    _page4_option_set_view_tip = st(rpane, label = 'check optiondict.py of sqlmap about options.')
    _options_example = ("{\n"
                        "  'url': 'http://www.site.com/vuln.php?id=1',\n"
                        "  'level': 1, 'risk': 1,\n\n"
                        "}\n")
    m._page4_option_set_view.Create(rpane,
                                    value = _options_example,
                                    style = wx.TE_MULTILINE)
    _rbox.Add(m._page4_option_get_entry, flag = EXPAND | ALL, border = 2)
    _rbox.Add(_page4_option_set_view_tip, flag = ALL, border = 2)
    _rbox.Add(m._page4_option_set_view, proportion = 1, flag = EXPAND | ALL, border = 2)
    rpane.SetSizer(_rbox)

    row3.SplitVertically(lpane, rpane)
    # win下, lpane是灰色的, 将row3设下颜色, 又是兼容代码...
    row3.SetBackgroundColour(m._page4_option_set_view.GetBackgroundColour())
    row3.SetSashPosition(lpane.GetMinWidth())

    m._page4_task_view.Create(p, value = 'response result:\n', style = wx.TE_MULTILINE | wx.TE_READONLY)

    vbox = BoxSizer(VERTICAL)
    vbox.Add(row1, flag = EXPAND | ALL, border = 5)
    vbox.Add(row2, flag = EXPAND | ALL, border = 5)
    vbox.Add(row3, proportion = 1, flag = EXPAND | LEFT | RIGHT, border = 10)
    vbox.Add(m._page4_task_view, proportion = 1, flag = EXPAND | ALL, border = 10)
    p.SetSizerAndFit(vbox)
    return p

  def build_page5(self, parent):
    p = Panel(parent)
    m = self.m

    self._get_sqlmap_path_btn = btn(p, label = 'sqlmap -hh')
    self._get_sqlmap_path_btn.Disable()
    # 多行文本框的默认size太小了
    # 默认高度太低, 不指定个高度, gtk会报 滚动条相关的size 警告
    m._page5_manual_view.Create(p,
                                size = (-1, 300),
                                style = wx.TE_MULTILINE | wx.TE_READONLY)

    self._get_sqlmap_path_btn.Bind(
      EVT_BUTTON, lambda evt, view = m._page5_manual_view:
        self._make_help_thread(evt, view))

    self._make_help_thread(None, m._page5_manual_view)

    vbox = BoxSizer(VERTICAL)
    vbox.Add(self._get_sqlmap_path_btn, flag = TOP | LEFT | BOTTOM, border = 10)
    vbox.Add(m._page5_manual_view, proportion = 1, flag = EXPAND | LEFT | RIGHT, border = 10)
    p.SetSizerAndFit(vbox)
    return p

  def _make_help_thread(self, event, view):
    isClick = True if event else False
    # 使用线程 填充 帮助标签, 加快启动速度
    t = Thread(target = self._set_manual_view,
               args = (view, isClick))
    t.daemon = True  # 主线程退出了, 当然守护进程也要退出
    t.start()

  def _set_manual_view(self, view, isClick):
    '''
    不用多线程能行嘛? 想要获得输出结果就一定会有阻塞的可能!
    https://www.jianshu.com/p/11090e197648
    https://wiki.gnome.org/Projects/PyGObject/Threading
    needle注: 操作的共享对象有两个: _get_sqlmap_path_btn, view
              原则一样, 所有对共用对象的操作都要用CallAfter
              这样写是不是很丑?
              另外, 如果没运行完, 主线程就退出了, 会卡住哦, 属于正常
    '''
    if isClick:
      wx.CallAfter(self._get_sqlmap_path_btn.Disable)
      wx.CallAfter(view.SetValue, '')

    byte_coding = 'utf8' if IS_POSIX else 'gbk'

    # _manual_hh = '/home/needle/bin/output_interval.sh'
    # win下的sqlmap -hh有Enter阻塞
    _manual_hh = 'echo y|%s -hh' % self._handlers.get_sqlmap_path()
    try:
      _subp = Popen(_manual_hh, stdout=PIPE, stderr=STDOUT, shell = True)

      for _an_bytes_line_tmp in iter(_subp.stdout.readline, b''):
        wx.CallAfter(view.write,
                     _an_bytes_line_tmp.decode(byte_coding))

      _subp.wait()
      _subp.stdout.close()
    except FileNotFoundError as e:
      wx.CallAfter(view.write, str(e))
    except Exception as e:
      print(e)  # 如果主线程结束太快, 会: AssertionError: No wx.App created yet
    finally:
      wx.CallAfter(self._get_sqlmap_path_btn.Enable)

    if isClick:
      # 用gtk时, 如果view不在屏幕上可见, ShowPosition会报错
      wx.CallAfter(view.ShowPosition, 0)
      wx.CallAfter(self._get_sqlmap_path_btn.SetFocus)

  def build_page6(self, parent):
    p = Panel(parent)

    _version = '0.3.3.1'
    _timestamp = '2021-01-31 05:12:52'

    _url_self = 'https://github.com/needle-wang/sqlmap-wx'
    _url_tutorial1 = 'https://wiki.wxpython.org/'
    _url_tutorial2 = 'http://zetcode.com/wxpython/'
    _url_api = 'https://wxpython.org/Phoenix/docs/html/index.html'
    _url_idea = 'https://github.com/kxcode'
    _about_str = f'''
    1. Website: {_url_self}
       VERSION: {_version}
       {_timestamp}
       required: python3.6+, wxPython4.0+,
                 requests, sqlmap\n
    2. use wxPython4 to recode sqlmap-gtk(driven by PyGObject)
    3. thanks to the idea from sqm(by python2 + tkinter),
                 author: KINGX, {_url_idea}\n
    4. wxPython tutorial: {_url_tutorial1}
                          {_url_tutorial2}
    5. wxPython API: {_url_api}
    '''
    hbox = BoxSizer()
    _page6_about = st(p, label = _about_str)
    # 完全居中!
    hbox.Add(_page6_about, flag = ALIGN_CENTER)

    vbox = BoxSizer(VERTICAL)
    vbox.Add(hbox, proportion = 1, flag = ALIGN_CENTER)
    p.SetSizerAndFit(vbox)
    return p


def main():
  import time
  # import wx.lib.mixins.inspection as wit
  # app = wit.InspectableApp()
  start = time.process_time()
  app = wx.App()
  # --------
  win = Window(None)
  win.Centre()
  win.Show()
  # --------
  end = time.process_time()
  print('loading cost: %.3f Seconds' % (end - start))
  app.MainLoop()


if __name__ == '__main__':
  main()
