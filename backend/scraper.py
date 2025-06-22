import requests
import time
from datetime import datetime
from pymongo import MongoClient

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
client = MongoClient("mongodb://localhost:27017")
db = client['propiedades']
collection = db['inmuebles']

COMUNAS_BIOBIO = [
    'alto-biobio', 'antuco', 'arauco', 'cabrero', 'canete', 'chiguayante',
    'concepcion', 'contulmo', 'coronel', 'florida', 'hualpen', 'hualqui',
    'lebu', 'los-alamos', 'los-angeles', 'lota', 'mulchen', 'Nacimiento',
    'negrete', 'penco', 'quilleco', 'quilaco', 'quillon', 'san-pedro-de-la-paz',
    'san-rosendo', 'santa-barbara', 'santa-juana', 'talcahuano', 'tome'
]

OPERACIONES = ['venta', 'arriendo']
TIPOS_INMUEBLE = ['casa', 'departamento']

def valor_uf():
    try:
        r = requests.get("https://mindicador.cl/api", timeout=5)
        r.raise_for_status()
        return r.json()["uf"]["valor"]
    except Exception as e:
        print(f"No se pudo obtener UF: {e}")
        return 37000

def get_attr(attrs, ids):
    if isinstance(ids, str):
        ids = [ids]
    for attr in attrs:
        if attr.get("id") in ids:
            return attr.get("value_name") or attr.get("value") or ""
    return ""

def guardar_aviso(item, comuna, tipo_operacion, tipo_inmueble, uf):
    p = item.get("price", {})
    precio_uf = p.get("amount", 0)
    precio_clp = int(precio_uf * uf) if p.get("currency_id") == "CLF" else precio_uf
    attrs = item.get("attributes", [])
    aviso = {
        "id_aviso": item.get("id", ""),  # Para identificar
        "tipo_operacion": tipo_operacion,
        "tipo_inmueble": tipo_inmueble,
        "titulo": item.get("title", ""),
        "precio_uf": precio_uf,
        "precio_clp": precio_clp,
        "direccion": item.get("location", ""),
        "comuna": comuna.replace("-", " ").title(),
        "superficie_m2": get_attr(attrs, ["TOTAL_AREA", "COVERED_AREA"]),
        "dormitorios": get_attr(attrs, ["BEDROOMS", "BEDROOMS_NUMBER"]),
        "baños": get_attr(attrs, ["FULL_BATHROOMS", "BATHROOMS"]),
        "url": item.get("permalink", ""),
        "fecha_scraping": datetime.utcnow().isoformat()
    }
    # Solo inserta si no existe ese aviso (por id o url)
    if not collection.find_one({"url": aviso["url"]}):
        collection.insert_one(aviso)

if __name__ == "__main__":
    UF_CLP = valor_uf()
    print(f"\nUF actual: {UF_CLP:,.0f} CLP\n")
    for comuna in COMUNAS_BIOBIO:
        for operacion in OPERACIONES:
            for tipo_inmueble in TIPOS_INMUEBLE:
                print(f"===> Scrapeando {comuna} | {tipo_inmueble} | {operacion} <===")
                pagina = 1
                prev_ids = set()
                repeticiones = 0
                while pagina < 50:  # No más de 50 páginas por comuna
                    url = f"https://www.portalinmobiliario.com/api/{operacion}/{tipo_inmueble}/{comuna}-biobio/_DisplayType_M"
                    if pagina > 1:
                        url += f"#{pagina}"
                    print(f"  Página {pagina}: {url}")
                    try:
                        resp = requests.get(url, headers=HEADERS, timeout=10)
                        resp.raise_for_status()
                        data = resp.json()
                    except Exception as e:
                        print(f"    Error: {e}")
                        break

                    results = data.get("results", [])
                    if not results:
                        print("    No más datos, cambio de comuna/tipo.")
                        break

                    ids = set(item.get("id") for item in results)
                    # Si la API devuelve siempre los mismos avisos, detén el ciclo
                    if ids == prev_ids:
                        repeticiones += 1
                        if repeticiones > 2:
                            print("    Páginas repetidas, deteniendo para esta comuna/tipo.")
                            break
                    else:
                        repeticiones = 0

                    for itm in results:
                        guardar_aviso(itm, comuna, operacion, tipo_inmueble, UF_CLP)

                    prev_ids = ids
                    pagina += 1
                    time.sleep(1)  # No abuses del server

    print("✅ Scraping completado.")
