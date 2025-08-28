import os
import folium
import pandas as pd
import requests
import json

# Variables de entorno (secrets)
AIRTABLE_TOKEN = os.environ['AIRTABLE_TOKEN']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']

def obtener_datos_airtable():
    """Obtener datos de Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Casos%20IA%20Sindical"
    headers = {
        'Authorization': f'Bearer {AIRTABLE_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        casos = []
        for record in data.get('records', []):
            fields = record.get('fields', {})
            casos.append(fields)
        
        return casos
    except Exception as e:
        print(f"Error obteniendo datos: {e}")
        return []

def crear_mapa_interactivo(casos):
    """Crear mapa con marcadores interactivos"""
    if not casos:
        print("No hay casos para procesar")
        return None
    
    # Calcular centro del mapa
    lats = [caso.get('Latitud') for caso in casos if caso.get('Latitud')]
    lons = [caso.get('Longitud') for caso in casos if caso.get('Longitud')]
    
    if lats and lons:
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
    else:
        center_lat, center_lon = 20, 0
    
    # Crear mapa
    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=3,
        tiles='OpenStreetMap'
    )
    
    # Colores por tipo de IA
    colores_tipo = {
        'Machine Learning': 'blue',
        'Inteligencia Artificial': 'red',
        'Automatización': 'green',
        'Algoritmos': 'orange',
        'default': 'gray'
    }
    
    # Agregar marcadores
    for caso in casos:
        lat = caso.get('Latitud')
        lon = caso.get('Longitud')
        
        if lat and lon:
            titulo = caso.get('Título del Caso', 'Sin título')
            pais = caso.get('País', 'No especificado')
            organizacion = caso.get('Organización Sindical', 'No especificada')
            tipo_ia = caso.get('Tipo de IA', 'No especificado')
            
            color = colores_tipo.get(tipo_ia, colores_tipo['default'])
            
            # Crear popup
            popup_html = f"""
            <div style="width: 300px; font-family: Arial;">
                <h3 style="color: #2E86AB; margin-bottom: 10px;">{titulo}</h3>
                <div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
                    <strong>🌍 País:</strong> {pais}<br>
                    <strong>🏢 Organización:</strong> {organizacion}<br>
                    <strong>🤖 Tipo IA:</strong> {tipo_ia}
                </div>
            </div>
            """
            
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=titulo,
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(mapa)
    
    return mapa

def main():
    """Función principal"""
    print("🚀 Iniciando generación del mapa...")
    
    # Obtener datos
    print("📊 Obteniendo datos de Airtable...")
    casos = obtener_datos_airtable()
    print(f"✅ {len(casos)} casos obtenidos")
    
    # Crear mapa
    print("🗺️ Creando mapa interactivo...")
    mapa = crear_mapa_interactivo(casos)
    
    if mapa:
        # Guardar como index.html
        print("💾 Guardando mapa como index.html...")
        mapa.save('index.html')
        print("✅ Mapa generado exitosamente: index.html")
    else:
        print("❌ Error generando el mapa")

if __name__ == "__main__":
    main()
