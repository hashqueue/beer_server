import request from '@/utils/request'
/*
1. 如果发送get请求, 需要传参的话使用params
2. 如果发送post/put/delete/patch请求, 需要传body类型的参数的话使用data
3. params和data都是对象类型：{...}
 */
export function getProjectsDataList(params) {
  return request({
    url: '/projects/',
    method: 'get',
    params
  })
}

export function createProject(data) {
  return request({
    url: '/projects/',
    method: 'post',
    data
  })
}

export function getProjectDetail(projectId) {
  return request({
    url: `/projects/${projectId}/`,
    method: 'get'
  })
}

export function updateProjectDetail(projectId, data) {
  return request({
    url: `/projects/${projectId}/`,
    method: 'put',
    data
  })
}

export function deleteDetailProject(projectId) {
  return request({
    url: `/projects/${projectId}/`,
    method: 'delete'
  })
}

export function runDetailProject(projectId, data) {
  return request({
    url: `/projects/${projectId}/run/`,
    method: 'post',
    data
  })
}

export default {
  getProjectsDataList,
  createProject,
  getProjectDetail,
  updateProjectDetail,
  deleteDetailProject,
  runDetailProject
}
