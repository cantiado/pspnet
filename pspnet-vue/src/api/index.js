import axios from 'axios'

const url = 'http://127.0.0.1:5000/'

export function authenticate(userData){
  return axios.post(url + 'login/', userData)
}

export function register(userData){
  return axios.post(url + 'register/', userData)
}

export function testProtect(userData, jwt){
  return axios.post(url + 'protected/',userData,  )
}
