import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { useEffect } from "react";


export default function Login() {
  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const token =
      localStorage.getItem(
        "access"
      );

    if (token) {
      navigate(
        "/leaderboard"
      );
    }
  }, [navigate]);

  const login = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    try {
      const { data } =
        await api.post(
          "/auth/login/",
          {
            username,
            password,
          }
        );

      localStorage.setItem(
        "access",
        data.access
      );

      localStorage.setItem(
        "refresh",
        data.refresh
      );

      toast.success(
        "Login successful"
      );

      navigate("/leaderboard");

    } catch {
      toast.error(
        "Invalid username or password"
      );
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">

      <div className="bg-white shadow rounded-xl p-8 w-96">

        <h1 className="text-2xl font-bold mb-6">
          Admin Login
        </h1>

        <form
          onSubmit={login}
          className="space-y-4"
        >

          <input
            className="w-full border p-3 rounded"
            placeholder="Username"
            onChange={(e) =>
              setUsername(
                e.target.value
              )
            }
          />

          <input
            type="password"
            className="w-full border p-3 rounded"
            placeholder="Password"
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          <button
            className="w-full bg-blue-600 text-white py-3 rounded"
          >
            Login
          </button>

        </form>

      </div>

    </div>
  );
}