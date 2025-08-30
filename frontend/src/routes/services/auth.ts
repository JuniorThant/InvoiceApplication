import axios from "axios"
import type { API } from "../api"

const APP_URL = import.meta.env.APP_URL || ""
export const registerUserService = async (data: any) => {
  try {
    const response = await axios.post<API.AccountRegister.Http201.ResponseBody>(
      `http://localhost:8015/api/access/signup`,
      data
    )
    return response.data
  } catch (error) {
    throw error
  }
}

export const loginUserService = async (data: any) => {
  try {
    return await axios.post<API.AccountLogin.Http201.ResponseBody>(
      `${APP_URL}/api/access/login`,
      data,
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }
    )
  } catch (error) {
    throw error
  }
}


export const createUserService = async (data: any,token:string) => {
  try {
    const response = await axios.post<API.AccountRegister.Http201.ResponseBody>(
      `http://localhost:8015/api/users`,
      data,
      {
        headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      }
    )
    return response.data
  } catch (error) {
    throw error
  }
}

export const getMeService=async(token:string)=>{
  try{
    const res=await axios.get<API.CreateUser.RequestBody>(
      `http://localhost:8015/api/me`,
      {
        headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      }
    )
    return res.data
  }catch(error){
    throw error
  }
}

export const getUsersService=async(token:string,search_term?:string)=>{
  try{
    return await axios.get<API.UserList.HTTP200.ResponseBody>(
      `http://localhost:8015/api/users`,
      {
        headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      params:{search_term}
      }
    )
  }catch(error){
    throw error
  }
}

export const changeRoleService = async (token: string, userId: string) => {
  try {
    const res= await axios.patch(
      `http://localhost:8015/api/access/changerole/${userId}`,
      {},  
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    )
    return res.data
  } catch (error) {
    throw error
  }
}

export const deleteUserService=async(userId:string,token:string)=>{
  if(!token) throw new Error("No auth token provided");
  try{
    await axios.delete(`http://localhost:8015/api/users/${userId}`,{
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
  }catch(error){
    throw error
  }
}

