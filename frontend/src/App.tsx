import { useState, useRef, useCallback } from "react";
import { AnimatedLogo } from "./components/AnimatedLogo";
import { ThemeToggle } from "./components/ThemeToggle";
import { FileUpload } from "./components/FileUpload";
import { LoadingSpinner } from "./components/LoadingSpinner";
import { ReviewResults } from "./components/ReviewResults";
import type { ReviewResult } from "./types";

const REQUEST_TIMEOUT = 60000;

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const handleFileSelect = useCallback((file: File) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
  }, []);

  const handleFileClear = useCallback(() => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
  }, []);

  const handleAnalyze = useCallback(async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    abortControllerRef.current?.abort();
    const controller = new AbortController();
    abortControllerRef.current = controller;

    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

    try {
      const formData = new FormData();
      formData.append("resume", selectedFile);

      const response = await fetch("/api/review/", {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      let data: unknown;
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        data = await response.json();
      } else {
        throw new Error("Server returned an unexpected response. Please try again.");
      }

      if (!response.ok) {
        const errorData = data as { error?: string };
        throw new Error(errorData.error || "Failed to analyze resume");
      }

      setResult(data as ReviewResult);
    } catch (err) {
      clearTimeout(timeoutId);
      if (err instanceof DOMException && err.name === "AbortError") {
        setError("Request timed out. The server took too long to respond.");
      } else if (err instanceof TypeError && (err as Error).message.includes("fetch")) {
        setError("Could not connect to the server. Please check your connection.");
      } else {
        setError(err instanceof Error ? err.message : "An unexpected error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  }, [selectedFile]);

  const handleReset = useCallback(() => {
    setResult(null);
    setError(null);
    setSelectedFile(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  return (
    <div className="min-h-screen transition-colors duration-300" style={{ backgroundColor: "var(--bg-primary)" }}>
      <header className="sticky top-0 z-50 border-b backdrop-blur-xl transition-colors duration-300" style={{ borderColor: "var(--border-color)", backgroundColor: "color-mix(in srgb, var(--bg-primary) 80%, transparent)" }}>
        <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-6">
          <AnimatedLogo />
          <ThemeToggle />
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-12">
        {!result && !isLoading && (
          <div className="flex flex-col items-center gap-8">
            <div className="text-center">
              <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-gray-50 sm:text-5xl">
                AI Resume Review
              </h1>
              <p className="mt-4 text-lg text-gray-600 dark:text-gray-400 max-w-xl mx-auto">
                Upload your resume and get instant AI-powered feedback on strengths, weaknesses, and areas for improvement.
              </p>
            </div>

            <FileUpload
              selectedFile={selectedFile}
              onFileSelect={handleFileSelect}
              onFileClear={handleFileClear}
              onAnalyze={handleAnalyze}
              isLoading={isLoading}
            />

            {error && (
              <div
                role="alert"
                aria-live="assertive"
                className="w-full max-w-2xl rounded-2xl bg-red-50 px-6 py-4 text-red-600 dark:bg-red-950/50 dark:text-red-400"
              >
                {error}
              </div>
            )}
          </div>
        )}

        {isLoading && (
          <div className="flex flex-col items-center gap-8">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-50">
                Reviewing Your Resume
              </h1>
              <p className="mt-2 text-gray-600 dark:text-gray-400">
                This usually takes 10-20 seconds
              </p>
            </div>
            <LoadingSpinner />
          </div>
        )}

        {result && !isLoading && (
          <div className="flex flex-col items-center gap-8">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-50">
                Resume Analysis Complete
              </h1>
              <p className="mt-1 text-gray-600 dark:text-gray-400">
                Here's what our AI found
              </p>
            </div>

            {error && (
              <div
                role="alert"
                aria-live="assertive"
                className="w-full max-w-2xl rounded-2xl bg-red-50 px-6 py-4 text-red-600 dark:bg-red-950/50 dark:text-red-400"
              >
                {error}
              </div>
            )}

            <ReviewResults result={result} />

            <button
              onClick={handleReset}
              className="rounded-xl border border-gray-200 px-6 py-3 text-sm font-medium text-gray-700 transition-all duration-300 hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
            >
              Review Another Resume
            </button>
          </div>
        )}
      </main>

      <footer className="border-t py-8 transition-colors duration-300" style={{ borderColor: "var(--border-color)" }}>
        <div className="mx-auto max-w-5xl px-6 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-500">
            Stack Resume &mdash; AI-powered resume analysis. Results are suggestions only.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
