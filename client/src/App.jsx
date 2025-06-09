import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Signup from "./Signup";
import Login from "./Login";
import UninePayment from "./Home"; // Fix import
import Navbar from "./Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<UninePayment />} /> {/* Fix Route */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
