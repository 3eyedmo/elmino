# Olympiad Frontend

Frontend application for the Olympiad Competition Management System.

## Tech Stack

* React 18
* TypeScript
* Vite
* Axios
* Tailwind CSS
* Recharts

---

## Run Locally

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

---

## Run with Docker

Build the image:

```bash
docker build -t olympiad-frontend .
```

Run the container:

```bash
docker run -d -p 80:80 olympiad-frontend
```

---

## Features

* JWT Authentication
* Participant Management
* Problem Management
* Submission Registration
* Leaderboard
* Leaderboard Statistics
* Score Distribution Chart
