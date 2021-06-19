module.exports = {
    base: "/beer_server/",
    title: 'Beer接口自动化测试平台',
    description: '基于Django和Vue开发的接口自动化测试平台',
    markdown: {
        lineNumbers: true
    },
    themeConfig: {
    sidebar: [
      ['/', '首页'],
      ['/用户与权限管理', '用户与权限管理'],
      ['/全局配置管理', '全局配置管理'],
      ['/全局函数管理', '全局函数管理'],
      ['/项目管理', '项目管理'],
      ['/套件管理', '套件管理'],
      ['/测试任务管理', '测试任务管理'],
    ]
  }
}