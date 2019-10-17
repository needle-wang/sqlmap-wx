#!/usr/bin/env python3
#
# 2019年 05月 05日 星期日 20:43:40 CST

from widgets import wx, Panel, Scroll, nb, st, btn
from layout import Layout_opts

EVT_BUTTON = wx.EVT_BUTTON
EVT_CHECKBOX = wx.EVT_CHECKBOX


class Notebook(nb):
  def __init__(self, parent, model, handlers):
    '''
    最大的宽应该是由最长的 request定制的第一行 决定

    以"其他"标签的height作为标准高,
    高于此height的标签页使用ScrolledPanel, 显示滚动条
    '''
    super().__init__(parent)
    self.m = model
    layout = Layout_opts(self, model)

    self._handlers = handlers
    # 选项区 - 设置, 请求, 枚举, 文件, 其他
    page1_setting = self.build_page1_setting(layout)
    page1_request = self.build_page1_request(layout)
    page1_enumeration = self.build_page1_enumeration(layout)
    page1_file = self.build_page1_file(layout)
    page1_other = self.build_page1_other(layout)

    self.AddPage(page1_setting, '测试(Q)')
    self.AddPage(page1_request, '请求(W)')
    self.AddPage(page1_enumeration, '枚举(E)')
    self.AddPage(page1_file, '文件(R)')
    self.AddPage(page1_other, '其他(T)')

  def cb_single(self, event, checkbox):
    cb = event.GetEventObject()
    if cb.IsChecked():
      checkbox.SetValue(False)
    # 这是最后一个Bind, 要skip哈! 不然改不了颜色
    event.Skip()

  def optimize_area_controller(self, event):
    if self.m._optimize_area_turn_all_ckbtn.IsChecked():
      self.m._optimize_area_predict_ckbtn.SetValue(False)
      self.m._optimize_area_keep_alive_ckbtn.SetValue(False)
      self.m._optimize_area_null_connect_ckbtn.SetValue(False)

      self.m._optimize_area_predict_ckbtn.Disable()
      self.m._optimize_area_keep_alive_ckbtn.Disable()
      self.m._optimize_area_null_connect_ckbtn.Disable()
    else:
      self.m._optimize_area_predict_ckbtn.Enable()
      self.m._optimize_area_keep_alive_ckbtn.Enable()
      self.m._optimize_area_null_connect_ckbtn.Enable()
    # 这是最后一个Bind, 要skip哈! 不然改不了颜色
    event.Skip()

  def build_page1_setting(self, layout):
    p = Scroll(self)
    m = self.m

    m._sqlmap_path_label.Create(p, label = '指定sqlmap路径:')
    m.sqlmap_path_entry.Create(p, value = 'sqlmap')
    m._sqlmap_path_chooser.Create(p, label = '打开')
    m._sqlmap_path_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m.sqlmap_path_entry]:
        self._handlers.set_file_entry_text(evt, data))

    self.build_page1_setting_inject(p, m)
    self.build_page1_setting_detection(p, m)
    self.build_page1_setting_tech(p, m)
    self.build_page1_setting_tamper(p, m)
    self.build_page1_setting_optimize(p, m)
    self.build_page1_setting_general(p, m)

    vbox = layout.setting_sizer()
    # 不能用SetSizerAndFit, Fit会自适应的, 从而没有滚动条
    # p.SetSizerAndFit(vbox)
    p.SetSizer(vbox)
    p.SetupScrolling(scroll_x = False, scrollIntoView = False)
    return p

  def build_page1_setting_inject(self, panel, m):
    _sb = m._inject_area
    _sb.Create(panel, label = '注入选项')

    _choices = ['GET', 'POST', 'URI', 'Cookie', 'User-Agent'
                'Referer', 'Host', '(custom) POST', '(custom HEADER)']

    m._inject_area_param_ckbtn.Create(_sb, label = '仅测参数')
    m._inject_area_param_entry.Create(_sb)
    m._inject_area_param_filter_ckbtn.Create(_sb, label = '仅测范围')
    m._inject_area_param_filter_combobox.Create(_sb, choices = _choices)
    m._inject_area_skip_static_ckbtn.Create(_sb, label = '跳过不像是动态的参数')
    m._inject_area_skip_static_ckbtn.SetValue(True)
    m._inject_area_skip_ckbtn.Create(_sb, label = '忽略参数')
    m._inject_area_skip_entry.Create(_sb)
    m._inject_area_param_exclude_ckbtn.Create(_sb, label = '忽略参数(正则)')
    m._inject_area_param_exclude_entry.Create(_sb)
    m._inject_area_prefix_ckbtn.Create(_sb, label = 'payload前缀')
    m._inject_area_prefix_entry.Create(_sb)
    m._inject_area_suffix_ckbtn.Create(_sb, label = 'payload后缀')
    m._inject_area_suffix_entry.Create(_sb)
    m._inject_area_dbms_ckbtn.Create(_sb, label = '固定DBMS为')
    m._inject_area_dbms_combobox.Create(_sb, choices = ['mysql', 'sqlite', 'sqlserver'])
    m._inject_area_dbms_cred_ckbtn.Create(_sb, label = 'DB认证')
    m._inject_area_dbms_cred_entry.Create(_sb)
    m._inject_area_os_ckbtn.Create(_sb, label = '固定OS为')
    m._inject_area_os_entry.Create(_sb)
    m._inject_area_no_cast_ckbtn.Create(_sb, label = '关闭数据类型转换')
    m._inject_area_no_escape_ckbtn.Create(_sb, label = '关掉string转义')
    self._inject_area_invalid_label = st(_sb, label = '对payload中无效值:')
    self._inject_area_invalid_label.SetToolTip('默认情况下, 要使原参数值无效时会改成相反数\n'
        '真: id=13 假: id=-13')
    m._inject_area_invalid_logic_ckbtn.Create(_sb, label = '使用布尔运算')
    m._inject_area_invalid_bignum_ckbtn.Create(_sb, label = '使用大数')
    m._inject_area_invalid_str_ckbtn.Create(_sb, label = '使用随机字串')

  def build_page1_setting_detection(self, panel, m):
    _sb = m._detection_area
    _sb.Create(panel, label = '探测选项')

    m._detection_area_level_ckbtn.Create(_sb, label = '探测等级(范围)')
    m._detection_area_level_scale.Create(_sb,
                                         value = 1,
                                         minValue = 1,
                                         maxValue = 5,
                                         style = wx.SL_VALUE_LABEL)
    m._detection_area_risk_ckbtn.Create(_sb, label = 'payload危险等级')
    m._detection_area_risk_scale.Create(_sb,
                                        value = 1,
                                        minValue = 1,
                                        maxValue = 3,
                                        style = wx.SL_VALUE_LABEL)
    m._detection_area_str_ckbtn.Create(_sb, label = '指定字符串')
    m._detection_area_str_entry.Create(_sb)
    m._detection_area_not_str_ckbtn.Create(_sb, label = '指定字符串')
    m._detection_area_not_str_entry.Create(_sb)
    m._detection_area_re_ckbtn.Create(_sb, label = '指定正则')
    m._detection_area_re_entry.Create(_sb)
    m._detection_area_code_ckbtn.Create(_sb, label = '指定http状态码')
    m._detection_area_code_entry.Create(_sb)
    m._detection_area_text_only_ckbtn.Create(_sb, label = '仅对比文本')
    m._detection_area_titles_ckbtn.Create(_sb, label = '仅对比title')

    m._detection_area_text_only_ckbtn.Bind(
      EVT_CHECKBOX,
      lambda evt, cbtmp = m._detection_area_titles_ckbtn:
        self.cb_single(evt, cbtmp))
    m._detection_area_titles_ckbtn.Bind(
      EVT_CHECKBOX,
      lambda evt, cbtmp = m._detection_area_text_only_ckbtn:
        self.cb_single(evt, cbtmp))

    m._detection_area_smart_ckbtn.Create(_sb, label = '寻找明显目标并测试')

    self._detection_area_hr = wx.StaticLine(_sb)
    self._detection_area_level_note = st(_sb,
        label = 'Level 1(默认): 所有GET, POST参数\n'
                'Level 2  追加: Cookie\n'
                'Level 3  追加: User-Agent/Referer\n'
                'Level 4  追加: 啥?\n'
                'Level 5  追加: Host报头')
    self._detection_area_risk_note = st(_sb,
        label = 'Risk 1(默认): 基本无风险\n'
                'Risk 2  追加: 大量时间型盲注\n'
                'Risk 3  追加: OR型布尔盲注')

  def build_page1_setting_tech(self, panel, m):
    _sb = m._tech_area
    _sb.Create(panel, label = '各注入技术的选项')

    m._tech_area_tech_ckbtn.Create(_sb, label = '注入技术')
    m._tech_area_tech_entry.Create(_sb)
    m._tech_area_tech_entry.SetInitialSize(
        m._tech_area_tech_entry.GetSizeFromTextSize(
          m._tech_area_tech_entry.GetTextExtent("a" * 15).x))
    m._tech_area_time_sec_ckbtn.Create(_sb, label = '指定DB延迟多少秒响应')
    m._tech_area_time_sec_entry.Create(_sb)
    m._tech_area_union_col_ckbtn.Create(_sb, label = '指定最大union列数')
    m._tech_area_union_col_entry.Create(_sb)
    m._tech_area_union_char_ckbtn.Create(_sb, label = '指定枚举列数时所用字符')
    m._tech_area_union_char_entry.Create(_sb)
    m._tech_area_union_from_ckbtn.Create(_sb, label = '指定枚举列数时from的表名')
    m._tech_area_union_from_entry.Create(_sb)
    m._tech_area_dns_ckbtn.Create(_sb, label = '指定DNS')
    m._tech_area_dns_entry.Create(_sb)
    m._tech_area_second_url_ckbtn.Create(_sb, label = '指定二阶响应的url')
    m._tech_area_second_url_entry.Create(_sb)
    m._tech_area_second_req_ckbtn.Create(_sb, label = '使用含二阶HTTP请求的文件:')
    m._tech_area_second_req_entry.Create(_sb)
    m._tech_area_second_req_chooser.Create(_sb, label = '打开')
    m._tech_area_second_req_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._tech_area_second_req_entry]:
        self._handlers.set_file_entry_text(evt, data))

  def build_page1_setting_tamper(self, panel, m):
    _sb = m._tamper_area
    _sb.Create(panel, label = 'tamper脚本')

    # 多行文本框的默认size太小了
    m._tamper_area_tamper_view.Create(_sb,
                                      size = (300, -1),
                                      style = wx.TE_MULTILINE)

  def build_page1_setting_optimize(self, panel, m):
    _sb = m._optimize_area
    _sb.Create(panel, label = '性能优化')

    m._optimize_area_turn_all_ckbtn.Create(_sb, label = '启用所有优化选项')
    m._optimize_area_thread_num_ckbtn.Create(_sb, label = '使用线程数:')
    m._optimize_area_thread_num_spinbtn.Create(_sb, value = '2', min = 2, max = 10000)
    m._optimize_area_predict_ckbtn.Create(_sb, label = '预测通常的查询结果')
    m._optimize_area_keep_alive_ckbtn.Create(_sb, label = 'http连接使用keep-alive')
    m._optimize_area_null_connect_ckbtn.Create(_sb, label = '只比较响应大小报头, 不获取响应主体')

    m._optimize_area_turn_all_ckbtn.Bind(EVT_CHECKBOX, self.optimize_area_controller)

  def build_page1_setting_general(self, panel, m):
    _sb = m._general_area
    _sb.Create(panel, label = '常用选项')

    m._general_area_verbose_ckbtn.Create(_sb, label = '输出详细程度')
    m._general_area_verbose_scale.Create(_sb,
                                         value = 1,
                                         minValue = 0,
                                         maxValue = 6,
                                         style = wx.SL_VALUE_LABEL)
    m._general_area_finger_ckbtn.Create(_sb, label = '精确检测DB等版本信息')
    m._general_area_hex_ckbtn.Create(_sb, label = '响应使用hex转换')
    m._general_area_batch_ckbtn.Create(_sb, label = '非交互模式, 一切皆默认')
    m._page1_misc_wizard_ckbtn.Create(_sb, label = '新手向导')

  def build_page1_request(self, layout):
    p = Scroll(self, style = wx.BORDER_THEME)
    m = self.m

    self.build_page1_request_header(p, m)
    self.build_page1_request_data(p, m)
    self.build_page1_request_custom(p, m)
    self.build_page1_request_proxy(p, m)

    vbox = layout.request_sizer()
    # 不能用SetSizerAndFit, Fit会自适应的, 从而没有滚动条
    # p.SetSizerAndFit(vbox)
    p.SetSizer(vbox)
    p.SetupScrolling(scroll_x = False, scrollIntoView = False)
    return p

  def build_page1_request_header(self, panel, m):
    _sb = m._request_header_area
    _sb.Create(panel, label = 'HTTP header')

    m._request_area_random_agent_ckbtn.Create(_sb, label = '随机User-Agent头')
    m._request_area_random_agent_ckbtn.SetValue(True)
    m._request_area_mobile_ckbtn.Create(_sb, label = '模拟手机请求')
    m._request_area_user_agent_ckbtn.Create(_sb, label = '指定User-Agent头')
    m._request_area_user_agent_entry.Create(_sb)
    m._request_area_host_ckbtn.Create(_sb, label = 'Host头')
    m._request_area_host_entry.Create(_sb)
    m._request_area_referer_ckbtn.Create(_sb, label = 'referer头')
    m._request_area_referer_entry.Create(_sb)
    m._request_area_header_ckbtn.Create(_sb, label = '额外的header(-H)')
    m._request_area_header_entry.Create(_sb)
    m._request_area_headers_ckbtn.Create(_sb, label = '额外的headers')
    m._request_area_headers_entry.Create(_sb)

  def build_page1_request_data(self, panel, m):
    _sb = m._request_data_area
    _sb.Create(panel, label = 'HTTP data')

    m._request_area_method_ckbtn.Create(_sb, label = 'HTTP请求方式')
    m._request_area_method_entry.Create(_sb)
    m._request_area_param_del_ckbtn.Create(_sb, label = '指定分隔data参数值的字符')
    m._request_area_param_del_entry.Create(_sb)
    m._request_area_chunked_ckbtn.Create(_sb, label = '"分块传输"发送POST请求')
    m._request_area_post_ckbtn.Create(_sb, label = '通过POST提交data:')
    self._request_data_hr1 = wx.StaticLine(_sb)
    m._request_area_post_entry.Create(_sb)
    m._request_area_cookie_ckbtn.Create(_sb, label = '请求中要包含的Cookie:')
    m._request_area_cookie_entry.Create(_sb)
    m._request_area_cookie_del_ckbtn.Create(_sb, label = '指定cookie分隔符')
    m._request_area_cookie_del_entry.Create(_sb)
    m._request_area_load_cookies_ckbtn.Create(_sb, label = '本地Cookie文件')
    m._request_area_load_cookies_entry.Create(_sb)
    m._request_area_load_cookies_chooser.Create(_sb, label = '打开')
    m._request_area_load_cookies_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._request_area_load_cookies_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._request_area_drop_set_cookie_ckbtn.Create(_sb, label = '丢弃Set-Cookie头')
    self._request_data_hr2 = wx.StaticLine(_sb)
    m._request_area_auth_type_ckbtn.Create(_sb, label = 'http认证类型')
    m._request_area_auth_type_entry.Create(_sb)
    m._request_area_auth_cred_ckbtn.Create(_sb, label = 'http认证账密')
    m._request_area_auth_cred_entry.Create(_sb)
    m._request_area_auth_file_ckbtn.Create(_sb, label = 'http认证文件')
    m._request_area_auth_file_entry.Create(_sb)
    m._request_area_auth_file_chooser.Create(_sb, label = '打开')
    m._request_area_auth_file_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._request_area_auth_file_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._request_area_csrf_method_ckbtn.Create(_sb, label = 'csrf_method')
    m._request_area_csrf_method_entry.Create(_sb)
    m._request_area_csrf_token_ckbtn.Create(_sb, label = 'csrf_token')
    m._request_area_csrf_token_entry.Create(_sb)
    m._request_area_csrf_url_ckbtn.Create(_sb, label = '获取csrf_token的url')
    m._request_area_csrf_url_entry.Create(_sb)

  def build_page1_request_custom(self, panel, m):
    _sb = m._request_custom_area
    _sb.Create(panel, label = 'request定制')

    m._request_area_ignore_timeouts_ckbtn.Create(_sb, label = '忽略连接超时')
    m._request_area_ignore_redirects_ckbtn.Create(_sb, label = '忽略重定向')
    m._request_area_ignore_code_ckbtn.Create(_sb, label = '忽略错误型状态码:')
    m._request_area_ignore_code_entry.Create(_sb, value = '401')
    m._request_area_ignore_code_entry.SetInitialSize(
        m._request_area_ignore_code_entry.GetSizeFromTextSize(
          m._request_area_ignore_code_entry.GetTextExtent("a" * 20).x))
    m._request_area_skip_urlencode_ckbtn.Create(_sb, label = 'payload不使用url编码')
    m._request_area_force_ssl_ckbtn.Create(_sb, label = '强制使用HTTPS')
    m._request_area_hpp_ckbtn.Create(_sb, label = 'HTTP参数污染')
    m._request_area_delay_ckbtn.Create(_sb, label = '请求间隔(秒)')
    m._request_area_delay_entry.Create(_sb)
    m._request_area_timeout_ckbtn.Create(_sb, label = '超时前等几秒')
    m._request_area_timeout_entry.Create(_sb, value = '30')
    m._request_area_retries_ckbtn.Create(_sb, label = '超时重试次数')
    m._request_area_retries_entry.Create(_sb, value = '3')
    m._request_area_randomize_ckbtn.Create(_sb, label = '指定要随机改变值的参数')
    m._request_area_randomize_entry.Create(_sb)
    m._request_area_eval_ckbtn.Create(_sb, label = '--eval=')
    m._request_area_eval_entry.Create(_sb)

  def build_page1_request_proxy(self, panel, m):
    _sb = m._request_proxy_area
    _sb.Create(panel, label = '隐匿/代理')

    m._request_area_safe_url_ckbtn.Create(_sb, label = '顺便掺杂地访问一个安全url')
    m._request_area_safe_url_entry.Create(_sb)
    m._request_area_safe_post_ckbtn.Create(_sb, label = '提交到安全url的post数据')
    m._request_area_safe_post_entry.Create(_sb)
    m._request_area_safe_req_ckbtn.Create(_sb, label = '从文件载入safe HTTP请求')
    m._request_area_safe_req_entry.Create(_sb)
    m._request_area_safe_req_chooser.Create(_sb, label = '打开')

    m._request_area_safe_req_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._request_area_safe_req_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._request_area_safe_freq_ckbtn.Create(_sb, label = '访问安全url的频率')
    m._request_area_safe_freq_entry.Create(_sb)
    self._request_proxy_hr = wx.StaticLine(_sb)
    m._request_area_ignore_proxy_ckbtn.Create(_sb, label = '忽略系统默认代理')
    m._request_area_proxy_ckbtn.Create(_sb, label = '使用代理')
    m._request_area_proxy_file_ckbtn.Create(_sb, label = '代理列表文件')
    m._request_area_proxy_file_entry.Create(_sb)
    m._request_area_proxy_file_chooser.Create(_sb, label = '打开')

    m._request_area_proxy_file_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._request_area_proxy_file_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._request_area_proxy_ip_label.Create(_sb, label = 'IP:')
    m._request_area_proxy_ip_entry.Create(_sb)
    m._request_area_proxy_port_label.Create(_sb, label = 'PORT:')
    m._request_area_proxy_port_entry.Create(_sb)
    m._request_area_proxy_username_label.Create(_sb, label = 'username:')
    m._request_area_proxy_username_entry.Create(_sb)
    m._request_area_proxy_password_label.Create(_sb, label = 'password:')
    m._request_area_proxy_password_entry.Create(_sb)
    m._request_area_tor_ckbtn.Create(_sb, label = '使用Tor匿名网络')
    m._request_area_tor_port_ckbtn.Create(_sb, label = 'Tor端口:')
    m._request_area_tor_port_entry.Create(_sb)
    m._request_area_tor_type_ckbtn.Create(_sb, label = 'Tor代理类型')
    m._request_area_tor_type_entry.Create(_sb)
    m._request_area_check_tor_ckbtn.Create(_sb, label = '检查Tor连接')

  def build_page1_enumeration(self, layout):
    p = Panel(self)
    m = self.m

    self.build_page1_enumeration_enum(p, m)
    self.build_page1_enumeration_dump(p, m)
    self.build_page1_enumeration_limit(p, m)
    self.build_page1_enumeration_blind(p, m)
    self.build_page1_enumeration_meta(p, m)
    self.build_page1_enumeration_runsql(p, m)
    self.build_page1_enumeration_brute_force(p, m)

    vbox = layout.enumeration_sizer()
    p.SetSizer(vbox)
    return p

  def build_page1_enumeration_enum(self, panel, m):
    _sb = m._enum_area
    _sb.Create(panel, label = '枚举')
    # 要求要与_enum_area_opts_ckbtns的结构一致!
    _enum_area_enum_labels = (
      ('DB banner', '当前用户', '当前数据库', '主机名', '是否为DBA'),
      ('用户', '密码', '权限', '角色', '库名'),
      ('表名', '列名', '架构', '行数', '备注'))
    for _i, _l in enumerate(m._enum_area_opts_ckbtns):  # 三列
      for _j, _cb in enumerate(_l):
        _cb.Create(_sb, label = _enum_area_enum_labels[_i][_j])

  def build_page1_enumeration_dump(self, panel, m):
    _sb = m._dump_area
    _sb.Create(panel, label = 'Dump(转储)')

    m._dump_area_dump_ckbtn.Create(_sb, label = 'dump(某库某表的条目)')
    m._dump_area_repair_ckbtn.Create(_sb, label = '重新获取有未知符号(?)的条目')
    m._dump_area_statements_ckbtn.Create(_sb, label = '获取正在运行的sql语句')
    m._dump_area_search_ckbtn.Create(_sb, label = '搜索')
    m._dump_area_no_sys_db_ckbtn.Create(_sb, label = '排除系统库')
    m._dump_area_dump_all_ckbtn.Create(_sb, label = '全部dump(拖库)')

  def build_page1_enumeration_limit(self, panel, m):
    _sb = m._limit_area
    _sb.Create(panel, label = 'limit(dump时的限制)')

    m._limit_area_start_ckbtn.Create(_sb, label = '始于第')
    m._limit_area_start_entry.Create(_sb)
    m._limit_area_start_entry.SetInitialSize(
        m._limit_area_start_entry.GetSizeFromTextSize(
          m._limit_area_start_entry.GetTextExtent("a" * 15).x))
    self._limit_area_start_label = st(_sb, label = '行')
    m._limit_area_stop_ckbtn.Create(_sb, label = '止于第')
    m._limit_area_stop_entry.Create(_sb)
    m._limit_area_stop_entry.SetInitialSize(
        m._limit_area_stop_entry.GetSizeFromTextSize(
          m._limit_area_stop_entry.GetTextExtent("a" * 15).x))
    self._limit_area_stop_label = st(_sb, label = '行')

  def build_page1_enumeration_blind(self, panel, m):
    _sb = m._blind_area
    _sb.Create(panel, label = '盲注选项')

    m._blind_area_first_ckbtn.Create(_sb, label = '从第')
    m._blind_area_first_entry.Create(_sb)
    self._blind_area_first_label = st(_sb, label = '个字符')
    m._blind_area_last_ckbtn.Create(_sb, label = '到第')
    m._blind_area_last_entry.Create(_sb)
    self._blind_area_last_label = st(_sb, label = '个字符')
    self._blind_area_note_label = st(_sb, label = '只适用于盲注,\n因为报错,union注入要求列数相同')

  def build_page1_enumeration_meta(self, panel, m):
    _sb = m._meta_area
    _sb.Create(panel, label = '数据库名, 表名, 列名...')

    m._meta_area_D_ckbtn.Create(_sb, label = '指定库名')
    m._meta_area_D_entry.Create(_sb)
    m._meta_area_T_ckbtn.Create(_sb, label = '指定表名')
    m._meta_area_T_entry.Create(_sb)
    m._meta_area_C_ckbtn.Create(_sb, label = '指定列名')
    m._meta_area_C_entry.Create(_sb)
    m._meta_area_U_ckbtn.Create(_sb, label = '指定用户')
    m._meta_area_U_entry.Create(_sb)
    m._meta_area_X_ckbtn.Create(_sb, label = '排除标志符')
    m._meta_area_X_entry.Create(_sb)
    m._meta_area_pivot_ckbtn.Create(_sb, label = '指定Pivot列名')
    m._meta_area_pivot_entry.Create(_sb)
    m._meta_area_where_ckbtn.Create(_sb, label = 'where子句')
    m._meta_area_where_entry.Create(_sb)

  def build_page1_enumeration_runsql(self, panel, m):
    _sb = m._runsql_area
    _sb.Create(panel, label = '执行SQL语句')

    m._runsql_area_sql_query_ckbtn.Create(_sb, label = 'SQL语句:')
    m._runsql_area_sql_query_entry.Create(_sb)
    m._runsql_area_sql_shell_ckbtn.Create(_sb, label = '打开一个SQL交互shell')
    m._runsql_area_sql_file_ckbtn.Create(_sb, label = '本地SQL文件:')
    m._runsql_area_sql_file_entry.Create(_sb)
    m._runsql_area_sql_file_chooser.Create(_sb, label = '打开')
    m._runsql_area_sql_file_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._runsql_area_sql_file_entry]:
        self._handlers.set_file_entry_text(evt, data))

  def build_page1_enumeration_brute_force(self, panel, m):
    _sb = m._brute_force_area
    _sb.Create(panel, label = '暴破表名/列名')

    self._brute_force_area_label = st(_sb, label = '检查是否存在:')
    m._brute_force_area_common_tables_ckbtn.Create(_sb, label = '常用表名')
    m._brute_force_area_common_columns_ckbtn.Create(_sb, label = '常用列名')
    m._brute_force_area_common_files_ckbtn.Create(_sb, label = '常用文件')

  def build_page1_file(self, layout):
    p = Panel(self)
    m = self.m

    self._page1_file_note_label = st(p,
        label = '注: 存在Stacked queries(堆查询注入)时, '
                '才能使用该标签下的功能(udf功能除外)!')
    self.build_page1_file_read(p, m)
    self.build_page1_file_write(p, m)
    self.build_page1_file_os_access(p, m)
    self.build_page1_file_os_registry(p, m)

    vbox = layout.file_sizer()
    p.SetSizer(vbox)
    return p

  def build_page1_file_read(self, panel, m):
    _sb = m._file_read_area
    _sb.Create(panel, label = '读取远程文件')

    m._file_read_area_file_read_ckbtn.Create(_sb, label = '远程文件路径(--file-read=)')
    m._file_read_area_file_read_entry.Create(_sb, value = '/etc/passwd')
    m._file_read_area_file_read_btn.Create(_sb, label = '查看')

    m._file_read_area_file_read_btn.Bind(EVT_BUTTON, self._handlers.read_dumped_file)

  def build_page1_file_write(self, panel, m):
    _sb = m._file_write_area
    _sb.Create(panel, label = '文件上传')

    m._file_write_area_udf_ckbtn.Create(_sb, label = '注入UDF(仅限MySQL和PostgreSQL)')
    m._file_write_area_shared_lib_ckbtn.Create(_sb, label = '本地共享库路径(--shared-lib=)')
    m._file_write_area_shared_lib_entry.Create(_sb)
    m._file_write_area_shared_lib_chooser.Create(_sb, label = '打开')
    m._file_write_area_shared_lib_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._file_write_area_shared_lib_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._file_write_area_file_write_ckbtn.Create(_sb, label = '本地文件路径(--file-write=)')
    m._file_write_area_file_write_entry.Create(_sb)
    m._file_write_area_file_write_chooser.Create(_sb, label = '打开')
    m._file_write_area_file_write_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._file_write_area_file_write_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._file_write_area_file_dest_ckbtn.Create(_sb, label = '远程文件路径(--file-dest=)')
    m._file_write_area_file_dest_entry.Create(_sb)

  def build_page1_file_os_access(self, panel, m):
    _sb = m._file_os_access_area
    _sb.Create(panel, label = '访问后端OS')

    m._file_os_access_os_cmd_ckbtn.Create(_sb, label = '执行CLI命令')
    m._file_os_access_os_cmd_entry.Create(_sb)
    m._file_os_access_os_shell_ckbtn.Create(_sb, label = '获取交互shell')
    self._file_os_access_for_msf_label = st(_sb, label = 'Meterpreter相关(TCP连接):')
    m._file_os_access_os_pwn_ckbtn.Create(_sb, label = '--os-pwn')
    m._file_os_access_os_smbrelay_ckbtn.Create(_sb, label = '--os-smbrelay')
    m._file_os_access_os_bof_ckbtn.Create(_sb, label = '--os-bof')
    m._file_os_access_priv_esc_ckbtn.Create(_sb, label = '--priv-esc')
    m._file_os_access_msf_path_ckbtn.Create(_sb, label = '本地Metasploit安装路径')
    m._file_os_access_msf_path_entry.Create(_sb)
    m._file_os_access_msf_path_chooser.Create(_sb, label = '打开')
    m._file_os_access_msf_path_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._file_os_access_msf_path_entry, '选择 本地Metasploit安装目录']:
        self._handlers.set_file_entry_text(evt, data))

    m._file_os_access_tmp_path_ckbtn.Create(_sb, label = '远程临时目录(绝对路径)')
    m._file_os_access_tmp_path_entry.Create(_sb)

  def build_page1_file_os_registry(self, panel, m):
    _sb = m._file_os_registry_area
    _sb.Create(panel, label = '访问WIN下注册表')

    m._file_os_registry_reg_ckbtn.Create(_sb, label = '键值操作:')
    m._file_os_registry_reg_choice.Create(_sb,
                                          choices = ['--reg-read', '--reg-add', '--reg-del'])
    m._file_os_registry_reg_choice.SetSelection(0)
    m._file_os_registry_reg_key_label.Create(_sb, label = '键路径')
    m._file_os_registry_reg_key_entry.Create(_sb)
    m._file_os_registry_reg_value_label.Create(_sb, label = '键名')
    m._file_os_registry_reg_value_entry.Create(_sb)
    m._file_os_registry_reg_data_label.Create(_sb, label = '键值')
    m._file_os_registry_reg_data_entry.Create(_sb)
    m._file_os_registry_reg_type_label.Create(_sb, label = '键值类型')
    m._file_os_registry_reg_type_entry.Create(_sb)

  def build_page1_other(self, layout):
    p = Panel(self)
    # p = Scroll(self)  # 总有一个标签会被掩盖widget, 只能使用_dummy
    m = self.m

    self.build_page1_other_general(p, m)
    self.build_page1_other_misc(p, m)

    vbox = layout.other_sizer()
    # p.SetSizerAndFit(vbox), 没用~, 最后一个widget还是会被掩盖
    p.SetSizer(vbox)
    # p.SetupScrolling(scroll_x = False)
    return p

  def build_page1_other_general(self, panel, m):
    _sb = m._page1_other_general_area
    _sb.Create(panel, label = '通用项')

    m._page1_general_check_internet_ckbtn.Create(_sb, label = '检查与目标的网络连接')
    m._page1_general_fresh_queries_ckbtn.Create(_sb, label = '刷新此次查询')
    m._page1_general_forms_ckbtn.Create(_sb, label = '获取form表单参数并测试')
    m._page1_general_parse_errors_ckbtn.Create(_sb, label = '解析并显示响应中的错误信息')
    m._page1_misc_cleanup_ckbtn.Create(_sb, label = '清理DBMS中的入侵痕迹!')
    m._page1_general_table_prefix_ckbtn.Create(_sb, label = '临时表前缀')
    m._page1_general_table_prefix_entry.Create(_sb)
    # size = ()是以px为单位的, 如果想设成以字符长度为宽, 蛋疼如下~~:
    m._page1_general_table_prefix_entry.SetInitialSize(
        m._page1_general_table_prefix_entry.GetSizeFromTextSize(
          m._page1_general_table_prefix_entry.GetTextExtent("a" * 16).x))
    m._page1_general_binary_fields_ckbtn.Create(_sb, label = '有二进制值的字段')
    m._page1_general_binary_fields_entry.Create(_sb)
    m._page1_general_binary_fields_entry.SetInitialSize(
        m._page1_general_binary_fields_entry.GetSizeFromTextSize(
          m._page1_general_binary_fields_entry.GetTextExtent("a" * 16).x))
    m._page1_general_preprocess_ckbtn.Create(_sb, label = '指定预处理响应数据的脚本')
    m._page1_general_preprocess_entry.Create(_sb)
    m._page1_general_preprocess_chooser.Create(_sb, label = '打开')
    m._page1_general_preprocess_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_general_preprocess_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._page1_general_charset_ckbtn.Create(_sb, label = '盲注所用的字符集合')
    m._page1_general_charset_entry.Create(_sb, value = '0123456789abcdef')
    m._page1_general_encoding_ckbtn.Create(_sb, label = '字符编码(用于数据获取)')
    m._page1_general_encoding_entry.Create(_sb)
    m._page1_general_web_root_ckbtn.Create(_sb, label = '远程web的根目录')
    m._page1_general_web_root_entry.Create(_sb)
    m._page1_general_scope_ckbtn.Create(_sb, label = '从代理日志过滤出目标(正则)')
    m._page1_general_scope_entry.Create(_sb)
    m._page1_general_scope_chooser.Create(_sb, label = '打开')
    m._page1_general_scope_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_general_scope_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._page1_general_test_filter_ckbtn.Create(_sb, label = '测试过滤器(从payload/title选择)')
    m._page1_general_test_filter_entry.Create(_sb)
    m._page1_general_test_skip_ckbtn.Create(_sb, label = '测试跳过(从payload/title选择)')
    m._page1_general_test_skip_entry.Create(_sb)

    m._page1_general_crawl_ckbtn.Create(_sb, label = '爬网站(的层级/深度)')
    m._page1_general_crawl_entry.Create(_sb)
    m._page1_general_crawl_exclude_ckbtn.Create(_sb, label = '爬站时排除(正则)页面')
    m._page1_general_crawl_exclude_entry.Create(_sb)
    self._page1_general_hr = wx.StaticLine(_sb)
    m._page1_general_traffic_file_ckbtn.Create(_sb, label = '转存所有http流量到文本')
    m._page1_general_traffic_file_entry.Create(_sb)
    m._page1_general_traffic_file_chooser.Create(_sb, label = '打开')
    m._page1_general_traffic_file_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_general_traffic_file_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._page1_general_har_ckbtn.Create(_sb, label = '转存至HAR文件')
    m._page1_general_har_entry.Create(_sb)
    m._page1_general_har_chooser.Create(_sb, label = '打开')
    m._page1_general_har_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_general_har_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._page1_general_flush_session_ckbtn.Create(_sb, label = '清空目标的会话文件')
    m._page1_general_dump_format_ckbtn.Create(_sb, label = 'dump结果的文件格式')
    m._page1_general_dump_format_entry.Create(_sb)
    m._page1_general_csv_del_ckbtn.Create(_sb, label = '(csv文件的)分隔符')
    m._page1_general_csv_del_entry.Create(_sb, value = ',')
    m._page1_general_save_ckbtn.Create(_sb, label = '保存选项至INI文件')
    m._page1_general_save_entry.Create(_sb)
    m._page1_general_save_chooser.Create(_sb, label = '打开')
    m._page1_general_save_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_general_save_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._page1_general_session_file_ckbtn.Create(_sb, label = '载入会话文件')
    m._page1_general_session_file_entry.Create(_sb)
    m._page1_general_session_file_chooser.Create(_sb, label = '打开')
    m._page1_general_session_file_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_general_session_file_entry]:
        self._handlers.set_file_entry_text(evt, data))

    m._page1_general_output_dir_ckbtn.Create(_sb, label = '指定output目录')
    m._page1_general_output_dir_entry.Create(_sb)
    m._page1_general_output_dir_chooser.Create(_sb, label = '打开')
    m._page1_general_output_dir_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_general_output_dir_entry, '选择 结果保存在哪']:
        self._handlers.set_file_entry_text(evt, data))

  def build_page1_other_misc(self, panel, m):
    _sb = m._page1_other_misc_area
    _sb.Create(panel, label = '杂项')

    m._page1_misc_skip_waf_ckbtn.Create(_sb, label = '跳过WAF/IPS侦测')
    m._page1_misc_list_tampers_ckbtn.Create(_sb, label = '列出可用的tamper脚本')
    m._page1_misc_sqlmap_shell_ckbtn.Create(_sb, label = '打开sqlmap交互shell')
    m._page1_misc_disable_color_ckbtn.Create(_sb, label = '禁用终端输出的颜色')
    m._page1_general_eta_ckbtn.Create(_sb, label = '显示剩余时间')
    m._page1_misc_update_ckbtn.Create(_sb, label = '更新sqlmap')
    m._page1_misc_gpage_ckbtn.Create(_sb, label = 'GOOGLEDORK时的页码')
    m._page1_misc_gpage_spinbtn.Create(_sb, value = '1', min = 1, max = 100)
    m._page1_misc_beep_ckbtn.Create(_sb, label = '响铃')
    m._page1_misc_offline_ckbtn.Create(_sb, label = '离线模式(仅使用本地会话数据)')
    m._page1_misc_purge_ckbtn.Create(_sb, label = '抹除所有本地记录!')
    m._page1_misc_dependencies_ckbtn.Create(_sb, label = '检查丢失的(非核心的)sqlmap依赖')
    m._page1_misc_alert_ckbtn.Create(_sb, label = '发现注入时运行本地命令:')
    m._page1_misc_alert_entry.Create(_sb)
    m._page1_misc_tmp_dir_ckbtn.Create(_sb, label = '本地临时目录')
    m._page1_misc_tmp_dir_entry.Create(_sb)
    m._page1_misc_tmp_dir_chooser.Create(_sb, label = '打开')
    m._page1_misc_tmp_dir_chooser.Bind(
      EVT_BUTTON,
      lambda evt, data = [m._page1_misc_tmp_dir_entry, '选择 本地临时目录']:
        self._handlers.set_file_entry_text(evt, data))

    m._page1_misc_answers_ckbtn.Create(_sb, label = '设置交互时的问题答案:')
    m._page1_misc_answers_entry.Create(_sb, value = 'quit=N,follow=N')
    m._page1_misc_z_ckbtn.Create(_sb, label = '使用短的助记符')
    m._page1_misc_z_entry.Create(_sb, value = 'flu,bat,ban,tec=EU...')
    # 最后一行总是会变矮~, 添加一个无用的widget, 抵消一下~
    self._dummy = btn(_sb,
                 label = '一个无用按钮, 如果报GTK警告, 应该是我没显示出来')
    self._dummy.Disable()


def main():
  import time
  from widgets import EXPAND, BOTTOM
  from model import Model
  from handlers import Handler

  start = time.process_time()
  app = wx.App()
  # --------
  win = wx.Frame(None, title = 'options-wx', size = (800, 600))

  m = Model(False)
  n = Notebook(win, m, Handler(win, m))

  box = wx.BoxSizer()
  box.Add(n, proportion = 1, flag = EXPAND | BOTTOM, border = 5)
  win.SetSizerAndFit(box)

  win.Centre()
  win.Show()
  # --------
  end = time.process_time()
  print('loading cost: %s Seconds' % (end - start))
  app.MainLoop()


if __name__ == '__main__':
  main()
