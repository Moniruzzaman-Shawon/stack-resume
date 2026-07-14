interface ScoreGaugeProps {
  score: number;
}

export function ScoreGauge({ score }: ScoreGaugeProps) {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = (score: number) => {
    if (score >= 80) return { stroke: "#10b981", text: "text-emerald-600 dark:text-emerald-400", label: "Excellent" };
    if (score >= 60) return { stroke: "#f59e0b", text: "text-amber-600 dark:text-amber-400", label: "Good" };
    return { stroke: "#ef4444", text: "text-red-600 dark:text-red-400", label: "Needs Work" };
  };

  const color = getColor(score);

  return (
    <div className="flex flex-col items-center gap-3" role="img" aria-label={`Overall score: ${score} out of 100. Rating: ${color.label}`}>
      <div className="relative">
        <svg width="120" height="120" className="-rotate-90" aria-hidden="true">
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-200 dark:text-gray-700"
          />
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke={color.stroke}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{
              animation: "score-fill 1s ease-out forwards",
            }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-3xl font-bold ${color.text}`}>{score}</span>
          <span className="text-xs text-gray-600 dark:text-gray-400">/ 100</span>
        </div>
      </div>
      <span className={`text-sm font-semibold ${color.text}`}>{color.label}</span>
    </div>
  );
}
