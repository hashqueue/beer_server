import request from '@/utils/request'
import { removeToken, removeUserId } from '@/utils/auth'
/*
1. 如果发送get请求, 需要传参的话使用params
2. 如果发送post/put/delete/patch请求, 需要传body类型的参数的话使用data
3. params和data都是对象类型：{...}
 */
export function userRegister(data) {
  return request({
    url: '/auth/register/',
    method: 'post',
    data
  })
}

export function userLogin(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}
export function getUserProfile(userId) {
  return request({
    url: `/user/profile/${userId}/`,
    method: 'get'
  })
}

export function updateUserProfile(userId, data) {
  return request({
    url: `/user/profile/${userId}/`,
    method: 'put',
    data
  })
}

export function getGroupsList() {
  return request({
    url: '/groups/',
    method: 'get'
  })
}

export function logout() {
  removeToken()
  removeUserId()
}

export default {
  userLogin,
  userRegister,
  getUserProfile,
  updateUserProfile,
  getGroupsList,
  logout
}
