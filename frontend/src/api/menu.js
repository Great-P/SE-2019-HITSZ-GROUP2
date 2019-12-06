const Menu = [
  { header: '数据分析' },
  {
    text: '数据仪表板',
    icon: 'dashboard',
    to: '/dashboard',
  },

  {
    text: '图表分析',
    group: 'widgets',
    to: '/widgets',
    icon: 'mdi-chart-areaspline',
    children: [
      { to: '/widgets/func1', text: '民生事件性质分类' },
      { to: '/widgets/func2', text: '各街道民生事件情况', badge: 'new' },
      { to: '/widgets/func3', text: '民生事件结办情况' },
      { to: '/widgets/func4', text: '热点社区分析' },
      { to: '/widgets/func5', text: '滚动事件预警' },
      { to: '/widgets/func6', text: '时间线概览' },
    ],
  },
  {
    text: '文件上传',
    to: '/fileupload',
    icon: 'perm_media',
  },
  { header: '个人设置' },
  {
    text: '我的信息',
    group: 'layout',
    to: 'userinfo',
    icon: 'view_compact',
    children: [{ to: '/userinfo/usermanage', text: '用户管理' },
              { to: '/userinfo/userinfo', text: '个人信息' },
              ],
  },
];

export default Menu
