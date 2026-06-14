
export interface Participant {
  id: number;
  full_name: string;
  email: string;
  grade: number;
  city: string;
}

export interface Problem {
  id: number;
  title: string;
  score: number;
  difficulty: string;
}

export interface LeaderboardRow {
  id: number;
  full_name: string;
  city: string;
  total_score: number;
}