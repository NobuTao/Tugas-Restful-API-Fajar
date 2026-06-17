import os
from dotenv import load_dotenv
from supabase import create_client, Client
from app.schemas import BookSchema

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class BookService:
    @staticmethod
    def get_all():
        response = supabase.table("books").select("*").execute()
        return response.data

    @staticmethod
    def get_by_id(book_id: int):
        response = supabase.table("books").select("*").eq("id", book_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def create(book: BookSchema):
        response, count = supabase.table("books").insert(book.model_dump()).execute()
        return response[1]

    @staticmethod
    def update(book_id: int, book: BookSchema):
        response, count = supabase.table("books").update(book.model_dump()).eq("id", book_id).execute()
        return response[1] if response[1] else None

    @staticmethod
    def delete(book_id: int):
        supabase.table("books").delete().eq("id", book_id).execute()
        return True