import { Link } from "react-router-dom";
import type { ReactNode } from "react";
import { useNavigate } from "react-router-dom";


interface Props {
  children: ReactNode;
}

export default function MainLayout({
  children,
}: Props) {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.clear();

    navigate("/");
  };
  return (
    <div className="min-h-screen bg-gray-100">

      <nav className="bg-white shadow">

        <div className="max-w-6xl mx-auto p-4 flex gap-6">

          <Link to="/participants">
            Participants
          </Link>

          <Link to="/submissions">
            Submissions
          </Link>

          <Link to="/leaderboard">
            Leaderboard
          </Link>

          <button
            onClick={logout}
            className="text-red-600 ml-auto cursor-pointer"
          >
            Logout
          </button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto p-6">
        {children}
      </div>

    </div>
  );
}