import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  scenarios: {
    steady_load: {
      executor: "ramping-vus",
      stages: [
        { duration: "1m", target: 20 },
        { duration: "5m", target: 20 },
        { duration: "1m", target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500", "p(99)<1000"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
const API_KEY = __ENV.API_KEY || "my-secret-api-key";

export default function () {
  const health = http.get(`${BASE_URL}/api/v1/health`);
  check(health, {
    "health status is 200": (response) => response.status === 200,
  });

  const userPayload = JSON.stringify({
    username: `load-user-${__VU}-${__ITER}`,
    email: `load-user-${__VU}-${__ITER}@example.com`,
    age: 30,
  });

  const createUser = http.post(`${BASE_URL}/api/v1/users`, userPayload, {
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY,
    },
  });

  check(createUser, {
    "create user is successful or duplicate-safe": (response) =>
      response.status === 201 || response.status === 409,
  });

  sleep(1);
}
