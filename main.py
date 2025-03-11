import redis.asyncio as redis  # Import the asyncio version of Redis for async operations
from fastapi import FastAPI, Request, Depends  # Import FastAPI and necessary utilities for building APIs
from fastapi_limiter import FastAPILimiter  # Import FastAPI Limiter for rate limiting
from fastapi_limiter.depends import RateLimiter  # Import RateLimiter to limit request frequency
from fastapi.middleware.cors import CORSMiddleware  # Import middleware to handle CORS
from scr.routes import notes, users, tags, auth, cloud, comments, posts  # Import the route modules for the app
from scr.conf.config import config  # Import the configuration settings
from fastapi.responses import HTMLResponse  # Import HTMLResponse to return HTML content from endpoints

# Create FastAPI app instance
app = FastAPI()

# List of allowed origins for CORS (cross-origin resource sharing)
origins = ["*"]  # Allow all origins

# Add CORSMiddleware to the app to handle CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from all origins
    allow_credentials=True,  # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)

# Include the various route modules with their corresponding URL prefixes
app.include_router(auth.router, prefix='/api')  # Include auth routes under /api
app.include_router(users.router, prefix="/api")  # Include users routes under /api
app.include_router(tags.router, prefix='/api')  # Include tags routes under /api
app.include_router(comments.router, prefix="/api")  # Include comments routes under /api
app.include_router(posts.posts_router, prefix='/posts',  # Include posts routes under /posts with rate limiting
                   dependencies=[Depends(RateLimiter(times=2, seconds=5))])  # Limit 2 requests per 5 seconds
app.include_router(cloud.router, prefix='/api')  # Include cloud routes under /api

# Event handler that runs on app startup
@app.on_event("startup")
async def startup():
    # Connect to Redis server on startup
    r = await redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, encoding="utf-8",
                          password=config.REDIS_PASSWORD, decode_responses=True)
    # Initialize the FastAPI limiter with Redis backend
    await FastAPILimiter.init(r)


# Root endpoint returning a simple HTML page
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <body>
            <h1>Hello world, Team09 Python16 GoIT present Coursework on FastAPI</h1>  
            <a href="/docs">API Documentation</a>  
        </body>
    </html>
    """
