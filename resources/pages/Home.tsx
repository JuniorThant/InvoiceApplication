import { useAuth } from "@/contexts/AuthProvider";
import MainLayout from "@/layouts/MainLayout";
import { useEffect, useState } from "react";
import { getAllInvoiceService } from "@/services/invoice";
import { useNavigate } from "react-router-dom";
import type { API } from "@/types/api";

const Home: React.FC = () => {
  const { auth } = useAuth();
  const navigate = useNavigate();

  const [invoices, setInvoices] = useState<API.InvoiceList.Http200.InvoiceSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchInvoices = async () => {
      if (!auth?.token) {
        setError("No auth token found. Please log in.");
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const data = await getAllInvoiceService(auth.token);
        setInvoices(data.items);
      } catch (e: any) {
        setError(`Failed to fetch invoices: ${e.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchInvoices();
  }, [auth?.token]);

  const formatAmount = (amount: unknown): string => {
    const num = Number(amount);
    if (isNaN(num)) return "0.00";
    return num.toFixed(2);
  };

  return (
    <MainLayout
      title="Litestar Application - Home"
      description="Litestar Application - Home"
      keywords="home"
    >
      <div className="p-4">
        <button
          onClick={() => navigate("/create/invoice")}
          className="mb-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Create New Invoice
        </button>

        {loading && <p>Loading invoices...</p>}
        {error && <p className="text-red-600">{error}</p>}
        {!loading && !error && (
          <div className="relative overflow-x-auto shadow-md sm:rounded-lg">
            <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
              <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                  <th className="px-6 py-3">Invoice Number</th>
                  <th className="px-6 py-3">Customer Name</th>
                  <th className="px-6 py-3">Company Name</th>
                  <th className="px-6 py-3">Invoice Date</th>
                  <th className="px-6 py-3">Total Amount</th>
                </tr>
              </thead>
              <tbody>
                {invoices.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-4 text-center">
                      No invoices found.
                    </td>
                  </tr>
                ) : (
                  invoices.map((invoice) => (
                    <tr
                      key={invoice.id}
                      className="odd:bg-white even:bg-gray-50 border-b dark:border-gray-700"
                    >
                      <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                        {invoice.invoiceNumber}
                      </td>
                      <td className="px-6 py-4">{invoice.customerName}</td>
                      <td className="px-6 py-4">{invoice.companyName}</td>
                      <td className="px-6 py-4">{invoice.invoiceDate}</td>
                      <td className="px-6 py-4">${formatAmount(invoice.totalAmount)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default Home;
