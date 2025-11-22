# API Rate Limiter Service Sliding Window Log

Scalable API Rate Limiter Service (Sliding Window Log) 🔒

Overview and Project Goal

This project implements a critical backend component: a highly accurate, distributed Rate Limiter Service. The primary goal is to safeguard backend APIs from excessive traffic, abuse, and Denial-of-Service (DoS) attacks, ensuring stable resource availability for all users.

This implementation is a strong demonstration of Core Software Engineering, System Design principles, and Algorithmic Efficiency, making it highly relevant for senior engineering roles.

The service is built using Python / Flask to create the lightweight API interface.

Algorithm: Sliding Window Log

The service utilizes the Sliding Window Log algorithm for rate control, which is favored for its high accuracy in measuring request frequency over time, unlike simpler, less accurate methods (like fixed windows).
Mechanism:

Request Logging: The service maintains a precise timestamp log for every request made by a specific user (identified by IP or token).

Sliding: As time progresses, timestamps older than the configured time window (e.g., 60 seconds) are automatically discarded.

Check: The current count of valid timestamps determines the user's remaining request quota.

System Design and Technologies

The design is inherently scalable and fault-tolerant, achieved by separating state from logic:

Distributed Cache (Redis Mocked): The system relies on a mock distributed cache (simulating Redis or Memcached) to store the request logs. This is crucial for synchronization across multiple service instances and maintaining High Availability (HA).

Deployment Strategy (Docker/Kubernetes Conceptual): The service is designed to be easily containerized using Docker and deployed across a Kubernetes cluster. By being stateless (relying on external Redis), the service can be horizontally scaled to handle massive traffic loads.

Software Engineering Standards: Proper API communication is enforced using standard HTTP Headers. Exceeded limits result in an HTTP 429 (Too Many Requests) status code, and the Retry-After header informs the client exactly when they can make the next request.

API Endpoints

The API includes a protected endpoint and a health check:

The /status endpoint (GET method) serves as a simple health check.

The /api/data endpoint (GET method) is the protected resource. If the rate limit is exceeded, it returns the 429 Too Many Requests status with appropriate headers.

Execution & Scalability

The core logic is contained in the Python script (rate_limiter.py).

To run it locally:

# Assuming Flask is installed.
python rate_limiter.py


Scalability Notes (System Design Rationale)

Distributed State: The mock cache in the Python script must be replaced with a robust, external Redis instance in a production environment. This ensures all running pods/instances share the same, consistent rate data.

Client Identification: For simplicity, the script uses the request's IP address (request.remote_addr). In a secure, production environment, the rate limiter would use a secure, authenticated user ID or API key passed in the request header.
