module.exports = {
    plugins: ['@vuepress/medium-zoom'],
    base: "/beer_server/",
    title: 'Beer接口自动化测试平台',
    description: '基于Django和Vue开发的接口自动化测试平台',
    markdown: {
        lineNumbers: true
    },
    themeConfig: {
    sidebar: [
      ['/', '首页'],
      ['/user-permission', '用户与权限管理'],
      ['/global-config', '全局配置管理'],
      ['/global-func', '全局函数管理'],
      ['/project', '项目管理'],
      ['/testsuite', '套件管理'],
      ['/test-task', '测试任务管理'],
    ]
  }
}