import React, { useState } from "react";
import axios from "axios";

export default function FeatureCompare() {
    const [graphType, setGraphType] = useState("histogram");
    const [column1, setColumn1] = useState("TaskType");
    const [column2, setColumn2] = useState("Mood");
    const [imageUrl, setImageUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const validCols = [
        { value: "TaskType", label: "Task Type (Study, Exercise, etc.)" },
        { value: "Mood", label: "Mood (1-10)" },
        { value: "SleepHours", label: "Hours of Sleep" },
        { value: "Distractions", label: "Distraction Level" },
        { value: "ConfidenceScore", label: "Confidence Score" },
        { value: "DayOfWeek", label: "Day of Week" },
        { value: "Completed", label: "Tasks Completed" },
        { value: "Duration", label: "Duration" }
    ];

    const suggestions = {
        histogram: ["TaskType", "Mood", "SleepHours", "ConfidenceScore"],
        bar: [
            { x: "TaskType", y: "Mood", desc: "Average mood by task type" },
            { x: "DayOfWeek", y: "SleepHours", desc: "Sleep patterns by day" },
            { x: "TaskType", y: "Duration", desc: "Time spent on each activity" }
        ],
        scatter: [
            { x: "Mood", y: "ConfidenceScore", desc: "Mood vs Confidence relationship" },
            { x: "SleepHours", y: "Mood", desc: "Sleep quality impact on mood" },
            { x: "Distractions", y: "Completed", desc: "Distraction vs productivity" }
        ]
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError(null);
        setImageUrl(null);

        try {
            console.log("Sending visualization request:", {
                graphType,
                column1,
                column2: graphType === "scatter" || graphType === "bar" ? column2 : null,
            });

            const res = await axios.post("http://localhost:5000/visualize", {
                graphType,
                column1,
                column2: graphType === "scatter" || graphType === "bar" ? column2 : null,
            }, {
                responseType: 'blob',
                timeout: 30000
            });

            const url = URL.createObjectURL(res.data);
            setImageUrl(url);
        } catch (err) {
            console.error("Visualization error:", err);
            if (err.response) {
                const reader = new FileReader();
                reader.onload = () => {
                    try {
                        const errorData = JSON.parse(reader.result);
                        setError(errorData.error || 'Server error occurred');
                    } catch (e) {
                        setError(`Server error: ${err.response.status}`);
                    }
                };
                reader.readAsText(err.response.data);
            } else if (err.request) {
                setError('Cannot connect to server. Make sure backend is running on http://localhost:5000');
            } else {
                setError(`Error: ${err.message}`);
            }
        } finally {
            setLoading(false);
        }
    };

    const applySuggestion = (suggestion) => {
        if (typeof suggestion === 'object') {
            setColumn1(suggestion.x);
            setColumn2(suggestion.y);
        }
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-lg max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-800 mb-8">📊 Data Visualization</h2>

            {error && (
                <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                    {error}
                </div>
            )}

            <div className="flex flex-col space-y-8">
                {/* Controls Section */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">Graph Type</label>
                        <select
                            value={graphType}
                            onChange={e => setGraphType(e.target.value)}
                            className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                        >
                            <option value="histogram">📊 Histogram</option>
                            <option value="bar">📈 Bar Chart</option>
                            <option value="scatter">⚡ Scatter Plot</option>
                            <option value="heatmap">🔥 Correlation Heatmap</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            {graphType === "histogram" ? "Column" : "X-Axis (Primary)"}
                        </label>
                        <select
                            value={column1}
                            onChange={e => setColumn1(e.target.value)}
                            className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                        >
                            {validCols.map((col) => (
                                <option key={col.value} value={col.value}>{col.label}</option>
                            ))}
                        </select>
                    </div>

                    {(graphType === "scatter" || graphType === "bar") && (
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Y-Axis (Secondary)</label>
                            <select
                                value={column2}
                                onChange={e => setColumn2(e.target.value)}
                                className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                            >
                                {validCols.map((col) => (
                                    <option key={col.value} value={col.value}>{col.label}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    <div className="flex items-end">
                        <button
                            onClick={handleSubmit}
                            disabled={loading}
                            className="w-full bg-teal-600 text-white px-6 py-4 rounded-lg hover:bg-teal-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition duration-200 font-semibold text-lg"
                        >
                            {loading ? "Generating..." : "🎨 Generate Chart"}
                        </button>
                    </div>
                </div>

                {/* Suggestions Section */}
                {(graphType === "bar" || graphType === "scatter" || graphType === "histogram") && (
                    <div className="bg-gray-50 p-6 rounded-lg">
                        <h3 className="text-lg font-semibold text-gray-700 mb-4">💡 Quick Suggestions:</h3>
                        <div className="flex flex-wrap gap-3">
                            {graphType === "histogram" && suggestions.histogram.map((col, index) => (
                                <button
                                    key={index}
                                    onClick={() => setColumn1(col)}
                                    className="px-4 py-2 bg-white rounded-lg border hover:bg-teal-50 hover:border-teal-300 transition text-sm font-medium"
                                >
                                    {col} distribution
                                </button>
                            ))}

                            {(graphType === "bar" || graphType === "scatter") && suggestions[graphType] && suggestions[graphType].map((suggestion, index) => (
                                <button
                                    key={index}
                                    onClick={() => applySuggestion(suggestion)}
                                    className="px-4 py-2 bg-white rounded-lg border hover:bg-teal-50 hover:border-teal-300 transition text-sm"
                                >
                                    <div className="font-medium">{suggestion.x} vs {suggestion.y}</div>
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Chart Display Section - MUCH BIGGER */}
                <div className="w-full">
                    {loading && (
                        <div className="flex justify-center items-center h-96 bg-gray-50 rounded-lg">
                            <div className="text-center">
                                <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-teal-600 mx-auto mb-4"></div>
                                <p className="text-gray-600 text-lg">Generating your visualization...</p>
                            </div>
                        </div>
                    )}

                    {imageUrl && (
                        <div className="w-full">
                            <h3 className="text-xl font-semibold text-gray-800 mb-4">📈 Generated Visualization</h3>
                            <div className="w-full bg-white p-4 rounded-lg shadow-lg border">
                                <img
                                    src={imageUrl}
                                    alt="Generated Graph"
                                    className="w-full h-auto max-w-none rounded-lg"
                                    style={{ minHeight: '600px', objectFit: 'contain' }}
                                />
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
