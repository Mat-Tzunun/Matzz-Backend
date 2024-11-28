# Dockerfile para el backend Python

# Usar una imagen base de Python
FROM python:3.10.11

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Instalar dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Establecer variables de entorno
ENV MYSQL_HOST=db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=1234
ENV MYSQL_DB=matzunun
ENV MYSQL_PORT=3306
ENV ENV=development

# Comando para ejecutar la aplicación
CMD ["python", "-m", "main"]

