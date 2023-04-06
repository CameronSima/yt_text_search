export const API_URL = "http://localhost:8000/api/";

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
