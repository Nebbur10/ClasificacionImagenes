from fastapi import FastAPI, Request, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import boto3
from s3_utils import subir_imagen_a_s3
from database import SessionLocal, engine
from models import Base, Clasificacion

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

rekognition = boto3.client("rekognition", region_name="us-east-1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/subir", response_class=HTMLResponse)
async def subir_imagen(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contenido = await file.read()

        url_s3 = subir_imagen_a_s3(contenido, file.filename)

        respuesta = rekognition.detect_labels(
            Image={"Bytes": contenido},
            MaxLabels=10,
            MinConfidence=70
        )

        for label in respuesta["Labels"]:
            db.add(Clasificacion(
                nombre_archivo=file.filename,
                etiqueta=label["Name"],
                confianza=label["Confidence"],
                url_s3=url_s3
            ))
        db.commit()

        return templates.TemplateResponse("index.html", {
            "request": request,
            "mensaje": "Imagen procesada con éxito",
            "url_imagen": url_s3,
            "etiquetas": respuesta["Labels"]
        })

    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "mensaje": f"Error: {str(e)}"
        })
