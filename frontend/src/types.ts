export interface ReviewResult {
  strengths: string[];
  weaknesses: string[];
  missing_skills: string[];
  suggestions: string[];
  overall_score: number;
}

export type Theme = "light" | "dark";
