# 🏘️ Comuna-Dash — Scraper & Dashboard de Propiedades

> **IMPORTANTE:**  
> Este proyecto permite obtener información pública de propiedades **sin requerir autorización, API Key ni login de Mercado Libre/PortalInmobiliario**.  
> El scraper extrae los datos desde el **endpoint del mapa** (`_DisplayType_M`), que es de acceso abierto para cualquier usuario y no requiere autenticación ni permisos especiales.  
> **Esto permite hacer análisis y seguimiento del mercado inmobiliario de manera ética y respetando las políticas de acceso público.**

---

Este proyecto permite **scrapear propiedades** desde PortalInmobiliario para todas las comunas de una región, guardar los datos en MongoDB, exponer una **API REST** con FastAPI y visualizarlos en un frontend React.

---

## 1. 🔎 Scraping de Propiedades

### 1.1. Clonar el repositorio

```bash
git clone 
cd comuna-dash/backend
```

### 1.2. Instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Asegúrate de tener `pymongo`, `requests`, y `python-dotenv` si usas variables de entorno.

### 1.3. Configurar conexión a MongoDB

- Por defecto: `mongodb://localhost:27017`
- Si usas MongoDB Atlas, reemplaza la URI en el código.

### 1.4. Ejecutar el scraper

```bash
python scraper.py
```

- El scraper extrae y guarda los datos en la base MongoDB `propiedades` → colección `inmuebles`.

---

## 2. 🚦 Backend API (FastAPI)

### 2.1. Desde la carpeta `/backend` (con el venv activo):

```bash
uvicorn main:app --reload
```

- La API estará disponible en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2.2. Endpoints útiles

- `/propiedades/?comuna=Concepcion&tipo_operacion=venta&tipo_inmueble=casa&skip=0&limit=50`  
  → Lista de propiedades filtradas

- `/resumen/?comuna=Concepcion`  
  → Resumen de precios promedio, cantidad, etc.

---

## 3. 🖥️ Frontend (React)

### 3.1. Crear el frontend (si no existe)

```bash
cd ..
npm create vite@latest comuna-frontend -- --template react
cd comuna-frontend
npm install
```

### 3.2. Correr el frontend

```bash
npm run dev
```

- Accede en [http://localhost:5173](http://localhost:5173) (por defecto)

### 3.3. Consumir la API

- El frontend debe hacer requests al backend (por defecto en `http://localhost:8000`).
- Si tienes problemas de CORS, revisa el middleware en FastAPI.

---

## 4. 🗂️ Estructura recomendada

```
comuna-dash/
  backend/
    scraper.py
    main.py (FastAPI)
    requirements.txt
  comuna-frontend/
    src/
      components/
      pages/
    package.json
    vite.config.js
  comunas_biobio.csv (u otro CSV de comunas/regiones)
```

---

## 5. 🛠️ Otros Tips

- **Para ver los datos**: Usa MongoDB Compass, conecta a `localhost:27017`, abre la DB `propiedades` y la colección `inmuebles`.
- **Para eliminar duplicados**: Usa el pipeline de aggregation en Compass o desde código.
- **Para escalar**: Cambia el CSV para agregar más comunas o regiones.

---

## 6. 📦 Variables de entorno (opcional)

Si usas variables para la conexión Mongo, crea un archivo `.env` y usa `python-dotenv` en tu código para cargarlo.

---

## 7. 👨‍💻 Créditos

Proyecto desarrollado por John V. S.
Inspirado en necesidades reales de análisis de mercado inmobiliario.

---
