#!/usr/bin/env python3
# encoding: utf-8
#
# 2019年 05月 05日 星期日 21:09:49 CST

import wx


class Panel(wx.Panel):
  def __init__(self, *args, **kw):
    super().__init__(*args, **kw)
    self.szr = wx.BoxSizer(wx.VERTICAL)


class TextCtrl(wx.TextCtrl):
  def __init__(self, *args, **kw):
    super().__init__(*args, **kw)

    # self.SetSizeHints((168, 36))
    self.SetSize(168, 36)


def main():
  pass


if __name__ == '__main__':
  main()
