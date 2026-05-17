from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import boto3, database, models

# Crear tablas automáticamente
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

BUCKET = "user-1027741086-ueia-so"
s3 = boto3.client("s3", region_name="us-east-2")

FORMATOS_PERMITIDOS = {"image/png", "image/jpeg", "image/jpg"}

# ── POST: subir imagen ─────────────────────────────────────────────
@app.post("/upload")
async def subir_imagen(
    usuario: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    # Validar formato
    if archivo.content_type not in FORMATOS_PERMITIDOS:
        raise HTTPException(status_code=415, detail="Solo se aceptan PNG o JPG")

    # Ruta en S3 organizada por usuario
    ruta_s3 = f"{usuario}/{archivo.filename}"

    # Subir a S3
    contenido = await archivo.read()
    s3.put_object(
        Bucket=BUCKET,
        Key=ruta_s3,
        Body=contenido,
        ContentType=archivo.content_type
    )

    # Guardar en RDS
    registro = models.Imagen(
        usuario=usuario,
        ruta_s3=ruta_s3,
        fecha=datetime.utcnow()
    )
    db.add(registro)
    db.commit()

    return {"mensaje": "Imagen subida correctamente", "ruta": ruta_s3}


# ── GET: obtener imagen ────────────────────────────────────────────
@app.get("/image")
def obtener_imagen(
    usuario: str,
    nombre_imagen: str,
    db: Session = Depends(database.get_db)
):
    ruta_s3 = f"{usuario}/{nombre_imagen}"

    # Buscar en RDS
    registro = db.query(models.Imagen).filter(
        models.Imagen.usuario == usuario,
        models.Imagen.ruta_s3 == ruta_s3
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Usuario o imagen no encontrada")

    # Generar URL prefirmada (válida 1 hora)
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": ruta_s3},
        ExpiresIn=3600
    )

    return {
        "url": url,
        "fecha_creacion": registro.fecha
    }

# Adaptador para Lambda
from mangum import Mangum
handler = Mangum(app)
