from fastapi import APIRouter

router = APIRouter()

# This route will be used by the main app to retrieve stats
@router.get("/stats")
def get_stats(stats: dict):
    return stats