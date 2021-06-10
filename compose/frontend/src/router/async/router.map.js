// 视图组件
const view = {
  tabs: () => import('@/layouts/tabs'),
  blank: () => import('@/layouts/BlankView'),
  page: () => import('@/layouts/PageView')
}

// 路由组件注册
const routerMap = {
  login: {
    authority: '*',
    path: '/login',
    component: () => import('@/views/login')
  },
  exp403: {
    authority: '*',
    name: 'exp403',
    path: '403',
    component: () => import('@/views/exception/403')
  },
  exp404: {
    name: 'exp404',
    path: '404',
    component: () => import('@/views/exception/404')
  },
  exp500: {
    name: 'exp500',
    path: '500',
    component: () => import('@/views/exception/500')
  },
  root: {
    path: '/',
    name: '首页',
    redirect: '/login',
    component: view.tabs
  },
  parent1: {
    name: '父级路由1',
    icon: 'dashboard',
    component: view.blank
  },
  parent2: {
    name: '父级路由2',
    icon: 'form',
    component: view.page
  },
  exception: {
    name: '异常页',
    icon: 'warning',
    component: view.blank
  }
}
export default routerMap
