import Cookies from 'js-cookie'

const TokenKey = 'token'
const userIdKey = 'userId'

/**
 * 从浏览器cookies中获取token值
 * @returns {*}
 */
export function getToken() {
  return Cookies.get(TokenKey)
}

/***
 * 在cookies中设置用户的token值
 * @param token 登录接口返回的用户的token
 * @returns {*}
 */
export function setToken(token) {
  return Cookies.set(TokenKey, token, { expires: 1 })
}

/**
 * 用户退出系统时手动删除用户的token
 * @returns {*}
 */
export function removeToken() {
  return Cookies.remove(TokenKey)
}

/**
 * 获取当前登录用户的id
 * @returns {*}
 */
export function getUserId() {
  return Cookies.get(userIdKey)
}

/**
 * 用户登录时设置用户的id
 * @param userId
 * @returns {*}
 */
export function setUserId(userId) {
  return Cookies.set(userIdKey, userId)
}

/**
 * 用户退出系统时手动删除用户的id
 * @returns {*}
 */
export function removeUserId() {
  return Cookies.remove(userIdKey)
}

/**
 * 设置当前登录用户的信息
 * @param userInfo
 */
export function setUserInfo(userInfo) {
  localStorage.setItem(process.env.VUE_APP_USER_KEY, JSON.stringify(userInfo))
}

export function getUserInfo() {
  return JSON.parse(localStorage.getItem(process.env.VUE_APP_USER_KEY))
}

export function removeUserInfo() {
  localStorage.removeItem(process.env.VUE_APP_USER_KEY)
}
