import React from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

const Navbar = () => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user")); // 🔥 Check if user is logged in

  const handleLogout = async () => {
    try {
      await axios.post("http://localhost:5000/logout", {}, { withCredentials: true });

      // ✅ Clear stored user data
      localStorage.removeItem("user");
      localStorage.removeItem("token"); 

      alert("Logged out successfully!");
      navigate("/login");
    } catch (error) {
      console.error("Logout failed!", error.response?.data?.message || error.message);
    }
  };

  return (
    <nav className="bg-gray-900 text-white p-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold">Smart Invest</h1>
      <div className="space-x-4">
        {/* Always show Signup & Login */}
        <Link to="/signup" className="hover:text-green-400">Signup</Link>
        <Link to="/login" className="hover:text-green-400">Login</Link>

        {/* Show Logout only if user is logged in */}
        {user && (
          <button 
            onClick={handleLogout} 
            className="hover:text-red-400 ml-4"
          >
            Logout
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
