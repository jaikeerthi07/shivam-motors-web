from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Header, Depends
from typing import Optional, List
import os
import shutil
from database import get_db_connection

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sm/uploads"))
ADMIN_TOKEN = "shivadmin_secret_token_2026"

def verify_admin(authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized access. Valid token required.")
    return True

@router.get("/bikes")
def get_bikes(category: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if category:
            cursor.execute("SELECT * FROM bikes WHERE category = %s ORDER BY id DESC", (category,))
        else:
            cursor.execute("SELECT * FROM bikes ORDER BY id DESC")
        bikes = cursor.fetchall()
        return bikes
    finally:
        cursor.close()
        conn.close()

@router.get("/bikes/{category}")
def get_bikes_by_category(category: str):
    return get_bikes(category)

@router.post("/admin/bikes", status_code=201)
async def add_bike(
    title: str = Form(...),
    price: str = Form(...),
    category: str = Form(...),
    badge: Optional[str] = Form(None),
    info: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    status: str = Form("unsold"),
    photo: UploadFile = File(...),
    authenticated: bool = Depends(verify_admin)
):
    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save photo
    import time
    import random
    unique_suffix = f"{int(time.time() * 1000)}-{random.randint(0, 10**9)}"
    extension = os.path.splitext(photo.filename)[1]
    filename = f"{unique_suffix}{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    image_url = f"/uploads/{filename}"

    # Insert into DB
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO bikes (title, price, category, badge, info, description, image_url, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (title, price, category, badge, info, description, image_url, status))
        conn.commit()
        bike_id = cursor.lastrowid
        return {"id": bike_id, "message": "Bike added successfully"}
    finally:
        cursor.close()
        conn.close()

@router.delete("/admin/bikes/{bike_id}")
def delete_bike(bike_id: int, authenticated: bool = Depends(verify_admin)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get image URL first
        cursor.execute("SELECT image_url FROM bikes WHERE id = %s", (bike_id,))
        bike = cursor.fetchone()
        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

        # Delete image file
        image_url = bike['image_url']
        if image_url and image_url.startswith("/uploads/"):
            full_path = os.path.abspath(os.path.join(UPLOAD_DIR, "..", image_url.lstrip("/")))
            if os.path.exists(full_path):
                os.remove(full_path)

        # Delete from DB
        cursor.execute("DELETE FROM bikes WHERE id = %s", (bike_id,))
        conn.commit()
        return {"message": "Bike deleted successfully"}
    finally:
        cursor.close()
        conn.close()
