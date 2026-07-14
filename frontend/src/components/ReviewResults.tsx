import { TrendingUp, TrendingDown, AlertTriangle, Lightbulb } from "lucide-react";
import type { ReviewResult } from "../types";
import { ScoreGauge } from "./ScoreGauge";
import { SectionCard } from "./SectionCard";

interface ReviewResultsProps {
  result: ReviewResult;
}

export function ReviewResults({ result }: ReviewResultsProps) {
  const sections = [
    {
      title: "Strengths",
      items: result.strengths,
      accentColor: "#10b981",
      icon: <TrendingUp className="h-5 w-5" />,
    },
    {
      title: "Weaknesses",
      items: result.weaknesses,
      accentColor: "#ef4444",
      icon: <TrendingDown className="h-5 w-5" />,
    },
    {
      title: "Missing Skills",
      items: result.missing_skills,
      accentColor: "#f59e0b",
      icon: <AlertTriangle className="h-5 w-5" />,
    },
    {
      title: "Suggestions",
      items: result.suggestions,
      accentColor: "#3b82f6",
      icon: <Lightbulb className="h-5 w-5" />,
    },
  ];

  return (
    <div className="w-full max-w-3xl mx-auto space-y-8">
      <div className="flex justify-center">
        <ScoreGauge score={result.overall_score} />
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {sections.map((section) => (
          <SectionCard
            key={section.title}
            title={section.title}
            items={section.items}
            accentColor={section.accentColor}
            icon={section.icon}
          />
        ))}
      </div>
    </div>
  );
}
