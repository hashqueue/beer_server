import request from '@/utils/request'
/*
1. 如果发送get请求, 需要传参的话使用params
2. 如果发送post/put/delete/patch请求, 需要传body类型的参数的话使用data
3. params和data都是对象类型：{...}
 */
export function getTasksDataList(params) {
  return request({
    url: '/tasks/',
    method: 'get',
    params
  })
}

export function getTaskDetail(taskId) {
  return request({
    url: `/tasks/${taskId}/`,
    method: 'get'
  })
}

export function deleteDetailTask(taskId) {
  return request({
    url: `/tasks/${taskId}/`,
    method: 'delete'
  })
}

export default {
  getTasksDataList,
  getTaskDetail,
  deleteDetailTask
}
