import React, { useState, useRef, useEffect } from "react";

// UploadComponent.jsx
// Single-file React component (Tailwind CSS assumed available in the project)
// - supports images (jpeg/png/gif/etc), PDFs, and MP3
// - drag & drop + click-to-select
// - previews for images, embedded PDF preview, audio player for MP3
// - file validation (type + max size)
// - remove file, clear, and actual upload via XHR with progress

export default function UploadComponent({
  uploadUrl = "/api/upload", // endpoint to POST files (FormData)
  maxFileSizeMB = 10,
  multiple = true,
  onUploadComplete = () => {},
}) {
  const [files, setFiles] = useState([]); // { file, previewUrl, type }
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const inputRef = useRef(null);

  useEffect(() => {
    // Revoke object URLs on unmount
    return () => files.forEach((f) => f.previewUrl && URL.revokeObjectURL(f.previewUrl));
  }, [files]);

  const allowedTypes = [
    "application/pdf",
    "audio/mpeg",
    "audio/mp3",
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "image/bmp",
  ];

  const maxBytes = maxFileSizeMB * 1024 * 1024;

  function handleFiles(selection) {
    setError(null);
    const list = Array.from(selection);
    const valid = [];
    for (const file of list) {
      if (!allowedTypes.includes(file.type)) {
        setError(`\"${file.name}\" rejected — unsupported type: ${file.type || "unknown"}`);
        continue;
      }
      if (file.size > maxBytes) {
        setError(`\"${file.name}\" too large — max ${maxFileSizeMB} MB`);
        continue;
      }
      const previewUrl = file.type.startsWith("image/") || file.type === "application/pdf"
        ? URL.createObjectURL(file)
        : null;
      valid.push({ file, previewUrl, type: file.type });
    }

    setFiles((prev) => (multiple ? [...prev, ...valid] : valid));
  }

  function onInputChange(e) {
    handleFiles(e.target.files);
    e.target.value = null; // reset so same file can be re-selected
  }

  function onDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    handleFiles(e.dataTransfer.files);
  }

  function onDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
  }

  function removeIndex(idx) {
    const removed = files[idx];
    if (removed && removed.previewUrl) URL.revokeObjectURL(removed.previewUrl);
    setFiles((prev) => prev.filter((_, i) => i !== idx));
  }

  function clearAll() {
    files.forEach((f) => f.previewUrl && URL.revokeObjectURL(f.previewUrl));
    setFiles([]);
    setError(null);
    setProgress(0);
  }

  function uploadFiles() {
    if (files.length === 0) {
      setError("No files to upload");
      return;
    }

    setUploading(true);
    setProgress(0);
    setError(null);

    const form = new FormData();
    files.forEach((f, i) => form.append(multiple ? `files[]` : `file`, f.file));

    // Use XMLHttpRequest to get upload progress
    const xhr = new XMLHttpRequest();
    xhr.open("POST", uploadUrl, true);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percent = Math.round((event.loaded / event.total) * 100);
        setProgress(percent);
      }
    };

    xhr.onload = () => {
      setUploading(false);
      if (xhr.status >= 200 && xhr.status < 300) {
        setProgress(100);
        onUploadComplete(xhr.responseText);
      } else {
        setError(`Upload failed: ${xhr.status} ${xhr.statusText}`);
      }
    };

    xhr.onerror = () => {
      setUploading(false);
      setError("Upload failed due to a network error.");
    };

    xhr.send(form);
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <label className="block text-lg font-semibold mb-2">Upload files (images, PDF, MP3)</label>

      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        className="border-2 border-dashed rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 transition"
        onClick={() => inputRef.current && inputRef.current.click()}
      >
        <input
          ref={inputRef}
          type="file"
          multiple={multiple}
          accept="image/*,application/pdf,audio/mpeg"
          onChange={onInputChange}
          className="hidden"
        />

        <div className="space-y-2">
          <p className="text-sm text-gray-600">Drag & drop files here, or click to select.</p>
          <p className="text-xs text-gray-400">Allowed: .jpg .jpeg .png .gif .webp .bmp, .pdf, .mp3 — max {maxFileSizeMB} MB each</p>
        </div>
      </div>

      {error && (
        <div className="mt-3 text-red-600 text-sm">{error}</div>
      )}

      {files.length > 0 && (
        <div className="mt-4">
          <div className="grid grid-cols-1 gap-3">
            {files.map((fObj, idx) => (
              <div key={idx} className="flex items-center gap-3 border p-3 rounded">
                <div className="w-24 h-24 flex-shrink-0 bg-gray-50 rounded overflow-hidden flex items-center justify-center">
                  {fObj.type.startsWith("image/") && (
                    <img src={fObj.previewUrl} alt={fObj.file.name} className="object-cover w-full h-full" />
                  )}

                  {fObj.type === "application/pdf" && (
                    <div className="p-1 text-xs text-gray-600">PDF Preview</div>
                  )}

                  {fObj.type.startsWith("audio/") && (
                    <div className="px-2 text-xs text-gray-600">Audio</div>
                  )}
                </div>

                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium">{fObj.file.name}</div>
                      <div className="text-xs text-gray-500">{(fObj.file.size / 1024).toFixed(1)} KB • {fObj.type}</div>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => removeIndex(idx)} className="text-xs px-2 py-1 rounded bg-red-50 text-red-600">Remove</button>
                    </div>
                  </div>

                  <div className="mt-2">
                    {fObj.type === "application/pdf" && (
                      <div className="border rounded overflow-hidden" style={{ maxWidth: 500 }}>
                        <iframe src={fObj.previewUrl} title={fObj.file.name} className="w-full" style={{ height: 250 }} />
                      </div>
                    )}

                    {fObj.type.startsWith("audio/") && (
                      <audio controls src={URL.createObjectURL(fObj.file)} className="w-full" />
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 flex gap-2">
            <button
              onClick={uploadFiles}
              disabled={uploading}
              className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60"
            >
              {uploading ? `Uploading ${progress}%` : "Upload"}
            </button>

            <button onClick={clearAll} disabled={uploading} className="px-4 py-2 rounded border">
              Clear
            </button>
          </div>

          {uploading && (
            <div className="mt-3">
              <div className="w-full bg-gray-200 rounded h-2 overflow-hidden">
                <div className="h-2 rounded" style={{ width: `${progress}%` }} />
              </div>
              <div className="text-xs text-gray-600 mt-1">{progress}%</div>
            </div>
          )}
        </div>
      )}

      <div className="mt-6 text-sm text-gray-500">
        Tip: On the server accept a multipart/form-data POST and handle the `files[]` or `file` field(s). Adjust the `uploadUrl` prop to point to your API.
      </div>
    </div>
  );
}
