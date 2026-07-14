import { useRef, type DragEvent, type ChangeEvent } from "react";
import { Upload, FileText, X } from "lucide-react";

interface FileUploadProps {
  selectedFile: File | null;
  onFileSelect: (file: File) => void;
  onFileClear: () => void;
  onAnalyze: () => void;
  isLoading: boolean;
}

const MAX_SIZE = 5 * 1024 * 1024;

export function FileUpload({ selectedFile, onFileSelect, onFileClear, onAnalyze, isLoading }: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
      return;
    }
    if (file.size > MAX_SIZE) {
      return;
    }
    onFileSelect(file);
  };

  const handleDrag = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      inputRef.current?.click();
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {!selectedFile ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          onKeyDown={handleKeyDown}
          tabIndex={0}
          role="button"
          aria-label="Upload PDF resume. Click or drag and drop a file."
          className="glass-card relative cursor-pointer rounded-2xl border-2 border-dashed border-gray-300 dark:border-gray-700 p-12 text-center transition-all duration-300 hover:border-blue-600 hover:bg-blue-50/30 dark:hover:bg-blue-950/20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleChange}
            className="hidden"
            aria-hidden="true"
            tabIndex={-1}
          />

          <div className="flex flex-col items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100 text-blue-600 dark:bg-blue-900/50 dark:text-blue-400">
              <Upload className="h-8 w-8" />
            </div>

            <div>
              <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                Upload your resume
              </p>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                Drag and drop or click to browse
              </p>
              <p className="mt-1 text-xs text-gray-500 dark:text-gray-500">
                PDF only &middot; Max 5MB
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 dark:bg-blue-900/50">
              <FileText className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="truncate font-medium text-gray-900 dark:text-gray-100">
                {selectedFile.name}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {formatSize(selectedFile.size)}
              </p>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onFileClear();
                if (inputRef.current) inputRef.current.value = "";
              }}
              className="flex h-8 w-8 items-center justify-center rounded-lg text-gray-500 transition-colors hover:bg-gray-100 hover:text-gray-700 dark:hover:bg-gray-700 dark:hover:text-gray-300"
              aria-label="Remove selected file"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {selectedFile && (
        <button
          onClick={onAnalyze}
          disabled={isLoading}
          className="mt-4 w-full rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 px-6 py-3.5 text-base font-semibold text-white shadow-lg shadow-blue-500/25 transition-all duration-300 hover:from-blue-700 hover:to-blue-600 hover:shadow-blue-500/40 disabled:cursor-not-allowed disabled:opacity-50 dark:shadow-blue-500/20 dark:hover:shadow-blue-500/30"
        >
          {isLoading ? "Analyzing..." : "Analyze Resume"}
        </button>
      )}
    </div>
  );
}
