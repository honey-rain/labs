from fastapi import FastAPI, Request
from routers import version, posts
from routers.stats import router as stats_router

app = FastAPI()

# Middleware for counting requests
stats = {
    "GET": {"version": 0, "posts": 0, "stats": 0},
    "POST": {"posts": 0},
    "PUT": {"posts": 0},
    "DELETE": {"posts": 0},
}

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    method = request.method
    path = request.url.path

    if path.startswith("/version"):
        stats[method]["version"] += 1
    elif path.startswith("/posts"):
        if method in stats:
            stats[method]["posts"] += 1
    elif path.startswith("/stats"):
        stats[method]["stats"] += 1

    return response

app.include_router(version.router)
app.include_router(posts.router)
app.include_router(stats_router)

@app.get("/stats")
def get_stats():
    return stats
