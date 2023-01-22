import { authenticate, register} from '@/api'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const authStore = defineStore('authenticate', () => {
  const jwt = ref('')
  const user = ref({})
  const loading_data = ref(false)

  const loginUser = async (userData) => {
    try{
      loading_data.value = true
      const res = await authenticate(userData)
      jwt.value = res.data.token
      loading_data.value = false
      user.email = res.data.email
      user.firstname = res.data.firstname
      user.lastname = res.data.lastname
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
      await register(userData)
      loading_data.value = false
      return ''
    }
    catch(err){
      loading_data.value = false
      return err.response.data.message
    }
  }

  const isAuthenticated = computed(() => {
    if(!jwt.value || jwt.value.split('.').length < 3){
      return false
    }
    //Using Buffer from to decode the string that is encoded with base64 encoding
    const data = JSON.parse(Buffer.from(jwt.value.split('.')[1], 'base64'))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
  })
  return { loginUser, createUser, isAuthenticated, loading_data, user, jwt }
})
//note: axios will throw an error anytime the server responds with 4xx/5xx error. (i.e Bad Request 400)