import axios from "axios";
import type { API } from "../api"

const APP_URL = import.meta.env.APP_URL || "";

export const getAllInvoiceService = async (token: string,search_term?:string): Promise<API.InvoiceList.Http200.ResponseBody> => {
  if (!token) throw new Error("No auth token provided");

  try {
    const response = await axios.get("http://localhost:8015/invoice", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      params:{search_term},
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getInvoiceByNumber=async(token:string,invoiceId:string):Promise<API.InvoiceList.Http200.InvoiceSummary>=>{
  if (!token) throw new Error("No auth token provided");

  try{
    const response=await axios.get(`http://localhost:8015/invoice/${invoiceId}`,{
      headers:{
        Authorization:`Bearer ${token}`,
        "Content-Type":"application/json"
      }
    })
    return response.data
  }catch(error){
    throw error
  }

}

export const createInvoiceService = async (data: API.InvoiceCreate.RequestBody, token: string) => {
  if (!token) throw new Error("No auth token provided");

  try {
    const response = await axios.post<API.InvoiceCreate.Http201.ResponseBody>(
      `http://localhost:8015/invoice`,
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

export const deleteInvoiceService=async(invoiceId:string,token:string)=>{
  if(!token) throw new Error("No auth token provided");
  try{
    await axios.delete(`http://localhost:8015/invoice/${invoiceId}`,{
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
  }catch(error){
    throw error
  }
}

export const sendInvoiceEmailService = async (invoiceId: string, token: string): Promise<void> => {
  if (!token) throw new Error("No auth token provided");

  try {
    await axios.post(`http://localhost:8015/invoice/${invoiceId}/send`, null, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    throw error;
  }
};
