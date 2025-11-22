# --- Scalable API Rate Limiter Service (Sliding Window Log Algorithm Mock) ---
# This Python script implements the core logic of a distributed rate limiter 
# using the Sliding Window Log method, showcasing system design and algorithm skills.
# It uses Flask for the API interface and a dictionary to mock Redis or Memcached storage.

import time
import json
from flask import Flask, request, jsonify, Response
from collections import defaultdict

app = Flask(__name__)

# --- MOCK DISTRIBUTED CACHE (Simulating Redis/Memcached) ---
# In a real distributed system (e.g., using Kubernetes), this would be an external Redis instance
# accessed via a dedicated client.
MOCK_CACHE = defaultdict(list) 

# --- CONFIGURATION ---
RATE_LIMIT_MAX_REQUESTS = 5  # Maximum requests allowed
RATE_LIMIT_WINDOW_SECONDS = 60 # Time window (e.g., 60 seconds)

# --- RATE LIMITER ALGORITHM ---

def is_rate_limited(user_identifier):
    """
    Checks if the user has exceeded the defined rate limit using the Sliding Window Log algorithm.

    This algorithm stores a timestamp for every request made by the user within the window.
    It provides high accuracy but consumes more memory than other methods.
    
    Args:
        user_identifier (str): Unique identifier (e.g., IP address).
        
    Returns:
        tuple: (boolean: True if limited, integer: requests remaining)
    """
    current_time = int(time.time())
    
    # 1. Clean up old timestamps (The 'Sliding' part)
    # Filter out timestamps older than the configured window
    valid_timestamps = [
        t for t in MOCK_CACHE[user_identifier] 
        if t > current_time - RATE_LIMIT_WINDOW_SECONDS
    ]
    
    # Update the cache with only the valid timestamps
    MOCK_CACHE[user_identifier] = valid_timestamps
    
    current_request_count = len(valid_timestamps)
    
    # 2. Check Limit
    if current_request_count >= RATE_LIMIT_MAX_REQUESTS:
        requests_remaining = 0
        return True, requests_remaining
    
    # 3. Record new request (The 'Log' part)
    MOCK_CACHE[user_identifier].append(current_time)
    
    requests_remaining = RATE_LIMIT_MAX_REQUESTS - current_request_count - 1
    
    return False, requests_remaining


# --- API ENDPOINTS ---

@app.route('/api/data', methods=['GET'])
def get_data():
    # Identify user, usually via IP or an authenticated token
    user_ip = request.remote_addr 
    
    # Apply rate limiting check
    limited, remaining = is_rate_limited(user_ip)

    if limited:
        retry_after = RATE_LIMIT_WINDOW_SECONDS - (int(time.time()) - MOCK_CACHE[user_ip][0])
        
        # HTTP 429: Too Many Requests
        response = jsonify({"error": "Rate limit exceeded.", "message": f"Try again in {retry_after} seconds."})
        response.status_code = 429
        response.headers['X-RateLimit-Limit'] = RATE_LIMIT_MAX_REQUESTS
        response.headers['X-RateLimit-Remaining'] = 0
        response.headers['Retry-After'] = retry_after
        return response
    
    # If not limited, proceed with successful response
    response = jsonify({
        "status": "success",
        "message": "Data retrieved successfully.",
        "data": {"timestamp": time.time(), "user_id": user_ip}
    })
    
    # Add rate limiting headers to successful responses
    response.headers['X-RateLimit-Limit'] = RATE_LIMIT_MAX_REQUESTS
    response.headers['X-RateLimit-Remaining'] = remaining
    
    return response

@app.route('/status', methods=['GET'])
def get_status():
    """Simple health check endpoint."""
    return jsonify({"status": "OK", "service": "Rate Limiter API"})


if __name__ == '__main__':
    # Running the service on port 5000 (standard Flask port)
    print(f"Rate Limiter Service starting on http://127.0.0.1:5000/")
    print(f"Configuration: {RATE_LIMIT_MAX_REQUESTS} requests per {RATE_LIMIT_WINDOW_SECONDS} seconds.")
    app.run(debug=True, port=5000)
