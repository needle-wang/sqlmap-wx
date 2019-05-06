#!/usr/bin/env python3
#
# 2019年 05月 05日 星期日 14:50:15 CST

import wx
from page1_notebook import Page1Notebook
from handlers import Handler
from widgets import TextCtrl


class Window(wx.Frame):
  def __init__(self, parent):
    super().__init__(parent, title = 'sqlmap-wx', size = (300, 400))
    self.Bind(wx.EVT_MENU, self.onExit)
    accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
                                     (wx.ACCEL_CTRL, ord('W'), wx.ID_EXIT)])
    self.SetAcceleratorTable(accel_tbl)

    self._handlers = Handler(self)
    self.initUI()

  # @profile
  def initUI(self):
    vbox = wx.BoxSizer(wx.VERTICAL)
    self.build_page_target()

    _main_notebook = wx.Notebook(self)
    page1 = self.build_page1(_main_notebook)
    # page2 = self.build_page2(_main_notebook)
    # page3 = self.build_page3(_main_notebook)
    # page4 = self.build_page4(_main_notebook)
    # page5 = self.build_page5(_main_notebook)
    # page6 = self.build_page6(_main_notebook)

    _main_notebook.AddPage(page1, '选项区(&1)')
    # _main_notebook.AddPage(page2, '输出区(&2)')
    # _main_notebook.AddPage(page3, '日志区(&3)')
    # _main_notebook.AddPage(page4, 'API区(&4)')
    # _main_notebook.AddPage(page5, '选项区(&5)')
    # _main_notebook.AddPage(page6, '帮助(&6)')

    vbox.Add(self._target_notebook, flag = wx.EXPAND)
    vbox.Add(_main_notebook, proportion = 1, flag = wx.EXPAND)
    self.SetSizerAndFit(vbox)

  def clear_all_entry(self, event):
    m = self._notebook
    for _i in dir(m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(m, _i)
        if isinstance(_tmp_entry, wx.TextCtrl):
          _tmp_entry.SetValue('')

  def unselect_all_ckbtn(self, event):
    m = self._notebook
    for _i in dir(m):
      if _i.endswith('ckbtn'):
        _tmp_ckbtn = getattr(m, _i)
        if isinstance(_tmp_ckbtn, wx.CheckBox):
          _tmp_ckbtn.SetValue(False)
    for _i in m._enum_area_opts_ckbtns:
      for _j in _i:
        _j.SetValue(False)

  def onExit(self, event):
    # https://stackoverflow.com/questions/49454737/how-can-i-exit-out-of-a-wxpython-application-cleanly
    wx.CallAfter(self.Close)

  def build_page6(self, parent):
    p = wx.Panel(parent)

    return p

  def build_page5(self, parent):
    p = wx.Panel(parent)

    return p

  def build_page4(self, parent):
    p = wx.Panel(parent)

    return p

  def build_page3(self, parent):
    p = wx.Panel(parent)

    return p

  def build_page2(self, parent):
    p = wx.Panel(parent)

    return p

  def build_page1(self, parent):
    p = wx.Panel(parent)
    p.SetBackgroundColour(wx.LIGHT_GREY)
    vbox = wx.BoxSizer(wx.VERTICAL)

    # sqlmap命令语句
    cmd_area = wx.StaticBoxSizer(wx.VERTICAL, p, 'A.收集选项 的结果显示在这:')
    _cmd_area = cmd_area.GetStaticBox()

    self._cmd_entry = TextCtrl(_cmd_area)

    cmd_area.Add(self._cmd_entry, flag = wx.EXPAND)

    # 主构造区
    self._notebook = Page1Notebook(p)

    # 构造与执行
    hbox = wx.GridSizer(1, 4, 0, 0)
    _build_button = wx.Button(p, label = 'A.收集选项(&A)')
    _build_button.Bind(wx.EVT_BUTTON, self._handlers.build_all)
    # 用于改善ui的使用体验
    _unselect_all_btn = wx.Button(p, label = '反选所有复选框(&S)')
    _unselect_all_btn.Bind(wx.EVT_BUTTON, self.unselect_all_ckbtn)
    _clear_all_entry = wx.Button(p, label = '清空所有输入框(&D)')
    _clear_all_entry.Bind(wx.EVT_BUTTON, self.clear_all_entry)
    _run_button = wx.Button(p, label = 'B.开始(&F)')
    _run_button.Bind(wx.EVT_BUTTON, self._handlers.run_cmdline)

    hbox.AddMany((_build_button, _unselect_all_btn, _clear_all_entry, _run_button))

    vbox.Add(cmd_area, flag = wx.EXPAND)
    vbox.Add(self._notebook, proportion = 1, flag = wx.EXPAND)
    vbox.Add(hbox, flag = wx.EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page_target(self):
    # 正确的高度!
    # self.a = wx.Notebook(self, size = (400, 68))
    # b = wx.TextCtrl(a, size = (-1, 36))
    self._target_notebook = wx.Notebook(self, size = (-1, 68))
    _tc = TextCtrl(self._target_notebook)

    self._target_notebook.AddPage(_tc, '目标url')


def main():
  app = wx.App()

  win = Window(None)
  win.Centre()
  win.Show()

  app.MainLoop()


if __name__ == '__main__':
  main()
