import os
import folium
import pandas as pd
import requests

# Variables de entorno (secrets)
AIRTABLE_TOKEN = os.environ['AIRTABLE_TOKEN']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']

def get_casos_ia_sindical():
    """Obtener todos los casos desde Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Casos%20IA%20Sindical"
    
    headers = {
        'Authorization': f'Bearer {AIRTABLE_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("🔗 CONECTANDO CON AIRTABLE...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            print(f"✅ {len(records)} casos obtenidos exitosamente")
            return records
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return []

def create_interactive_map(records):
    """Crear mapa interactivo con casos IA sindical"""
    if not records:
        print("❌ No hay datos para crear el mapa")
        return None
    
    # Crear DataFrame
    casos_data = []
    for record in records:
        fields = record.get('fields', {})
        casos_data.append({
            'Titulo': fields.get('Título del Caso', 'Sin título'),
            'Pais': fields.get('País', 'No especificado'),
            'Organizacion': fields.get('Organización Sindical', 'No especificado'),
            'Tipo_IA': fields.get('Tipo de IA', 'No especificado'),
            'Latitud': fields.get('Latitud', 0),
            'Longitud': fields.get('Longitud', 0),
            'Estado': fields.get('Estado', 'No especificado')
        })
    
    df = pd.DataFrame(casos_data)
    print(f"📊 DataFrame creado con {len(df)} casos")
    
    # Crear mapa centrado
    center_lat = df['Latitud'].mean()
    center_lon = df['Longitud'].mean()
    
    mapa = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=3,
        tiles='OpenStreetMap'
    )
    
    # Colores por tipo de IA
    colores_ia = {
        'Machine Learning': 'blue',
        'Procesamiento de Lenguaje Natural': 'green',
        'Análisis Predictivo': 'red',
        'Automatización': 'purple',
        'Otros': 'orange'
    }
    
    # Agregar marcadores
    for _, caso in df.iterrows():
        if caso['Latitud'] != 0 and caso['Longitud'] != 0:
            color = colores_ia.get(caso['Tipo_IA'], 'gray')
            
            popup_html = f"""
            <div style="width: 300px; font-family: Arial;">
                <h3 style="color: #2E86AB; margin-bottom: 10px;">{caso['Titulo']}</h3>
                <div style="background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px;">
                    <strong>🌍 País:</strong> {caso['Pais']}<br>
                    <strong>🏢 Organización:</strong> {caso['Organizacion']}<br>
                    <strong>🤖 Tipo IA:</strong> {caso['Tipo_IA']}<br>
                    <strong>📊 Estado:</strong> {caso['Estado']}
                </div>
            </div>
            """
            
            folium.Marker(
                location=[caso['Latitud'], caso['Longitud']],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=caso['Titulo'],
                icon=folium.Icon(color=color, icon='cog', prefix='fa')
            ).add_to(mapa)
    
    print("🗺️ Mapa creado exitosamente")
    return mapa

def main():
    print("🚀 INICIANDO GENERACIÓN AUTOMÁTICA MAPA IA SINDICAL")
    print("=" * 60)
    
    # Obtener datos
    records = get_casos_ia_sindical()
    
    if records:
        # Crear mapa
        mapa = create_interactive_map(records)
        
        if mapa:
            # Guardar como index.html
            mapa.save('index.html')
            print("✅ index.html generado exitosamente")
            print("🌐 Disponible en GitHub Pages automáticamente")
        else:
            print("❌ Error creando el mapa")
    else:
        print("❌ No se pudieron obtener datos de Airtable")

if __name__ == "__main__":
    main()
