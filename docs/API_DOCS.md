# Authentication API

## Introduction

Welcome to the Authentication API! This API offers robust endpoints for managing user accounts, including registration, authentication, email verification, password management, and Google OAuth integration. Designed for seamless integration and performance, this API is a comprehensive solution for authentication needs.

## Installation

Follow these steps to set up the API locally:

### Prerequisites

- Ensure you have Python and pip installed on your system.

## API Endpoints

### 1. Register

- **URL:** `/auth/register`
- **Method:** `POST`
- **Description:** Registers a new user.
- **Request Body:**

  ```json
  {
    "email": "user@example.com",
    "hash_password": "Password123!",
    "repeat_password": "Password123!"
  }
  ```
  
- **Response Codes:**
  - `201 Created`: Registration successful.
  - `400 Bad Request`: Passwords do not match.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `409 Conflict`: Email is already in use.
  - `500 Internal Server Error`: Internal Server Error.
  - `504 External Service Is Not Responding`: Gateway Timeout.

### 2. Verify Email

- **URL:** `/auth/verify_email/{token}`
- **Method:** `GET`
- **Description:** Verifies a user's email address with the given token.
- **Parameters:**

  - `token`: The email verification token.

- **Response Codes:**
  - `200 OK`: Email verified successfully.
  - `400 Bad Request`: Token has expired.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `500 Internal Server Error`: Internal Server Error.

### 3. Login

- **URL:** `/auth/login`
- **Method:** `POST`
- **Description:** Authenticates a user and returns access tokens.
- **Request Body:**

  ```json
  {
    "email": "user@example.com",
    "password": "Password123!"
  }
  ```
  
- **Response Codes:**
  - `200 OK`: Login successful.
  - `401 Unauthorized`: Incorrect username or password.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `500 Internal Server Error`: Internal Server Error.

### 4. Resend Email Verification

- **URL:** `/auth/resend_email/{user_id}`
- **Method:** `GET`
- **Description:** Resend the email verification to the user.
- **Parameters:**

  - `user_id`: The user's UUID.

- **Response Codes:**
  - `200 OK`: Verification email resent.
  - `400 Bad Request`: Email verification token expired.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `429 Too Many Requests`: Request limit exceeded.
  - `500 Internal Server Error`: Internal Server Error.
  - `504 External Service Is Not Responding`: Gateway Timeout.

### 5. Google Authentication URL

- **URL:** `/auth/google_auth`
- **Method:** `GET`
- **Description:** Generates a URL for Google OAuth.
- **Response Codes:**
  - `200 OK`: Google OAuth URL generated successfully.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `500 Internal Server Error`: Internal Server Error.

### 6. Refresh Access Token

- **URL:** `/auth/refresh_access`
- **Method:** `POST`
- **Description:** Refreshes the user's access token using the refresh token.
- **Request Headers:** Requires `refresh_token` in cookies.
- **Response Codes:**
  - `200 OK`: Access token refreshed.
  - `401 Unauthorized`: Unauthorized access.
  - `404 Not Found`: User not found.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `500 Internal Server Error`: Internal Server Error.

### 7. Forgot Password

- **URL:** `/auth/forgot_password`
- **Method:** `POST`
- **Description:** Initiates the password reset process by sending a reset email.
- **Request Body:**

  ```json
  {
    "email": "user@example.com"
  }
  ```
  
- **Response Codes:**
  - `200 OK`: Password reset initiated.
  - `404 Not Found`: User not found.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `500 Internal Server Error`: Internal Server Error.

### 8. Verify User for Password Reset

- **URL:** `/auth/forgot_password/{token}`
- **Method:** `GET`
- **Description:** Verifies the user token for password reset purposes.
- **Parameters:**

  - `token`: The password reset token.

- **Response Codes:**
  - `200 OK`: User verification successful.
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `500 Internal Server Error`: Internal Server Error.

### 9. Change Password

- **URL:** `/auth/forgot_password/change`
- **Method:** `POST`
- **Description:** Changes the user's password after verification.
- **Request Body:**

  ```json
  {
    "id": "uuid-or-string",
    "hash_password": "NewPassword123!",
    "repeat_password": "NewPassword123!"
  }
  ```
  
- **Response Codes:**
  - `200 OK`: Password changed successfully.
  - `400 Bad Request`: Time expired or passwords do not match.
  - `401 Unauthorized`: Password Doesn`t Match
  - `405 Metod Not Allow`: Metod Not Allowed.
  - `500 Internal Server Error`: Internal Server Error.

### 10. Logout

- **URL:** `/auth/logout`
- **Method:** `GET`
- **Description:** Logs out the user by invalidating the refresh token.
- **Response Codes:**
  - `204 No Content`: User logged out successfully.

## Example Usage

```bash
# Register a new user
curl -X POST -H "Content-Type: application/json" -d '{"email":"user@example.com", "hash_password": "Password123!", "repeat_password": "Password123!"}' http://localhost:8000/auth/register

# Verify email
curl http://localhost:8000/auth/verify_email/your-verification-token

# Login
curl -X POST -H "Content-Type: application/json" -d '{"login":"user@example.com", "password": "Password123!"}' http://localhost:8000/auth/login
```
Replace `your-verification-token` with the actual token received by the user.

## Contributing

Contributions are welcome! Please fork the repo and submit a pull request for any proposed changes or bug fixes.
