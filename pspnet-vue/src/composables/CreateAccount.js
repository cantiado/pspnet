import { ref } from 'vue'
import axios from 'axios'

const isPending = ref(false)
const error = ref(null)

const createAccount = async (firstname, lastname, email, password) => {
  error.value = null
  isPending.value = true

  const path = 'http://127.0.0.1:5000/register'
  let user_info = {
        firstname : firstname,
        lastname : lastname,
        email : email,
        password : password}
  try{
    const res = await axios.post(path, user_info)
    isPending.value = false
    return res
  }catch(err){
    console.log(err)
    error.value = err
    isPending.value = false
  }
}

const useCreate = ()=> {
  return {error, isPending, createAccount}
}

export default useCreate