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
