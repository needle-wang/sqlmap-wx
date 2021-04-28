#!/usr/bin/env python3
#
# 2019-05-05 21:09:49
import string
import wx
import wx.lib.agw.flatnotebook as FNB
from wx.lib.scrolledpanel import ScrolledPanel


class Notebook(FNB.FlatNotebook):
  def __init__(self, *args, **kwargs):
    # emulate the old wx.Notebook style
    _bookStyle = FNB.FNB_NO_X_BUTTON | FNB.FNB_NO_NAV_BUTTONS | FNB.FNB_NODRAG
    # 标签不能有焦点, 不然win7下ScrolledPanel不响应滚轮,
    # ScrolledPanel needs focus inside to response wheel
    # use ribbon style
    _bookStyle |= FNB.FNB_NO_TAB_FOCUS | FNB.FNB_RIBBON_TABS
    super().__init__(*args, agwStyle=_bookStyle, **kwargs)
    self.SetBackgroundColour(wx.WHITE)


class CheckBox(wx.CheckBox):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # 一步构造, 不能调用Create
    if args or kwargs:
      self._set_win_color()

  def Create(self, *args, **kwargs):
    # Create方法用于两步构造
    super().Create(*args, **kwargs)
    self._set_win_color()

  def _set_win_color(self):
    # only for win, 背景(240, 240, 240, 255)是灰色, 却要重新设一遍前景才能去灰~
    # 侮辱智商! 脑子都搞蒙了
    self.SetForegroundColour(self.GetForegroundColour())

    self.origin_bgcolor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
    self.Bind(wx.EVT_CHECKBOX, self.set_color)

  def set_color(self, event):
    if self.IsChecked():
      # 跟sqlmap-gtk一样: #f6d488
      self.SetBackgroundColour(wx.Colour(246, 212, 136))
    else:
      self.SetBackgroundColour(self.origin_bgcolor)
    # 这里调不调skip无所谓吧~
    if event:
      event.Skip()

  def SetValue(self, state):
    super().SetValue(state)
    self.set_color(None)


class NumCtrl(wx.TextCtrl):
  '''
  https://stackoverflow.com/questions/1369086/is-it-possible-to-limit-textctrl-to-accept-numbers-only-in-wxpython
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.Bind(wx.EVT_CHAR, self.onChar)

  def onChar(self, event):
    keycode = event.GetKeyCode()
    obj = event.GetEventObject()
    val = obj.GetValue()
    # filter unicode characters
    if keycode == wx.WXK_NONE:
      pass
    # allow digits
    elif chr(keycode) in string.digits:
      event.Skip()
    # allow special, non-printable keycodes
    elif chr(keycode) not in string.printable:
      event.Skip()  # allow all other special keycode
    # allow '-' for negative numbers
    elif chr(keycode) == '-':
      # 负号只能是开头
      if '-' not in val:
        obj.SetValue('-' + val)  # 如果是首次输入"-", 则放在开头
        obj.SetInsertionPointEnd()
      else:
        obj.SetValue(val[1:])    # 如果已存在"-", 则去掉
        obj.SetInsertionPointEnd()
    # allow '.' for float numbers
    elif chr(keycode) == '.' and '.' not in val:
      event.Skip()
    return


EVT_BUTTON = wx.EVT_BUTTON
EVT_CHECKBOX = wx.EVT_CHECKBOX

# nb = wx.Notebook  # awful widget, don't use
nb = Notebook
Panel = wx.Panel
StaticBox = wx.StaticBox
SplitterWindow = wx.SplitterWindow
Scroll = ScrolledPanel

btn = wx.Button
cb = CheckBox
cbb = wx.ComboBox
ci = wx.Choice
nc = NumCtrl
sl = wx.Slider
sp = wx.SpinCtrl
st = wx.StaticText
tc = wx.TextCtrl

VERTICAL = wx.VERTICAL
HORIZONTAL = wx.HORIZONTAL

BoxSizer = wx.BoxSizer
GridSizer = wx.GridSizer
StaticBoxSizer = wx.StaticBoxSizer
FlexGridSizer = wx.FlexGridSizer

EXPAND = wx.EXPAND
ALL = wx.ALL
TOP = wx.TOP
BOTTOM = wx.BOTTOM
LEFT = wx.LEFT
RIGHT = wx.RIGHT
ALIGN_RIGHT = wx.ALIGN_RIGHT
ALIGN_CENTER = wx.ALIGN_CENTER

SizerFlags = wx.SizerFlags


def main():
  pass


if __name__ == '__main__':
  main()
