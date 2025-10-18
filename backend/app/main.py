from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import User, UserRole, BurgerSKU
from .auth import get_password_hash
from .routers import auth as auth_router
from .routers import admin as admin_router
from .routers import user as user_router
from .routers import notify as notify_router

app = FastAPI(title="Burger Ordering System", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # seed admin user and sample SKUs if empty
    db = next(get_db())
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role=UserRole.ADMIN,
            )
            db.add(admin)
            db.commit()
        if db.query(BurgerSKU).count() == 0:
            db.add_all(
                [
                    BurgerSKU(name="Classic Burger", description="Beef patty with sauce", price=8.99, size="REGULAR"),
                    BurgerSKU(name="Cheeseburger", description="Cheddar cheese", price=9.99, size="REGULAR"),
                    BurgerSKU(name="Veggie Burger", description="Plant-based patty", price=10.49, size="REGULAR"),
                ]
            )
            db.commit()
    finally:
        db.close()


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(admin_router.router)
app.include_router(notify_router.router)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}
