export function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center gap-6 py-12" role="status" aria-live="polite">
      <div className="relative" style={{ width: 80, height: 80 }}>
        <div
          className="absolute inset-0 rounded-full border-4 border-transparent"
          style={{
            borderTopColor: "rgb(37, 99, 235)",
            borderRightColor: "rgba(37, 99, 235, 0.3)",
            animation: "spin-outer 2s linear infinite",
          }}
        />
        <div
          className="absolute inset-2 rounded-full border-4 border-transparent"
          style={{
            borderTopColor: "rgba(59, 130, 246, 0.6)",
            borderLeftColor: "rgba(59, 130, 246, 0.2)",
            animation: "spin-middle 1.5s linear infinite",
          }}
        />
        <div
          className="absolute inset-4 rounded-full border-4 border-transparent"
          style={{
            borderTopColor: "rgba(96, 165, 250, 0.8)",
            borderBottomColor: "rgba(96, 165, 250, 0.3)",
            animation: "spin-inner 1s linear infinite",
          }}
        />
        <div
          className="absolute left-1/2 top-1/2 h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-600 dark:bg-blue-500"
          style={{ animation: "pulse-center 1.5s ease-in-out infinite" }}
        />
      </div>

      <div className="text-center">
        <p
          className="text-lg font-medium text-gray-900 dark:text-gray-100"
          style={{ animation: "text-pulse 2s ease-in-out infinite" }}
        >
          Analyzing your resume...
        </p>
        <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
          Our AI is reviewing your resume for strengths and improvements
        </p>
      </div>
      <span className="sr-only">Loading, please wait...</span>
    </div>
  );
}
