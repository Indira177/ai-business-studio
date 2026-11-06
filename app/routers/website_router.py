import os
import shutil
import zipfile

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.website import Website
from app.services.website_service import create_website


router = APIRouter(
    prefix="/api/websites",
    tags=["Websites"]
)


class WebsiteRequest(BaseModel):
    business_name: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=5)
    pages: list[str] = Field(
        default=["Home", "About", "Services", "Contact"]
    )
    style: str = Field(default="Modern")


@router.post("/generate")
def generate_website(
    request: WebsiteRequest,
    db: Session = Depends(get_db)
):
    try:
        result = create_website(
            business_name=request.business_name,
            description=request.description,
            pages=request.pages,
            style=request.style,
            db=db
        )

        return {
            "status": "success",
            "message": "Website generated successfully",
            "data": result
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Website generation failed: {str(e)}"
        )


@router.get("")
def list_websites(db: Session = Depends(get_db)):
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
            "created_at": website.created_at,
            "preview_url": f"/api/websites/{website.id}/preview",
            "download_url": f"/api/websites/{website.id}/download"
        })

    return {
        "status": "success",
        "count": len(data),
        "data": data
    }


def get_website_or_404(website_id: int, db: Session):
    website = (
        db.query(Website)
        .filter(Website.id == website_id)
        .first()
    )

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    if not website.folder_path:
        raise HTTPException(status_code=404, detail="Website files not found")

    return website


@router.get("/{website_id}/preview")
def preview_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    website = get_website_or_404(website_id, db)

    index_file = os.path.join(website.folder_path, "index.html")

    if not os.path.isfile(index_file):
        raise HTTPException(
            status_code=404,
            detail="Website index file not found"
        )

    return FileResponse(index_file, media_type="text/html")


def serve_preview_asset(
    website_id: int,
    file_name: str,
    media_type: str,
    db: Session
):
    website = get_website_or_404(website_id, db)
    file_path = os.path.join(website.folder_path, file_name)

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"{file_name} not found"
        )

    return FileResponse(file_path, media_type=media_type)


@router.get("/{website_id}/style.css")
def preview_css(
    website_id: int,
    db: Session = Depends(get_db)
):
    return serve_preview_asset(
        website_id, "style.css", "text/css", db
    )


@router.get("/{website_id}/script.js")
def preview_javascript(
    website_id: int,
    db: Session = Depends(get_db)
):
    return serve_preview_asset(
        website_id, "script.js", "application/javascript", db
    )


@router.get("/{website_id}/download")
def download_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    website = get_website_or_404(website_id, db)

    if not os.path.isdir(website.folder_path):
        raise HTTPException(
            status_code=404,
            detail="Website folder not found"
        )

    zip_file = website.folder_path + ".zip"

    with zipfile.ZipFile(
        zip_file,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:
        for root, dirs, files in os.walk(website.folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(
                    file_path,
                    website.folder_path
                )
                zipf.write(file_path, arcname)

    return FileResponse(
        zip_file,
        media_type="application/zip",
        filename=f"{website.business_name}.zip"
    )


@router.delete("/{website_id}")
def delete_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    website = (
        db.query(Website)
        .filter(Website.id == website_id)
        .first()
    )

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    folder_path = website.folder_path
    zip_file = folder_path + ".zip" if folder_path else None

    try:
        if folder_path and os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        if zip_file and os.path.exists(zip_file):
            os.remove(zip_file)

        db.delete(website)
        db.commit()

        return {
            "status": "success",
            "message": "Website deleted successfully",
            "website_id": website_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Website deletion failed: {str(e)}"
        )