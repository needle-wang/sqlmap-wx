#!/usr/bin/env python3
#
# 2019年 05月 05日 星期日 20:43:40 CST

import wx
cb = wx.CheckBox
tc = wx.TextCtrl
st = wx.StaticText
sl = wx.Slider


class Page1Notebook(wx.Notebook):
  def __init__(self, parent):
    super().__init__(parent)

    page1_setting = self.build_page1_setting()
    page1_request = self.build_page1_request()
    page1_enumeration = self.build_page1_enumeration()
    page1_file = self.build_page1_file()
    page1_other = self.build_page1_other()

    self.AddPage(page1_setting, '测试(&Q)')
    self.AddPage(page1_request, '请求(&W)')
    self.AddPage(page1_enumeration, '枚举(&E)')
    self.AddPage(page1_file, '文件(&E)')
    self.AddPage(page1_other, '其他(&T)')

  def build_page1_other(self):
    p = wx.Panel(self)
    p.SetBackgroundColour(wx.LIGHT_GREY)

    vbox = wx.BoxSizer(wx.VERTICAL)
    page1_other_general_area = self.build_page1_other_general(p)
    page1_other_misc_area = self.build_page1_other_misc(p)

    vbox.Add(page1_other_general_area, flag = wx.EXPAND)
    vbox.Add(page1_other_misc_area, flag = wx.EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page1_other_misc(self, panel):
    page1_other_misc_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '杂项')
    _page1_other_misc_area = page1_other_misc_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._page1_misc_web_root_ckbtn = cb(_page1_other_misc_area, label = '远程web的root目录')
    self._page1_misc_web_root_entry = tc(_page1_other_misc_area)
    self._page1_misc_tmp_dir_ckbtn = cb(_page1_other_misc_area, label = '本地临时目录')
    self._page1_misc_tmp_dir_entry = tc(_page1_other_misc_area)

    row1.Add(self._page1_misc_web_root_ckbtn)
    row1.Add(self._page1_misc_web_root_entry, proportion = 1)
    row1.Add(self._page1_misc_tmp_dir_ckbtn)
    row1.Add(self._page1_misc_tmp_dir_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._page1_misc_identify_waf_ckbtn = cb(_page1_other_misc_area, label = '鉴别WAF')
    self._page1_misc_skip_waf_ckbtn = cb(_page1_other_misc_area, label = '跳过对WAF/IPS保护的启发式侦测')
    self._page1_misc_smart_ckbtn = cb(_page1_other_misc_area, label = '只对明显注入点进行详细测试')
    self._page1_misc_list_tampers_ckbtn = cb(_page1_other_misc_area, label = '列出可用的tamper脚本')
    self._page1_misc_sqlmap_shell_ckbtn = cb(_page1_other_misc_area, label = '打开sqlmap交互shell')
    self._page1_misc_disable_color_ckbtn = cb(_page1_other_misc_area, label = '禁用终端输出的颜色')

    row2.Add(self._page1_misc_identify_waf_ckbtn)
    row2.Add(self._page1_misc_skip_waf_ckbtn)
    row2.Add(self._page1_misc_smart_ckbtn)
    row2.Add(self._page1_misc_list_tampers_ckbtn)
    row2.Add(self._page1_misc_sqlmap_shell_ckbtn)
    row2.Add(self._page1_misc_disable_color_ckbtn)

    row3 = wx.BoxSizer()
    self._page1_misc_offline_ckbtn = cb(_page1_other_misc_area, label = '离线模式(只使用保存的会话数据)')
    self._page1_misc_mobile_ckbtn = cb(_page1_other_misc_area, label = '模拟手机请求')
    self._page1_misc_beep_ckbtn = cb(_page1_other_misc_area, label = '响铃')
    self._page1_misc_purge_ckbtn = cb(_page1_other_misc_area, label = '彻底清除所有记录')
    self._page1_misc_dependencies_ckbtn = cb(_page1_other_misc_area, label = '检查丢失的(非核心的)sqlmap依赖')
    self._page1_general_update_ckbtn = cb(_page1_other_misc_area, label = '更新sqlmap')

    row3.Add(self._page1_misc_offline_ckbtn)
    row3.Add(self._page1_misc_mobile_ckbtn)
    row3.Add(self._page1_misc_beep_ckbtn)
    row3.Add(self._page1_misc_purge_ckbtn)
    row3.Add(self._page1_misc_dependencies_ckbtn)
    row3.Add(self._page1_general_update_ckbtn)

    row4 = wx.BoxSizer()
    self._page1_misc_answers_ckbtn = cb(_page1_other_misc_area, label = '设置交互时的问题答案:')
    self._page1_misc_answers_entry = tc(_page1_other_misc_area)
    self._page1_misc_alert_ckbtn = cb(_page1_other_misc_area, label = '发现注入时运行本地命令:')
    self._page1_misc_alert_entry = tc(_page1_other_misc_area)
    self._page1_misc_gpage_ckbtn = cb(_page1_other_misc_area, label = 'GOOGLEDORK时的页码')
    self._page1_misc_gpage_spinbtn = tc(_page1_other_misc_area)

    row4.Add(self._page1_misc_answers_ckbtn)
    row4.Add(self._page1_misc_answers_entry, proportion = 1)
    row4.Add(self._page1_misc_alert_ckbtn)
    row4.Add(self._page1_misc_alert_entry, proportion = 1)
    row4.Add(self._page1_misc_gpage_ckbtn)
    row4.Add(self._page1_misc_gpage_spinbtn, proportion = 1)

    row5 = wx.BoxSizer()
    self._page1_misc_z_ckbtn = cb(_page1_other_misc_area, label = '使用短的助记符')
    self._page1_misc_z_entry = tc(_page1_other_misc_area)

    row5.Add(self._page1_misc_z_ckbtn)
    row5.Add(self._page1_misc_z_entry, proportion = 1)

    page1_other_misc_area.Add(row1, flag = wx.EXPAND)
    page1_other_misc_area.Add(row2, flag = wx.EXPAND)
    page1_other_misc_area.Add(row3, flag = wx.EXPAND)
    page1_other_misc_area.Add(row4, flag = wx.EXPAND)
    page1_other_misc_area.Add(row5, flag = wx.EXPAND)

    return page1_other_misc_area

  def build_page1_other_general(self, panel):
    page1_other_general_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '通用项')
    _page1_other_general_area = page1_other_general_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._page1_general_check_internet_ckbtn = cb(_page1_other_general_area, label = '检查与目标的网络连接')
    self._page1_general_fresh_queries_ckbtn = cb(_page1_other_general_area, label = '刷新此次查询')
    self._page1_general_flush_session_ckbtn = cb(_page1_other_general_area, label = '清空目标的会话文件')
    self._page1_general_eta_ckbtn = cb(_page1_other_general_area, label = '显示剩余时间')
    self._page1_general_binary_fields_ckbtn = cb(_page1_other_general_area, label = '生成有二进制值的字段')
    self._page1_general_binary_fields_entry = tc(_page1_other_general_area)

    row1.Add(self._page1_general_check_internet_ckbtn)
    row1.Add(self._page1_general_fresh_queries_ckbtn)
    row1.Add(self._page1_general_flush_session_ckbtn)
    row1.Add(self._page1_general_eta_ckbtn)
    row1.Add(self._page1_general_binary_fields_ckbtn)
    row1.Add(self._page1_general_binary_fields_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._page1_general_forms_ckbtn = cb(_page1_other_general_area, label = '解析和测试目标url内的表单')
    self._page1_general_parse_errors_ckbtn = cb(_page1_other_general_area, label = '解析并显示DB错误信息')
    self._page1_misc_cleanup_ckbtn = cb(_page1_other_general_area, label = '清理DBMS中sqlmap产生的UDF和表')
    self._page1_general_preprocess_ckbtn = cb(_page1_other_general_area, label = '指定预处理响应数据的脚本')
    self._page1_general_preprocess_entry = tc(_page1_other_general_area)

    row2.Add(self._page1_general_forms_ckbtn)
    row2.Add(self._page1_general_parse_errors_ckbtn)
    row2.Add(self._page1_misc_cleanup_ckbtn)
    row2.Add(self._page1_general_preprocess_ckbtn)
    row2.Add(self._page1_general_preprocess_entry, proportion = 1)

    row3 = wx.BoxSizer()
    self._page1_general_crawl_ckbtn = cb(_page1_other_general_area, label = '爬网站(的层级/深度')
    self._page1_general_crawl_entry = tc(_page1_other_general_area)
    self._page1_general_crawl_exclude_ckbtn = cb(_page1_other_general_area, label = '爬站时排除(正则)页面')
    self._page1_general_crawl_exclude_entry = tc(_page1_other_general_area)

    row3.Add(self._page1_general_crawl_ckbtn)
    row3.Add(self._page1_general_crawl_entry, proportion = 1)
    row3.Add(self._page1_general_crawl_exclude_ckbtn)
    row3.Add(self._page1_general_crawl_exclude_entry, proportion = 1)

    row4 = wx.BoxSizer()
    self._page1_general_charset_ckbtn = cb(_page1_other_general_area, label = '盲注所用的字符集合')
    self._page1_general_charset_entry = tc(_page1_other_general_area)
    self._page1_general_encoding_ckbtn = cb(_page1_other_general_area, label = '字符编码(用于数据获取)')
    self._page1_general_encoding_entry = tc(_page1_other_general_area)

    row4.Add(self._page1_general_charset_ckbtn)
    row4.Add(self._page1_general_charset_entry, proportion = 1)
    row4.Add(self._page1_general_encoding_ckbtn)
    row4.Add(self._page1_general_encoding_entry)

    row5 = wx.BoxSizer()
    self._page1_general_session_file_ckbtn = cb(_page1_other_general_area, label = '指定会话文件')
    self._page1_general_session_file_entry = tc(_page1_other_general_area)
    self._page1_general_output_dir_ckbtn = cb(_page1_other_general_area, label = '输出的保存目录')
    self._page1_general_output_dir_entry = tc(_page1_other_general_area)

    row5.Add(self._page1_general_session_file_ckbtn)
    row5.Add(self._page1_general_session_file_entry, proportion = 1)
    row5.Add(self._page1_general_output_dir_ckbtn)
    row5.Add(self._page1_general_output_dir_entry, proportion = 1)

    row6 = wx.BoxSizer()
    self._page1_general_dump_format_ckbtn = cb(_page1_other_general_area, label = 'dump结果的文件格式')
    self._page1_general_dump_format_entry = tc(_page1_other_general_area)
    self._page1_general_csv_del_ckbtn = cb(_page1_other_general_area, label = '(csv文件的)分隔符')
    self._page1_general_csv_del_entry = tc(_page1_other_general_area)

    row6.Add(self._page1_general_dump_format_ckbtn)
    row6.Add(self._page1_general_dump_format_entry)
    row6.Add(self._page1_general_csv_del_ckbtn)
    row6.Add(self._page1_general_csv_del_entry)

    row7 = wx.BoxSizer()
    self._page1_general_traffic_file_ckbtn = cb(_page1_other_general_area, label = '转存所有http流量到文本')
    self._page1_general_traffic_file_entry = tc(_page1_other_general_area)
    self._page1_general_har_ckbtn = cb(_page1_other_general_area, label = '转存至HAR文件')
    self._page1_general_har_entry = tc(_page1_other_general_area)

    row7.Add(self._page1_general_traffic_file_ckbtn)
    row7.Add(self._page1_general_traffic_file_entry, proportion = 1)
    row7.Add(self._page1_general_har_ckbtn)
    row7.Add(self._page1_general_har_entry, proportion = 1)

    row8 = wx.BoxSizer()
    self._page1_general_save_ckbtn = cb(_page1_other_general_area, label = '保存选项至INI文件')
    self._page1_general_save_entry = tc(_page1_other_general_area)
    self._page1_general_scope_ckbtn = cb(_page1_other_general_area, label = '从代理日志过滤出目标(正则)')
    self._page1_general_scope_entry = tc(_page1_other_general_area)

    row8.Add(self._page1_general_save_ckbtn)
    row8.Add(self._page1_general_save_entry, proportion = 1)
    row8.Add(self._page1_general_scope_ckbtn)
    row8.Add(self._page1_general_scope_entry, proportion = 1)

    row9 = wx.BoxSizer()
    self._page1_general_test_filter_ckbtn = cb(_page1_other_general_area, label = '测试过滤器(从payload/title选择)')
    self._page1_general_test_filter_entry = tc(_page1_other_general_area)
    self._page1_general_test_skip_ckbtn = cb(_page1_other_general_area, label = '测试跳过(从payload/title选择)')
    self._page1_general_test_skip_entry = tc(_page1_other_general_area)

    row9.Add(self._page1_general_test_filter_ckbtn)
    row9.Add(self._page1_general_test_filter_entry, proportion = 1)
    row9.Add(self._page1_general_test_skip_ckbtn)
    row9.Add(self._page1_general_test_skip_entry, proportion = 1)

    page1_other_general_area.Add(row1, flag = wx.EXPAND)
    page1_other_general_area.Add(row2, flag = wx.EXPAND)
    page1_other_general_area.Add(row3, flag = wx.EXPAND)
    page1_other_general_area.Add(row4, flag = wx.EXPAND)
    page1_other_general_area.Add(row5, flag = wx.EXPAND)
    page1_other_general_area.Add(row6, flag = wx.EXPAND)
    page1_other_general_area.Add(row7, flag = wx.EXPAND)
    page1_other_general_area.Add(row8, flag = wx.EXPAND)
    page1_other_general_area.Add(row9, flag = wx.EXPAND)

    return page1_other_general_area

  def build_page1_file(self):
    p = wx.Panel(self)
    p.SetBackgroundColour(wx.LIGHT_GREY)

    vbox = wx.BoxSizer(wx.VERTICAL)
    file_read_area = self.build_page1_file_read(p)
    file_write_area = self.build_page1_file_write(p)
    file_os_access_area = self.build_page1_file_os_access(p)
    file_os_registry_area = self.build_page1_file_os_registry(p)

    vbox.Add(file_read_area, flag = wx.EXPAND)
    vbox.Add(file_write_area, flag = wx.EXPAND)
    vbox.Add(file_os_access_area, flag = wx.EXPAND)
    vbox.Add(file_os_registry_area, flag = wx.EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page1_file_os_registry(self, panel):
    file_os_registry_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '访问WIN下注册表')
    _file_os_registry_area = file_os_registry_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._file_os_registry_reg_ckbtn = cb(_file_os_registry_area, label = '键值操作:')

    row1.Add(self._file_os_registry_reg_ckbtn)

    row2 = wx.BoxSizer()
    self._file_os_registry_reg_key_label = st(_file_os_registry_area, label = '键')
    self._file_os_registry_reg_key_entry = tc(_file_os_registry_area)
    self._file_os_registry_reg_value_label = st(_file_os_registry_area, label = '值')
    self._file_os_registry_reg_value_entry = tc(_file_os_registry_area)

    row2.Add(self._file_os_registry_reg_key_label)
    row2.Add(self._file_os_registry_reg_key_entry, proportion = 1)
    row2.Add(self._file_os_registry_reg_value_label)
    row2.Add(self._file_os_registry_reg_value_entry, proportion = 1)

    row3 = wx.BoxSizer()
    self._file_os_registry_reg_data_label = st(_file_os_registry_area, label = '数据')
    self._file_os_registry_reg_data_entry = tc(_file_os_registry_area)
    self._file_os_registry_reg_type_label = st(_file_os_registry_area, label = '类型')
    self._file_os_registry_reg_type_entry = tc(_file_os_registry_area)

    row3.Add(self._file_os_registry_reg_data_label)
    row3.Add(self._file_os_registry_reg_data_entry, proportion = 1)
    row3.Add(self._file_os_registry_reg_type_label)
    row3.Add(self._file_os_registry_reg_type_entry, proportion = 1)

    file_os_registry_area.Add(row1, flag = wx.EXPAND)
    file_os_registry_area.Add(row2, flag = wx.EXPAND)
    file_os_registry_area.Add(row3, flag = wx.EXPAND)

    return file_os_registry_area

  def build_page1_file_os_access(self, panel):
    file_os_access_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '访问后端OS')
    _file_os_access_area = file_os_access_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._file_os_access_os_cmd_ckbtn = cb(_file_os_access_area, label = '执行CLI命令')
    self._file_os_access_os_cmd_entry = tc(_file_os_access_area)

    row1.Add(self._file_os_access_os_cmd_ckbtn)
    row1.Add(self._file_os_access_os_cmd_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._file_os_access_os_shell_ckbtn = cb(_file_os_access_area, label = '获取交互shell')
    self._file_os_access_os_pwn_ckbtn = cb(_file_os_access_area, label = '--os-pwn')
    self._file_os_access_os_smbrelay_ckbtn = cb(_file_os_access_area, label = '--os-smbrelay')
    self._file_os_access_os_bof_ckbtn = cb(_file_os_access_area, label = '--os-bof')
    self._file_os_access_priv_esc_ckbtn = cb(_file_os_access_area, label = '--priv-esc')

    row2.Add(self._file_os_access_os_shell_ckbtn)
    row2.Add(self._file_os_access_os_pwn_ckbtn)
    row2.Add(self._file_os_access_os_smbrelay_ckbtn)
    row2.Add(self._file_os_access_os_bof_ckbtn)
    row2.Add(self._file_os_access_priv_esc_ckbtn)

    row3 = wx.BoxSizer()
    self._file_os_access_msf_path_ckbtn = cb(_file_os_access_area, label = '本地Metasploit安装路径')
    self._file_os_access_msf_path_entry = tc(_file_os_access_area)
    self._file_os_access_tmp_path_ckbtn = cb(_file_os_access_area, label = '远程临时目录(绝对路径)')
    self._file_os_access_tmp_path_entry = tc(_file_os_access_area)

    row3.Add(self._file_os_access_msf_path_ckbtn)
    row3.Add(self._file_os_access_msf_path_entry, proportion = 1)
    row3.Add(self._file_os_access_tmp_path_ckbtn)
    row3.Add(self._file_os_access_tmp_path_entry, proportion = 1)

    file_os_access_area.Add(row1, flag = wx.EXPAND)
    file_os_access_area.Add(row2, flag = wx.EXPAND)
    file_os_access_area.Add(row3, flag = wx.EXPAND)

    return file_os_access_area

  def build_page1_file_write(self, panel):
    file_write_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '文件上传')
    _file_write_area = file_write_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._file_write_area_udf_ckbtn = cb(_file_write_area, label = '注入(默认sqlmap自带的)用户定义函数')
    self._file_write_area_shared_lib_ckbtn = cb(_file_write_area, label = '本地共享库路径(--shared-lib=)')
    self._file_write_area_shared_lib_entry = tc(_file_write_area)

    row1.Add(self._file_write_area_udf_ckbtn)
    row1.Add(self._file_write_area_shared_lib_ckbtn)
    row1.Add(self._file_write_area_shared_lib_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._file_write_area_file_write_ckbtn = cb(_file_write_area, label = '本地文件路径(--file-write=)')
    self._file_write_area_file_write_entry = tc(_file_write_area)

    row2.Add(self._file_write_area_file_write_ckbtn)
    row2.Add(self._file_write_area_file_write_entry, proportion = 1)

    row3 = wx.BoxSizer()
    self._file_write_area_file_dest_ckbtn = cb(_file_write_area, label = '远程文件路径(--file-dest=)')
    self._file_write_area_file_dest_entry = tc(_file_write_area)

    row3.Add(self._file_write_area_file_dest_ckbtn)
    row3.Add(self._file_write_area_file_dest_entry, proportion = 1)

    file_write_area.Add(row1, flag = wx.EXPAND)
    file_write_area.Add(row2, flag = wx.EXPAND)
    file_write_area.Add(row3, flag = wx.EXPAND)

    return file_write_area

  def build_page1_file_read(self, panel):
    file_read_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '读取远程文件')
    _file_read_area = file_read_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._file_read_area_file_read_ckbtn = cb(_file_read_area, label = '远程文件路径(--file-read=)')
    self._file_read_area_file_read_entry = tc(_file_read_area)

    row1.Add(self._file_read_area_file_read_ckbtn)
    row1.Add(self._file_read_area_file_read_entry, proportion = 1)

    file_read_area.Add(row1, flag = wx.EXPAND)

    return file_read_area

  def build_page1_enumeration(self):
    p = wx.Panel(self)
    p.SetBackgroundColour(wx.LIGHT_GREY)

    hbox1 = wx.BoxSizer()
    enum_area = self.build_page1_enumeration_enum(p)
    dump_area = self.build_page1_enumeration_dump(p)
    limit_area = self.build_page1_enumeration_limit(p)
    blind_area = self.build_page1_enumeration_blind(p)
    hbox1.Add(enum_area)
    hbox1.Add(dump_area)
    hbox1.Add(limit_area)
    hbox1.Add(blind_area)

    hbox2 = wx.BoxSizer()
    meta_area = self.build_page1_enumeration_meta(p)
    hbox2.Add(meta_area, proportion = 1)

    hbox3 = wx.BoxSizer()
    runsql_area = self.build_page1_enumeration_runsql(p)
    hbox3.Add(runsql_area, proportion = 1)

    hbox4 = wx.BoxSizer()
    brute_force_area = self.build_page1_enumeration_brute_force(p)
    hbox4.Add(brute_force_area)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox1)
    vbox.Add(hbox2, flag = wx.EXPAND)
    vbox.Add(hbox3, flag = wx.EXPAND)
    vbox.Add(hbox4)
    p.SetSizerAndFit(vbox)
    return p

  def build_page1_enumeration_brute_force(self, panel):
    brute_force_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '暴破表名/列名')
    _brute_force_area = brute_force_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._brute_force_area_common_tables_ckbtn = cb(_brute_force_area, label = '常用表名')
    self._brute_force_area_common_columns_ckbtn = cb(_brute_force_area, label = '常用列名')

    row1.Add(st(_brute_force_area, label = '检查是否存在:'))
    row1.Add(self._brute_force_area_common_tables_ckbtn)
    row1.Add(self._brute_force_area_common_columns_ckbtn)

    brute_force_area.Add(row1)

    return brute_force_area

  def build_page1_enumeration_runsql(self, panel):
    runsql_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '执行SQL语句')
    _runsql_area = runsql_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._runsql_area_sql_query_ckbtn = cb(_runsql_area, label = 'SQL语句:')
    self._runsql_area_sql_query_entry = tc(_runsql_area)

    row1.Add(self._runsql_area_sql_query_ckbtn)
    row1.Add(self._runsql_area_sql_query_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._runsql_area_sql_shell_ckbtn = cb(_runsql_area, label = '打开个SQL交互shell')
    self._runsql_area_sql_file_ckbtn = cb(_runsql_area, label = '本地SQL文件:')
    self._runsql_area_sql_file_entry = tc(_runsql_area)

    row2.Add(self._runsql_area_sql_shell_ckbtn)
    row2.Add(self._runsql_area_sql_file_ckbtn)
    row2.Add(self._runsql_area_sql_file_entry, proportion = 1)

    runsql_area.Add(row1, flag = wx.EXPAND)
    runsql_area.Add(row2, flag = wx.EXPAND)

    return runsql_area

  def build_page1_enumeration_meta(self, panel):
    meta_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '数据库名, 表名, 列名...')
    _meta_area = meta_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._meta_area_D_ckbtn = cb(_meta_area, label = '指定库名')
    self._meta_area_D_entry = tc(_meta_area)
    self._meta_area_T_ckbtn = cb(_meta_area, label = '指定表名')
    self._meta_area_T_entry = tc(_meta_area)
    self._meta_area_C_ckbtn = cb(_meta_area, label = '指定列名')
    self._meta_area_C_entry = tc(_meta_area)
    self._meta_area_U_ckbtn = cb(_meta_area, label = '指定用户')
    self._meta_area_U_entry = tc(_meta_area)

    row1.Add(self._meta_area_D_ckbtn)
    row1.Add(self._meta_area_D_entry, proportion = 1)
    row1.Add(self._meta_area_T_ckbtn)
    row1.Add(self._meta_area_T_entry, proportion = 1)
    row1.Add(self._meta_area_C_ckbtn)
    row1.Add(self._meta_area_C_entry, proportion = 1)
    row1.Add(self._meta_area_U_ckbtn)
    row1.Add(self._meta_area_U_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._meta_area_X_ckbtn = cb(_meta_area, label = '排除标志符')
    self._meta_area_X_entry = tc(_meta_area)
    self._meta_area_pivot_ckbtn = cb(_meta_area, label = '指定Pivot列名')
    self._meta_area_pivot_entry = tc(_meta_area)

    row2.Add(self._meta_area_X_ckbtn)
    row2.Add(self._meta_area_X_entry)
    row2.Add(self._meta_area_pivot_ckbtn)
    row2.Add(self._meta_area_pivot_entry)

    row3 = wx.BoxSizer()
    self._meta_area_where_ckbtn = cb(_meta_area, label = 'where子句')
    self._meta_area_where_entry = tc(_meta_area)

    row3.Add(self._meta_area_where_ckbtn)
    row3.Add(self._meta_area_where_entry, proportion = 1)

    meta_area.Add(row1, flag = wx.EXPAND)
    meta_area.Add(row2, flag = wx.EXPAND)
    meta_area.Add(row3, flag = wx.EXPAND)
    return meta_area

  def build_page1_enumeration_blind(self, panel):
    blind_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '盲注选项')
    _blind_area = blind_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._blind_area_first_ckbtn = cb(_blind_area, label = '首字符')
    self._blind_area_first_entry = tc(_blind_area)

    row1.Add(self._blind_area_first_ckbtn)
    row1.Add(self._blind_area_first_entry)

    row2 = wx.BoxSizer()
    self._blind_area_last_ckbtn = cb(_blind_area, label = '末字符')
    self._blind_area_last_entry = tc(_blind_area)

    row2.Add(self._blind_area_last_ckbtn)
    row2.Add(self._blind_area_last_entry)

    blind_area.Add(row1, flag = wx.EXPAND)
    blind_area.Add(row2, flag = wx.EXPAND)

    return blind_area

  def build_page1_enumeration_limit(self, panel):
    limit_area = wx.StaticBoxSizer(wx.VERTICAL, panel, 'limit(dump时的限制)')
    _limit_area = limit_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._limit_area_start_ckbtn = cb(_limit_area, label = '始于第')
    self._limit_area_start_entry = tc(_limit_area)

    row1.Add(self._limit_area_start_ckbtn)
    row1.Add(self._limit_area_start_entry)
    row1.Add(st(_limit_area, label = '条'))

    row2 = wx.BoxSizer()
    self._limit_area_stop_ckbtn = cb(_limit_area, label = '止于第')
    self._limit_area_stop_entry = tc(_limit_area)
    row2.Add(self._limit_area_stop_ckbtn)
    row2.Add(self._limit_area_stop_entry)
    row2.Add(st(_limit_area, label = '条'))

    limit_area.Add(row1, flag = wx.EXPAND)
    limit_area.Add(row2, flag = wx.EXPAND)

    return limit_area

  def build_page1_enumeration_dump(self, panel):
    dump_area = wx.StaticBoxSizer(wx.VERTICAL, panel, 'Dump(转储)')
    _dump_area = dump_area.GetStaticBox()

    self._dump_area_dump_ckbtn = cb(_dump_area, label = 'dump(某库某表的条目)')
    self._dump_area_dump_all_ckbtn = cb(_dump_area, label = '全部dump(拖库)')
    self._dump_area_search_ckbtn = cb(_dump_area, label = '搜索')
    self._dump_area_no_sys_db_ckbtn = cb(_dump_area, label = '排除系统库')
    self._dump_area_repair_ckbtn = cb(_dump_area, label = '重新获取有未知符号(?)的条目')

    dump_area.Add(self._dump_area_dump_ckbtn)
    dump_area.Add(self._dump_area_dump_all_ckbtn)
    dump_area.Add(self._dump_area_search_ckbtn)
    dump_area.Add(self._dump_area_no_sys_db_ckbtn)
    dump_area.Add(self._dump_area_repair_ckbtn)

    return dump_area

  def build_page1_enumeration_enum(self, panel):
    enum_area = wx.StaticBoxSizer(wx.HORIZONTAL, panel, '枚举')
    _enum_area = enum_area.GetStaticBox()

    _enum_area_enum_labels = (
      ('DB banner', '当前用户', '当前数据库', '主机名', '是否是DBA'),
      ('用户', '密码', '权限', '角色', '数据库'),
      ('表', '字段', '架构', '计数', '备注'))
    self._enum_area_opts_ckbtns = ([], [], [])
    _enu_area_opts_cols = [wx.BoxSizer(wx.VERTICAL),
                           wx.BoxSizer(wx.VERTICAL),
                           wx.BoxSizer(wx.VERTICAL)]

    for _x in range(len(_enum_area_enum_labels)):  # 三列
      for _y in _enum_area_enum_labels[_x]:
        _ckbtn = cb(_enum_area, label = _y)
        self._enum_area_opts_ckbtns[_x].append(_ckbtn)
        # 每列, 至上往下add
        _enu_area_opts_cols[_x].Add(_ckbtn)

      enum_area.Add(_enu_area_opts_cols[_x])

    return enum_area

  def build_page1_request(self):
    p = wx.Panel(self)
    p.SetBackgroundColour(wx.LIGHT_GREY)

    vbox = wx.BoxSizer(wx.VERTICAL)
    request_header_area = self.build_page1_request_header(p)
    request_data_area = self.build_page1_request_data(p)
    request_custom_area = self.build_page1_request_custom(p)
    request_proxy_area = self.build_page1_request_proxy(p)

    vbox.Add(request_header_area, flag = wx.EXPAND)
    vbox.Add(request_data_area, flag = wx.EXPAND)
    vbox.Add(request_custom_area, flag = wx.EXPAND)
    vbox.Add(request_proxy_area, flag = wx.EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page1_request_proxy(self, panel):
    request_proxy_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '隐匿/代理')
    _request_proxy_area = request_proxy_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._request_area_safe_url_ckbtn = cb(_request_proxy_area, label = '顺便掺杂地访问一个安全url')
    self._request_area_safe_url_entry = tc(_request_proxy_area)
    self._request_area_safe_post_ckbtn = cb(_request_proxy_area, label = '提交到安全url的post数据')
    self._request_area_safe_post_entry = tc(_request_proxy_area)

    row1.Add(self._request_area_safe_url_ckbtn)
    row1.Add(self._request_area_safe_url_entry, proportion = 1)
    row1.Add(self._request_area_safe_post_ckbtn)
    row1.Add(self._request_area_safe_post_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._request_area_safe_req_ckbtn = cb(_request_proxy_area, label = '从文件载入safe HTTP请求')
    self._request_area_safe_req_entry = tc(_request_proxy_area)
    self._request_area_safe_freq_ckbtn = cb(_request_proxy_area, label = '访问安全url的频率')
    self._request_area_safe_freq_entry = tc(_request_proxy_area)

    row2.Add(self._request_area_safe_req_ckbtn)
    row2.Add(self._request_area_safe_req_entry, proportion = 1)
    row2.Add(self._request_area_safe_freq_ckbtn)
    row2.Add(self._request_area_safe_freq_entry)

    row3 = wx.BoxSizer()
    self._request_area_ignore_proxy_ckbtn = cb(_request_proxy_area, label = '忽略系统默认代理')
    self._request_area_proxy_ckbtn = cb(_request_proxy_area, label = '使用代理')
    self._request_area_proxy_file_ckbtn = cb(_request_proxy_area, label = '代理列表文件')
    self._request_area_proxy_file_entry = tc(_request_proxy_area)

    row3.Add(self._request_area_ignore_proxy_ckbtn)
    row3.Add(self._request_area_proxy_ckbtn)
    row3.Add(self._request_area_proxy_file_ckbtn)
    row3.Add(self._request_area_proxy_file_entry, proportion = 1)

    row4 = wx.BoxSizer()
    self._request_area_proxy_ip_label = st(_request_proxy_area, label = 'IP:')
    self._request_area_proxy_ip_entry = tc(_request_proxy_area)
    self._request_area_proxy_port_label = st(_request_proxy_area, label = 'PORT:')
    self._request_area_proxy_port_entry = tc(_request_proxy_area)
    self._request_area_proxy_username_label = st(_request_proxy_area, label = 'username:')
    self._request_area_proxy_username_entry = tc(_request_proxy_area)
    self._request_area_proxy_password_label = st(_request_proxy_area, label = 'password:')
    self._request_area_proxy_password_entry = tc(_request_proxy_area)

    row4.Add(self._request_area_proxy_ip_label)
    row4.Add(self._request_area_proxy_ip_entry, proportion = 1)
    row4.Add(self._request_area_proxy_port_label)
    row4.Add(self._request_area_proxy_port_entry, proportion = 1)
    row4.Add(self._request_area_proxy_username_label)
    row4.Add(self._request_area_proxy_username_entry, proportion = 1)
    row4.Add(self._request_area_proxy_password_label)
    row4.Add(self._request_area_proxy_password_entry, proportion = 1)

    row5 = wx.BoxSizer()
    self._request_area_tor_ckbtn = cb(_request_proxy_area, label = '使用Tor匿名网络')
    self._request_area_tor_port_ckbtn = cb(_request_proxy_area, label = 'Tor端口:')
    self._request_area_tor_port_entry = tc(_request_proxy_area)
    self._request_area_tor_type_ckbtn = cb(_request_proxy_area, label = 'Tor代理类型')
    self._request_area_tor_type_entry = tc(_request_proxy_area)
    self._request_area_check_tor_ckbtn = cb(_request_proxy_area, label = '检查Tor连接')

    row5.Add(self._request_area_tor_ckbtn)
    row5.Add(self._request_area_tor_port_ckbtn)
    row5.Add(self._request_area_tor_port_entry)
    row5.Add(self._request_area_tor_type_ckbtn)
    row5.Add(self._request_area_tor_type_entry)
    row5.Add(self._request_area_check_tor_ckbtn)

    request_proxy_area.Add(row1, flag = wx.EXPAND)
    request_proxy_area.Add(row2, flag = wx.EXPAND)
    request_proxy_area.Add(row3, flag = wx.EXPAND)
    request_proxy_area.Add(row4, flag = wx.EXPAND)
    request_proxy_area.Add(row5, flag = wx.EXPAND)

    return request_proxy_area

  def build_page1_request_custom(self, panel):
    request_custom_area = wx.StaticBoxSizer(wx.VERTICAL, panel, 'request定制')
    _request_custom_area = request_custom_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._request_area_ignore_redirects_ckbtn = cb(_request_custom_area, label = '忽略重定向')
    self._request_area_ignore_timeouts_ckbtn = cb(_request_custom_area, label = '忽略连接超时')
    self._request_area_ignore_code_ckbtn = cb(_request_custom_area, label = '忽略错误型状态码:')
    self._request_area_ignore_code_entry = tc(_request_custom_area)
    self._request_area_skip_urlencode_ckbtn = cb(_request_custom_area, label = 'payload不使用url编码')
    self._request_area_force_ssl_ckbtn = cb(_request_custom_area, label = '强制使用HTTPS')
    self._request_area_chunked_ckbtn = cb(_request_custom_area, label = '用Chunked编码发送POST请求')
    self._request_area_hpp_ckbtn = cb(_request_custom_area, label = '使用HTTP参数污染')

    row1.Add(self._request_area_ignore_redirects_ckbtn)
    row1.Add(self._request_area_ignore_timeouts_ckbtn)
    row1.Add(self._request_area_ignore_code_ckbtn)
    row1.Add(self._request_area_ignore_code_entry, proportion = 1)
    row1.Add(self._request_area_skip_urlencode_ckbtn)
    row1.Add(self._request_area_force_ssl_ckbtn)
    row1.Add(self._request_area_chunked_ckbtn)
    row1.Add(self._request_area_hpp_ckbtn)

    row2 = wx.BoxSizer()
    self._request_area_delay_ckbtn = cb(_request_custom_area, label = '请求间隔(秒)')
    self._request_area_delay_entry = tc(_request_custom_area)
    self._request_area_timeout_ckbtn = cb(_request_custom_area, label = '几秒超时')
    self._request_area_timeout_entry = tc(_request_custom_area)
    self._request_area_retries_ckbtn = cb(_request_custom_area, label = '超时重试次数')
    self._request_area_retries_entry = tc(_request_custom_area)
    self._request_area_randomize_ckbtn = cb(_request_custom_area, label = '指定要随机改变值的参数')
    self._request_area_randomize_entry = tc(_request_custom_area)

    row2.Add(self._request_area_delay_ckbtn)
    row2.Add(self._request_area_delay_entry)
    row2.Add(self._request_area_timeout_ckbtn)
    row2.Add(self._request_area_timeout_entry)
    row2.Add(self._request_area_retries_ckbtn)
    row2.Add(self._request_area_retries_entry)
    row2.Add(self._request_area_randomize_ckbtn)
    row2.Add(self._request_area_randomize_entry, proportion = 1)

    row3 = wx.BoxSizer()
    self._request_area_eval_ckbtn = cb(_request_custom_area, label = '--eval=')
    self._request_area_eval_entry = tc(_request_custom_area)
    row3.Add(self._request_area_eval_ckbtn)
    row3.Add(self._request_area_eval_entry, proportion = 1)

    request_custom_area.Add(row1, flag = wx.EXPAND)
    request_custom_area.Add(row2, flag = wx.EXPAND)
    request_custom_area.Add(row3, flag = wx.EXPAND)

    return request_custom_area

  def build_page1_request_data(self, panel):
    request_data_area = wx.StaticBoxSizer(wx.VERTICAL, panel, 'HTTP data')
    _request_data_area = request_data_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._request_area_method_ckbtn = cb(_request_data_area, label = 'HTTP请求方式')
    self._request_area_method_entry = tc(_request_data_area)
    self._request_area_param_del_ckbtn = cb(_request_data_area, label = '指定分隔data参数值的字符')
    self._request_area_param_del_entry = tc(_request_data_area)

    row1.Add(self._request_area_method_ckbtn)
    row1.Add(self._request_area_method_entry)
    row1.Add(self._request_area_param_del_ckbtn)
    row1.Add(self._request_area_param_del_entry)

    row2 = wx.BoxSizer()
    self._request_area_post_ckbtn = cb(_request_data_area, label = '通过POST提交data:')
    self._request_area_post_entry = tc(_request_data_area)

    row2.Add(self._request_area_post_ckbtn)
    row2.Add(self._request_area_post_entry, proportion = 1)

    row3 = wx.BoxSizer()
    self._request_area_cookie_ckbtn = cb(_request_data_area, label = '请求中要包含的Cookie:')
    self._request_area_cookie_entry = tc(_request_data_area)
    self._request_area_cookie_del_ckbtn = cb(_request_data_area, label = '指定cookie分隔符')
    self._request_area_cookie_del_entry = tc(_request_data_area)

    row3.Add(self._request_area_cookie_ckbtn)
    row3.Add(self._request_area_cookie_entry, proportion = 1)
    row3.Add(self._request_area_cookie_del_ckbtn)
    row3.Add(self._request_area_cookie_del_entry)

    row4 = wx.BoxSizer()
    self._request_area_load_cookies_ckbtn = cb(_request_data_area, label = '本地Cookie文件')
    self._request_area_load_cookies_entry = tc(_request_data_area)
    self._request_area_drop_set_cookie_ckbtn = cb(_request_data_area, label = '丢弃Set-Cookie头')

    row4.Add(self._request_area_load_cookies_ckbtn)
    row4.Add(self._request_area_load_cookies_entry, proportion = 1)
    row4.Add(self._request_area_drop_set_cookie_ckbtn)

    row5 = wx.BoxSizer()
    self._request_area_auth_type_ckbtn = cb(_request_data_area, label = 'http认证类型')
    self._request_area_auth_type_entry = tc(_request_data_area)
    self._request_area_auth_cred_ckbtn = cb(_request_data_area, label = 'http认证账密')
    self._request_area_auth_cred_entry = tc(_request_data_area)
    self._request_area_auth_file_ckbtn = cb(_request_data_area, label = 'http认证文件')
    self._request_area_auth_file_entry = tc(_request_data_area)

    row5.Add(self._request_area_auth_type_ckbtn)
    row5.Add(self._request_area_auth_type_entry, proportion = 1)
    row5.Add(self._request_area_auth_cred_ckbtn)
    row5.Add(self._request_area_auth_cred_entry, proportion = 1)
    row5.Add(self._request_area_auth_file_ckbtn)
    row5.Add(self._request_area_auth_file_entry, proportion = 1)

    row6 = wx.BoxSizer()
    self._request_area_csrf_token_ckbtn = cb(_request_data_area, label = 'csrf_token')
    self._request_area_csrf_token_entry = tc(_request_data_area)
    self._request_area_csrf_url_ckbtn = cb(_request_data_area, label = '获取csrf_token的url')
    self._request_area_csrf_url_entry = tc(_request_data_area)

    row6.Add(self._request_area_csrf_token_ckbtn)
    row6.Add(self._request_area_csrf_token_entry, proportion = 1)
    row6.Add(self._request_area_csrf_url_ckbtn)
    row6.Add(self._request_area_csrf_url_entry, proportion = 1)

    request_data_area.Add(row1, flag = wx.EXPAND)
    request_data_area.Add(row2, flag = wx.EXPAND)
    request_data_area.Add(row3, flag = wx.EXPAND)
    request_data_area.Add(row4, flag = wx.EXPAND)
    request_data_area.Add(row5, flag = wx.EXPAND)
    request_data_area.Add(row6, flag = wx.EXPAND)

    return request_data_area

  def build_page1_request_header(self, panel):
    request_header_area = wx.StaticBoxSizer(wx.VERTICAL, panel, 'HTTP header')
    _request_header_area = request_header_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._request_area_random_agent_ckbtn = cb(_request_header_area, label = '随机User-Agent头')
    self._request_area_user_agent_ckbtn = cb(_request_header_area, label = '指定User-Agent头')
    self._request_area_user_agent_entry = tc(_request_header_area)

    row1.Add(self._request_area_random_agent_ckbtn)
    row1.Add(self._request_area_user_agent_ckbtn)
    row1.Add(self._request_area_user_agent_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._request_area_host_ckbtn = cb(_request_header_area, label = 'Host头')
    self._request_area_host_entry = tc(_request_header_area)
    self._request_area_referer_ckbtn = cb(_request_header_area, label = 'referer头')
    self._request_area_referer_entry = tc(_request_header_area)

    row2.Add(self._request_area_host_ckbtn)
    row2.Add(self._request_area_host_entry, proportion = 1)
    row2.Add(self._request_area_referer_ckbtn)
    row2.Add(self._request_area_referer_entry, proportion = 1)

    row3 = wx.BoxSizer()
    self._request_area_header_ckbtn = cb(_request_header_area, label = '额外的header(-H)')
    self._request_area_header_entry = tc(_request_header_area)
    self._request_area_headers_ckbtn = cb(_request_header_area, label = '额外的headers')
    self._request_area_headers_entry = tc(_request_header_area)

    row3.Add(self._request_area_header_ckbtn)
    row3.Add(self._request_area_header_entry, proportion = 1)
    row3.Add(self._request_area_headers_ckbtn)
    row3.Add(self._request_area_headers_entry, proportion = 1)

    request_header_area.Add(row1, flag = wx.EXPAND)
    request_header_area.Add(row2, flag = wx.EXPAND)
    request_header_area.Add(row3, flag = wx.EXPAND)

    return request_header_area

  def build_page1_setting(self):
    p = wx.Panel(self)
    p.SetBackgroundColour(wx.LIGHT_GREY)

    hbox1 = wx.BoxSizer()
    inject_area = self.build_page1_setting_inject(p)
    detection_area = self.build_page1_setting_detection(p)
    tech_area = self.build_page1_setting_tech(p)

    hbox1.Add(inject_area, flag = wx.EXPAND)
    hbox1.Add(detection_area, proportion = 1)
    hbox1.Add(tech_area, flag = wx.EXPAND)

    hbox2 = wx.BoxSizer()
    tamper_area = self.build_page1_setting_tamper(p)
    optimize_area = self.build_page1_setting_optimize(p)
    general_area = self.build_page1_setting_general(p)

    hbox2.Add(tamper_area, flag = wx.EXPAND)
    hbox2.Add(optimize_area, flag = wx.EXPAND)
    hbox2.Add(general_area, flag = wx.EXPAND)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox1, flag = wx.EXPAND)
    vbox.Add(hbox2, flag = wx.EXPAND)
    p.SetSizerAndFit(vbox)
    return p

  def build_page1_setting_general(self, panel):
    general_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '常用选项')
    _general_area = general_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._general_area_verbose_ckbtn = cb(_general_area, label = '输出详细程度')
    self._general_area_verbose_scale = sl(_general_area,
                                          value = 1,
                                          minValue = 0,
                                          maxValue = 6,
                                          style = wx.SL_VALUE_LABEL)

    row1.Add(self._general_area_verbose_ckbtn)
    row1.Add(self._general_area_verbose_scale, proportion = 1)

    self._general_area_finger_ckbtn = cb(_general_area, label = '执行宽泛的DB版本检测')
    self._general_area_hex_ckbtn = cb(_general_area, label = '获取数据时使用hex转换')
    self._general_area_batch_ckbtn = cb(_general_area, label = '非交互模式, 一切皆默认')
    self._page1_misc_wizard_ckbtn = cb(_general_area, label = '新手向导')

    general_area.Add(row1, flag = wx.EXPAND)
    general_area.Add(self._general_area_finger_ckbtn, flag = wx.EXPAND)
    general_area.Add(self._general_area_hex_ckbtn, flag = wx.EXPAND)
    general_area.Add(self._general_area_batch_ckbtn, flag = wx.EXPAND)
    general_area.Add(self._page1_misc_wizard_ckbtn, flag = wx.EXPAND)
    return general_area

  def build_page1_setting_optimize(self, panel):
    optimize_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '性能优化')
    _optimize_area = optimize_area.GetStaticBox()

    self._optimize_area_turn_all_ckbtn = cb(_optimize_area, label = '启用所有优化选项')
    self._optimize_area_turn_all_ckbtn.Bind(wx.EVT_CHECKBOX, self.optimize_area_controller)

    row2 = wx.BoxSizer()
    self._optimize_area_thread_num_ckbtn = cb(_optimize_area, label = '使用线程数:')
    self._optimize_area_thread_num_spinbtn = tc(_optimize_area)

    row2.Add(self._optimize_area_thread_num_ckbtn)
    row2.Add(self._optimize_area_thread_num_spinbtn, proportion = 1)

    self._optimize_area_predict_ckbtn = cb(_optimize_area, label = '预测通常的查询结果')
    self._optimize_area_keep_alive_ckbtn = cb(_optimize_area, label = 'http连接使用keep-alive')
    self._optimize_area_null_connect_ckbtn = cb(_optimize_area, label = '只用页面长度报头来比较, 不去获取实际的响应体')

    optimize_area.Add(self._optimize_area_turn_all_ckbtn, flag = wx.EXPAND)
    optimize_area.Add(row2, flag = wx.EXPAND)
    optimize_area.Add(self._optimize_area_predict_ckbtn, flag = wx.EXPAND)
    optimize_area.Add(self._optimize_area_keep_alive_ckbtn, flag = wx.EXPAND)
    optimize_area.Add(self._optimize_area_null_connect_ckbtn, flag = wx.EXPAND)

    return optimize_area

  def optimize_area_controller(self, event):
    if self._optimize_area_turn_all_ckbtn.IsChecked():
      self._optimize_area_predict_ckbtn.SetValue(False)
      self._optimize_area_keep_alive_ckbtn.SetValue(False)
      self._optimize_area_null_connect_ckbtn.SetValue(False)

      self._optimize_area_predict_ckbtn.Disable()
      self._optimize_area_keep_alive_ckbtn.Disable()
      self._optimize_area_null_connect_ckbtn.Disable()
    else:
      self._optimize_area_predict_ckbtn.Enable()
      self._optimize_area_keep_alive_ckbtn.Enable()
      self._optimize_area_null_connect_ckbtn.Enable()

  def build_page1_setting_tamper(self, panel):
    tamper_area = wx.StaticBoxSizer(wx.VERTICAL, panel, 'tamper脚本')
    _tamper_area = tamper_area.GetStaticBox()

    self._tamper_area_tamper_view = tc(_tamper_area, size = (300, -1), style = wx.TC_MULTILINE)

    tamper_area.Add(self._tamper_area_tamper_view, proportion = 1)

    return tamper_area

  def build_page1_setting_tech(self, panel):
    tech_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '各注入技术的选项')
    _tech_area = tech_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._tech_area_tech_ckbtn = cb(_tech_area, label = '注入技术')
    self._tech_area_tech_entry = tc(_tech_area)

    row1.Add(self._tech_area_tech_ckbtn)
    row1.Add(self._tech_area_tech_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._tech_area_time_sec_ckbtn = cb(_tech_area, label = '指定DB延迟多少秒响应')
    self._tech_area_time_sec_entry = tc(_tech_area)

    row2.Add(self._tech_area_time_sec_ckbtn)
    row2.Add(self._tech_area_time_sec_entry, proportion = 1)

    row3 = wx.BoxSizer()
    self._tech_area_union_col_ckbtn = cb(_tech_area, label = '指定最大union列数')
    self._tech_area_union_col_entry = tc(_tech_area)

    row3.Add(self._tech_area_union_col_ckbtn)
    row3.Add(self._tech_area_union_col_entry, proportion = 1)

    row4 = wx.BoxSizer()
    self._tech_area_union_chr_ckbtn = cb(_tech_area, label = '指定枚举列数时所用字符')
    self._tech_area_union_chr_entry = tc(_tech_area)

    row4.Add(self._tech_area_union_chr_ckbtn)
    row4.Add(self._tech_area_union_chr_entry, proportion = 1)

    row5 = wx.BoxSizer()
    self._tech_area_union_from_ckbtn = cb(_tech_area, label = '指定枚举列数时from的表名')
    self._tech_area_union_from_entry = tc(_tech_area)

    row5.Add(self._tech_area_union_from_ckbtn)
    row5.Add(self._tech_area_union_from_entry, proportion = 1)

    row6 = wx.BoxSizer()
    self._tech_area_dns_ckbtn = cb(_tech_area, label = '指定DNS')
    self._tech_area_dns_entry = tc(_tech_area)

    row6.Add(self._tech_area_dns_ckbtn)
    row6.Add(self._tech_area_dns_entry, proportion = 1)

    row7 = wx.BoxSizer()
    self._tech_area_second_url_ckbtn = cb(_tech_area, label = '指定二阶响应的url')
    self._tech_area_second_url_entry = tc(_tech_area)

    row7.Add(self._tech_area_second_url_ckbtn)
    row7.Add(self._tech_area_second_url_entry, proportion = 1)

    row8 = wx.BoxSizer()
    self._tech_area_second_req_ckbtn = cb(_tech_area, label = '使用含二阶HTTP请求的文件:')

    row8.Add(self._tech_area_second_req_ckbtn)

    row9 = wx.BoxSizer()
    self._tech_area_second_req_entry = tc(_tech_area)

    row9.Add(self._tech_area_second_req_entry, proportion = 1)

    tech_area.Add(row1, flag = wx.EXPAND)
    tech_area.Add(row2, flag = wx.EXPAND)
    tech_area.Add(row3, flag = wx.EXPAND)
    tech_area.Add(row4, flag = wx.EXPAND)
    tech_area.Add(row5, flag = wx.EXPAND)
    tech_area.Add(row6, flag = wx.EXPAND)
    tech_area.Add(row7, flag = wx.EXPAND)
    tech_area.Add(row8, flag = wx.EXPAND)
    tech_area.Add(row9, flag = wx.EXPAND)

    return tech_area

  def build_page1_setting_detection(self, panel):
    detection_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '探测选项')
    _detection_area = detection_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._detection_area_level_ckbtn = cb(_detection_area, label = '探测等级(范围)')
    self._detection_area_level_scale = sl(_detection_area,
                                          value = 1,
                                          minValue = 1,
                                          maxValue = 5,
                                          style = wx.SL_VALUE_LABEL)

    row1.Add(self._detection_area_level_ckbtn)
    row1.Add(self._detection_area_level_scale, proportion = 1)

    row2 = wx.BoxSizer()
    self._detection_area_risk_ckbtn = cb(_detection_area, label = 'payload危险等级')
    self._detection_area_risk_scale = sl(_detection_area,
                                         value = 1,
                                         minValue = 1,
                                         maxValue = 3,
                                         style = wx.SL_VALUE_LABEL)

    row2.Add(self._detection_area_risk_ckbtn)
    row2.Add(self._detection_area_risk_scale, proportion = 1)

    row3 = wx.BoxSizer()
    self._detection_area_str_ckbtn = cb(_detection_area, label = '指定字符串')
    self._detection_area_str_entry = tc(_detection_area)

    row3.Add(self._detection_area_str_ckbtn)
    row3.Add(self._detection_area_str_entry, proportion = 1)

    row4 = wx.BoxSizer()
    self._detection_area_not_str_ckbtn = cb(_detection_area, label = '指定字符串')
    self._detection_area_not_str_entry = tc(_detection_area)

    row4.Add(self._detection_area_not_str_ckbtn)
    row4.Add(self._detection_area_not_str_entry, proportion = 1)

    row5 = wx.BoxSizer()
    self._detection_area_re_ckbtn = cb(_detection_area, label = '指定正则')
    self._detection_area_re_entry = tc(_detection_area)

    row5.Add(self._detection_area_re_ckbtn)
    row5.Add(self._detection_area_re_entry, proportion = 1)

    row6 = wx.BoxSizer()
    self._detection_area_code_ckbtn = cb(_detection_area, label = '指定http状态码')
    self._detection_area_code_entry = tc(_detection_area)

    row6.Add(self._detection_area_code_ckbtn)
    row6.Add(self._detection_area_code_entry, proportion = 1)

    row7 = wx.BoxSizer()
    self._detection_area_text_only_ckbtn = cb(_detection_area, label = '仅对比文本')
    self._detection_area_titles_ckbtn = cb(_detection_area, label = '仅对比title')

    row7.Add(self._detection_area_text_only_ckbtn)
    row7.Add(self._detection_area_titles_ckbtn, proportion = 1)

    detection_area.Add(row1, flag = wx.EXPAND)
    detection_area.Add(row2, flag = wx.EXPAND)
    detection_area.Add(row3, flag = wx.EXPAND)
    detection_area.Add(row4, flag = wx.EXPAND)
    detection_area.Add(row5, flag = wx.EXPAND)
    detection_area.Add(row6, flag = wx.EXPAND)
    detection_area.Add(row7, flag = wx.EXPAND)

    return detection_area

  def build_page1_setting_inject(self, panel):
    inject_area = wx.StaticBoxSizer(wx.VERTICAL, panel, '注入选项')
    _inject_area = inject_area.GetStaticBox()

    row1 = wx.BoxSizer()
    self._inject_area_param_ckbtn = cb(_inject_area, label = '可测试的参数')
    self._inject_area_param_entry = tc(_inject_area)

    row1.Add(self._inject_area_param_ckbtn)
    row1.Add(self._inject_area_param_entry, proportion = 1)

    row2 = wx.BoxSizer()
    self._inject_area_skip_static_ckbtn = cb(_inject_area, label = '跳过无动态特性的参数')
    row2.Add(self._inject_area_skip_static_ckbtn)

    row3 = wx.BoxSizer()
    self._inject_area_prefix_ckbtn = cb(_inject_area, label = 'payload前缀')
    self._inject_area_prefix_entry = tc(_inject_area)
    row3.Add(self._inject_area_prefix_ckbtn)
    row3.Add(self._inject_area_prefix_entry, proportion = 1)

    row4 = wx.BoxSizer()
    self._inject_area_suffix_ckbtn = cb(_inject_area, label = 'payload后缀')
    self._inject_area_suffix_entry = tc(_inject_area)
    row4.Add(self._inject_area_suffix_ckbtn)
    row4.Add(self._inject_area_suffix_entry, proportion = 1)

    row5 = wx.BoxSizer()
    self._inject_area_skip_ckbtn = cb(_inject_area, label = '排除参数')
    self._inject_area_skip_entry = tc(_inject_area)
    row5.Add(self._inject_area_skip_ckbtn)
    row5.Add(self._inject_area_skip_entry, proportion = 1)

    row6 = wx.BoxSizer()
    self._inject_area_param_exclude_ckbtn = cb(_inject_area, label = '排除参数(正则)')
    self._inject_area_param_exclude_entry = tc(_inject_area)
    row6.Add(self._inject_area_param_exclude_ckbtn)
    row6.Add(self._inject_area_param_exclude_entry, proportion = 1)

    row7 = wx.BoxSizer()
    self._inject_area_dbms_ckbtn = cb(_inject_area, label = '固定DB类型为')
    self._inject_area_dbms_entry = tc(_inject_area)
    row7.Add(self._inject_area_dbms_ckbtn)
    row7.Add(self._inject_area_dbms_entry, proportion = 1)

    row8 = wx.BoxSizer()
    self._inject_area_dbms_cred_ckbtn = cb(_inject_area, label = 'DB认证')
    self._inject_area_dbms_cred_entry = tc(_inject_area)
    row8.Add(self._inject_area_dbms_cred_ckbtn)
    row8.Add(self._inject_area_dbms_cred_entry, proportion = 1)

    row9 = wx.BoxSizer()
    self._inject_area_os_ckbtn = cb(_inject_area, label = '固定OS为')
    self._inject_area_os_entry = tc(_inject_area)
    row9.Add(self._inject_area_os_ckbtn)
    row9.Add(self._inject_area_os_entry, proportion = 1)

    row10 = wx.BoxSizer()
    self._inject_area_no_cast_ckbtn = cb(_inject_area, label = '关掉payload变形机制')
    self._inject_area_no_escape_ckbtn = cb(_inject_area, label = '关掉string转义')
    row10.Add(self._inject_area_no_cast_ckbtn)
    row10.Add(self._inject_area_no_escape_ckbtn)    # 需要右对齐

    row11 = wx.BoxSizer()
    _invalid_label = st(_inject_area, label = '对payload中的废值:')
    self._inject_area_invalid_logic_ckbtn = cb(_inject_area, label = '使用逻辑运算符')
    row11.Add(_invalid_label, flag = wx.RIGHT)          # 需要对齐
    row11.Add(self._inject_area_invalid_logic_ckbtn)    # 需要对齐

    row12 = wx.BoxSizer()
    self._inject_area_invalid_bignum_ckbtn = cb(_inject_area, label = '使用大数')
    self._inject_area_invalid_str_ckbtn = cb(_inject_area, label = '使用随机字符串')
    row12.Add(self._inject_area_invalid_bignum_ckbtn)   # 需要对齐
    row12.Add(self._inject_area_invalid_str_ckbtn)      # 需要对齐

    inject_area.Add(row1, flag = wx.EXPAND)
    inject_area.Add(row2, flag = wx.EXPAND)
    inject_area.Add(row3, flag = wx.EXPAND)
    inject_area.Add(row4, flag = wx.EXPAND)
    inject_area.Add(row5, flag = wx.EXPAND)
    inject_area.Add(row6, flag = wx.EXPAND)
    inject_area.Add(row7, flag = wx.EXPAND)
    inject_area.Add(row8, flag = wx.EXPAND)
    inject_area.Add(row9, flag = wx.EXPAND)
    inject_area.Add(row10, flag = wx.EXPAND)
    inject_area.Add(row11, flag = wx.EXPAND)
    inject_area.Add(row12, flag = wx.EXPAND)

    return inject_area  # 一定要返回StaticBoxSizer, 不然会段错!


def main():
  app = wx.App()

  win = wx.Frame(None, title = 'sqlmap')

  n = Page1Notebook(win)

  box = wx.BoxSizer()
  box.Add(n, proportion = 1)
  win.SetSizerAndFit(box)

  win.Centre()
  win.Show()

  app.MainLoop()


if __name__ == '__main__':
  main()
