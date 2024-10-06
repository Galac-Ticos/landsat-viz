import React from "react";
import { Navigate } from "react-router-dom";

const isAuthenticated = () => {
  return localStorage.getItem("authToken") !== null;
};

const ProtectedRoute = ({ element }) => {
  return isAuthenticated() ? element : <Navigate to="/login" replace />;
};

export default ProtectedRoute;
