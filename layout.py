#!/usr/bin/env python3
#
# 2019年 10月 13日 星期日 00:00:23 CST

from widgets import wx
from widgets import HORIZONTAL, VERTICAL, EXPAND, ALL, TOP, BOTTOM, LEFT, RIGHT, ALIGN_CENTER, ALIGN_RIGHT

BoxSizer = wx.BoxSizer
GridSizer = wx.GridSizer
StaticBoxSizer = wx.StaticBoxSizer

SizerFlags = wx.SizerFlags


class Layout_opts(object):
  def __init__(self, topwindow, model):
    super().__init__()
    # 某些不重要的组件是放在topwindow中的,
    # 如不重要的label不在model中, 也要布局嘛!
    # 布局需要部件, 最后返回boxsizer, 所以此类是拥有这两个属性的!
    self.nb = topwindow
    self.moo = model

  def setting_sizer(self):
    spacing = SizerFlags().Expand().Border(ALL, 5)

    hbox0 = BoxSizer()
    hbox0.Add(self.moo._sqlmap_path_label, flag = ALIGN_CENTER)
    hbox0.Add(self.moo.sqlmap_path_entry, proportion = 1, flag = EXPAND)
    hbox0.Add(self.moo._sqlmap_path_chooser, flag = EXPAND | RIGHT, border = 25)

    hbox1 = BoxSizer()
    # win下 探测选项staticbox不能用proportion = 1, 最大化时会让右侧的staticbox消失
    # hbox1_grid为了win写的兼容sizer, 怎么感觉在写html?
    hbox1_grid = GridSizer(1, 2, 0, 0)

    inject_area = self._setting_inject()

    detection_area = self._setting_detection()
    tech_area = self._setting_tech()
    hbox1_grid.Add(detection_area, flag = EXPAND | RIGHT, border = 10)
    hbox1_grid.Add(tech_area, flag = EXPAND)

    hbox1.Add(inject_area, spacing)
    hbox1.Add(hbox1_grid, spacing)

    hbox2 = BoxSizer()
    tamper_area = self._setting_tamper()
    optimize_area = self._setting_optimize()
    general_area = self._setting_general()

    hbox2.Add(tamper_area, spacing)
    hbox2.Add(optimize_area, spacing)
    hbox2.Add(general_area, spacing)

    vbox = BoxSizer(VERTICAL)
    vbox.Add(hbox0, flag = EXPAND | LEFT | RIGHT, border = 5)
    vbox.Add(hbox1, flag = EXPAND | RIGHT, border = 20)  # 20: 让win下的滚动条不致于掩盖末端内容~~
    vbox.Add(hbox2)
    return vbox

  def _setting_inject(self):
    inject_area = StaticBoxSizer(self.moo._inject_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    _boxes = [BoxSizer() for _ in range(10)]
    _ = 0
    _boxes[_].Add(self.moo._inject_area_param_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_param_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_param_filter_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_param_filter_combobox, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_skip_static_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_skip_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_skip_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_param_exclude_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_param_exclude_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_prefix_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_prefix_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_suffix_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_suffix_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_dbms_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_dbms_combobox, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_dbms_cred_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_dbms_cred_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._inject_area_os_ckbtn, border)
    _boxes[_].Add(self.moo._inject_area_os_entry, proportion_border)

    grid = GridSizer(3, 2, 0, 0)
    grid.Add(self.moo._inject_area_no_cast_ckbtn)
    grid.Add(self.moo._inject_area_no_escape_ckbtn, flag = LEFT, border = 20)
    grid.Add(self.nb._inject_area_invalid_label, flag = wx.ALIGN_CENTER)
    grid.Add(self.moo._inject_area_invalid_logic_ckbtn, flag = LEFT, border = 20)
    grid.Add(self.moo._inject_area_invalid_bignum_ckbtn, flag = ALIGN_RIGHT)
    grid.Add(self.moo._inject_area_invalid_str_ckbtn, flag = LEFT, border = 20)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 2)
    for _ in _boxes:
      inject_area.Add(_, spacing)

    inject_area.Add(grid, flag = EXPAND | LEFT, border = 5)
    return inject_area  # 一定要返回Sizer(StaticBoxSizer), 不然会段错误!

  def _setting_detection(self):
    detection_area = StaticBoxSizer(self.moo._detection_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    _boxes = [BoxSizer() for _ in range(9)]
    _ = 0
    _boxes[_].Add(self.moo._detection_area_level_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_level_scale, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._detection_area_risk_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_risk_scale, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._detection_area_str_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_str_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._detection_area_not_str_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_not_str_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._detection_area_re_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_re_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._detection_area_code_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_code_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._detection_area_text_only_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_titles_ckbtn, border)
    _boxes[_].Add(self.moo._detection_area_smart_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.nb._detection_area_hr, proportion_border)
    _ += 1
    _boxes[_].Add(self.nb._detection_area_level_note, border)
    _boxes[_].Add(self.nb._detection_area_risk_note, border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 2)
    for _ in _boxes:
      detection_area.Add(_, spacing)

    return detection_area

  def _setting_tech(self):
    tech_area = StaticBoxSizer(self.moo._tech_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    grid = GridSizer(5, 2, 6, 0)
    grid.Add(self.moo._tech_area_tech_ckbtn, border)
    grid.Add(self.moo._tech_area_tech_entry, border)
    grid.Add(self.moo._tech_area_time_sec_ckbtn, border)
    grid.Add(self.moo._tech_area_time_sec_entry, border)
    grid.Add(self.moo._tech_area_union_col_ckbtn, border)
    grid.Add(self.moo._tech_area_union_col_entry, border)
    grid.Add(self.moo._tech_area_union_char_ckbtn, border)
    grid.Add(self.moo._tech_area_union_char_entry, border)
    grid.Add(self.moo._tech_area_union_from_ckbtn, border)
    grid.Add(self.moo._tech_area_union_from_entry, border)

    _boxes = [BoxSizer() for _ in range(4)]
    _boxes[0].Add(self.moo._tech_area_dns_ckbtn, border)
    _boxes[0].Add(self.moo._tech_area_dns_entry, proportion_border)
    _boxes[1].Add(self.moo._tech_area_second_url_ckbtn, border)
    _boxes[1].Add(self.moo._tech_area_second_url_entry, proportion_border)
    _boxes[2].Add(self.moo._tech_area_second_req_ckbtn, border)
    _boxes[3].Add(self.moo._tech_area_second_req_entry, proportion = 1, flag = EXPAND | LEFT, border = 5)
    _boxes[3].Add(self.moo._tech_area_second_req_chooser, border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 2)

    tech_area.Add(grid, spacing)

    for _ in _boxes:
      tech_area.Add(_, spacing)

    return tech_area

  def _setting_tamper(self):
    tamper_area = StaticBoxSizer(self.moo._tamper_area, VERTICAL)

    tamper_area.Add(self.moo._tamper_area_tamper_view, proportion = 1)
    return tamper_area

  def _setting_optimize(self):
    optimize_area = StaticBoxSizer(self.moo._optimize_area, VERTICAL)

    row2 = BoxSizer()
    row2.Add(self.moo._optimize_area_thread_num_ckbtn, flag = EXPAND)
    row2.Add(self.moo._optimize_area_thread_num_spinbtn, proportion = 1, flag = RIGHT, border = 10)

    spacing = SizerFlags().Expand().Border(ALL, 3)
    optimize_area.Add(self.moo._optimize_area_turn_all_ckbtn, spacing)
    optimize_area.Add(row2, spacing)
    optimize_area.Add(self.moo._optimize_area_predict_ckbtn, spacing)
    optimize_area.Add(self.moo._optimize_area_keep_alive_ckbtn, spacing)
    optimize_area.Add(self.moo._optimize_area_null_connect_ckbtn, spacing)
    return optimize_area

  def _setting_general(self):
    general_area = StaticBoxSizer(self.moo._general_area, VERTICAL)

    row1 = BoxSizer()
    row1.Add(self.moo._general_area_verbose_ckbtn, flag = EXPAND)
    row1.Add(self.moo._general_area_verbose_scale, proportion = 1)

    spacing = SizerFlags().Expand().Border(ALL, 3)
    general_area.Add(row1, spacing)
    general_area.Add(self.moo._general_area_finger_ckbtn, spacing)
    general_area.Add(self.moo._general_area_hex_ckbtn, spacing)
    general_area.Add(self.moo._general_area_batch_ckbtn, spacing)
    general_area.Add(self.moo._page1_misc_wizard_ckbtn, spacing)
    return general_area

  def request_sizer(self):
    vbox = BoxSizer(VERTICAL)

    proportion_border = SizerFlags(1).Expand().Border(RIGHT, 20)
    # 本来没必要加行的, 为了让win下的滚动条不致于掩盖末端内容~~
    row1 = BoxSizer()
    request_header_area = self._request_header()
    row1.Add(request_header_area, proportion_border)

    row2 = BoxSizer()
    request_data_area = self._request_data()
    row2.Add(request_data_area, proportion_border)

    row3 = BoxSizer()
    request_custom_area = self._request_custom()
    row3.Add(request_custom_area, proportion_border)

    row4 = BoxSizer()
    request_proxy_area = self._request_proxy()
    row4.Add(request_proxy_area, proportion_border)

    spacing = SizerFlags().Expand().Border(LEFT | RIGHT | TOP, 5)
    vbox.Add(row1, spacing)
    vbox.Add(row2, spacing)
    vbox.Add(row3, spacing)
    vbox.Add(row4, spacing)
    return vbox

  def _request_header(self):
    request_header_area = StaticBoxSizer(self.moo._request_header_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    _boxes = [BoxSizer() for _ in range(3)]
    _ = 0
    _boxes[_].Add(self.moo._request_area_random_agent_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_mobile_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_user_agent_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_user_agent_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_host_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_host_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_referer_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_referer_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_header_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_header_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_headers_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_headers_entry, proportion_border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 2)
    for _ in _boxes:
      request_header_area.Add(_, spacing)

    return request_header_area

  def _request_data(self):
    request_data_area = StaticBoxSizer(self.moo._request_data_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    _boxes = [BoxSizer() for _ in range(6)]
    _ = 0
    _boxes[_].Add(self.moo._request_area_method_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_method_entry, border)
    _boxes[_].Add(self.moo._request_area_param_del_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_param_del_entry, border)
    _boxes[_].Add(self.moo._request_area_chunked_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_post_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_post_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_cookie_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_cookie_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_cookie_del_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_cookie_del_entry, border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_load_cookies_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_load_cookies_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._request_area_load_cookies_chooser, border)
    _boxes[_].Add(self.moo._request_area_drop_set_cookie_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_auth_type_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_auth_type_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_auth_cred_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_auth_cred_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_auth_file_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_auth_file_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._request_area_auth_file_chooser, border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_csrf_method_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_csrf_method_entry, border)
    _boxes[_].Add(self.moo._request_area_csrf_token_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_csrf_token_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_csrf_url_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_csrf_url_entry, proportion_border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 2)
    request_data_area.Add(_boxes[0], spacing)
    request_data_area.Add(_boxes[1], spacing)
    request_data_area.Add(self.nb._request_data_hr1, spacing)
    request_data_area.Add(_boxes[2], spacing)
    request_data_area.Add(_boxes[3], spacing)
    request_data_area.Add(self.nb._request_data_hr2, spacing)
    request_data_area.Add(_boxes[4], spacing)
    request_data_area.Add(_boxes[5], spacing)
    return request_data_area

  def _request_custom(self):
    request_custom_area = StaticBoxSizer(self.moo._request_custom_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    _boxes = [BoxSizer() for _ in range(3)]
    _ = 0
    _boxes[_].Add(self.moo._request_area_ignore_timeouts_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_ignore_redirects_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_ignore_code_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_ignore_code_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_skip_urlencode_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_force_ssl_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_hpp_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_delay_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_delay_entry, border)
    _boxes[_].Add(self.moo._request_area_timeout_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_timeout_entry, border)
    _boxes[_].Add(self.moo._request_area_retries_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_retries_entry, border)
    _boxes[_].Add(self.moo._request_area_randomize_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_randomize_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_eval_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_eval_entry, proportion_border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 2)
    for _ in _boxes:
      request_custom_area.Add(_, spacing)

    return request_custom_area

  def _request_proxy(self):
    request_proxy_area = StaticBoxSizer(self.moo._request_proxy_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    _boxes = [BoxSizer() for _ in range(5)]
    _ = 0
    _boxes[_].Add(self.moo._request_area_safe_url_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_safe_url_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_safe_post_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_safe_post_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_safe_req_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_safe_req_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._request_area_safe_req_chooser, border)
    _boxes[_].Add(self.moo._request_area_safe_freq_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_safe_freq_entry, border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_ignore_proxy_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_proxy_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_proxy_file_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_proxy_file_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._request_area_proxy_file_chooser, border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_proxy_ip_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    _boxes[_].Add(self.moo._request_area_proxy_ip_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_proxy_port_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    _boxes[_].Add(self.moo._request_area_proxy_port_entry, border)
    _boxes[_].Add(self.moo._request_area_proxy_username_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    _boxes[_].Add(self.moo._request_area_proxy_username_entry, proportion_border)
    _boxes[_].Add(self.moo._request_area_proxy_password_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    _boxes[_].Add(self.moo._request_area_proxy_password_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._request_area_tor_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_tor_port_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_tor_port_entry, border)
    _boxes[_].Add(self.moo._request_area_tor_type_ckbtn, border)
    _boxes[_].Add(self.moo._request_area_tor_type_entry, border)
    _boxes[_].Add(self.moo._request_area_check_tor_ckbtn, border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 2)
    request_proxy_area.Add(_boxes[0], spacing)
    request_proxy_area.Add(_boxes[1], spacing)
    request_proxy_area.Add(self.nb._request_proxy_hr, spacing)
    request_proxy_area.Add(_boxes[2], spacing)
    request_proxy_area.Add(_boxes[3], spacing)
    request_proxy_area.Add(_boxes[4], spacing)

    return request_proxy_area

  def enumeration_sizer(self):
    hbox1 = BoxSizer()
    enum_area = self._enumeration_enum()
    dump_area = self._enumeration_dump()
    limit_area = self._enumeration_limit()
    blind_area = self._enumeration_blind()

    spacing = SizerFlags().Expand().Border(LEFT | RIGHT, 10)
    hbox1.Add(enum_area, spacing)
    hbox1.Add(dump_area, spacing)
    hbox1.Add(limit_area, spacing)
    hbox1.Add(blind_area, spacing)

    meta_area = self._enumeration_meta()
    runsql_area = self._enumeration_runsql()
    brute_force_area = self._enumeration_brute_force()

    vbox = BoxSizer(VERTICAL)
    vbox.Add(hbox1, flag = TOP, border = 10)
    vbox.Add(meta_area, flag = EXPAND | LEFT | RIGHT | TOP, border = 10)
    vbox.Add(runsql_area, flag = EXPAND | LEFT | RIGHT | TOP, border = 10)
    vbox.Add(brute_force_area, flag = LEFT | TOP, border = 10)
    return vbox

  def _enumeration_enum(self):
    enum_area = StaticBoxSizer(self.moo._enum_area, HORIZONTAL)

    _enu_area_opts_cols = [BoxSizer(VERTICAL) for _ in self.moo._enum_area_opts_ckbtns]

    spacing = SizerFlags().Border(LEFT | RIGHT, 13)
    for _i, _l in enumerate(self.moo._enum_area_opts_ckbtns):  # 三列
      for _ in _l:
        _enu_area_opts_cols[_i].Add(_)

      enum_area.Add(_enu_area_opts_cols[_i], spacing)

    return enum_area

  def _enumeration_dump(self):
    dump_area = StaticBoxSizer(self.moo._dump_area, VERTICAL)

    spacing = SizerFlags().Expand().Border(LEFT | RIGHT, 10)
    dump_area.Add(self.moo._dump_area_dump_ckbtn, spacing)
    dump_area.Add(self.moo._dump_area_repair_ckbtn, spacing)
    dump_area.Add(self.moo._dump_area_statements_ckbtn, spacing)
    _ = BoxSizer()
    _.Add(self.moo._dump_area_search_ckbtn)
    _.Add(self.moo._dump_area_no_sys_db_ckbtn, spacing)
    dump_area.Add(_, spacing)
    dump_area.Add(self.moo._dump_area_dump_all_ckbtn, spacing)
    return dump_area

  def _enumeration_limit(self):
    limit_area = StaticBoxSizer(self.moo._limit_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)

    row1 = BoxSizer()

    row1.Add(self.moo._limit_area_start_ckbtn, border)
    row1.Add(self.moo._limit_area_start_entry)
    row1.Add(self.nb._limit_area_start_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)

    row2 = BoxSizer()
    row2.Add(self.moo._limit_area_stop_ckbtn, border)
    row2.Add(self.moo._limit_area_stop_entry)
    row2.Add(self.nb._limit_area_stop_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 10)
    limit_area.Add(row1, spacing)
    limit_area.Add(row2, spacing)
    return limit_area

  def _enumeration_blind(self):
    blind_area = StaticBoxSizer(self.moo._blind_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)

    row1, row2, row3 = (BoxSizer() for _ in range(3))
    row1.Add(self.moo._blind_area_first_ckbtn, border)
    row1.Add(self.moo._blind_area_first_entry, border)
    row1.Add(self.nb._blind_area_first_label, flag = ALIGN_CENTER | LEFT, border = 5)
    row2.Add(self.moo._blind_area_last_ckbtn, border)
    row2.Add(self.moo._blind_area_last_entry, border)
    row2.Add(self.nb._blind_area_last_label, flag = ALIGN_CENTER | LEFT, border = 5)
    row3.Add(self.nb._blind_area_note_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 10)
    blind_area.Add(row1, spacing)
    blind_area.Add(row2, spacing)
    blind_area.Add(row3, spacing)
    return blind_area

  def _enumeration_meta(self):
    meta_area = StaticBoxSizer(self.moo._meta_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 10)
    proportion_border = SizerFlags(1).Border(RIGHT, 10)

    _boxes = [BoxSizer() for _ in range(3)]
    _boxes[0].Add(self.moo._meta_area_D_ckbtn, border)
    _boxes[0].Add(self.moo._meta_area_D_entry, proportion_border)
    _boxes[0].Add(self.moo._meta_area_T_ckbtn, border)
    _boxes[0].Add(self.moo._meta_area_T_entry, proportion_border)
    _boxes[0].Add(self.moo._meta_area_C_ckbtn, border)
    _boxes[0].Add(self.moo._meta_area_C_entry, proportion_border)
    _boxes[1].Add(self.moo._meta_area_U_ckbtn, border)
    _boxes[1].Add(self.moo._meta_area_U_entry, proportion_border)
    _boxes[1].Add(self.moo._meta_area_X_ckbtn, border)
    _boxes[1].Add(self.moo._meta_area_X_entry, proportion_border)
    _boxes[1].Add(self.moo._meta_area_pivot_ckbtn, border)
    _boxes[1].Add(self.moo._meta_area_pivot_entry, proportion_border)
    _boxes[2].Add(self.moo._meta_area_where_ckbtn, border)
    _boxes[2].Add(self.moo._meta_area_where_entry, proportion_border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 5)
    for _ in _boxes:
      meta_area.Add(_, spacing)

    return meta_area

  def _enumeration_runsql(self):
    runsql_area = StaticBoxSizer(self.moo._runsql_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 10)

    row1 = BoxSizer()
    row2 = BoxSizer()
    row1.Add(self.moo._runsql_area_sql_query_ckbtn, border)
    row1.Add(self.moo._runsql_area_sql_query_entry, proportion = 1, flag = RIGHT, border = 10)
    row2.Add(self.moo._runsql_area_sql_shell_ckbtn, border)
    row2.Add(self.moo._runsql_area_sql_file_ckbtn, border)
    row2.Add(self.moo._runsql_area_sql_file_entry, proportion = 1, flag = EXPAND)
    row2.Add(self.moo._runsql_area_sql_file_chooser, border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 6)
    runsql_area.Add(row1, spacing)
    runsql_area.Add(row2, spacing)
    return runsql_area

  def _enumeration_brute_force(self):
    brute_force_area = StaticBoxSizer(self.moo._brute_force_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 6)

    row1 = BoxSizer()
    row1.Add(self.nb._brute_force_area_label, flag = ALIGN_CENTER | LEFT, border = 6)
    row1.Add(self.moo._brute_force_area_common_tables_ckbtn, border)
    row1.Add(self.moo._brute_force_area_common_columns_ckbtn, border)
    row1.Add(self.moo._brute_force_area_common_files_ckbtn, border)

    brute_force_area.Add(row1, flag = EXPAND | ALL, border = 6)

    return brute_force_area

  def file_sizer(self):
    vbox = BoxSizer(VERTICAL)

    file_read_area = self._file_read()
    file_write_area = self._file_write()
    file_os_access_area = self._file_os_access()
    file_os_registry_area = self._file_os_registry()

    spacing = SizerFlags().Expand().Border(TOP | LEFT | RIGHT, 10)
    vbox.Add(self.nb._page1_file_note_label, spacing)
    vbox.Add(file_read_area, spacing)
    vbox.Add(file_write_area, spacing)
    vbox.Add(file_os_access_area, spacing)
    vbox.Add(file_os_registry_area, spacing)

    return vbox

  def _file_read(self):
    file_read_area = StaticBoxSizer(self.moo._file_read_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)

    row1 = BoxSizer()
    row1.Add(self.moo._file_read_area_file_read_ckbtn, border)
    row1.Add(self.moo._file_read_area_file_read_entry, proportion = 1)
    row1.Add(self.moo._file_read_area_file_read_btn, border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 6)
    file_read_area.Add(row1, spacing)

    return file_read_area

  def _file_write(self):
    file_write_area = StaticBoxSizer(self.moo._file_write_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    row1 = BoxSizer()
    row2 = BoxSizer()
    row3 = BoxSizer()
    row1.Add(self.moo._file_write_area_udf_ckbtn, border)
    row1.Add(self.moo._file_write_area_shared_lib_ckbtn, border)
    row1.Add(self.moo._file_write_area_shared_lib_entry, proportion = 1, flag = EXPAND)
    row1.Add(self.moo._file_write_area_shared_lib_chooser, border)
    row2.Add(self.moo._file_write_area_file_write_ckbtn, border)
    row2.Add(self.moo._file_write_area_file_write_entry, proportion = 1, flag = EXPAND)
    row2.Add(self.moo._file_write_area_file_write_chooser, border)
    row3.Add(self.moo._file_write_area_file_dest_ckbtn, border)
    row3.Add(self.moo._file_write_area_file_dest_entry, proportion_border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 6)
    file_write_area.Add(row1, spacing)
    file_write_area.Add(row2, spacing)
    file_write_area.Add(row3, spacing)
    return file_write_area

  def _file_os_access(self):
    file_os_access_area = StaticBoxSizer(self.moo._file_os_access_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    row1, row2, row3 = (BoxSizer() for _ in range(3))
    row1.Add(self.moo._file_os_access_os_cmd_ckbtn, border)
    row1.Add(self.moo._file_os_access_os_cmd_entry, proportion_border)
    row2.Add(self.moo._file_os_access_os_shell_ckbtn, border)
    row2.Add(self.nb._file_os_access_for_msf_label, flag = LEFT, border = 50)
    row2.Add(self.moo._file_os_access_os_pwn_ckbtn, border)
    row2.Add(self.moo._file_os_access_os_smbrelay_ckbtn, border)
    row2.Add(self.moo._file_os_access_os_bof_ckbtn, border)
    row2.Add(self.moo._file_os_access_priv_esc_ckbtn, border)
    row3.Add(self.moo._file_os_access_msf_path_ckbtn, border)
    row3.Add(self.moo._file_os_access_msf_path_entry, proportion = 1, flag = EXPAND)
    row3.Add(self.moo._file_os_access_msf_path_chooser, border)
    row3.Add(self.moo._file_os_access_tmp_path_ckbtn, border)
    row3.Add(self.moo._file_os_access_tmp_path_entry, proportion_border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 3)
    file_os_access_area.Add(row1, spacing)
    file_os_access_area.Add(row2, spacing)
    file_os_access_area.Add(row3, spacing)

    return file_os_access_area

  def _file_os_registry(self):
    file_os_registry_area = StaticBoxSizer(self.moo._file_os_registry_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    row1, row2, row3 = (BoxSizer() for _ in range(3))

    row1.Add(self.moo._file_os_registry_reg_ckbtn, border)
    row1.Add(self.moo._file_os_registry_reg_choice, border)
    row2.Add(self.moo._file_os_registry_reg_key_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    row2.Add(self.moo._file_os_registry_reg_key_entry, proportion_border)
    row2.Add(self.moo._file_os_registry_reg_value_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    row2.Add(self.moo._file_os_registry_reg_value_entry, proportion_border)
    row3.Add(self.moo._file_os_registry_reg_data_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    row3.Add(self.moo._file_os_registry_reg_data_entry, proportion_border)
    row3.Add(self.moo._file_os_registry_reg_type_label, flag = ALIGN_CENTER | LEFT | RIGHT, border = 5)
    row3.Add(self.moo._file_os_registry_reg_type_entry, proportion_border)

    file_os_registry_area.Add(row1, flag = EXPAND)
    file_os_registry_area.Add(row2, flag = EXPAND)
    file_os_registry_area.Add(row3, flag = EXPAND)

    return file_os_registry_area

  def other_sizer(self):
    vbox = BoxSizer(VERTICAL)

    page1_other_general_area = self._other_general()
    page1_other_misc_area = self._other_misc()

    expand_border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)

    vbox.Add(page1_other_general_area, expand_border)
    vbox.Add(page1_other_misc_area, expand_border)
    return vbox

  def _other_general(self):
    page1_other_general_area = StaticBoxSizer(self.moo._page1_other_general_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)
    # 一定有更好的办法...
    _boxes = [BoxSizer() for _ in range(10)]
    _ = 0
    _boxes[_].Add(self.moo._page1_general_check_internet_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_fresh_queries_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_forms_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_parse_errors_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_cleanup_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_table_prefix_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_table_prefix_entry, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_binary_fields_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_binary_fields_entry, border)
    _boxes[_].Add(self.moo._page1_general_preprocess_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_preprocess_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_preprocess_chooser, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_charset_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_charset_entry, proportion_border)
    _boxes[_].Add(self.moo._page1_general_encoding_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_encoding_entry, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_web_root_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_web_root_entry, proportion_border)
    _boxes[_].Add(self.moo._page1_general_scope_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_scope_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_scope_chooser, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_test_filter_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_test_filter_entry, proportion_border)
    _boxes[_].Add(self.moo._page1_general_test_skip_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_test_skip_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_crawl_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_crawl_entry, border)
    _boxes[_].Add(self.moo._page1_general_crawl_exclude_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_crawl_exclude_entry, proportion_border)
    _ += 1
    _boxes[_].Add(self.nb._page1_general_hr, proportion_border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_traffic_file_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_traffic_file_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_traffic_file_chooser, border)
    _boxes[_].Add(self.moo._page1_general_har_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_har_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_har_chooser, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_flush_session_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_dump_format_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_dump_format_entry, border)
    _boxes[_].Add(self.moo._page1_general_csv_del_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_csv_del_entry, border)
    _boxes[_].Add(self.moo._page1_general_save_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_save_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_save_chooser, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_general_session_file_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_session_file_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_session_file_chooser, border)
    _boxes[_].Add(self.moo._page1_general_output_dir_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_output_dir_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_general_output_dir_chooser, border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 3)
    for _ in _boxes:
      page1_other_general_area.Add(_, spacing)

    return page1_other_general_area

  def _other_misc(self):
    page1_other_misc_area = StaticBoxSizer(self.moo._page1_other_misc_area, VERTICAL)

    border = SizerFlags().Expand().Border(LEFT | RIGHT, 5)
    proportion_border = SizerFlags(1).Border(LEFT | RIGHT, 5)

    _boxes = [BoxSizer() for _ in range(4)]
    _ = 0
    _boxes[_].Add(self.moo._page1_misc_skip_waf_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_list_tampers_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_sqlmap_shell_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_disable_color_ckbtn, border)
    _boxes[_].Add(self.moo._page1_general_eta_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_update_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_misc_gpage_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_gpage_spinbtn)
    _boxes[_].Add(self.moo._page1_misc_beep_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_offline_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_purge_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_dependencies_ckbtn, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_misc_alert_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_alert_entry, proportion_border)
    _boxes[_].Add(self.moo._page1_misc_tmp_dir_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_tmp_dir_entry, proportion = 1, flag = EXPAND)
    _boxes[_].Add(self.moo._page1_misc_tmp_dir_chooser, border)
    _ += 1
    _boxes[_].Add(self.moo._page1_misc_answers_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_answers_entry, proportion_border)
    _boxes[_].Add(self.moo._page1_misc_z_ckbtn, border)
    _boxes[_].Add(self.moo._page1_misc_z_entry, proportion_border)

    spacing = SizerFlags().Expand().Border(TOP | BOTTOM, 3)
    for _ in _boxes:
      page1_other_misc_area.Add(_, spacing)

    page1_other_misc_area.Add(self.nb._dummy, spacing)
    return page1_other_misc_area


def main():
  pass


if __name__ == '__main__':
  main()
