import React, { useState } from "react";
import axios from "axios";

export default function PredictionForm({ onPredict }) {
    const [inputs, setInputs] = useState({
        Mood: 5,
        Hour: 14,
        "Week(day/end)": 0,
        SleepHours: 7,
        Distractions: 2,
        ConfidenceScore: 6,
        Completed: 1,
        DayOfWeek: 2,
    });

    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const fieldLabels = {
        Mood: "Mood (1-10)",
        Hour: "Current Hour (0-23)",
        "Week(day/end)": "Weekend (0=Weekday, 1=Weekend)",
        SleepHours: "Hours of Sleep (0-24)",
        Distractions: "Distraction Level (0-10)",
        ConfidenceScore: "Confidence Score (1-10)",
        Completed: "Tasks Completed Today (0-50)",
        DayOfWeek: "Day of Week (0=Mon, 6=Sun)",
    };

    const fieldDescriptions = {
        Mood: "How are you feeling right now?",
        Hour: "What time is it?",
        "Week(day/end)": "Is it a weekend?",
        SleepHours: "How many hours did you sleep last night?",
        Distractions: "How distracted do you feel?",
        ConfidenceScore: "How confident do you feel about being productive?",
        Completed: "How many tasks have you completed today?",
        DayOfWeek: "What day of the week is it?",
    };

    const fieldConstraints = {
        Mood: { min: 1, max: 10 },
        Hour: { min: 0, max: 23 },
        "Week(day/end)": { min: 0, max: 1 },
        SleepHours: { min: 0, max: 24 },
        Distractions: { min: 0, max: 10 },
        ConfidenceScore: { min: 1, max: 10 },
        Completed: { min: 0, max: 50 },
        DayOfWeek: { min: 0, max: 6 },
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        const numValue = Number(value);

        // Check validity
        const { min, max } = fieldConstraints[name];
        setErrors((prev) => ({
            ...prev,
            [name]: numValue < min || numValue > max ? `Value must be between ${min} and ${max}` : null,
        }));

        setInputs({ ...inputs, [name]: numValue });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Check if there are any errors
        const hasErrors = Object.values(errors).some((err) => err !== null);
        if (hasErrors) return alert("Please fix the errors before submitting.");

        setLoading(true);

        try {
            const res = await axios.post("http://localhost:5000/predict", inputs);
            onPredict(res.data.prediction);
        } catch (err) {
            alert("Failed to get prediction. Please try again.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-8 rounded-xl shadow-lg max-w-2xl">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Enter Your Current State</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {Object.keys(inputs).map((key) => (
                    <div key={key} className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-700">{fieldLabels[key]}</label>
                        <p className="text-xs text-gray-500">{fieldDescriptions[key]}</p>
                        <input
                            type="number"
                            name={key}
                            value={inputs[key]}
                            onChange={handleChange}
                            min={fieldConstraints[key].min}
                            max={fieldConstraints[key].max}
                            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition duration-200 ${errors[key] ? "border-red-500" : "border-gray-300"
                                }`}
                            required
                        />
                        {errors[key] && <p className="text-red-500 text-xs">{errors[key]}</p>}
                    </div>
                ))}
            </div>

            <button
                type="submit"
                disabled={loading || Object.values(errors).some((e) => e)}
                className="w-full mt-8 bg-teal-600 text-white px-6 py-4 rounded-lg hover:bg-teal-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition duration-200 font-semibold text-lg"
            >
                {loading ? "Analyzing..." : "Get My Productivity Recommendation"}
            </button>
        </form>
    );
}
