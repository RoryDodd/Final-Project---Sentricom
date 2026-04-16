import React from "react";

// Import ReactDOM for rendering the app
import ReactDOM from "react-dom/client";

// Import BrowserRouter for handling routing in the app
import { BrowserRouter } from "react-router-dom";

// Import the main App component and global styles
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
