from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.website import Website


router = APIRouter(
    prefix="/api/websites",
    tags=["Websites"]
)


@router.get("")
def get_websites(
    db: Session = Depends(get_db)
):

    websites = (
        db.query(Website)
        .order_by(Website.id.desc())
        .all()
    )

    data = []

    for website in websites:

        data.append({
            "website_id": website.id,
            "business_name": website.business_name,
            "description": website.description,
            "style": website.style,
            "folder_path": website.folder_path,
            "created_at": (
                website.created_at.isoformat()
                if website.created_at
                else None
            ),
            "preview_url":
                f"/api/websites/{website.id}/preview",
            "download_url":
                f"/api/websites/{website.id}/download"
        })

    return {
        "status": "success",
        "count": len(data),
        "data": data
    }