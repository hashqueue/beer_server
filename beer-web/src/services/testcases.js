import request from '@/utils/request'
/*
1. 如果发送get请求, 需要传参的话使用params
2. 如果发送post/put/delete/patch请求, 需要传body类型的参数的话使用data
3. params和data都是对象类型：{...}
 */
export function getTestcasesDataList(params) {
  return request({
    url: '/testcases/',
    method: 'get',
    params
  })
}

export function createTestcase(data) {
  return request({
    url: '/testcases/',
    method: 'post',
    data
  })
}

export function getTestcaseDetail(testcaseId) {
  return request({
    url: `/testcases/${testcaseId}/`,
    method: 'get'
  })
}

export function updateTestcaseDetail(testcaseId, data) {
  return request({
    url: `/testcases/${testcaseId}/`,
    method: 'put',
    data
  })
}

export function deleteDetailTestcase(testcaseId) {
  return request({
    url: `/testcases/${testcaseId}/`,
    method: 'delete'
  })
}

export function runDetailTestcase(testcaseId, data) {
  return request({
    url: `/testcases/${testcaseId}/run/`,
    method: 'post',
    data
  })
}

export default {
  getTestcasesDataList,
  createTestcase,
  getTestcaseDetail,
  updateTestcaseDetail,
  deleteDetailTestcase,
  runDetailTestcase
}
