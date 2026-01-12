import React from "react";
import FeatureCompare from "../components/FeatureCompare.jsx";

export default function Visualize() {
    return (
        <div>
            <h1 className="text-3xl font-semibold text-teal-800 mb-6">Compare Features & Generate Graphs</h1>
            <FeatureCompare />
        </div>
    );
}

