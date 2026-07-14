import { useState, useId } from "react";
import { ChevronDown } from "lucide-react";
import type { ReactNode } from "react";

interface SectionCardProps {
  title: string;
  items: string[];
  accentColor: string;
  icon: ReactNode;
}

export function SectionCard({ title, items, accentColor, icon }: SectionCardProps) {
  const [expanded, setExpanded] = useState(true);
  const contentId = useId();

  return (
    <div className="glass-card rounded-2xl overflow-hidden transition-all duration-300">
      <button
        onClick={() => setExpanded(!expanded)}
        aria-expanded={expanded}
        aria-controls={contentId}
        className="flex w-full items-center gap-3 p-5 text-left transition-colors hover:bg-gray-50/50 dark:hover:bg-gray-800/50"
      >
        <div
          className="flex h-10 w-10 items-center justify-center rounded-xl"
          style={{ backgroundColor: `${accentColor}20` }}
        >
          <div style={{ color: accentColor }}>{icon}</div>
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {items.length} {items.length === 1 ? "item" : "items"}
          </p>
        </div>
        <ChevronDown
          className={`h-5 w-5 text-gray-500 transition-transform duration-300 ${
            expanded ? "rotate-180" : ""
          }`}
        />
      </button>

      {expanded && (
        <div id={contentId} className="border-t border-gray-100 px-5 pb-5 dark:border-gray-800">
          <ul className="space-y-3 pt-4">
            {items.map((item, index) => (
              <li key={index} className="flex items-start gap-3">
                <span
                  className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full"
                  style={{ backgroundColor: accentColor }}
                  aria-hidden="true"
                />
                <span className="text-sm leading-relaxed text-gray-700 dark:text-gray-300">
                  {item}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
