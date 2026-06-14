import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import api from "../api/axios";

import type {
  Participant,
  Problem,
} from "../types";

export default function Submission() {
  const [participants, setParticipants] =
    useState<Participant[]>([]);

  const [problems, setProblems] =
    useState<Problem[]>([]);

  const [participantId, setParticipantId] =
    useState("");

  const [problemId, setProblemId] =
    useState("");

  const [scoreEarned, setScoreEarned] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const participantsResponse =
        await api.get("/participants/");

      const problemsResponse =
        await api.get("/problems/");

      setParticipants(
        participantsResponse.data
      );

      setProblems(
        problemsResponse.data
      );
    } catch {
      toast.error(
        "Failed to load data"
      );
    }
  }

  async function submit() {
    setError("");

    const selectedProblem =
      problems.find(
        (problem) =>
          problem.id === Number(problemId)
      );

    if (
      selectedProblem &&
      Number(scoreEarned) >
        selectedProblem.score
    ) {
      setError(
        `Maximum score is ${selectedProblem.score}`
      );

      return;
    }

    try {
      setLoading(true);

      await api.post(
        "/submissions/",
        {
          participant:
            participantId,
          problem: problemId,
          score_earned:
            scoreEarned,
        }
      );

      toast.success(
        "Submission saved"
      );

      setParticipantId("");
      setProblemId("");
      setScoreEarned("");
    } catch (err: any) {
      toast.error(
        "Failed to save submission"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow">

      <h1 className="text-2xl font-semibold mb-6">
        Create Submission
      </h1>

      {error && (
        <div className="bg-red-100 text-red-600 p-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="space-y-4">

        <select
          value={participantId}
          onChange={(e) =>
            setParticipantId(
              e.target.value
            )
          }
          className="w-full border p-3 rounded"
        >
          <option value="">
            Select Participant
          </option>

          {participants.map(
            (participant) => (
              <option
                key={participant.id}
                value={
                  participant.id
                }
              >
                {
                  participant.full_name
                }
              </option>
            )
          )}
        </select>

        <select
          value={problemId}
          onChange={(e) =>
            setProblemId(
              e.target.value
            )
          }
          className="w-full border p-3 rounded"
        >
          <option value="">
            Select Problem
          </option>

          {problems.map(
            (problem) => (
              <option
                key={problem.id}
                value={problem.id}
              >
                {problem.title}
                {" - "}
                {problem.score}
              </option>
            )
          )}
        </select>

        <input
          type="number"
          value={scoreEarned}
          onChange={(e) =>
            setScoreEarned(
              e.target.value
            )
          }
          placeholder="Score Earned"
          className="w-full border p-3 rounded"
        />

        <button
          onClick={submit}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-3 rounded"
        >
          {loading
            ? "Saving..."
            : "Save Submission"}
        </button>

      </div>
    </div>
  );
}