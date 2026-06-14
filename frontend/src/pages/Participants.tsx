import { useState } from "react";
import api from "../api/axios";
import toast from "react-hot-toast";


export default function Participants() {
  const [form, setForm] =
    useState({
      full_name: "",
      email: "",
      grade: "",
      city: "",
    });

  async function submit(
    e: React.FormEvent
  ) {
    e.preventDefault();
    if (
      Number(form.grade) < 7 ||
      Number(form.grade) > 12
    ) {
      toast.error(
        "Grade must be between 7 and 12"
      );

      return;
    }
    await api.post(
      "/participants/",
      form
    );

    toast.success(
      "Participant created"
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow">

      <h1 className="text-2xl mb-6">
        Register Participant
      </h1>

      <form
        onSubmit={submit}
        className="space-y-4"
      >

        <input
          className="w-full border p-3 rounded"
          placeholder="Full Name"
          onChange={(e) =>
            setForm({
              ...form,
              full_name:
                e.target.value,
            })
          }
        />

        <input
          className="w-full border p-3 rounded"
          placeholder="Email"
          onChange={(e) =>
            setForm({
              ...form,
              email:
                e.target.value,
            })
          }
        />

        <input
          type="number"
          className="w-full border p-3 rounded"
          placeholder="Grade"
          onChange={(e) =>
            setForm({
              ...form,
              grade:
                e.target.value,
            })
          }
        />

        <input
          className="w-full border p-3 rounded"
          placeholder="City"
          onChange={(e) =>
            setForm({
              ...form,
              city:
                e.target.value,
            })
          }
        />

        <button
          className="bg-green-600 text-white px-4 py-3 rounded"
        >
          Save
        </button>

      </form>

    </div>
  );
}