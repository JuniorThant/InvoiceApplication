import axios from "axios";
import { API } from "@/types/api";

const APP_URL = import.meta.env.APP_URL || "";

export const getAllInvoiceService = async (token: string): Promise<API.InvoiceList.Http200.ResponseBody> => {
  if (!token) throw new Error("No auth token provided");

  try {
    const response = await axios.get(`${APP_URL}/invoice`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createInvoiceService = async (data: API.InvoiceCreate.RequestBody, token: string) => {
  if (!token) throw new Error("No auth token provided");

  try {
    const response = await axios.post<API.InvoiceCreate.Http201.ResponseBody>(
      `${APP_URL}/invoice`,
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
    await axios.delete(`${APP_URL}/invoice/${invoiceId}`,{
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
    await axios.post(`${APP_URL}/invoice/${invoiceId}/send`, null, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
  } catch (error) {
    throw error;
  }
};
