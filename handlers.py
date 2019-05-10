#!/usr/bin/env python3
# encoding: utf-8
#
# 2018年 08月 29日 星期三 15:34:10 CST

import ast
import time
from os import environ, name as OS_NAME
# python3.5+
from pathlib import Path
from subprocess import Popen
from urllib.parse import urlparse
import requests
import wx

IS_POSIX = True if OS_NAME == 'posix' else False
QUOTE = "'%s'" if OS_NAME == 'posix' else '"%s"'  # dos下只能用双引号


class Handler(object):
  def __init__(self, frame):
    '''
    frame: wx.Frame
    '''
    self.w = frame
    # m = self.w._notebook不能写在这, 因为还没初始化完, _notebook还不存在

  def build_all(self, event):
    _target = self._get_target()

    self._collect_opts()
    _opts_list = (
      self._setting_opts + self._request_opts +
      self._enumeration_opts + self._file_opts + self._other_opts
    )

    _final_line = _target + ''.join(_opts_list)
    # print(_final_line)
    if _final_line is not None:
      self.w._cmd_entry.SetValue(_final_line.strip())
      self.w._notebook.SetFocus()

  def run_cmdline(self, event):
    self.w._notebook.SetFocus()
    sqlmap_path = 'sqlmap'
    _path = self.w._notebook.sqlmap_path_entry.GetValue().strip()
    if _path:
      sqlmap_path = _path
    _sqlmap_opts = self.w._cmd_entry.GetValue().strip()
    if IS_POSIX:
      _cmdline_str = '/usr/bin/env xterm -hold -e %s %s' % (sqlmap_path, _sqlmap_opts)
    else:
      _cmdline_str = 'start cmd /k %s %s' % (sqlmap_path, _sqlmap_opts)

    # self.w.main_notebook.SetSelection(1)
    # print(_cmdline_str)
    Popen(_cmdline_str, shell = True)

  def set_file_entry_text(self, event, data):
    '''
    data: [file_entry, 'title of chooser']
    '''
    if len(data) > 1:   # 选择目录
      dialog = wx.DirDialog(self.w, message=data[1])
    else:
      dialog = wx.FileDialog(self.w, message="选择文件")

    with dialog:
      if dialog.ShowModal() == wx.ID_OK:
        data[0].SetValue(dialog.GetPath())
        data[0].SetFocus()

  def clear_log_view_buffer(self, event):
    self.w._page3_log_view.SetValue(
      'sqlmap的运行记录都放在这: %s\n' % (Path.home() / '.sqlmap/output'))

  def _get_url_dir(self):
    '''
    return: pathlib.Path
    '''
    _load_url = self.w._url_combobox.GetValue()

    if _load_url:
      if not _load_url.startswith('http'):
        _load_url = 'http://%s' % _load_url

      _load_host = urlparse(_load_url).netloc

      return Path.home() / '.sqlmap/output' / _load_host

  def _log_view_insert(self, file_path):
    '''
    file_path: pathlib.Path
               sqlmap库中dataToOutFile默认utf8写入
    '''
    try:
      with file_path.open(encoding = 'utf8') as _f:
        _line_list_tmp = _f.readlines()
        if _line_list_tmp:
          for _line_tmp in _line_list_tmp:
            self.w._page3_log_view.write(_line_tmp)
        else:
          self.w._page3_log_view.write('%s: 空文件' % file_path)
    except EnvironmentError as e:
      self.w._page3_log_view.write(str(e))
    finally:
      self.w._page3_log_view.write(
        time.strftime('\n%Y-%m-%d %R:%S: ----------我是分割线----------\n',
                      time.localtime()))

      self.w._page3_log_view.SetFocus()
      _mark = self.w._page3_log_view.GetInsertionPoint()
      wx.CallAfter(self.w._page3_log_view.ShowPosition, _mark)

  def read_log_file(self, event):
    _base_dir = self._get_url_dir()

    if _base_dir:
      _log_file_path = _base_dir / 'log'
      self._log_view_insert(_log_file_path)

  def read_target_file(self, event):
    _base_dir = self._get_url_dir()

    if _base_dir:
      _target_file_path = _base_dir / 'target.txt'
      self._log_view_insert(_target_file_path)

  def read_dumped_file(self, event):
    self.w.main_notebook.SetSelection(2)
    m = self.w._notebook

    _base_dir = self._get_url_dir()
    _load_file = m._file_read_area_file_read_entry.GetValue()

    if _base_dir and _load_file:
      # 不能用os.sep, 因为是依据远程OS的sep而定
      # 沿用sqlmap库中的filePathToSafeString函数
      _load_file = (_load_file.replace("/", "_").replace("\\", "_")
                              .replace(" ", "_").replace(":", "_"))

      _dumped_file_path = _base_dir / 'files' / _load_file
      self._log_view_insert(_dumped_file_path)

  def _get_target(self):
    w = self.w
    _pagenum = self.w._target_notebook.GetSelection()
    _target_list = [("-u ", w._url_combobox),
                    ("-l ", w._burp_logfile),
                    ("-r ", w._request_file),
                    ("-m ", w._bulkfile),
                    ("-c ", w._configfile),
                    ("-x ", w._sitemap_url),
                    ("-g ", w._google_dork)]

    _target_tmp = _target_list[_pagenum][1].GetValue().strip()
    if _target_tmp:
      return _target_list[_pagenum][0] + QUOTE % _target_tmp
    else:
      return ''

  def _collect_opts(self):
    m = self.w._notebook

    self._other_opts = [
      self._get_text_only_ckbtn("--check-internet",
                                m._page1_general_check_internet_ckbtn),
      self._get_text_only_ckbtn("--fresh-queries",
                                m._page1_general_fresh_queries_ckbtn),
      self._get_text_only_ckbtn("--flush-session",
                                m._page1_general_flush_session_ckbtn),
      self._get_text_only_ckbtn("--eta",
                                m._page1_general_eta_ckbtn),
      self._get_text_from_entry("--binary-fields=",
                                m._page1_general_binary_fields_ckbtn,
                                m._page1_general_binary_fields_entry),
      self._get_text_only_ckbtn("--forms",
                                m._page1_general_forms_ckbtn),
      self._get_text_only_ckbtn("--parse-errors",
                                m._page1_general_parse_errors_ckbtn),
      self._get_text_only_ckbtn("--cleanup",
                                m._page1_misc_cleanup_ckbtn),
      self._get_text_from_entry("--preprocess=",
                                m._page1_general_preprocess_ckbtn,
                                m._page1_general_preprocess_entry),
      self._get_text_from_entry("--crawl=",
                                m._page1_general_crawl_ckbtn,
                                m._page1_general_crawl_entry),
      self._get_text_from_entry("--crawl-exclude=",
                                m._page1_general_crawl_exclude_ckbtn,
                                m._page1_general_crawl_exclude_entry),
      self._get_text_from_entry("--charset=",
                                m._page1_general_charset_ckbtn,
                                m._page1_general_charset_entry),
      self._get_text_from_entry("--encoding=",
                                m._page1_general_encoding_ckbtn,
                                m._page1_general_encoding_entry),
      self._get_text_from_entry("-s ",
                                m._page1_general_session_file_ckbtn,
                                m._page1_general_session_file_entry),
      self._get_text_from_entry("--output-dir=",
                                m._page1_general_output_dir_ckbtn,
                                m._page1_general_output_dir_entry),
      self._get_text_from_entry("--dump-format=",
                                m._page1_general_dump_format_ckbtn,
                                m._page1_general_dump_format_entry),
      self._get_text_from_entry("--csv-del=",
                                m._page1_general_csv_del_ckbtn,
                                m._page1_general_csv_del_entry),
      self._get_text_from_entry("-t ",
                                m._page1_general_traffic_file_ckbtn,
                                m._page1_general_traffic_file_entry),
      self._get_text_from_entry("--har=",
                                m._page1_general_har_ckbtn,
                                m._page1_general_har_entry),
      self._get_text_from_entry("--save=",
                                m._page1_general_save_ckbtn,
                                m._page1_general_save_entry),
      self._get_text_from_entry("--scope=",
                                m._page1_general_scope_ckbtn,
                                m._page1_general_scope_entry),
      self._get_text_from_entry("--test-filter=",
                                m._page1_general_test_filter_ckbtn,
                                m._page1_general_test_filter_entry),
      self._get_text_from_entry("--test-skip=",
                                m._page1_general_test_skip_ckbtn,
                                m._page1_general_test_skip_entry),
      self._get_text_from_entry("--web-root=",
                                m._page1_misc_web_root_ckbtn,
                                m._page1_misc_web_root_entry),
      self._get_text_from_entry("--tmp-dir=",
                                m._page1_misc_tmp_dir_ckbtn,
                                m._page1_misc_tmp_dir_entry),
      self._get_text_only_ckbtn("--identify-waf",
                                m._page1_misc_identify_waf_ckbtn),
      self._get_text_only_ckbtn("--skip-waf",
                                m._page1_misc_skip_waf_ckbtn),
      self._get_text_only_ckbtn("--smart",
                                m._page1_misc_smart_ckbtn),
      self._get_text_only_ckbtn("--list-tampers",
                                m._page1_misc_list_tampers_ckbtn),
      self._get_text_only_ckbtn("--sqlmap-shell",
                                m._page1_misc_sqlmap_shell_ckbtn),
      self._get_text_only_ckbtn("--disable-coloring",
                                m._page1_misc_disable_color_ckbtn),
      self._get_text_only_ckbtn("--offline",
                                m._page1_misc_offline_ckbtn),
      self._get_text_only_ckbtn("--mobile",
                                m._page1_misc_mobile_ckbtn),
      self._get_text_only_ckbtn("--beep",
                                m._page1_misc_beep_ckbtn),
      self._get_text_only_ckbtn("--purge",
                                m._page1_misc_purge_ckbtn),
      self._get_text_only_ckbtn("--dependencies",
                                m._page1_misc_dependencies_ckbtn),
      self._get_text_only_ckbtn("--update",
                                m._page1_general_update_ckbtn),
      self._get_text_from_entry("--answers=",
                                m._page1_misc_answers_ckbtn,
                                m._page1_misc_answers_entry),
      self._get_text_from_entry("--alert=",
                                m._page1_misc_alert_ckbtn,
                                m._page1_misc_alert_entry),
      self._get_text_from_entry("--gpage=",
                                m._page1_misc_gpage_ckbtn,
                                m._page1_misc_gpage_spinbtn, None),
      self._get_text_from_entry("-z ",
                                m._page1_misc_z_ckbtn,
                                m._page1_misc_z_entry),
    ]

    self._file_opts = [
      self._get_text_from_entry("--file-read=",
                                m._file_read_area_file_read_ckbtn,
                                m._file_read_area_file_read_entry),
      self._get_text_only_ckbtn("--udf-inject",
                                m._file_write_area_udf_ckbtn),
      self._get_text_from_entry("--shared-lib=",
                                m._file_write_area_shared_lib_ckbtn,
                                m._file_write_area_shared_lib_entry),
      self._get_text_from_entry("--file-write=",
                                m._file_write_area_file_write_ckbtn,
                                m._file_write_area_file_write_entry),
      self._get_text_from_entry("--file-dest=",
                                m._file_write_area_file_dest_ckbtn,
                                m._file_write_area_file_dest_entry),
      self._get_text_from_entry("--os-cmd=",
                                m._file_os_access_os_cmd_ckbtn,
                                m._file_os_access_os_cmd_entry),
      self._get_text_only_ckbtn("--os-shell",
                                m._file_os_access_os_shell_ckbtn),
      self._get_text_only_ckbtn("--os-pwn",
                                m._file_os_access_os_pwn_ckbtn),
      self._get_text_only_ckbtn("--os-smbrelay",
                                m._file_os_access_os_smbrelay_ckbtn),
      self._get_text_only_ckbtn("--os-bof",
                                m._file_os_access_os_bof_ckbtn),
      self._get_text_only_ckbtn("--priv-esc",
                                m._file_os_access_priv_esc_ckbtn),
      self._get_text_from_entry("--msf-path=",
                                m._file_os_access_msf_path_ckbtn,
                                m._file_os_access_msf_path_entry),
      self._get_text_from_entry("--tmp-path=",
                                m._file_os_access_tmp_path_ckbtn,
                                m._file_os_access_tmp_path_entry),
      self._get_text_only_ckbtn(
        m._file_os_registry_reg_choice.GetString(
          m._file_os_registry_reg_choice.GetSelection()),
        m._file_os_registry_reg_ckbtn),
      self._get_text_from_entry("--reg-key=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_key_entry),
      self._get_text_from_entry("--reg-value=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_value_entry),
      self._get_text_from_entry("--reg-data=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_data_entry),
      self._get_text_from_entry("--reg-type=",
                                m._file_os_registry_reg_ckbtn,
                                m._file_os_registry_reg_type_entry),
    ]

    self._enumeration_opts = [
      self._get_text_only_ckbtn("-b",
                                m._enum_area_opts_ckbtns[0][0]),
      self._get_text_only_ckbtn("--current-user",
                                m._enum_area_opts_ckbtns[0][1]),
      self._get_text_only_ckbtn("--current-db",
                                m._enum_area_opts_ckbtns[0][2]),
      self._get_text_only_ckbtn("--hostname",
                                m._enum_area_opts_ckbtns[0][3]),
      self._get_text_only_ckbtn("--is-dba",
                                m._enum_area_opts_ckbtns[0][4]),
      self._get_text_only_ckbtn("--users",
                                m._enum_area_opts_ckbtns[1][0]),
      self._get_text_only_ckbtn("--passwords",
                                m._enum_area_opts_ckbtns[1][1]),
      self._get_text_only_ckbtn("--privileges",
                                m._enum_area_opts_ckbtns[1][2]),
      self._get_text_only_ckbtn("--roles",
                                m._enum_area_opts_ckbtns[1][3]),
      self._get_text_only_ckbtn("--dbs",
                                m._enum_area_opts_ckbtns[1][4]),
      self._get_text_only_ckbtn("--tables",
                                m._enum_area_opts_ckbtns[2][0]),
      self._get_text_only_ckbtn("--columns",
                                m._enum_area_opts_ckbtns[2][1]),
      self._get_text_only_ckbtn("--schema",
                                m._enum_area_opts_ckbtns[2][2]),
      self._get_text_only_ckbtn("--count",
                                m._enum_area_opts_ckbtns[2][3]),
      self._get_text_only_ckbtn("--comments",
                                m._enum_area_opts_ckbtns[2][4]),
      self._get_text_only_ckbtn("--dump",
                                m._dump_area_dump_ckbtn),
      self._get_text_only_ckbtn("--dump-all",
                                m._dump_area_dump_all_ckbtn),
      self._get_text_only_ckbtn("--search",
                                m._dump_area_search_ckbtn),
      self._get_text_only_ckbtn("--exclude-sysdb",
                                m._dump_area_no_sys_db_ckbtn),
      self._get_text_only_ckbtn("--repair",
                                m._dump_area_repair_ckbtn),
      self._get_text_from_entry("--start=",
                                m._limit_area_start_ckbtn,
                                m._limit_area_start_entry, None),
      self._get_text_from_entry("--stop=",
                                m._limit_area_stop_ckbtn,
                                m._limit_area_stop_entry, None),
      self._get_text_from_entry("--first=",
                                m._blind_area_first_ckbtn,
                                m._blind_area_first_entry),
      self._get_text_from_entry("--last=",
                                m._blind_area_last_ckbtn,
                                m._blind_area_last_entry),
      self._get_text_from_entry("-D ",
                                m._meta_area_D_ckbtn,
                                m._meta_area_D_entry),
      self._get_text_from_entry("-T ",
                                m._meta_area_T_ckbtn,
                                m._meta_area_T_entry),
      self._get_text_from_entry("-C ",
                                m._meta_area_C_ckbtn,
                                m._meta_area_C_entry),
      self._get_text_from_entry("-U ",
                                m._meta_area_U_ckbtn,
                                m._meta_area_U_entry),
      self._get_text_from_entry("-X ",
                                m._meta_area_X_ckbtn,
                                m._meta_area_X_entry),
      self._get_text_from_entry("--pivot-column=",
                                m._meta_area_pivot_ckbtn,
                                m._meta_area_pivot_entry),
      self._get_text_from_entry("--where=",
                                m._meta_area_where_ckbtn,
                                m._meta_area_where_entry),
      self._get_text_from_entry("--sql-query=",
                                m._runsql_area_sql_query_ckbtn,
                                m._runsql_area_sql_query_entry),
      self._get_text_only_ckbtn("--sql-shell",
                                m._runsql_area_sql_shell_ckbtn),
      self._get_text_from_entry("--sql-file=",
                                m._runsql_area_sql_file_ckbtn,
                                m._runsql_area_sql_file_entry),
      self._get_text_only_ckbtn("--common-tables",
                                m._brute_force_area_common_tables_ckbtn),
      self._get_text_only_ckbtn("--common-columns",
                                m._brute_force_area_common_columns_ckbtn),
    ]

    self._request_opts = [
      self._get_text_only_ckbtn("--random-agent",
                                m._request_area_random_agent_ckbtn),
      self._get_text_from_entry("--user-agent=",
                                m._request_area_user_agent_ckbtn,
                                m._request_area_user_agent_entry),
      self._get_text_from_entry("--host=",
                                m._request_area_host_ckbtn,
                                m._request_area_host_entry),
      self._get_text_from_entry("--referer=",
                                m._request_area_referer_ckbtn,
                                m._request_area_referer_entry),
      self._get_text_from_entry("--header=",
                                m._request_area_header_ckbtn,
                                m._request_area_header_entry),
      self._get_text_from_entry("--headers=",
                                m._request_area_headers_ckbtn,
                                m._request_area_headers_entry),
      self._get_text_from_entry("--method=",
                                m._request_area_method_ckbtn,
                                m._request_area_method_entry, None),
      self._get_text_from_entry("--param-del=",
                                m._request_area_param_del_ckbtn,
                                m._request_area_param_del_entry),
      self._get_text_from_entry("--data=",
                                m._request_area_post_ckbtn,
                                m._request_area_post_entry),
      self._get_text_from_entry("--cookie=",
                                m._request_area_cookie_ckbtn,
                                m._request_area_cookie_entry),
      self._get_text_from_entry("--cookie-del=",
                                m._request_area_cookie_del_ckbtn,
                                m._request_area_cookie_del_entry),
      self._get_text_from_entry("--load-cookies=",
                                m._request_area_load_cookies_ckbtn,
                                m._request_area_load_cookies_entry),
      self._get_text_only_ckbtn("--drop-set-cookie",
                                m._request_area_drop_set_cookie_ckbtn),
      self._get_text_from_entry("--auth-type=",
                                m._request_area_auth_type_ckbtn,
                                m._request_area_auth_type_entry),
      self._get_text_from_entry("--auth-cred=",
                                m._request_area_auth_cred_ckbtn,
                                m._request_area_auth_cred_entry),
      self._get_text_from_entry("--auth-file=",
                                m._request_area_auth_file_ckbtn,
                                m._request_area_auth_file_entry),
      self._get_text_from_entry("--csrf-token=",
                                m._request_area_csrf_token_ckbtn,
                                m._request_area_csrf_token_entry),
      self._get_text_from_entry("--csrf-url=",
                                m._request_area_csrf_url_ckbtn,
                                m._request_area_csrf_url_entry),
      self._get_text_only_ckbtn("--ignore-redirects",
                                m._request_area_ignore_redirects_ckbtn),
      self._get_text_only_ckbtn("--ignore-timeouts",
                                m._request_area_ignore_timeouts_ckbtn),
      self._get_text_from_entry("--ignore-code=",
                                m._request_area_ignore_code_ckbtn,
                                m._request_area_ignore_code_entry, None),
      self._get_text_only_ckbtn("--skip-urlencode",
                                m._request_area_skip_urlencode_ckbtn),
      self._get_text_only_ckbtn("--force-ssl",
                                m._request_area_force_ssl_ckbtn),
      self._get_text_only_ckbtn("--chunked",
                                m._request_area_chunked_ckbtn),
      self._get_text_only_ckbtn("--hpp",
                                m._request_area_hpp_ckbtn),
      self._get_text_from_entry("--delay=",
                                m._request_area_delay_ckbtn,
                                m._request_area_delay_entry, None),
      self._get_text_from_entry("--timeout=",
                                m._request_area_timeout_ckbtn,
                                m._request_area_timeout_entry, None),
      self._get_text_from_entry("--retries=",
                                m._request_area_retries_ckbtn,
                                m._request_area_retries_entry, None),
      self._get_text_from_entry("--randomize=",
                                m._request_area_randomize_ckbtn,
                                m._request_area_randomize_entry),
      self._get_text_from_entry("--eval=",
                                m._request_area_eval_ckbtn,
                                m._request_area_eval_entry),
      self._get_text_from_entry("--safe-url=",
                                m._request_area_safe_url_ckbtn,
                                m._request_area_safe_url_entry),
      self._get_text_from_entry("--safe-post=",
                                m._request_area_safe_post_ckbtn,
                                m._request_area_safe_post_entry),
      self._get_text_from_entry("--safe-req=",
                                m._request_area_safe_req_ckbtn,
                                m._request_area_safe_req_entry),
      self._get_text_from_entry("--safe-freq=",
                                m._request_area_safe_freq_ckbtn,
                                m._request_area_safe_freq_entry),
      self._get_text_only_ckbtn("--ignore-proxy",
                                m._request_area_ignore_proxy_ckbtn),
      self._get_http_proxy(),
      self._get_http_proxy_cred(),
      self._get_text_from_entry("--proxy-file=",
                                m._request_area_proxy_file_ckbtn,
                                m._request_area_proxy_file_entry),
      self._get_text_only_ckbtn("--tor",
                                m._request_area_tor_ckbtn),
      self._get_text_from_entry("--tor-port=",
                                m._request_area_tor_port_ckbtn,
                                m._request_area_tor_port_entry),
      self._get_text_from_entry("--tor-type=",
                                m._request_area_tor_type_ckbtn,
                                m._request_area_tor_type_entry),
      self._get_text_only_ckbtn("--check-tor",
                                m._request_area_check_tor_ckbtn),
    ]

    self._setting_opts = [
      self._get_text_from_entry("-p ",
                                m._inject_area_param_ckbtn,
                                m._inject_area_param_entry),
      self._get_text_only_ckbtn("--skip-static",
                                m._inject_area_skip_static_ckbtn),
      self._get_text_from_entry("--prefix=",
                                m._inject_area_prefix_ckbtn,
                                m._inject_area_prefix_entry),
      self._get_text_from_entry("--suffix=",
                                m._inject_area_suffix_ckbtn,
                                m._inject_area_suffix_entry),
      self._get_text_from_entry("--skip=",
                                m._inject_area_skip_ckbtn,
                                m._inject_area_skip_entry),
      self._get_text_from_entry("--para-exclude=",
                                m._inject_area_param_exclude_ckbtn,
                                m._inject_area_param_exclude_entry),
      self._get_text_from_entry("--dbms=",
                                m._inject_area_dbms_ckbtn,
                                m._inject_area_dbms_combobox),
      self._get_text_from_entry("--dbms-cred=",
                                m._inject_area_dbms_cred_ckbtn,
                                m._inject_area_dbms_cred_entry),
      self._get_text_from_entry("--os=",
                                m._inject_area_os_ckbtn,
                                m._inject_area_os_entry),
      self._get_text_only_ckbtn("--no-cast",
                                m._inject_area_no_cast_ckbtn),
      self._get_text_only_ckbtn("--no-escape",
                                m._inject_area_no_escape_ckbtn),
      self._get_text_only_ckbtn("--invalid-logic",
                                m._inject_area_invalid_logic_ckbtn),
      self._get_text_only_ckbtn("--invalid-bignum",
                                m._inject_area_invalid_bignum_ckbtn),
      self._get_text_only_ckbtn("--invalid-str",
                                m._inject_area_invalid_str_ckbtn),
      self._get_text_from_scale("--level=",
                                m._detection_area_level_ckbtn,
                                m._detection_area_level_scale),
      self._get_text_only_ckbtn("--text-only",
                                m._detection_area_text_only_ckbtn),
      self._get_text_from_scale("--risk=",
                                m._detection_area_risk_ckbtn,
                                m._detection_area_risk_scale),
      self._get_text_only_ckbtn("--titles",
                                m._detection_area_titles_ckbtn),
      self._get_text_from_entry("--string=",
                                m._detection_area_str_ckbtn,
                                m._detection_area_str_entry),
      self._get_text_from_entry("--not-string=",
                                m._detection_area_not_str_ckbtn,
                                m._detection_area_not_str_entry),
      self._get_text_from_entry("--regexp=",
                                m._detection_area_re_ckbtn,
                                m._detection_area_re_entry),
      self._get_text_from_entry("--code=",
                                m._detection_area_code_ckbtn,
                                m._detection_area_code_entry, None),
      self._get_text_from_entry("--technique=",
                                m._tech_area_tech_ckbtn,
                                m._tech_area_tech_entry, None),
      self._get_text_from_entry("--time-sec=",
                                m._tech_area_time_sec_ckbtn,
                                m._tech_area_time_sec_entry, None),
      self._get_text_from_entry("--union-cols=",
                                m._tech_area_union_col_ckbtn,
                                m._tech_area_union_col_entry, None),
      self._get_text_from_entry("--union-char=",
                                m._tech_area_union_chr_ckbtn,
                                m._tech_area_union_chr_entry),
      self._get_text_from_entry("--union-from=",
                                m._tech_area_union_from_ckbtn,
                                m._tech_area_union_from_entry),
      self._get_text_from_entry("--dns-domain=",
                                m._tech_area_dns_ckbtn,
                                m._tech_area_dns_entry),
      self._get_text_from_entry("--second-url=",
                                m._tech_area_second_url_ckbtn,
                                m._tech_area_second_url_entry),
      self._get_text_from_entry("--second-req=",
                                m._tech_area_second_req_ckbtn,
                                m._tech_area_second_req_entry),
      self._get_text_only_ckbtn("-o",
                                m._optimize_area_turn_all_ckbtn),
      self._get_text_from_entry("--threads=",
                                m._optimize_area_thread_num_ckbtn,
                                m._optimize_area_thread_num_spinbtn, None),
      self._get_text_only_ckbtn("--predict-output",
                                m._optimize_area_predict_ckbtn),
      self._get_text_only_ckbtn("--keep-alive",
                                m._optimize_area_keep_alive_ckbtn),
      self._get_text_only_ckbtn("--null-connection",
                                m._optimize_area_null_connect_ckbtn),
      self._get_text_from_scale("-v ",
                                m._general_area_verbose_ckbtn,
                                m._general_area_verbose_scale),
      self._get_text_only_ckbtn("--fingerprint",
                                m._general_area_finger_ckbtn),
      self._get_text_only_ckbtn("--hex",
                                m._general_area_hex_ckbtn),
      self._get_text_only_ckbtn("--batch",
                                m._general_area_batch_ckbtn),
      self._get_text_only_ckbtn("--wizard",
                                m._page1_misc_wizard_ckbtn),
      self._get_tampers(),
    ]

  def _get_http_proxy_cred(self):
    m = self.w._notebook
    _use_proxy = m._request_area_proxy_ckbtn.IsChecked()
    _username = m._request_area_proxy_username_entry.GetValue()
    _pass = m._request_area_proxy_password_entry.GetValue()

    if all((_use_proxy, _username, _pass)) :
      return ''.join((" --proxy-cred=", QUOTE % '{}:{}'.format(_username, _pass)))
    return ''

  def _get_http_proxy(self):
    m = self.w._notebook
    _use_proxy = m._request_area_proxy_ckbtn.IsChecked()
    _ip = m._request_area_proxy_ip_entry.GetValue().strip()
    _port = m._request_area_proxy_port_entry.GetValue()

    if _use_proxy and _ip:
      if _port:
        return "".join((" --proxy=", QUOTE % '{}:{}'.format(_ip, _port)))
      else:
        return "".join((" --proxy=", QUOTE % _ip))
    return ''

  def _get_tampers(self):
    '''
    简单处理
    '''
    m = self.w._notebook
    _tamper_textbuffer = m._tamper_area_tamper_view.GetValue()
    _tampers = ''

    for _tamper_tmp in _tamper_textbuffer.splitlines():
      if _tamper_tmp.strip():
        _tampers = _tampers + _tamper_tmp.strip() + ','

    if _tampers:
      return " --tamper=" + QUOTE % _tampers.rstrip(',')
    return ''

  def _get_text_from_scale(self, opt_str, ckbtn, scale):
    if ckbtn.IsChecked():
      return ''.join((' ', opt_str, str(scale.GetValue())))
    return ''

  def _get_text_only_ckbtn(self, opt_str, ckbtn):
    if ckbtn.IsChecked():
      return ''.join((' ', opt_str))
    return ''

  def _get_text_from_entry(self, opt_str, ckbtn, entry, quote = QUOTE):
    _entry_str = str(entry.GetValue()).strip()
    if ckbtn.IsChecked() and _entry_str:

      if quote:
        return ''.join((' ',
                        opt_str,
                        quote % self._escape_quote_in_QUOTE(_entry_str)))
      else:
        return ''.join((' ',
                        opt_str,
                        self._escape_quote(_entry_str)))
    return ''

  def _escape_quote_in_QUOTE(self, widget_text):
    '''
    注意bash中, 双单引号内无法使用'(即无法转义)
    '''
    if widget_text:
      if IS_POSIX:
        return widget_text.replace("'", r"'\''")
      else:
        return widget_text.replace('"', r"\"")
    return widget_text

  def _escape_quote(self, widget_text):
    if widget_text:
      return widget_text.replace("'", r"\'").replace('"', r'\"')
    return widget_text


def main():
  import wx
  from sqlmap_wx import Window

  app = wx.App()
  win = Window(None)
  win.Centre()
  win.Show()
  app.MainLoop()


if __name__ == '__main__':
  main()
