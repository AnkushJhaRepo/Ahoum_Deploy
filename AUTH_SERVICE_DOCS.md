# AuthService Documentation

The `AuthService` class provides secure authentication utilities for password hashing, verification, and JWT token management.

## Features

- **bcrypt Password Hashing**: Secure password hashing with salt
- **JWT Token Management**: Generate, verify, and refresh JWT tokens
- **Error Handling**: Comprehensive error handling with logging
- **Type Safety**: Full type hints for better code quality

## Installation

Add bcrypt to your requirements:

```bash
pip install bcrypt==4.1.2
```

## Usage

### Import the Service

```python
from main_app.routes.auth_service import AuthService
```

### Password Management

#### Hash a Password

```python
# Hash a plain text password
password = "mySecurePassword123"
hashed_password = AuthService.hash_password(password)
print(hashed_password)
# Output: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iQeO
```

#### Verify a Password

```python
# Verify a password against its hash
is_valid = AuthService.verify_password("mySecurePassword123", hashed_password)
print(is_valid)  # True

# Wrong password
is_invalid = AuthService.verify_password("wrongPassword", hashed_password)
print(is_invalid)  # False
```

### JWT Token Management

#### Generate JWT Token

```python
# Generate a basic JWT token
user_id = 123
token = AuthService.generate_jwt(user_id)
print(token)
# Output: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# Generate JWT with additional claims
additional_claims = {
    'role': 'admin',
    'permissions': ['read', 'write']
}
token_with_claims = AuthService.generate_jwt(user_id, additional_claims)
```

#### Verify JWT Token

```python
# Verify and decode a JWT token
payload = AuthService.verify_jwt(token)
if payload:
    print(f"User ID: {payload.get('user_id')}")
    print(f"Expiration: {payload.get('exp')}")
    print(f"Role: {payload.get('role')}")
else:
    print("Invalid or expired token")
```

#### Extract User ID from Token

```python
# Get user ID from token
user_id = AuthService.get_user_id_from_token(token)
if user_id:
    print(f"User ID: {user_id}")
else:
    print("Invalid token")
```

#### Refresh JWT Token

```python
# Refresh an existing token (extends expiration)
refreshed_token = AuthService.refresh_jwt(token)
if refreshed_token:
    print("Token refreshed successfully")
else:
    print("Failed to refresh token")
```

## API Reference

### AuthService Class

#### Static Methods

##### `hash_password(password: str) -> str`

Hashes a password using bcrypt with a random salt.

**Parameters:**
- `password` (str): Plain text password to hash

**Returns:**
- `str`: Hashed password string

**Raises:**
- `Exception`: If hashing fails

##### `verify_password(password: str, hashed_password: str) -> bool`

Verifies a password against its hash.

**Parameters:**
- `password` (str): Plain text password to verify
- `hashed_password` (str): Hashed password from database

**Returns:**
- `bool`: True if password matches, False otherwise

##### `generate_jwt(user_id: int, additional_claims: Optional[Dict[str, Any]] = None) -> str`

Generates a JWT token for a user.

**Parameters:**
- `user_id` (int): User ID to include in token
- `additional_claims` (dict, optional): Additional claims to include

**Returns:**
- `str`: JWT token string

**Raises:**
- `Exception`: If JWT generation fails

##### `verify_jwt(token: str) -> Optional[Dict[str, Any]]`

Verifies and decodes a JWT token.

**Parameters:**
- `token` (str): JWT token to verify

**Returns:**
- `dict`: Decoded token payload if valid, None otherwise

##### `get_user_id_from_token(token: str) -> Optional[int]`

Extracts user ID from JWT token.

**Parameters:**
- `token` (str): JWT token

**Returns:**
- `int`: User ID if token is valid, None otherwise

##### `refresh_jwt(token: str) -> Optional[str]`

Refreshes a JWT token (extends expiration).

**Parameters:**
- `token` (str): Current JWT token

**Returns:**
- `str`: New JWT token if original is valid, None otherwise

## Configuration

The service requires the following Flask configuration:

```python
app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'
```

## Security Features

1. **bcrypt Hashing**: Uses bcrypt with salt for password hashing
2. **JWT Security**: HS256 algorithm with configurable secret key
3. **Token Expiration**: 24-hour default expiration
4. **Error Logging**: Comprehensive error logging without exposing sensitive data
5. **Input Validation**: Proper handling of invalid inputs

## Error Handling

The service includes comprehensive error handling:

- **Password Hashing Errors**: Logged and re-raised
- **Password Verification Errors**: Logged and return False
- **JWT Generation Errors**: Logged and re-raised
- **JWT Verification Errors**: Logged and return None
- **Expired Tokens**: Properly handled with warnings

## Testing

Run the test script to verify functionality:

```bash
python test_auth_service.py
```

## Integration with Flask Routes

The `AuthService` is integrated with the authentication routes:

```python
# In auth_routes.py
from main_app.routes.auth_service import AuthService

# Registration
hashed_password = AuthService.hash_password(password)

# Login
if AuthService.verify_password(password, user.password):
    token = AuthService.generate_jwt(user.id)

# Protected routes
user_id = AuthService.get_user_id_from_token(token)
```

## Best Practices

1. **Never store plain text passwords**
2. **Use strong JWT secret keys**
3. **Implement token refresh for long sessions**
4. **Log authentication failures for security monitoring**
5. **Use HTTPS in production**
6. **Regularly rotate JWT secret keys**

## Migration from werkzeug.security

If migrating from werkzeug's password hashing:

```python
# Old way (werkzeug)
from werkzeug.security import generate_password_hash, check_password_hash
hashed = generate_password_hash(password, method='sha256')
is_valid = check_password_hash(hashed, password)

# New way (AuthService)
from main_app.routes.auth_service import AuthService
hashed = AuthService.hash_password(password)
is_valid = AuthService.verify_password(password, hashed)
```

**Note**: bcrypt is more secure than SHA-256 for password hashing as it's specifically designed for this purpose and includes salt automatically. 