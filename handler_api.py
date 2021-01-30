#!/usr/bin/env python3
#
# 2018-08-29 15:34:10

import ast
from os import name as OS_NAME
import requests

from widgets import wx, btn, st

IS_POSIX = True if OS_NAME == 'posix' else False
QUOTE = "'%s'" if OS_NAME == 'posix' else '"%s"'  # dos下只能用双引号
EVT_BUTTON = wx.EVT_BUTTON


class Api(object):
  def __init__(self, topwindow, m):
    '''
    topwindow: sqlmap_wx.Window
    m: model.Model
    '''
    self.w = topwindow
    self.m = m

  def task_new(self, event):
    '''
    rest api获取自: https://github.com/PyxYuYu/MyBlog/issues/69
    @get("/task/new") 创建新任务
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      try:
        _resp = requests.get('http://%s/task/new' % _host,
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          self._task_view_append('%s: 创建成功.' % _resp['taskid'])
      except Exception as e:
        self._task_view_append(e)

  def admin_list(self, event):
    '''
    @get("/admin/<taskid>/list") 查看所有任务，并显示运行状态
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _token = self.get_tc_value(self.m._page4_admin_token_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host and _token:
      try:
        _resp = requests.get('http://%s/admin/%s/list' % (_host, _token),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        # print(_resp)
        if _resp['success']:
          self._task_view_append('总任务数: %s' % _resp['tasks_num'])
          p = self.w._api_admin_list_rows
          vbox = p.GetSizer()
          # 清空之前的任务列表
          vbox.Clear(delete_windows = True)
          # 填充任务列表
          _id = 0
          for _taskid, _status in _resp['tasks'].items():
            _a_task_row = wx.BoxSizer()

            _task_del_btn = btn(p, label = '删除', style = wx.BU_EXACTFIT)
            _task_del_btn.Bind(EVT_BUTTON,
              lambda evt, row = _a_task_row, tid = _taskid:
                self.task_delete(row, tid))

            _scan_kill_btn = btn(p, label = '杀死', style = wx.BU_EXACTFIT)
            _scan_kill_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.scan_kill(tid))

            _scan_stop_btn = btn(p, label = '停止', style = wx.BU_EXACTFIT)
            _scan_stop_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.scan_stop(tid))

            _scan_start_btn = btn(p, label = '启动', style = wx.BU_EXACTFIT)
            _scan_start_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.scan_start(tid))

            _scan_data_btn = btn(p, label = 'data', style = wx.BU_EXACTFIT)
            _scan_data_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.scan_data(tid))

            _scan_log_btn = btn(p, label = 'log', style = wx.BU_EXACTFIT)
            _scan_log_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.scan_log(tid))

            _option_list_btn = btn(p, label = '所有选项', style = wx.BU_EXACTFIT)
            _option_list_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.option_list(tid))

            _option_get_btn = btn(p, label = '选项:', style = wx.BU_EXACTFIT)
            _option_get_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.option_get(tid))

            _option_set_btn = btn(p, label = '设置:', style = wx.BU_EXACTFIT)
            _option_set_btn.Bind(EVT_BUTTON,
              lambda evt, tid = _taskid:
                self.option_set(tid))

            _id += 1
            _a_task_row.Add(st(p, label = '%s. %s' % (_id, _taskid)), flag = wx.ALIGN_CENTER)
            _a_task_row.Add(st(p, label = '(%s)' % _status), flag = wx.ALIGN_CENTER)
            _a_task_row.Add(_task_del_btn, flag = wx.EXPAND)
            _a_task_row.Add(_scan_kill_btn, flag = wx.EXPAND)
            _a_task_row.Add(_scan_stop_btn, flag = wx.EXPAND)
            _a_task_row.Add(_scan_start_btn, flag = wx.EXPAND)
            _a_task_row.Add(st(p, label = '查看:('), flag = wx.ALIGN_CENTER)
            _a_task_row.Add(_scan_data_btn, flag = wx.EXPAND)
            _a_task_row.Add(_scan_log_btn, flag = wx.EXPAND)
            _a_task_row.Add(_option_list_btn, flag = wx.EXPAND)
            _a_task_row.Add(_option_get_btn, flag = wx.EXPAND)
            _a_task_row.Add(st(p, label = ')'), flag = wx.ALIGN_CENTER)
            _a_task_row.Add(_option_set_btn, flag = wx.EXPAND)

            vbox.Add(_a_task_row, flag = wx.EXPAND)

          vbox.Layout()
          p.SetupScrolling()
      except Exception as e:
        self._task_view_append(e)
    else:
        self._task_view_append('需要填写API server和admin token.')

  def option_list(self, taskid):
    '''
    @get("/option/<taskid>/list") 获取指定任务的options
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      try:
        _resp = requests.get('http://%s/option/%s/list' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          for _key, _value in _resp['options'].items():
            if _value:
              self._task_view_append('%s: %s' % (_key, _value))
      except Exception as e:
        self._task_view_append(e)

  def option_get(self, taskid):
    '''
    @post("/option/<taskid>/get") 获取指定任务的option(s)
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _opts_text = self.get_tc_value(self.m._page4_option_get_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    _options = {}
    for _tmp in _opts_text.split():
      _options[_tmp] = None
    if _host and _options:
      _mesg = '%s:\n' % taskid
      try:
        _headers = {'Content-Type': 'application/json'}
        _resp = requests.post('http://%s/option/%s/get' % (_host, taskid),
                              json = _options,
                              headers = _headers,
                              auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          if _resp['options'].items():
            for _key, _value in _resp['options'].items():
              _mesg += '%s: %s, ' % (_key, _value)
          else:
            _mesg += 'None'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg.strip())

  def option_set(self, taskid):
    '''
    @post("/option/<taskid>/set") 设置指定任务的option(s)
    Warning: any option can be set, even a invalid option which
             is unable to remove, except deleting the task.
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _buffer_text = self.get_tc_value(self.m._page4_option_set_view)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    try:
      _json = ast.literal_eval(_buffer_text)
    except Exception as e:
      _json = str(e)

    _mesg = '%s: ' % taskid
    if _json and isinstance(_json, dict):
      if _host:
        try:
          _headers = {'Content-Type': 'application/json'}
          # data, json参数都要求是字典类型, 而非字符串
          # 另外, 字典的格式比json的宽松(json不能使用单引号, 不能多个逗号)
          _resp = requests.post('http://%s/option/%s/set' % (_host, taskid),
                                json = _json,
                                headers = _headers,
                                auth = (_username, _password))
          if not _resp:
            _resp.raise_for_status()

          _resp = _resp.json()
          if _resp['success']:
            _mesg += '设置成功'
        except Exception as e:
          _mesg += str(e)
    else:
      _mesg += '需要一个有效的python dict'

    self._task_view_append(_mesg)

  def admin_flush(self, event):
    '''
    @get("/admin/<taskid>/flush") 删除所有任务
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _token = self.get_tc_value(self.m._page4_admin_token_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host and _token:
      try:
        _resp = requests.get('http://%s/admin/%s/flush' % (_host, _token),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          self.w._api_admin_list_rows.GetSizer().Clear(delete_windows = True)
          self._task_view_append('清空全部任务: 成功')
      except Exception as e:
        self._task_view_append(e)

  def task_delete(self, row, taskid):
    '''
    @get("/task/<taskid>/delete") 删除指定任务
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      try:
        _resp = requests.get('http://%s/task/%s/delete' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          # TODO, 要两步哈! 要查下是否真的成功了!
          row.Clear(delete_windows = True)
          self.w._api_admin_list_rows.GetSizer().Remove(row)
          self._task_view_append('%s: 删除成功' % taskid)
      except Exception as e:
        self._task_view_append(e)

  def scan_start(self, taskid):
    '''
    @post("/scan/<taskid>/start") 指定任务 开始扫描
    要求发送json, 会执行/option/<taskid>/set
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _headers = {'Content-Type': 'application/json'}
        _resp = requests.post('http://%s/scan/%s/start' % (_host, taskid),
                              json = {},
                              headers = _headers,
                              auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          _mesg = '%sengineid: %s' % (_mesg, _resp['engineid'])
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)

      self._task_view_append(_mesg)

  def scan_stop(self, taskid):
    '''
    @get("/scan/<taskid>/stop") 指定任务 停止扫描
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/stop' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          _mesg += 'ok, stoped.'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg)

  def scan_kill(self, taskid):
    '''
    @get("/scan/<taskid>/kill") kill -9 指定任务
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      _mesg = '%s: ' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/kill' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          _mesg += 'ok, killed.'
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)

      self._task_view_append(_mesg)

  def scan_data(self, taskid):
    '''
    @get("/scan/<taskid>/data") 查看指定任务的扫描数据,
                                data若有内容说明存在注入
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      _mesg = '%s:\n' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/data' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        # print(_resp)    # _resp['data'], _resp['error'] are list
        if _resp['success']:
          del[_resp['success']]
          _mesg = '%s%s' % (_mesg, _resp)
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg)

  def scan_log(self, taskid):
    '''
    @get("/scan/<taskid>/log") 查看指定任务的扫描日志
    '''
    _host = self.get_tc_value(self.m._page4_api_server_entry)
    _username = self.get_tc_value(self.m._page4_username_entry)
    _password = self.get_tc_value(self.m._page4_password_entry)
    if _host:
      _mesg = '%s:\n' % taskid
      try:
        _resp = requests.get('http://%s/scan/%s/log' % (_host, taskid),
                             auth = (_username, _password))
        if not _resp:
          _resp.raise_for_status()

        _resp = _resp.json()
        if _resp['success']:
          _logs = ''
          for _tmp in _resp['log']:
            _log = '%s %s: %s\n' % (_tmp['time'], _tmp['level'], _tmp['message'])
            _logs = ''.join((_logs, _log))
          if _logs:
            _mesg += _logs.strip()
          else:
            _mesg += "没有log."
        else:
          _mesg += _resp['message']
      except Exception as e:
        _mesg += str(e)
      self._task_view_append(_mesg)

  def get_tc_value(self, textctrl):
    return textctrl.GetValue().strip()

  def _task_view_append(self, output):
    _task_view = self.m._page4_task_view

    _task_view.write('%s\n' % output)

    _task_view.SetFocus()
    _mark = _task_view.GetInsertionPoint()
    wx.CallAfter(_task_view.ShowPosition, _mark)

