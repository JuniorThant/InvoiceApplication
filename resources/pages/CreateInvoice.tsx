// import React, { useState } from "react";
// import { createInvoiceService } from "@/services/invoice";
// import { useNavigate } from "react-router-dom";
// import { useAuth } from "@/contexts/AuthProvider";
// import { API } from "@/types/api";

// export default function CreateInvoice() {
//   const { auth } = useAuth();
//   const navigate = useNavigate();

//   const [formData, setFormData] = useState<API.InvoiceCreate.RequestBody>({
//     invoiceNumber: "",
//     customerName: "",
//     customerMail:"",
//     companyName: "",
//     invoiceDate: "",
//     credit: "",
//     dueDate: "",
//     remark: "",
//     subtotal: 0,
//     vat: 0,
//     totalAmount: 0,
//     items: [],
//   });

//   const [message, setMessage] = useState("");
//   const [itemsCount,setItemsCount]=useState([]);

//   const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
//     const { name, value } = e.target;
//     const formItems=itemsCount
//     setFormData((prev) => ({
//       ...prev,
//       formItems,
//       [name]: ["subtotal", "vat", "totalAmount"].includes(name) ? parseFloat(value) : value,
//     }));
//   };

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();

//     if (!auth?.token) {
//       setMessage("Unauthorized.");
//       return;
//     }

//     try {
//       await createInvoiceService(formData, auth.token);
//       setMessage("Invoice created successfully!");
//       setTimeout(() => navigate("/"), 1000);
//     } catch (error: any) {
//       setMessage(`Error creating invoice: ${error.message}`);
//     }
//   };

//   return (
//     <div className="p-6">
//       <h2 className="text-2xl font-bold mb-4 text-center">Create Invoice</h2>
//       <form onSubmit={handleSubmit} className="space-y-4 flex w-[100%]">
//         <div className="w-[40%]">
//         <div>
//           <label className="block mb-1 font-medium">Invoice Number</label>
//           <input
//             name="invoiceNumber"
//             value={formData.invoiceNumber}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Customer Name</label>
//           <input
//             name="customerName"
//             value={formData.customerName}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Customer Email</label>
//           <input
//             name="customerMail"
//             value={formData.customerMail}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Company Name</label>
//           <input
//             name="companyName"
//             value={formData.companyName}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Invoice Date</label>
//           <input
//             type="date"
//             name="invoiceDate"
//             value={formData.invoiceDate}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Credit Terms</label>
//           <input
//             name="credit"
//             value={formData.credit}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Due Date</label>
//           <input
//             type="date"
//             name="dueDate"
//             value={formData.dueDate}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Remark</label>
//           <textarea
//             name="remark"
//             value={formData.remark}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Subtotal</label>
//           <input
//             type="number"
//             name="subtotal"
//             value={formData.subtotal}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">VAT</label>
//           <input
//             type="number"
//             name="vat"
//             value={formData.vat}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Total Amount</label>
//           <input
//             type="number"
//             name="totalAmount"
//             value={formData.totalAmount}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>
//           <button
//           type="submit"
//           className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
//         >
//           Submit Invoice
//         </button>

//         {message && <p className="mt-2 text-sm text-red-600">{message}</p>}
//         </div>
//         <div className="w-[20%]"></div>
//         <div className="w-[40%]">
//         <button type="button" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700" onClick={handleItems}>
//           Add Items
//         </button>
//         <div>
//           <label className="block mb-1 font-medium">Customer Name</label>
//           <input
//             name="customerName"
//             value={formData.items.name}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Customer Email</label>
//           <input
//             name="customerMail"
//             value={formData.customerMail}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>

//         <div>
//           <label className="block mb-1 font-medium">Company Name</label>
//           <input
//             name="companyName"
//             value={formData.companyName}
//             onChange={handleChange}
//             className="w-full p-2 border rounded"
//             required
//           />
//         </div>
//         </div>
      
 
//       </form>
//     </div>
//   );
// }
