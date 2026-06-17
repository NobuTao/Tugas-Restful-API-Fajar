from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import BookSchema
from app.service import BookService

app = FastAPI(title="Tugas Terpisah - Service & Front-end")

# WAJIB: Agar Frontend bisa berkomunikasi dengan Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Di dunia nyata ini diisi URL frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/books")
def read_books():
    return {"data": BookService.get_all()}

@app.post("/books", status_code=201)
def create_book(book: BookSchema):
    return {"message": "Sukses", "data": BookService.create(book)}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookSchema):
    updated = BookService.update(book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    return {"message": "Diperbarui", "data": updated}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    BookService.delete(book_id)
    return {"message": f"Buku {book_id} dihapus"}