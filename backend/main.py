import os
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

# Render 'postgres://' deta hai, par SQLAlchemy 'postgresql://' maangta hai
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Tables (जो schema.sql में थीं) ---
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name_hi = Column(String)
    name_en = Column(String)
    parent_id = Column(Integer)

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    logo_url = Column(String)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name_hi = Column(String)
    name_en = Column(String)
    brand_id = Column(Integer)
    category_id = Column(Integer)
    weight = Column(String)
    unit = Column(String)
    barcode = Column(String)
    photo_url = Column(String)

class Seller(Base):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    city = Column(String)
    phone = Column(String)

class Rate(Base):
    __tablename__ = "rates"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer)
    seller_id = Column(Integer)
    wholesale_price = Column(Numeric(10, 2))
    retail_price = Column(Numeric(10, 2))
    source = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

# जब सर्वर चालू होगा, ये टेबल्स अपने आप डेटाबेस में बन जाएँगी
Base.metadata.create_all(bind=engine)

# --- FastAPI App ---
app = FastAPI(title="HopDukan API", description="भारत का रेट कार्ड")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to HopDukan API"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running perfectly"}

@app.get("/api/db-check")
def db_check():
    try:
        db = SessionLocal()
        # डेटाबेस से एक छोटा सा सवाल पूछकर देखते हैं
        db.query(Category).first()
        db.close()
        return {"status": "ok", "message": "Database connected successfully! 🎉"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

from pydantic import BaseModel

class ItemCreate(BaseModel):
    name_hi: str
    name_en: str
    wholesale_price: float

# 1. डेटाबेस में नया आइटम जोड़ने के लिए (सिर्फ टेस्टिंग के लिए)
@app.post("/api/add-item")
def add_item(item: ItemCreate):
    db = SessionLocal()
    try:
        new_item = Item(name_hi=item.name_hi, name_en=item.name_en)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        new_rate = Rate(item_id=new_item.id, wholesale_price=item.wholesale_price, source="manual")
        db.add(new_rate)
        db.commit()
        return {"status": "ok", "message": f"{item.name_hi} जोड़ दिया गया है!"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

# 2. डेटाबेस से सारे आइटम निकालने के लिए
@app.get("/api/items")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    result = []
    for item in items:
        rate = db.query(Rate).filter(Rate.item_id == item.id).first()
        result.append({
            "id": item.id,
            "name_hi": item.name_hi,
            "name_en": item.name_en,
            "price": float(rate.wholesale_price) if rate else 0
        })
    db.close()
    return {"items": result}
