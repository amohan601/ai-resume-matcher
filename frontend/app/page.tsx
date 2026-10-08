"use client";

import { useEffect, useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api";

type MatchResult = {
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  experience_gap: string;
  rationale: string;
};

type MatchAnalysisResponse = {
  match_result: MatchResult;
  thread_id: string;
};

type RewrittenResume = {
  tailored_resume: string;
  changes_summary: string;
};

function scoreColorClass(score: number) {
  if (score >= 70) return "text-emerald-600 dark:text-emerald-400";
  if (score >= 50) return "text-amber-600 dark:text-amber-400";
  return "text-rose-600 dark:text-rose-400";
}

function authHeaders(token: string) {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

export default function Home() {
  const [resume, setResume] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [matchAnalysis, setMatchAnalysis] = useState<MatchAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [rewrittenResume, setRewrittenResume] = useState<RewrittenResume | null>(null);
  const [generating, setGenerating] = useState(false);
  const [generateError, setGenerateError] = useState<string | null>(null);
  const [generateDecision, setGenerateDecision] = useState<"yes" | "no" | null>(null);
  const [inputsCollapsed, setInputsCollapsed] = useState(false);
  const [matchCollapsed, setMatchCollapsed] = useState(false);
  const [accessToken, setAccessToken] = useState("");

  useEffect(() => {
    setAccessToken(sessionStorage.getItem("accessToken") ?? "");
  }, []);

  function handleTokenChange(value: string) {
    setAccessToken(value);
    sessionStorage.setItem("accessToken", value);
  }

  async function handleAnalyzeMatch() {
    setLoading(true);
    setError(null);
    setMatchAnalysis(null);
    setRewrittenResume(null);
    setGenerateDecision(null);
    setGenerateError(null);
    setMatchCollapsed(false);

    try {

      const res = await fetch(`${API_BASE_URL}/match-analysis`, {
        method: "POST",
        // MISSING Authorization header
        headers: authHeaders(accessToken),
        body: JSON.stringify({
          resume_text: resume,
          job_description: jobDescription,
        }),
      });
      

      if (res && res.status === 401) {
        throw new Error("Invalid or missing access token");
      }

      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
      }

      setMatchAnalysis(await res.json());
      setInputsCollapsed(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  async function handleGenerateDecision(decision: "yes" | "no") {
    if (!matchAnalysis) return;
    setGenerating(true);
    setGenerateError(null);
    
    try {
      const res = await fetch(`${API_BASE_URL}/approve-tailoring`, {
        method: "POST",
        // MISSING Authorization header
        headers: authHeaders(accessToken),
        body: JSON.stringify({ thread_id: matchAnalysis.thread_id, decision }),
      });
      
      if (res &&  res.status === 401) {
        throw new Error("Invalid or missing access token");
      }

      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
      }

      setGenerateDecision(decision);

      if (decision === "yes") {
        setRewrittenResume(await res.json());
        setMatchCollapsed(true);
      }
    } catch (err) {
      setGenerateError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setGenerating(false);
    }
  }

  const canSubmit = resume.trim() !== "" 
          && jobDescription.trim() !== "" 
          && accessToken.trim() !== "" 
          && !loading;

  return (
    <div className="flex flex-1 flex-col items-center bg-gradient-to-b from-indigo-50 via-white to-white font-sans dark:from-zinc-950 dark:via-indigo-950/10 dark:to-zinc-950">
      <main className="flex w-full max-w-5xl flex-1 flex-col gap-8 px-6 py-16 sm:px-10">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-semibold text-zinc-900 dark:text-zinc-50">
            Resume <span className="text-indigo-600 dark:text-indigo-400">Matcher</span>
          </h1>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            Paste a resume and a job description to see how well they match.
          </p>
        </div>
      
       <div className="flex flex-col gap-2">
        <label
          htmlFor="access-token"
          className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
        >
        Access token
        </label>
        <input
          id="access-token"
          type="password"
          autoComplete="off"
          value={accessToken}
          onChange={(e) => handleTokenChange(e.target.value)}
          placeholder="Enter the access token to use this app"
          className="w-full max-w-md rounded-lg border border-zinc-200 bg-white p-3 text-sm text-zinc-900 shadow-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-50 dark:focus:ring-indigo-950"
        />
        {!accessToken.trim() && (
          <p className="text-xs text-zinc-500 dark:text-zinc-400">
            Access token required to run an analysis.
          </p>
        )}
      </div>

        {inputsCollapsed ? (
          <div className="flex items-center justify-between gap-4 rounded-lg border border-zinc-200 bg-white px-4 py-3 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <span className="text-sm text-zinc-600 dark:text-zinc-400">
              Resume ({resume.length} chars) · Job description ({jobDescription.length} chars)
            </span>
            <button
              type="button"
              onClick={() => setInputsCollapsed(false)}
              className="rounded-full border border-zinc-300 px-4 py-1.5 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
            >
              View/Edit Resume/Job Description
            </button>
          </div>
        ) : (
        <>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div className="flex flex-col gap-2">
            <label
              htmlFor="resume"
              className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
            >
              Resume
            </label>
            <textarea
              id="resume"
              value={resume}
              onChange={(e) => setResume(e.target.value)}
              placeholder="Paste your resume text here"
              rows={14}
              className="w-full resize-y rounded-lg border border-zinc-200 bg-white p-3 font-mono text-sm text-zinc-900 shadow-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-50 dark:focus:ring-indigo-950"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label
              htmlFor="job-description"
              className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
            >
              Job Description
            </label>
            <textarea
              id="job-description"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here"
              rows={14}
              className="w-full resize-y rounded-lg border border-zinc-200 bg-white p-3 font-mono text-sm text-zinc-900 shadow-sm focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-50 dark:focus:ring-indigo-950"
            />
          </div>
        </div>

        <div>
          <button
            type="button"
            onClick={handleAnalyzeMatch}
            disabled={!canSubmit}
            className="rounded-full bg-indigo-600 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-indigo-500 dark:hover:bg-indigo-400"
          >
            {loading ? "Analyzing..." : "Analyze Match"}
          </button>
        </div>
        </>
        )}

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300">
            {error}
          </div>
        )}

        {matchAnalysis && rewrittenResume && (
          <div className="flex items-center justify-between gap-4 rounded-lg border border-zinc-200 bg-white px-4 py-3 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <span className="text-sm text-zinc-600 dark:text-zinc-400">
              Match score:{" "}
              <span
                className={`font-semibold ${scoreColorClass(matchAnalysis.match_result.match_score)}`}
              >
                {Math.round(matchAnalysis.match_result.match_score)}
              </span>{" "}
              / 100
            </span>
            <button
              type="button"
              onClick={() => setMatchCollapsed(!matchCollapsed)}
              className="rounded-full border border-zinc-300 px-4 py-1.5 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
            >
              {matchCollapsed ? "View Match Analysis" : "Hide Match Analysis"}
            </button>
          </div>
        )}

        {matchAnalysis && !(rewrittenResume && matchCollapsed) && (
          <div className="flex flex-col gap-4 rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <div className="flex items-baseline gap-2">
              <span
                className={`text-4xl font-semibold ${scoreColorClass(matchAnalysis.match_result.match_score)}`}
              >
                {Math.round(matchAnalysis.match_result.match_score)}
              </span>
              <span className="text-sm text-zinc-500 dark:text-zinc-400">
                / 100 match score
              </span>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="flex flex-col gap-2">
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                  Matched
                </span>
                <div className="flex flex-wrap gap-2">
                  {matchAnalysis.match_result.matched_skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full bg-green-100 px-3 py-1 text-xs text-green-800 dark:bg-green-950 dark:text-green-300"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                  Missing
                </span>
                <div className="flex flex-wrap gap-2">
                  {matchAnalysis.match_result.missing_skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full bg-red-100 px-3 py-1 text-xs text-red-800 dark:bg-red-950 dark:text-red-300"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                Experience gap
              </span>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                {matchAnalysis.match_result.experience_gap}
              </p>
            </div>

            <div className="flex flex-col gap-1">
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                Rationale
              </span>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                {matchAnalysis.match_result.rationale}
              </p>
            </div>
          </div>
        )}

        {matchAnalysis && generateDecision === null && (
          <div className="flex items-center gap-3 rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <span className="text-sm text-zinc-700 dark:text-zinc-300">
              Generate a tailored resume for this job?
            </span>
            <button
              type="button"
              onClick={() => handleGenerateDecision("yes")}
              disabled={generating}
              className="rounded-full bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-indigo-500 dark:hover:bg-indigo-400"
            >
              {generating ? "Generating..." : "Yes"}
            </button>
            <button
              type="button"
              onClick={() => handleGenerateDecision("no")}
              disabled={generating}
              className="rounded-full border border-zinc-300 px-4 py-2 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-100 disabled:cursor-not-allowed disabled:opacity-40 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
            >
              No
            </button>
          </div>
        )}

        {generateDecision === "no" && (
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            No tailored resume generated.
          </p>
        )}

        {generateError && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300">
            {generateError}
          </div>
        )}

        {rewrittenResume && (
          <div className="flex flex-col gap-4 rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              Tailored resume
            </h2>
            <pre className="whitespace-pre-wrap rounded-lg border border-zinc-200 bg-zinc-50 p-4 font-mono text-sm text-zinc-900 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-50">
              {rewrittenResume.tailored_resume}
            </pre>
            <div className="flex flex-col gap-1">
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                What changed
              </span>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                {rewrittenResume.changes_summary}
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
