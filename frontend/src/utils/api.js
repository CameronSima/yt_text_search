export const API_URL =
  process.env.NODE_ENV === "production"
    ? "https://yttextsearch-production.up.railway.app/"
    : "http://localhost:8000/api/";

export function post(path, data) {
  return fetch(API_URL + path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

export function get(path) {
  return fetch(API_URL + path, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
}
