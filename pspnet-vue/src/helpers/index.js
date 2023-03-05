import { updateUserData } from '@/api'

export async function update_user_settings(user_data){
  const token = localStorage.getItem('userToken')
  try{
    await updateUserData(user_data, token)
  }
  catch(err){
    console.log(err)
  }
}