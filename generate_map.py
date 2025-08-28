# 🗺️ MAPA INTERACTIVO IA SINDICAL - POPUP FORMATO EXACTO ACORDADO
# FECHA: 28 Agosto 2025 - CORRECCIÓN POPUP ESPECÍFICO
# CAMBIO: Popup formato exacto según especificaciones usuario

import pandas as pd
import folium
import requests
import os

print("🚀 INICIANDO MAPA IA SINDICAL - POPUP FORMATO EXACTO")
print("=" * 60)

# 🔑 CONFIGURACIÓN API AIRTABLE
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TOKEN = os.environ.get('AIRTABLE_TOKEN')
AIRTABLE_TABLE_NAME = "Casos IA Sindical"

# 🌍 COORDENADAS MUNDIALES
COORDENADAS_PAISES = {
    'Argentina': [-34.6118, -58.3960],
    'Chile': [-33.4489, -70.6693],
    'Brasil': [-15.7975, -47.8919],
    'Colombia': [4.7110, -74.0721],
    'Perú': [-12.0464, -77.0428],
    'Uruguay': [-34.9011, -56.1645],
    'España': [40.4168, -3.7038],
    'Francia': [48.8566, 2.3522],
    'Alemania': [52.5200, 13.4050],
    'Reino Unido': [51.5074, -0.1278],
    'Italia': [41.9028, 12.4964],
    'Estados Unidos': [38.9072, -77.0369],
    'Canadá': [45.4215, -75.6972],
    'México': [19.4326, -99.1332],
    'Global': [20.0, 0.0],
    'Internacional': [0.0, 0.0]
}

def get_casos_ia_sindical():
    """Obtener casos desde Airtable"""
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
    
    headers = {
        'Authorization': f'Bearer {AIRTABLE_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("🔗 CONECTANDO CON AIRTABLE...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            casos = []
            
            for record in data['records']:
                fields = record['fields']
                
                # Obtener coordenadas
                lat = fields.get('Latitud')
                lon = fields.get('Longitud')
                pais = fields.get('País', 'No especificado')
                
                # Si no hay coordenadas, usar diccionario
                if not lat or not lon:
                    if pais in COORDENADAS_PAISES:
                        lat, lon = COORDENADAS_PAISES[pais]
                
                caso = {
                    'ID': record['id'],
                    'Titulo': fields.get('Título', 'Sin título'),
                    'País': pais,
                    'Latitud': lat,
                    'Longitud': lon,
                    'Organización_Sindical': fields.get('Organización Sindical', 'No especificada'),
                    'Tipo_IA': fields.get('Tipo IA', 'No especificado'),
                    'Estado': fields.get('Estado del Caso', 'No especificado'),
                    'Fuente': fields.get('Fuente', 'No especificada'),
                    'Actores': fields.get('Actores Involucrados', 'No especificados'),
                    'Descripción': fields.get('Descripción', 'Sin descripción disponible'),
                    'URL': fields.get('URL', '')
                }
                casos.append(caso)
            
            print(f"✅ CONEXIÓN EXITOSA: {len(casos)} casos encontrados")
            return pd.DataFrame(casos)
            
        else:
            print(f"❌ ERROR API: {response.status_code}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ ERROR CONEXIÓN: {e}")
        return pd.DataFrame()

def create_map_with_exact_popup_format(df):
    """Crear mapa con popup formato exacto acordado"""
    
    print("🗺️ Creando mapa con popup formato exacto acordado...")
    
    # Filtrar casos válidos
    df_valid = df.dropna(subset=['Latitud', 'Longitud'])
    
    if len(df_valid) == 0:
        print("❌ No hay casos con coordenadas válidas")
        return None
    
    # Crear mapa
    mapa = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles='OpenStreetMap',
        max_bounds=True,
        min_zoom=1,
        max_zoom=18
    )
    
    # Bounds limitados
    mapa.fit_bounds([[-60, -180], [70, 180]], padding=(20, 20))
    
    print(f"📍 Procesando {len(df_valid)} casos con popup formato exacto...")
    
    # Agregar marcadores con popup formato exacto
    for index, row in df_valid.iterrows():
        if pd.notna(row['Latitud']) and pd.notna(row['Longitud']):
            
            # POPUP FORMATO EXACTO ACORDADO
            popup_html = f"""
            <div style="width: 350px; font-family: 'Courier New', monospace; 
                       background: white; border: 2px solid #333; padding: 0; border-radius: 5px;">
                
                <!-- TÍTULO CON BORDE -->
                <div style="background: #f0f0f0; padding: 10px; border-bottom: 1px solid #333; 
                           font-weight: bold; text-align: center; border-radius: 3px 3px 0 0;">
                    Caso IA Sindical - {row['País']}
                </div>
                
                <!-- CONTENIDO PRINCIPAL -->
                <div style="padding: 12px; font-size: 13px; line-height: 1.5;">
                    <div style="margin-bottom: 4px;">🏢 <strong>Organización:</strong> {row['Organización_Sindical']}</div>
                    <div style="margin-bottom: 4px;">🤖 <strong>Tipo IA:</strong> {row['Tipo_IA']}</div>
                    <div style="margin-bottom: 4px;">📊 <strong>Estado:</strong> {row['Estado']}</div>
                    <div style="margin-bottom: 4px;">📄 <strong>Fuente:</strong> {row['Fuente']}</div>
                    <div style="margin-bottom: 8px;">👥 <strong>Actores:</strong> {row['Actores']}</div>
                    
                    <!-- SEPARADOR -->
                    <div style="border-top: 1px solid #ccc; margin: 10px 0;"></div>
                    
                    <!-- DESCRIPCIÓN -->
                    <div style="margin-bottom: 10px;">
                        <div style="margin-bottom: 5px;"><strong>📝 Descripción:</strong></div>
                        <div style="font-size: 12px; color: #555; line-height: 1.4; text-align: justify;">
                            {row['Descripción'][:200]}{'...' if len(str(row['Descripción'])) > 200 else ''}
                        </div>
                    </div>
                    
                    <!-- URL SI EXISTE -->
                    {f'<div style="text-align: center; margin-top: 8px;"><a href="{row["URL"]}" target="_blank" style="color: #0066cc; text-decoration: none; font-weight: bold;">🔗 Ver más información</a></div>' if row['URL'] and str(row['URL']).strip() else ''}
                </div>
            </div>
            """
            
            # Agregar marcador
            folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=folium.Popup(popup_html, max_width=370),
                tooltip=f"{row['Titulo']} - {row['País']}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
    
    print("✅ MAPA CREADO CON POPUP FORMATO EXACTO")
    return mapa

# 🚀 PROCESO PRINCIPAL
if __name__ == "__main__":
    df = get_casos_ia_sindical()
    
    if not df.empty:
        mapa = create_map_with_exact_popup_format(df)
        
        if mapa:
            nombre_archivo = 'index.html'
            mapa.save(nombre_archivo)
            print(f"💾 MAPA GUARDADO: {nombre_archivo}")
            print("🎯 POPUP FORMATO EXACTO IMPLEMENTADO SEGÚN ACORDADO")
        else:
            print("❌ Error creando mapa")
    else:
        print("❌ No se pudieron obtener datos")
