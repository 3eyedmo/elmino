import { useEffect, useState } from "react";
import api from "../api/axios";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

interface LeaderboardRow {
  id: number;
  full_name: string;
  email: string;
  grade: number;
  city: string;
  registered_at: string;
  total_score: number;
}

interface LeaderboardResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: LeaderboardRow[];
}

interface DistributionItem {
  range: string;
  count: number;
}

interface StatsResponse {
  participant_count: number;
  average_score: number;
  max_score: number;
  min_score: number;
  distribution: DistributionItem[];
}

export default function Leaderboard() {
  const [rows, setRows] = useState<LeaderboardRow[]>([]);
  const [city, setCity] = useState("");
  const [page, setPage] = useState(1);

  const [count, setCount] = useState(0);

  const [stats, setStats] = useState<StatsResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadData() {
    try {
      setError("");

      const leaderboardRes =
        await api.get<LeaderboardResponse>(
          `/leaderboard/?city=${city}&page=${page}&page_size=10`
        );

      setRows(leaderboardRes.data.results);
      setCount(leaderboardRes.data.count);

      const statsRes =
        await api.get<StatsResponse>(
          `/leaderboard/stats/?city=${city}`
        );

      setStats(statsRes.data);
    } catch {
      setError("Failed to load leaderboard");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();

    const interval = setInterval(() => {
      loadData();
    }, 30000);

    return () => clearInterval(interval);
  }, [city, page]);

  if (loading) {
    return (
      <div className="text-center py-10">
        Loading...
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {/* HEADER */}
      <div className="bg-white p-6 rounded-xl shadow">

        <div className="flex justify-between items-center mb-6">

          <h1 className="text-2xl font-bold">
            Leaderboard
          </h1>

          <input
            value={city}
            onChange={(e) => {
              setCity(e.target.value);
              setPage(1);
            }}
            placeholder="Filter by city"
            className="border p-2 rounded w-64"
          />

        </div>

        {error && (
          <div className="bg-red-100 text-red-600 p-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* STATS CARDS */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">

            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500">
                Participants
              </div>
              <div className="text-xl font-bold">
                {stats.participant_count}
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500">
                Average
              </div>
              <div className="text-xl font-bold">
                {stats.average_score?.toFixed(1)}
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500">
                Max
              </div>
              <div className="text-xl font-bold">
                {stats.max_score}
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500">
                Min
              </div>
              <div className="text-xl font-bold">
                {stats.min_score}
              </div>
            </div>

          </div>
        )}

        {/* TABLE */}
        <table className="w-full border-collapse">

          <thead>
            <tr className="bg-gray-100">
              <th className="p-3 text-left">Rank</th>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">City</th>
              <th className="p-3 text-left">Grade</th>
              <th className="p-3 text-left">Score</th>
            </tr>
          </thead>

          <tbody>

            {rows.length === 0 ? (
              <tr>
                <td colSpan={5} className="p-4 text-center">
                  No data found
                </td>
              </tr>
            ) : (
              rows.map((row, index) => (
                <tr key={row.id} className="border-t">

                  <td className="p-3">
                    #{(page - 1) * 10 + index + 1}
                  </td>

                  <td className="p-3">{row.full_name}</td>
                  <td className="p-3">{row.city}</td>
                  <td className="p-3">{row.grade}</td>

                  <td className="p-3 font-semibold">
                    {row.total_score}
                  </td>

                </tr>
              ))
            )}

          </tbody>

        </table>

        {/* PAGINATION */}
        <div className="flex justify-between mt-6">

          <button
            disabled={page === 1}
            onClick={() => setPage(page - 1)}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Prev
          </button>

          <span>
            Page {page}
          </span>

          <button
            disabled={page * 10 >= count}
            onClick={() => setPage(page + 1)}
            className="px-4 py-2 border rounded disabled:opacity-50"
          >
            Next
          </button>

        </div>

      </div>

      {/* CHART */}
      {stats && stats.distribution.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow">

          <h2 className="text-xl font-bold mb-4">
            Score Distribution
          </h2>

          <ResponsiveContainer width="100%" height={350}>

            <BarChart data={stats.distribution}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="range" />
              <YAxis />

              <Tooltip />

              <Bar dataKey="count" />

            </BarChart>

          </ResponsiveContainer>

        </div>
      )}

    </div>
  );
}