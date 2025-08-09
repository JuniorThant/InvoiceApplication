import axios from "axios";
import { API } from "@/types/api";

const APP_URL = import.meta.env.APP_URL || "";

export const getAllReceiptService = async (token: string,search_term?:string): Promise<API.ReceiptList.Http200.ResponseBody> => {
  if (!token) throw new Error("No auth token provided");

  try {
    const response = await axios.get(`${APP_URL}/receipt`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      params:{search_term}
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createReceiptService = async (data: API.ReceiptCreate.RequestBody, token: string) => {
  if (!token) throw new Error("No auth token provided");

  try {
    const response = await axios.post<API.ReceiptCreate.Http201.ResponseBody>(
      `${APP_URL}/receipt`,
      data,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteReceiptService=async(receiptId:string,token:string)=>{
  if(!token) throw new Error("No auth token provided");
  try{
    await axios.delete(`${APP_URL}/receipt/${receiptId}`,{
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
  }catch(error){
    throw error
  }
}


export const sendReceiptEmailService=async(receiptId:string,token:string):Promise<void>=>{
  if(!token) throw new Error("No auth token provided");

  try{
    await axios.post(`${APP_URL}/receipt/${receiptId}/send`,null,{
      headers:{
        Authorization:`Bear ${token}`,
        "Content-Type":"application/json"
      }
    })
  }catch(error){
    throw error;
  }
}