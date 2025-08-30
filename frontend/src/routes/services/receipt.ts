import axios from "axios";
import type { API } from "../api"

const APP_URL = import.meta.env.APP_URL || "";

export const getAllReceiptService = async (token: string,search_term?:string,currentPage?:number): Promise<API.ReceiptList.Http200.ResponseBody> => {
  if (!token) throw new Error("No auth token provided");

  try {
    const response = await axios.get(`http://localhost:8015/receipt`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      params:{search_term,currentPage}
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
      `http://localhost:8015/receipt`,
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
    await axios.delete(`http://localhost:8015/receipt/${receiptId}`,{
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
    await axios.post(`http://localhost:8015/receipt/${receiptId}/send`,null,{
      headers:{
        Authorization:`Bear ${token}`,
        "Content-Type":"application/json"
      }
    })
  }catch(error){
    throw error;
  }
}