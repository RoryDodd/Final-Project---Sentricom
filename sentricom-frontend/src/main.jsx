// React core
import React from "react";

// Render app to DOM
import ReactDOM from "react-dom/client";

// Router for navigation
import { BrowserRouter } from "react-router-dom";

// Main app + styles
import App from "./App";
import "./index.css";

// Mount app to root element
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* Enable routing */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);