import request from '@/utils/request'
/*
1. 如果发送get请求, 需要传参的话使用params
2. 如果发送post/put/delete/patch请求, 需要传body类型的参数的话使用data
3. params和data都是对象类型：{...}
 */
export function getConfigsDataList(params) {
  return request({
    url: '/configs/',
    method: 'get',
    params
  })
}

export function createConfig(data) {
  return request({
    url: '/configs/',
    method: 'post',
    data
  })
}

export function getConfigDetail(configId) {
  return request({
    url: `/configs/${configId}/`,
    method: 'get'
  })
}

export function updateConfigDetail(configId, data) {
  return request({
    url: `/configs/${configId}/`,
    method: 'put',
    data
  })
}

export function deleteDetailConfig(configId) {
  return request({
    url: `/configs/${configId}/`,
    method: 'delete'
  })
}

export default {
  getConfigsDataList,
  createConfig,
  getConfigDetail,
  updateConfigDetail,
  deleteDetailConfig
}
