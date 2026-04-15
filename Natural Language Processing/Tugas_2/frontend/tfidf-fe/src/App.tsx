import { useState, FormEvent } from "react";
import type { QueryRequest, TypeMethodEnum } from "./types";

function App() {
  const [query, setQuery] = useState<string>("");
  const [type, setType] = useState<TypeMethodEnum>("TFIDF");
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const payload: QueryRequest = {
      query,
      type,
    };

    try {
      setLoading(true);
      setError(null);

      const res = await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error("Failed to fetch");
      }
      

      const data: SearchResponse = await res.text();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="bg-gray-100 min-h-screen flex items-center justify-center">
      <div className="bg-white p-6 rounded-2xl shadow-lg w-full m-10">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">
          Document Search
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Query */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Query
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. geeks"
              required
              className="w-full px-4 py-2 border rounded-xl focus:ring-2 focus:ring-blue-400 focus:outline-none"
            />
          </div>

          {/* Method */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-2">
              Method
            </label>

            <div className="flex gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  value="TFIDF"
                  checked={type === "TFIDF"}
                  onChange={(e) =>
                    setType(e.target.value as TypeMethodEnum)
                  }
                />
                <span>TF-IDF</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  value="COSINE"
                  checked={type === "COSINE"}
                  onChange={(e) =>
                    setType(e.target.value as TypeMethodEnum)
                  }
                />
                <span>Cosine</span>
              </label>
            </div>
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 text-white py-2 rounded-xl hover:bg-blue-600 transition disabled:opacity-50"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        {/* Error */}
        {error && (
          <div className="mt-4 text-red-500 text-sm">
            {error}
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="mt-4 p-3 bg-gray-50 rounded-xl">
            <h3 className="font-semibold mb-2">Result:</h3>
            <div
              className="text-sm text-gray-700"
              dangerouslySetInnerHTML={{ __html: result }}
            />
          </div>
          
        )}
      </div>
    </div>
    </>
  )
}

export default App
