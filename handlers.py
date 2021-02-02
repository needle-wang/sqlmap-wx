#!/usr/bin/env python3
#
# 2018-08-29 15:34:10

import time
from os import name as OS_NAME
from pathlib import Path
from shlex import quote as quote_posix
from subprocess import Popen
from urllib.parse import urlparse

from widgets import wx
from handler_api import Api

IS_POSIX = True if OS_NAME == 'posix' else False


class Handler(object):
  def __init__(self, topwindow, m):
    '''
    topwindow: sqlmap_wx.Window
    m: model.Model
    还不能用注解, 会相互import
    '''
    self.w = topwindow
    self.m = m
    # m = self.w._notebook不能写在这, 因为还没初始化完, _notebook还不存在
    self.api = Api(topwindow, m)

  def build_all(self, event):
    _ = self._collect_opts()
    _ = ' '.join(_).strip()
    # print(_)
    self.m._cmd_entry.SetValue(_)
    self.w._notebook.SetFocus()

  def get_tc_value(self, textctrl):
    return textctrl.GetValue().strip()

  def run_cmdline(self, event):
    self.w._notebook.SetFocus()

    sqlmap_path = self.get_sqlmap_path()
    _target = self._get_target()
    _sqlmap_opts = self.get_tc_value(self.m._cmd_entry).strip()

    if IS_POSIX:
      # _ = f'/usr/bin/env x-terminal-emulator --hold -e {sqlmap_path} {_target} {_sqlmap_opts}'
      _ = f'/usr/bin/env xterm -hold -e {sqlmap_path} {_target} {_sqlmap_opts}'
    else:
      _ = f'start cmd /k {sqlmap_path} {_target} {_sqlmap_opts}'

    # self.w.main_notebook.SetSelection(1)
    # print(_)
    Popen(_, shell = True)

  def get_sqlmap_path(self, path = 'sqlmap'):
    path_in_tc = self.get_tc_value(self.m.sqlmap_path_entry)

    if IS_POSIX:
      if path_in_tc:
        path = path_in_tc
    else:
      # sqlmap.exe and sqlmap.py in win
      if path_in_tc:
        if path_in_tc.endswith('.py'):
          path = f'python3 "{path_in_tc}"'
        else:
          path = path_in_tc

    return path

  def set_file_entry_text(self, event, data):
    '''
    data: [file_entry, 'title of chooser']
    '''
    if len(data) > 1:   # choose folder
      dialog = wx.DirDialog(self.w, message=data[1])
    else:
      dialog = wx.FileDialog(self.w, message="Choose file")

    with dialog:
      if dialog.ShowModal() == wx.ID_OK:
        data[0].SetValue(dialog.GetPath())
        data[0].SetFocus()

  def clear_task_view_buffer(self, event):
    self.m._page4_task_view.SetValue('')

  def clear_log_view_buffer(self, event):
    self.m._page3_log_view.SetValue(
      'sqlmap\'s log folder: %s\n' % self.get_output_dir())

  def _get_url_dir(self):
    '''
    return: pathlib.Path
    '''
    _load_url = self.get_tc_value(self.m._url_combobox)

    if _load_url:
      if not _load_url.startswith('http'):
        _load_url = f'http://{_load_url}'

      _load_host = urlparse(_load_url).netloc

      return self.get_output_dir() / _load_host

  def get_output_dir(self):
    if IS_POSIX:
      return Path.home() / '.sqlmap/output'
    else:
      return Path.home() / 'AppData/Local/sqlmap/output'

  def _log_view_insert(self, file_path):
    '''
    file_path: pathlib.Path
               dataToOutFile in sqlmap lib writes with utf8 (default)
    '''
    m = self.m
    try:
      with file_path.open(encoding = 'utf8') as _f:
        _line_list_tmp = _f.readlines()
        if _line_list_tmp:
          for _line_tmp in _line_list_tmp:
            m._page3_log_view.write(_line_tmp)
        else:
          m._page3_log_view.write(f'{file_path}: empty file')
    except EnvironmentError as e:
      m._page3_log_view.write(str(e))
    finally:
      m._page3_log_view.write(
        time.strftime('\n%Y-%m-%d %R:%S: ', time.localtime()))
      # win下, strftime方法无法处理unicode, py的bug, 到此时还没修复
      m._page3_log_view.write('----------split line----------\n',)

      m._page3_log_view.SetFocus()
      _mark = m._page3_log_view.GetInsertionPoint()
      wx.CallAfter(m._page3_log_view.ShowPosition, _mark)

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
    m = self.m

    _base_dir = self._get_url_dir()
    _load_file = self.get_tc_value(m._file_read_area_file_read_entry)

    if _base_dir and _load_file:
      # 不能用os.sep, 因为是依据远程OS的sep而定
      # 沿用sqlmap库中的filePathToSafeString函数
      _load_file = (_load_file.replace("/", "_").replace("\\", "_")
                              .replace(" ", "_").replace(":", "_"))

      _dumped_file_path = _base_dir / 'files' / _load_file
      self._log_view_insert(_dumped_file_path)

  def _get_target(self):
    m = self.m
    _pagenum = self.w._target_notebook.GetSelection()
    _target_list = [("-u", m._url_combobox),
                    ("-l", m._burp_logfile),
                    ("-r", m._request_file),
                    ("-m", m._bulkfile),
                    ("-c", m._configfile),
                    ("-g", m._google_dork),
                    ("-d", m._direct_connect)]

    _ = self.get_tc_value(_target_list[_pagenum][1])
    if _:
      return '{} {}'.format(_target_list[_pagenum][0], self.quote(_))

  def _collect_opts(self):
    m = self.m

    _other_opts = [
      self._get_text_only_ckbtn("--check-internet",
                                m._general_area_check_internet_ckbtn),
      self._get_text_only_ckbtn("--fresh-queries",
                                m._general_area_fresh_queries_ckbtn),
      self._get_text_only_ckbtn("--forms",
                                m._general_area_forms_ckbtn),
      self._get_text_only_ckbtn("--parse-errors",
                                m._general_area_parse_errors_ckbtn),
      self._get_text_only_ckbtn("--cleanup",
                                m._misc_area_cleanup_ckbtn),
      self._get_text_from_entry("--base64=",
                                m._general_area_base64_ckbtn,
                                m._general_area_base64_entry),
      self._get_text_only_ckbtn("--base64-safe",
                                m._general_area_base64_safe_ckbtn),
      self._get_text_from_entry("--table-prefix=",
                                m._general_area_table_prefix_ckbtn,
                                m._general_area_table_prefix_entry),
      self._get_text_from_entry("--binary-fields=",
                                m._general_area_binary_fields_ckbtn,
                                m._general_area_binary_fields_entry),
      self._get_text_from_entry("--preprocess=",
                                m._general_area_preprocess_ckbtn,
                                m._general_area_preprocess_entry),
      self._get_text_from_entry("--postprocess=",
                                m._general_area_postprocess_ckbtn,
                                m._general_area_postprocess_entry),
      self._get_text_from_entry("--charset=",
                                m._general_area_charset_ckbtn,
                                m._general_area_charset_entry),
      self._get_text_from_entry("--encoding=",
                                m._general_area_encoding_ckbtn,
                                m._general_area_encoding_entry),
      self._get_text_from_entry("--web-root=",
                                m._general_area_web_root_ckbtn,
                                m._general_area_web_root_entry),
      self._get_text_from_entry("--scope=",
                                m._general_area_scope_ckbtn,
                                m._general_area_scope_entry),
      self._get_text_from_entry("--test-filter=",
                                m._general_area_test_filter_ckbtn,
                                m._general_area_test_filter_entry),
      self._get_text_from_entry("--test-skip=",
                                m._general_area_test_skip_ckbtn,
                                m._general_area_test_skip_entry),
      self._get_text_from_entry("--crawl=",
                                m._general_area_crawl_ckbtn,
                                m._general_area_crawl_entry),
      self._get_text_from_entry("--crawl-exclude=",
                                m._general_area_crawl_exclude_ckbtn,
                                m._general_area_crawl_exclude_entry),
      self._get_text_from_entry("-t ",
                                m._general_area_traffic_file_ckbtn,
                                m._general_area_traffic_file_entry),
      self._get_text_from_entry("--har=",
                                m._general_area_har_ckbtn,
                                m._general_area_har_entry),
      self._get_text_only_ckbtn("--flush-session",
                                m._general_area_flush_session_ckbtn),
      self._get_text_from_entry("--dump-format=",
                                m._general_area_dump_format_ckbtn,
                                m._general_area_dump_format_entry),
      self._get_text_from_entry("--csv-del=",
                                m._general_area_csv_del_ckbtn,
                                m._general_area_csv_del_entry),
      self._get_text_from_entry("--save=",
                                m._general_area_save_ckbtn,
                                m._general_area_save_entry),
      self._get_text_from_entry("-s ",
                                m._general_area_session_file_ckbtn,
                                m._general_area_session_file_entry),
      self._get_text_from_entry("--output-dir=",
                                m._general_area_output_dir_ckbtn,
                                m._general_area_output_dir_entry),
      self._get_text_only_ckbtn("--skip-heuristics",
                                m._misc_area_skip_heuristics_ckbtn),
      self._get_text_only_ckbtn("--skip-waf",
                                m._misc_area_skip_waf_ckbtn),
      self._get_text_only_ckbtn("--unstable",
                                m._misc_area_unstable_ckbtn),
      self._get_text_only_ckbtn("--list-tampers",
                                m._misc_area_list_tampers_ckbtn),
      self._get_text_only_ckbtn("--sqlmap-shell",
                                m._misc_area_sqlmap_shell_ckbtn),
      self._get_text_only_ckbtn("--disable-coloring",
                                m._misc_area_disable_color_ckbtn),
      self._get_text_only_ckbtn("--eta",
                                m._general_area_eta_ckbtn),
      self._get_text_from_entry("--gpage=",
                                m._misc_area_gpage_ckbtn,
                                m._misc_area_gpage_spinbtn),
      self._get_text_only_ckbtn("--beep",
                                m._misc_area_beep_ckbtn),
      self._get_text_only_ckbtn("--offline",
                                m._misc_area_offline_ckbtn),
      self._get_text_only_ckbtn("--purge",
                                m._misc_area_purge_ckbtn),
      self._get_text_only_ckbtn("--dependencies",
                                m._misc_area_dependencies_ckbtn),
      self._get_text_only_ckbtn("--update",
                                m._misc_area_update_ckbtn),
      self._get_text_from_entry("--alert=",
                                m._misc_area_alert_ckbtn,
                                m._misc_area_alert_entry),
      self._get_text_from_entry("--tmp-dir=",
                                m._misc_area_tmp_dir_ckbtn,
                                m._misc_area_tmp_dir_entry),
      self._get_text_from_entry("--answers=",
                                m._misc_area_answers_ckbtn,
                                m._misc_area_answers_entry),
      self._get_text_from_entry("-z ",
                                m._misc_area_z_ckbtn,
                                m._misc_area_z_entry),
      self._get_text_from_entry("--results-file=",
                                m._misc_area_results_file_ckbtn,
                                m._misc_area_results_file_entry),
    ]

    _file_opts = [
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
                                m._os_access_area_os_cmd_ckbtn,
                                m._os_access_area_os_cmd_entry),
      self._get_text_only_ckbtn("--os-shell",
                                m._os_access_area_os_shell_ckbtn),
      self._get_text_only_ckbtn("--os-pwn",
                                m._os_access_area_os_pwn_ckbtn),
      self._get_text_only_ckbtn("--os-smbrelay",
                                m._os_access_area_os_smbrelay_ckbtn),
      self._get_text_only_ckbtn("--os-bof",
                                m._os_access_area_os_bof_ckbtn),
      self._get_text_only_ckbtn("--priv-esc",
                                m._os_access_area_priv_esc_ckbtn),
      self._get_text_from_entry("--msf-path=",
                                m._os_access_area_msf_path_ckbtn,
                                m._os_access_area_msf_path_entry),
      self._get_text_from_entry("--tmp-path=",
                                m._os_access_area_tmp_path_ckbtn,
                                m._os_access_area_tmp_path_entry),
      self._get_text_only_ckbtn(
        m._registry_area_reg_choice.GetString(
          m._registry_area_reg_choice.GetSelection()),
        m._registry_area_reg_ckbtn),
      self._get_text_from_entry("--reg-key=",
                                m._registry_area_reg_ckbtn,
                                m._registry_area_reg_key_entry),
      self._get_text_from_entry("--reg-value=",
                                m._registry_area_reg_ckbtn,
                                m._registry_area_reg_value_entry),
      self._get_text_from_entry("--reg-data=",
                                m._registry_area_reg_ckbtn,
                                m._registry_area_reg_data_entry),
      self._get_text_from_entry("--reg-type=",
                                m._registry_area_reg_ckbtn,
                                m._registry_area_reg_type_entry),
    ]

    _enumeration_opts = [
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
      self._get_text_only_ckbtn("--repair",
                                m._dump_area_repair_ckbtn),
      self._get_text_only_ckbtn("--statements",
                                m._dump_area_statements_ckbtn),
      self._get_text_only_ckbtn("--search",
                                m._dump_area_search_ckbtn),
      self._get_text_only_ckbtn("--exclude-sysdbs",
                                m._dump_area_no_sys_db_ckbtn),
      self._get_text_only_ckbtn("--dump-all",
                                m._dump_area_dump_all_ckbtn),
      self._get_text_from_entry("--start=",
                                m._limit_area_start_ckbtn,
                                m._limit_area_start_entry),
      self._get_text_from_entry("--stop=",
                                m._limit_area_stop_ckbtn,
                                m._limit_area_stop_entry),
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
      self._get_text_only_ckbtn("--common-files",
                                m._brute_force_area_common_files_ckbtn),
    ]

    _request_opts = [
      self._get_text_only_ckbtn("--random-agent",
                                m._request_area_random_agent_ckbtn),
      self._get_text_only_ckbtn("--mobile",
                                m._request_area_mobile_ckbtn),
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
                                m._request_area_method_entry),
      self._get_text_from_entry("--param-del=",
                                m._request_area_param_del_ckbtn,
                                m._request_area_param_del_entry),
      self._get_text_only_ckbtn("--chunked",
                                m._request_area_chunked_ckbtn),
      self._get_text_from_entry("--data=",
                                m._request_area_post_ckbtn,
                                m._request_area_post_entry),
      self._get_text_from_entry("--cookie=",
                                m._request_area_cookie_ckbtn,
                                m._request_area_cookie_entry),
      self._get_text_from_entry("--cookie-del=",
                                m._request_area_cookie_del_ckbtn,
                                m._request_area_cookie_del_entry),
      self._get_text_only_ckbtn("--drop-set-cookie",
                                m._request_area_drop_set_cookie_ckbtn),
      self._get_text_from_entry("--live-cookies=",
                                m._request_area_live_cookies_ckbtn,
                                m._request_area_live_cookies_entry),
      self._get_text_from_entry("--load-cookies=",
                                m._request_area_load_cookies_ckbtn,
                                m._request_area_load_cookies_entry),
      self._get_text_from_entry("--auth-type=",
                                m._request_area_auth_type_ckbtn,
                                m._request_area_auth_type_entry),
      self._get_text_from_entry("--auth-cred=",
                                m._request_area_auth_cred_ckbtn,
                                m._request_area_auth_cred_entry),
      self._get_text_from_entry("--auth-file=",
                                m._request_area_auth_file_ckbtn,
                                m._request_area_auth_file_entry),
      self._get_text_from_entry("--csrf-method=",
                                m._request_area_csrf_method_ckbtn,
                                m._request_area_csrf_method_entry),
      self._get_text_from_entry("--csrf-retries=",
                                m._request_area_csrf_retries_ckbtn,
                                m._request_area_csrf_retries_entry),
      self._get_text_from_entry("--csrf-token=",
                                m._request_area_csrf_token_ckbtn,
                                m._request_area_csrf_token_entry),
      self._get_text_from_entry("--csrf-url=",
                                m._request_area_csrf_url_ckbtn,
                                m._request_area_csrf_url_entry),
      self._get_text_only_ckbtn("--ignore-timeouts",
                                m._request_area_ignore_timeouts_ckbtn),
      self._get_text_only_ckbtn("--ignore-redirects",
                                m._request_area_ignore_redirects_ckbtn),
      self._get_text_from_entry("--ignore-code=",
                                m._request_area_ignore_code_ckbtn,
                                m._request_area_ignore_code_entry),
      self._get_text_only_ckbtn("--skip-urlencode",
                                m._request_area_skip_urlencode_ckbtn),
      self._get_text_only_ckbtn("--force-ssl",
                                m._request_area_force_ssl_ckbtn),
      self._get_text_only_ckbtn("--hpp",
                                m._request_area_hpp_ckbtn),
      self._get_text_from_entry("--delay=",
                                m._request_area_delay_ckbtn,
                                m._request_area_delay_entry),
      self._get_text_from_entry("--timeout=",
                                m._request_area_timeout_ckbtn,
                                m._request_area_timeout_entry),
      self._get_text_from_entry("--retries=",
                                m._request_area_retries_ckbtn,
                                m._request_area_retries_entry),
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
      self._get_http_proxy("--proxy="),
      self._get_http_proxy_cred("--proxy-cred="),
      self._get_text_from_entry("--proxy-freq=",
                                m._request_area_proxy_freq_ckbtn,
                                m._request_area_proxy_freq_entry),
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

    _setting_opts = [
      self._get_text_from_entry("-p ",
                                m._inject_area_param_ckbtn,
                                m._inject_area_param_entry),
      self._get_text_from_entry("--param-filter=",
                                m._inject_area_param_filter_ckbtn,
                                m._inject_area_param_filter_combobox),
      self._get_text_only_ckbtn("--skip-static",
                                m._inject_area_skip_static_ckbtn),
      self._get_text_from_entry("--skip=",
                                m._inject_area_skip_ckbtn,
                                m._inject_area_skip_entry),
      self._get_text_from_entry("--param-exclude=",
                                m._inject_area_param_exclude_ckbtn,
                                m._inject_area_param_exclude_entry),
      self._get_text_from_entry("--prefix=",
                                m._inject_area_prefix_ckbtn,
                                m._inject_area_prefix_entry),
      self._get_text_from_entry("--suffix=",
                                m._inject_area_suffix_ckbtn,
                                m._inject_area_suffix_entry),
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
      self._get_text_only_ckbtn("--invalid-bignum",
                                m._inject_area_invalid_bignum_ckbtn),
      self._get_text_only_ckbtn("--invalid-logic",
                                m._inject_area_invalid_logic_ckbtn),
      self._get_text_only_ckbtn("--invalid-string",
                                m._inject_area_invalid_string_ckbtn),
      self._get_text_from_scale("--level=",
                                m._detection_area_level_ckbtn,
                                m._detection_area_level_scale),
      self._get_text_from_scale("--risk=",
                                m._detection_area_risk_ckbtn,
                                m._detection_area_risk_scale),
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
                                m._detection_area_code_entry),
      self._get_text_only_ckbtn("--text-only",
                                m._detection_area_text_only_ckbtn),
      self._get_text_only_ckbtn("--titles",
                                m._detection_area_titles_ckbtn),
      self._get_text_only_ckbtn("--smart",
                                m._detection_area_smart_ckbtn),
      self._get_text_from_entry("--technique=",
                                m._tech_area_tech_ckbtn,
                                m._tech_area_tech_entry),
      self._get_text_from_entry("--time-sec=",
                                m._tech_area_time_sec_ckbtn,
                                m._tech_area_time_sec_entry),
      self._get_text_from_entry("--union-cols=",
                                m._tech_area_union_col_ckbtn,
                                m._tech_area_union_col_entry),
      self._get_text_from_entry("--union-char=",
                                m._tech_area_union_char_ckbtn,
                                m._tech_area_union_char_entry),
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
                                m._optimize_area_thread_num_spinbtn),
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
                                m._misc_area_wizard_ckbtn),
      self._get_tampers("--tamper=",
                        m._tamper_area_tamper_view),
    ]
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    return filter(None, (_setting_opts
                        + _request_opts
                        + _enumeration_opts
                        + _file_opts
                        + _other_opts))

  def _get_http_proxy_cred(self, opt_str):
    m = self.m
    _use_proxy = m._request_area_proxy_ckbtn.IsChecked()
    _username = self.get_tc_value(m._request_area_proxy_username_entry)
    _pass = self.get_tc_value(m._request_area_proxy_password_entry)

    if all((_use_proxy, _username, _pass)) :
      return f'{opt_str}{_username}:{_pass}'

  def _get_http_proxy(self, opt_str):
    m = self.m

    _use_proxy = m._request_area_proxy_ckbtn.IsChecked()

    _ip = self.get_tc_value(m._request_area_proxy_ip_entry)
    _port = self.get_tc_value(m._request_area_proxy_port_entry)

    if _use_proxy and _ip:
      if _port:
        _port = f':{_port}'
      return f"{opt_str}{_ip}{_port}"

  def _get_tampers(self, opt_str, view):
    '''
    简单处理
    '''
    _tamper_textbuffer = self.get_tc_value(view)
    _checked = []

    for _tamper_line in _tamper_textbuffer.splitlines():
      if _tamper_line.strip():
        for _a_tamper in _tamper_line.strip().split(','):
          _checked.append(_a_tamper.strip())

    _ = ','.join(_checked)
    if _:
      return f"{opt_str}{_}"

  def _get_text_from_scale(self, opt_str, ckbtn, scale):
    if ckbtn.IsChecked():
      return f'{opt_str}{scale.GetValue()}'

  def _get_text_only_ckbtn(self, opt_str, ckbtn):
    if ckbtn.IsChecked():
      return opt_str

  def _get_text_from_entry(self, opt_str, ckbtn, entry):
    _ = str(entry.GetValue()).strip()  # 有的返回int
    if ckbtn.IsChecked() and _:
      return '{}{}'.format(opt_str, self.quote(_))

  def quote(self, s):
    '''
    bash: 2个单引号内无法使用'(即无法转义)
    '''
    if IS_POSIX:
      return quote_posix(s)
    else:
      if s:
        # dos下只能用双引号
        return '"{}"'.format(s.replace('"', r'\"'))
    return s


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
