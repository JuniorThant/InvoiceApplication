import { NavLink } from "react-router";

export default function SideBar() {

  return (
    <div className="w-64 h-screen bg-gray-100 text-gray-800 p-4 border-r fixed top-0 left-0 z-40 overflow-y-auto">
      <h2 className="text-2xl font-bold mb-8 text-gray-900">Invoice System</h2>
      <nav>
        <ul>
          <li>
            <NavLink
              to="/"
              className={({ isActive }: { isActive: boolean }) =>
                `block py-2 px-4 rounded ${
                  isActive ? "bg-gray-300" : "hover:bg-gray-200"
                }`
              }
            >
              Invoices
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/receipt"
              className={({ isActive }: { isActive: boolean }) =>
                `block py-2 px-4 rounded ${
                  isActive ? "bg-gray-300" : "hover:bg-gray-200"
                }`
              }
            >
              Receipts
            </NavLink>
          </li>
        </ul>
      </nav>
    </div>
  )
}
