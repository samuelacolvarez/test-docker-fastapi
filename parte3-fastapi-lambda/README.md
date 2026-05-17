# Mi FastAPI S3 - Taller AWS

## Descripción
API REST para subir y consultar imágenes usando FastAPI, Amazon S3, RDS y Lambda.

## Endpoints
- POST /upload — sube una imagen PNG/JPG a S3 y registra en RDS
- GET /image — consulta una imagen y retorna URL prefirmada

## Tecnologías
- FastAPI + Mangum
- Amazon S3
- Amazon RDS (MySQL)
- Amazon ECR
- AWS Lambda

## Cómo correr localmente
```bash
docker build -t mi-fastapi .
docker run -p 9000:80 \
  -e AWS_ACCESS_KEY_ID=tu-key \
  -e AWS_SECRET_ACCESS_KEY=tu-secret \
  -e AWS_DEFAULT_REGION=us-east-2 \
  mi-fastapi
```
Abrir http://localhost:9000/docs

## URL Lambda
https://fhhugflv3h7gimzor72ay5ybf40nzpqb.lambda-url.us-east-2.on.aws/docs
