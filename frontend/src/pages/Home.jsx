import React, { useState } from "react";
import PredictionForm from "../components/PredictionForm.jsx";
import ResultCard from "../components/ResultCard.jsx";

export default function Home() {
    const [prediction, setPrediction] = useState(null);

    return (
        <div className="max-w-6xl mx-auto">
            <div className="text-center mb-10">
                <h1 className="text-5xl font-bold text-teal-800 mb-4">
                    🎯 Productivity Optimizer
                </h1>
                <p className="text-xl text-gray-600 mb-2">
                    Discover what activity will make you most productive right now
                </p>
                <p className="text-gray-500">
                    Based on your current mood, energy, and circumstances
                </p>
            </div>

            <div className="flex flex-col items-center">
                <PredictionForm onPredict={setPrediction} />
                {prediction !== null && <ResultCard prediction={prediction} />}
            </div>
        </div>
    );
}

