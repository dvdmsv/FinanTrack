# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /project-back

# Copia los archivos del proyecto dentro del contenedor
COPY . /project-back

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto 5000
EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["python", "app.py"]
