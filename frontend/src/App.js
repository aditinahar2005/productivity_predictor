import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home.jsx";
import Visualize from "./pages/Visualize.jsx";


export default function App() {
    return (
        <Router>
            <div className="min-h-screen flex bg-gradient-to-br from-teal-50 via-blue-50 to-indigo-100">
                {/* Sidebar */}
                <nav className="w-72 bg-white shadow-xl p-8 flex flex-col">
                    <div className="mb-8">
                        <h1 className="text-3xl font-bold text-teal-600 mb-2">
                            🚀 Productivity
                        </h1>
                        <p className="text-gray-500 text-sm">Smart Activity Recommendations</p>
                    </div>

                    <div className="space-y-4">
                        <Link
                            to="/"
                            className="block p-4 text-gray-700 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition duration-200 font-medium"
                        >
                            🎯 Home - Get Recommendations
                        </Link>
                        <Link
                            to="/visualize"
                            className="block p-4 text-gray-700 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition duration-200 font-medium"
                        >
                            📊 Visualize Data
                        </Link>
                    </div>

                    <div className="mt-auto pt-8 border-t border-gray-200">
                        <p className="text-xs text-gray-400">
                            AI-powered productivity insights
                        </p>
                    </div>
                </nav>

                {/* Main content */}
                <main className="flex-1 p-10 overflow-auto">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/visualize" element={<Visualize />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}
