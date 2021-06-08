import request from '@/utils/request'
/*
1. 如果发送get请求, 需要传参的话使用params
2. 如果发送post/put/delete/patch请求, 需要传body类型的参数的话使用data
3. params和data都是对象类型：{...}
 */
export function getFunctionsDataList(params) {
  return request({
    url: '/functions/',
    method: 'get',
    params
  })
}

export function createFunction(data) {
  return request({
    url: '/functions/',
    method: 'post',
    data
  })
}

export function getFunctionDetail(functionId) {
  return request({
    url: `/functions/${functionId}/`,
    method: 'get'
  })
}

export function updateFunctionDetail(functionId, data) {
  return request({
    url: `/functions/${functionId}/`,
    method: 'put',
    data
  })
}

export function deleteDetailFunction(functionId) {
  return request({
    url: `/functions/${functionId}/`,
    method: 'delete'
  })
}

export default {
  getFunctionsDataList,
  createFunction,
  getFunctionDetail,
  updateFunctionDetail,
  deleteDetailFunction
}
