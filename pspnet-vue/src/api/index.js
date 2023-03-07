import axios from 'axios'

const url = 'http://127.0.0.1:5000/'

export function authenticate(userData){
  return axios.post(url + 'login/', userData)
}

export function register(userData){
  return axios.post(url + 'register/', userData)
}

export async function getUserData(jwt){
  return await axios.get(url + 'userdata/', { headers: { token : jwt}})
}

export async function updateUserData(userData, jwt){
  return await axios.put(url + 'settings/', userData, {headers : {token : jwt}})
}

export async function getProfileData(id){
  return await axios.put(url + 'profile/')
}

export async function getExplore(){
  return await axios.put(url + 'explore/')
}

export async function getDatasets(ds_name) {
  return await axios.post(url + 'datasets/')
}

<<<<<<< HEAD
export function sendEmail(userEmail){
  return axios.post(url + 'forgotpass/', { 'email' : userEmail})
}

export function resetPass(userData, jwt){
  return axios.post(url + 'changePass/', userData, {headers : {token : jwt}})
=======
export async function getDatasetImgs(ds_name) {
  return await axios.post(url + 'datasetview/')
>>>>>>> main
}