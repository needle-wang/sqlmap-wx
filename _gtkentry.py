#!/usr/bin/env python3
#
# 2019-05-05 17:34:08

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as g

win = g.Window()
win.connect('destroy', lambda x: g.main_quit())

a = g.Entry()
win.add(a)

print(a.get_allocation().width, a.get_allocation().height)
win.show_all()
print(a.get_allocation().width, a.get_allocation().height)

g.main()
