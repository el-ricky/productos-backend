from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Producto
from schemas import ProductoCreate

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes (solo para prueba)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/productos")
def obtener_productos():
    db = SessionLocal()
    productos = db.query(Producto).all()
    resultado = [{"id": p.id, "nombre": p.nombre, "precio": float(p.precio)} for p in productos]
    db.close()
    return resultado

@app.get("/productos/{id}")
def obtener_producto(id: int):
    db = SessionLocal()
    producto = db.query(Producto).filter(Producto.id == id).first()
    db.close()
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return {"id": producto.id, "nombre": producto.nombre, "precio": float(producto.precio)}

@app.post("/productos")
def crear_producto(producto: ProductoCreate):
    db = SessionLocal()
    nuevo = Producto(nombre=producto.nombre, precio=producto.precio)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()
    return {"mensaje": "Producto creado", "id": nuevo.id}

@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoCreate):
    db = SessionLocal()
    existente = db.query(Producto).filter(Producto.id == id).first()
    if not existente:
        db.close()
        raise HTTPException(404, "Producto no encontrado")
    existente.nombre = producto.nombre
    existente.precio = producto.precio
    db.commit()
    db.close()
    return {"mensaje": "Producto actualizado"}

@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    db = SessionLocal()
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        db.close()
        raise HTTPException(404, "Producto no encontrado")
    db.delete(producto)
    db.commit()
    db.close()
    return {"mensaje": "Producto eliminado"}