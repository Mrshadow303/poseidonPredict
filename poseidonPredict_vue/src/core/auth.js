import Cookies from 'js-cookie'

const TokenKey = 'token'

export function getToken() {
  return Cookies.get(TokenKey)
}
export function getUsername() {
  return Cookies.get('username')
}

export function getAccountNumber() {
  return Cookies.get('accountNumber')
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function setUsername(username) {
  return Cookies.set('username', username)
}

export function setAccountNumber(accountNumber) {
  return Cookies.set('accountNumber', accountNumber)
}

export function removeKey() {
  return Cookies.remove(TokenKey)
}

export function removeUsername() {
  return Cookies.remove('username')
}

export function removeAccountNumber() {
  return Cookies.remove('accountNumber')
}
