# Auth API (Backend AI Assignment 4)

This project is a FastAPI application that implements a secure authentication flow using Supabase as the Identity Provider (IdP). It demonstrates how to properly protect endpoints using stateless JWTs (JSON Web Tokens).

## Environment Setup

To run this project, you will need to connect it to your own Supabase instance.

1. Copy the `.env.example` file and rename it to `.env`:
   
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and replace the placeholder values with your actual Supabase project URL and Anon Key.
   *(Note: The `.env` file is intentionally ignored by git to protect your secrets).*

## Running the API

Once your `.env` is set up, you can start the application with a single command:

```bash
fastapi dev main.py
```

## API Reference

| Endpoint | Method | Auth Required? | Description |
| :--- | :--- | :--- | :--- |
| `/auth/signup` | POST | No | Registers a new user. |
| `/auth/login` | POST | No | Authenticates a user and returns a JWT. |
| `/auth/logout` | POST | Yes | Invalidates the user session. |
| `/public/info` | GET | No | A public endpoint accessible to anyone. |
| `/protected/profile` | GET | Yes | Returns the authenticated user's profile info. |
| `/protected/dashboard` | GET | Yes | Returns a dashboard message for the user. |

## Swagger UI

Once the app is running, visit `http://127.0.0.1:8000/docs` in your browser. Use the green "Authorize" button to inject your token into the protected endpoints.

<img width="1487" height="872" alt="swagger" src="https://github.com/user-attachments/assets/0fe844dd-e6d3-4b5f-be49-42f8b420f00f" />

---

## AI vs Me (Stage 7 Rematch)

**My Prompt:** 
> "Write a FastAPI app with Supabase authentication. Include 5 routes: signup, login, public info, protected profile, protected dashboard. Return appropriate status codes (201/200/204/400/401). Use HTTPBearer for Swagger token extraction."

### 1. How did it handle token extraction?
The AI correctly utilized `HTTPBearer` from FastAPI's security module, extracting the token using `credentials.credentials`. Because it used `HTTPBearer`, it didn't have to manually parse or split the "Bearer " prefix, avoiding potential crashes or slip-throughs if the prefix was missing or formatted incorrectly.

### 2. What security flaws might it have introduced?
The AI's token verification lacked a robust `try-except` block around `supabase.auth.get_user(token)`. If an invalid or expired token is passed, the Supabase client will raise an exception rather than returning a clean `None`. Because the AI didn't catch this, the server would crash with an unhandled 500 error instead of safely returning a 401 Unauthorized status. Additionally, the AI mistakenly returned a 400 Bad Request on a failed login, rather than the standard 401 Unauthorized.

### 3. What did your prompt forget to specify — and what did the AI silently decide for you?
I forgot to specify the logout route, and the AI entirely omitted it from the code. I also forgot to specify that the Supabase client should be initialized conditionally or defensively, so the AI silently assumed the environment variables would always be present and perfectly valid, initializing the client globally at the top level without any error handling.

### One Rematch
**What Changed:** I explicitly instructed the AI to wrap the token verification in a `try-except` block to catch Supabase errors and return a 401, and I added the missing logout route to the requirements; the AI successfully implemented these changes and safely caught the invalid token exception.
