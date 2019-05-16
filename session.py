#!/usr/bin/env python3
#
# 2018年 11月 09日 星期五 15:06:50 CST

from configparser import ConfigParser
from widgets import cb, tc

LAST_TMP = 'last.tmp'


class Session(object):
  def __init__(self, w):
    '''
    w: sqlmap_wx.Window
    m: opts_wx.Notebook
    '''
    self.w = w
    self.m = w._notebook

    self._cfg = ConfigParser()
    # https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
    # 所有选项的key, 都会传给optionxform(), 该方法会将key转成小写!
    # 将optionxform替换成str, 表示不做转换
    self._cfg.optionxform = str

  def save_to_tmp(self):
    self._save_to_tmp_target()
    self._save_to_tmp_ckbtn()
    self._save_to_tmp_entry()

    with open(LAST_TMP, 'w') as f:
      self._cfg.write(f)

  def load_from_tmp(self):
    # 如果文件不存在, 不会报错
    self._cfg.read(LAST_TMP, 'utf8')

    self._load_from_tmp_target()
    self._load_from_tmp_ckbtn()
    self._load_from_tmp_entry()

  def _save_to_tmp_target(self):
    if self._cfg.has_section('Target'):
      self._cfg.remove_section('Target')

    self._cfg.add_section('Target')

    _tmp_url = self.w._url_combobox.GetValue().strip()

    if _tmp_url:
      self._cfg['Target']['_url_combobox'] = _tmp_url

  def _save_to_tmp_entry(self):
    if self._cfg.has_section('Entry'):
      self._cfg.remove_section('Entry')

    self._cfg.add_section('Entry')

    for _i in dir(self.m):
      if _i.endswith('entry'):
        _tmp_entry = getattr(self.m, _i)

        if isinstance(_tmp_entry, tc) and _tmp_entry.GetValue().strip():
          self._cfg['Entry'][_i] = _tmp_entry.GetValue()

  def _save_to_tmp_ckbtn(self):
    if self._cfg.has_section('CheckButton'):
      self._cfg.remove_section('CheckButton')

    self._cfg.add_section('CheckButton')

    _checked = []
    for _i in dir(self.m):
      if _i.endswith('ckbtn'):
        _tmp_ckbtn = getattr(self.m, _i)

        if isinstance(_tmp_ckbtn, cb) and _tmp_ckbtn.IsChecked():
          _checked.append(_i)

    self._cfg['CheckButton']['checked'] = ','.join(_checked)

  def _load_from_tmp_target(self):
    if not self._cfg.has_section('Target'):
      self._cfg.add_section('Target')

    for _i in self._cfg.options('Target'):
      if _i == '_url_combobox':
        # 不去手动改LAST_TMP, self.m就肯定有_i属性了
        _tmp_url = self.w._url_combobox

        if self._cfg['Target'][_i]:
          _tmp_url.SetValue(self._cfg['Target'][_i])

      break

  def _load_from_tmp_ckbtn(self):
    if not self._cfg.has_section('CheckButton'):
      self._cfg.add_section('CheckButton')

    try:
      _checked = self._cfg['CheckButton']['checked'].split(',')
      for _i in _checked:
        if _i:  # _i可能为''
          # 不去手动改LAST_TMP, self.m就肯定有_i属性了
          _tmp_ckbtn = getattr(self.m, _i)
          _tmp_ckbtn.SetValue(True)
        else:  # _checked = [''], 则使用默认值
          pass
    except KeyError as e:
      # 如果没有checked项, 则pass
      pass

  def _load_from_tmp_entry(self):
    if not self._cfg.has_section('Entry'):
      self._cfg.add_section('Entry')

    for _i in self._cfg.options('Entry'):
      # 不去手动改LAST_TMP, self.m就肯定有_i属性了
      _tmp_entry = getattr(self.m, _i)

      if isinstance(_tmp_entry, tc) and self._cfg['Entry'][_i]:
        # print(type(self._cfg['Entry'][_i]))
        _tmp_entry.SetValue(self._cfg['Entry'][_i])


def main():
  pass


if __name__ == '__main__':
  main()
