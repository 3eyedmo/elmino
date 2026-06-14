import { Navigate } from "react-router-dom";
import type { PropsWithChildren } from "react";

export default function ProtectedRoute({
  children,
}: PropsWithChildren) {
  const token =
    localStorage.getItem("access");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  return children;
}