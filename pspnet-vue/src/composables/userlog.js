import { ref } from 'vue'
import axios from 'axios'

const error = ref(null)
const isPending = ref(false)

const login = async (email, pass) => {
  error.value = null
  isPending.value = true


  const path = 'http://127.0.0.1:5000/login'
  let login_credentials = {
        password : pass,
        email : email
      }
  try {
    const res = await axios.post(path, login_credentials)
    if (res.data.status == 'success'){
      error.value = null
    }
    else{
      error.value = "Incorrect Login Credentials"
    }
    isPending.value = false
    return res
  }catch(err){
    console.log(err)
    isPending.value = false
  }
}

const useLogin = () =>{
  return { error, login, isPending}
}

export default useLogin