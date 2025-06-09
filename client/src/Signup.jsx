import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // 👈 Import useNavigate

const Signup = () => {
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState(""); // State for error messages
  const navigate = useNavigate(); // 👈 Initialize navigate

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Reset error message

    console.log("Signup button clicked!");  
    console.log("User Data:", formData);  

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match!"); // Show error instead of alert
      return;
    }

    try {
      console.log("Sending request to backend...");
      const res = await axios.post("http://localhost:5000/signup", formData);

      console.log("Response received:", res);
      alert("Signup successful! Redirecting to login...");
      navigate("/login"); // ✅ Redirect to login page

    } catch (error) {
      console.error("Axios request failed!", error);
      setError(error.response?.data?.message || "Signup failed! Please try again.");
    }
  };

  return (
    <div className="bg-black text-white min-h-screen flex justify-center items-center">
      <div className="bg-gray-900 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-3xl font-bold text-center mb-6">Register</h2>
        {error && <p className="text-red-500 text-center">{error}</p>} {/* Display error message */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="name" className="block font-bold mb-2">Name</label>
            <input type="text" name="name" placeholder="Enter your name" value={formData.name} onChange={handleChange} className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg" required />
          </div>
          <div>
            <label htmlFor="phone" className="block font-bold mb-2">Phone Number</label>
            <input type="tel" name="phone" placeholder="Enter your phone number" value={formData.phone} onChange={handleChange} className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg" required />
          </div>
          <div>
            <label htmlFor="email" className="block font-bold mb-2">Email</label>
            <input type="email" name="email" placeholder="Enter your email" value={formData.email} onChange={handleChange} className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg" required />
          </div>
          <div>
            <label htmlFor="password" className="block font-bold mb-2">Password</label>
            <input type="password" name="password" placeholder="Enter your password" value={formData.password} onChange={handleChange} className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg" required />
          </div>
          <div>
            <label htmlFor="confirmPassword" className="block font-bold mb-2">Confirm Password</label>
            <input type="password" name="confirmPassword" placeholder="Confirm your password" value={formData.confirmPassword} onChange={handleChange} className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg" required />
          </div>
          <button type="submit" className="bg-green-500 text-black px-6 py-3 rounded-lg hover:bg-green-400 w-full">
            Register
          </button>
        </form>
      </div>
    </div>
  );
};

export default Signup;
