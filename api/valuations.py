from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from database import get_db_connection

router = APIRouter()

@router.post("/valuations", status_code=201)
def submit_valuation(
    name: str = Body(...),
    phone: str = Body(...),
    bike_model: str = Body(...),
    year: Optional[str] = Body(""),
    kilometers: Optional[str] = Body(""),
    city: Optional[str] = Body("")
):
    if not name or not phone or not bike_model:
        raise HTTPException(status_code=400, detail="Name, phone, and bike model are required.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO valuations (name, phone, bike_model, year, kilometers, city)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, phone, bike_model, year, kilometers, city))
        conn.commit()
        valuation_id = cursor.lastrowid
        return {"id": valuation_id, "message": "Valuation request received!"}
    finally:
        cursor.close()
        conn.close()
