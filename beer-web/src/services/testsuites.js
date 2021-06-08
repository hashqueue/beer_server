import request from '@/utils/request'
/*
1. 如果发送get请求, 需要传参的话使用params
2. 如果发送post/put/delete/patch请求, 需要传body类型的参数的话使用data
3. params和data都是对象类型：{...}
 */
export function getTestSuitesDataList(params) {
  return request({
    url: '/testsuites/',
    method: 'get',
    params
  })
}

export function createTestSuite(data) {
  return request({
    url: '/testsuites/',
    method: 'post',
    data
  })
}

export function getTestSuiteDetail(testsuiteId) {
  return request({
    url: `/testsuites/${testsuiteId}/`,
    method: 'get'
  })
}

export function updateTestSuiteDetail(testsuiteId, data) {
  return request({
    url: `/testsuites/${testsuiteId}/`,
    method: 'put',
    data
  })
}

export function deleteDetailTestSuite(testsuiteId) {
  return request({
    url: `/testsuites/${testsuiteId}/`,
    method: 'delete'
  })
}

export function runDetailTestSuite(testsuiteId, data) {
  return request({
    url: `/testsuites/${testsuiteId}/run/`,
    method: 'post',
    data
  })
}

export default {
  getTestSuitesDataList,
  createTestSuite,
  getTestSuiteDetail,
  updateTestSuiteDetail,
  deleteDetailTestSuite,
  runDetailTestSuite
}
