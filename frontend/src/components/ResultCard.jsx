import React from "react";

const activityData = {
    0: {
        name: "Study",
        color: "blue",
        description: "Perfect time for learning and absorbing new information",
        tips: ["Find a quiet space", "Remove distractions", "Take breaks every 25 minutes"]
    },
    1: {
        name: "Exercise",
        color: "green",
        description: "Your body and mind are ready for physical activity",
        tips: ["Stay hydrated", "Warm up properly", "Listen to your body"]
    },
    2: {
        name: "Social",
        color: "purple",
        description: "Great time to connect with friends, family, or colleagues",
        tips: ["Be present in conversations", "Put away devices", "Plan fun activities"]
    },
    3: {
        name: "Leisure",
        color: "yellow",
        description: "Time to relax and enjoy your favorite activities",
        tips: ["Choose activities you truly enjoy", "Don't feel guilty about relaxing", "Set time limits if needed"]
    },
    4: {
        name: "Sleep",
        color: "indigo",
        description: "Your body needs rest to recharge",
        tips: ["Create a calming environment", "Avoid screens 1 hour before sleep", "Keep room cool and dark"]
    },
    5: {
        name: "Work",
        color: "red",
        description: "Optimal time for focused work and professional tasks",
        tips: ["Prioritize important tasks", "Minimize interruptions", "Use productivity techniques"]
    }
};

export default function ResultCard({ prediction }) {
    const activity = activityData[prediction];
    const colorClasses = {
        blue: "bg-blue-100 border-blue-300 text-blue-800",
        green: "bg-green-100 border-green-300 text-green-800",
        purple: "bg-purple-100 border-purple-300 text-purple-800",
        yellow: "bg-yellow-100 border-yellow-300 text-yellow-800",
        indigo: "bg-indigo-100 border-indigo-300 text-indigo-800",
        red: "bg-red-100 border-red-300 text-red-800"
    };

    return (
        <div className={`mt-8 p-8 rounded-xl border-2 ${colorClasses[activity.color]} transform transition duration-300 hover:scale-105`}>
            <div className="text-center">
                <div className="text-6xl mb-4">{activity.icon}</div>
                <h2 className="text-3xl font-bold mb-2">
                    Recommended Activity: {activity.name}
                </h2>
                <p className="text-lg mb-6 opacity-80">{activity.description}</p>

                <div className="text-left max-w-md mx-auto">
                    <h3 className="text-lg font-semibold mb-3">💡 Tips for Success:</h3>
                    <ul className="space-y-2">
                        {activity.tips.map((tip, index) => (
                            <li key={index} className="flex items-start">
                                <span className="text-sm mr-2">•</span>
                                <span className="text-sm">{tip}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}
