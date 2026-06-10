import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inisialisasi Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inisialisasi FastAPI
app = FastAPI(
    title="Tugas RESTful API - Buku",
    description="API Sederhana menggunakan FastAPI dan Supabase",
    version="1.0.0"
)

# Pydantic Schema untuk validasi data data masuk
class BookSchema(BaseModel):
    title: str
    author: str
    is_read: bool = False

# ==================== ENDPOINTS ====================

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Selamat datang di API Perpustakaan Sederhana!"}


# 1. CREATE: Menambahkan buku baru
@app.post("/books", status_code=201, tags=["Books"])
def create_book(book: BookSchema):
    try:
        data, count = supabase.table("books").insert(book.model_dump()).execute()
        return {"message": "Buku berhasil ditambahkan", "data": data[1]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2. READ: Mengambil semua data buku
@app.get("/books", tags=["Books"])
def get_all_books():
    try:
        response = supabase.table("books").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 3. READ: Mengambil satu buku berdasarkan ID
@app.get("/books/{book_id}", tags=["Books"])
def get_book_by_id(book_id: int):
    try:
        response = supabase.table("books").select("*").eq("id", book_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
        return {"data": response.data[0]}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))


# 4. UPDATE: Mengubah data buku berdasarkan ID
@app.put("/books/{book_id}", tags=["Books"])
def update_book(book_id: int, book: BookSchema):
    try:
        # Cek apakah data ada
        check = supabase.table("books").select("*").eq("id", book_id).execute()
        if not check.data:
            raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
        
        data, count = supabase.table("books").update(book.model_dump()).eq("id", book_id).execute()
        return {"message": "Buku berhasil diperbarui", "data": data[1]}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=400, detail=str(e))


# 5. DELETE: Menghapus buku berdasarkan ID
@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    try:
        # Cek apakah data ada
        check = supabase.table("books").select("*").eq("id", book_id).execute()
        if not check.data:
            raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
        
        supabase.table("books").delete().eq("id", book_id).execute()
        return {"message": f"Buku dengan ID {book_id} berhasil dihapus"}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))