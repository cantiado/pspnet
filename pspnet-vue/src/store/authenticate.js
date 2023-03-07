import { authenticate, register, getUserData} from '@/api'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { Buffer } from 'buffer'

export const authStore = defineStore('authenticate', () => {
  const loading_data = ref(false)

  const loginUser = async (userData) => {
    try{
      loading_data.value = true
      const res = await authenticate(userData)
      localStorage.setItem('userToken', res.data.token)
      loading_data.value = false
      return ''
    }
    catch(err){
      loading_data.value = false
      return err.response.data.message
    }
  }

  const createUser = async (userData) => {
    try{
      loading_data.value = true
      const res = await register(userData)
      loading_data.value = false
      if (res.message == 'success'){
        return ''
      }
    }
    catch(err){
      loading_data.value = false
      return err.response.data.message
    }
  }

  const isAuthenticated = () => {
    const token = localStorage.getItem('userToken')
    if(!token){
      return false
    }
    if(token.split('.').length < 3){
      return false
    }
    //Using Buffer from to decode the string that is encoded with base64 encoding
    const jwt_str = Buffer.from(token.split('.')[1], 'base64')
    const data = JSON.parse(jwt_str)
    console.log(data)
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    console.log('exp', exp)
    console.log('now', now)
    return now < exp
  }

  const userData = async () => {
    try{
      const token = localStorage.getItem('userToken')
      const res = await getUserData(token)
      console.log(res.data)
      const name = res.data.name
      const email = res.data.email
      const role = res.data.role
      const id = res.data.id
      return {name, email, role, id}
    }catch(err){
      console.log(err.response.data.message)
    }
  }

  return { loginUser, createUser, isAuthenticated, userData, loading_data}
})
//note: axios will throw an error anytime the server responds with 4xx/5xx error. (i.e Bad Request 400)