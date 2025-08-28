# 🗺️ MAPA INTERACTIVO IA SINDICAL - VERSIÓN MEJORADA COMPLETA
# FECHA: 28 Agosto 2025 - SOLUCIÓN 3 PROBLEMAS
# MEJORAS: Popups profesionales + Bounds limitados + Escalabilidad mundial

import pandas as pd
import folium
from folium.plugins import MarkerCluster
import requests
import json
import os

print("🚀 INICIANDO MAPA IA SINDICAL - VERSIÓN MEJORADA COMPLETA")
print("=" * 60)

# 🔑 CONFIGURACIÓN API AIRTABLE (desde GitHub Secrets)
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TOKEN = os.environ.get('AIRTABLE_TOKEN')
AIRTABLE_TABLE_NAME = "Casos IA Sindical"

# 🌍 COORDENADAS MUNDIALES PARA ESCALABILIDAD
COORDENADAS_PAISES = {
    # América del Sur
    'Argentina': [-34.6118, -58.3960],
    'Chile': [-33.4489, -70.6693],
    'Brasil': [-15.7975, -47.8919],
    'Colombia': [4.7110, -74.0721],
    'Perú': [-12.0464, -77.0428],
    'Uruguay': [-34.9011, -56.1645],
    
    # Europa
    'España': [40.4168, -3.7038],
    'Francia': [48.8566, 2.3522],
    'Alemania': [52.5200, 13.4050],
    'Reino Unido': [51.5074, -0.1278],
    'Italia': [41.9028, 12.4964],
    
    # América del Norte
    'Estados Unidos': [38.9072, -77.0369],
    'Canadá': [45.4215, -75.6972],
    'México': [19.4326, -99.1332],
    
    # Asia
    'China': [39.9042, 116.4074],
    'Japón': [35.6762, 139.6503],
    'India': [28.6139, 77.2090],
    
    # Casos especiales
    'Global': [20.0, 0.0],
    'Internacional': [0.0, 0.0]
}

# 📊 FUNCIÓN OBTENER DATOS
def get_casos_ia_sindical():
    """Obtener todos los casos desde Airtable"""
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
                
                # Obtener coordenadas (desde Airtable o diccionario)
                lat = fields.get('Latitud')
                lon = fields.get('Longitud')
                pais = fields.get('País', 'No especificado')
                
                # Si no hay coordenadas en Airtable, usar diccionario
                if not lat or not lon:
                    if pais in COORDENADAS_PAISES:
                        lat, lon = COORDENADAS_PAISES[pais]
                        print(f"📍 Coordenadas automáticas para {pais}: ({lat}, {lon})")
                
                caso = {
                    'ID': record['id'],
                    'Titulo': fields.get('Título', 'Sin título'),
                    'País': pais,
                    'Latitud': lat,
                    'Longitud': lon,
                    'Organización_Sindical': fields.get('Organización Sindical', 'No especificada'),
                    'Tipo_IA': fields.get('Tipo IA', 'No especificado'),
                    'Descripción': fields.get('Descripción', 'Sin descripción'),
                    'URL': fields.get('URL', ''),
                    'Contacto': fields.get('Contacto', 'No disponible'),
                    'Fecha': fields.get('Fecha', 'No especificada')
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

# 🗺️ FUNCIÓN CREAR MAPA OPTIMIZADO
def create_optimized_map(df):
    """Crear mapa optimizado sin continentes repetidos"""
    
    print("🗺️ Creando mapa con bounds optimizados...")
    
    # Filtrar casos con coordenadas válidas
    df_valid = df.dropna(subset=['Latitud', 'Longitud'])
    
    if len(df_valid) == 0:
        print("❌ No hay casos con coordenadas válidas")
        return None
    
    # SOLUCIÓN PROBLEMA 2: BOUNDS LIMITADOS (sin continentes repetidos)
    mapa = folium.Map(
        location=[0, 0],  # Centro mundial
        zoom_start=2,
        tiles='OpenStreetMap',
        max_bounds=True,    # ← CRÍTICO: Evita continentes repetidos
        min_zoom=1,
        max_zoom=18
    )
    
    # Configurar bounds estrictos
    mapa.fit_bounds([[-60, -180], [70, 180]], padding=(20, 20))
    
    print(f"📍 Procesando {len(df_valid)} casos con coordenadas...")
    
    # Agregar marcadores
    for index, row in df_valid.iterrows():
        if pd.notna(row['Latitud']) and pd.notna(row['Longitud']):
            
            # SOLUCIÓN PROBLEMA 1: POPUP PROFESIONAL COMPLETO
            popup_html = f"""
            <div style="width: 320px; font-family: Arial, sans-serif;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           color: white; padding: 15px; margin: -10px -10px 10px -10px; 
                           border-radius: 8px 8px 0 0;">
                    <h3 style="margin: 0; font-size: 16px; font-weight: bold;">
                        {row['Titulo']}
                    </h3>
                </div>
                
                <div style="padding: 10px;">
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>🌍 País:</strong> {row['País']}
                    </p>
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>🏢 Organización:</strong> {row['Organización_Sindical']}
                    </p>
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>🤖 Tipo IA:</strong> {row['Tipo_IA']}
                    </p>
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>📅 Fecha:</strong> {row['Fecha']}
                    </p>
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>📧 Contacto:</strong> {row['Contacto']}
                    </p>
            """
            
            # Agregar URL si existe
            if row['URL'] and row['URL'].strip():
                popup_html += f"""
                    <p style="margin: 8px 0; font-size: 14px;">
                        <strong>🔗 Más información:</strong> 
                        <a href="{row['URL']}" target="_blank" style="color: #667eea; text-decoration: none;">
                            Ver detalles →
                        </a>
                    </p>
                """
            
            popup_html += """
                </div>
            </div>
            """
            
            # Color por tipo de IA
            colores_tipo = {
                'Machine Learning': '#e74c3c',
                'Inteligencia Artificial': '#3498db',
                'Automatización': '#f39c12',
                'Análisis de Datos': '#27ae60',
                'Chatbots': '#9b59b6'
            }
            
            color = colores_tipo.get(row['Tipo_IA'], '#95a5a6')
            
            # Agregar marcador
            folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"{row['Titulo']} - {row['País']}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
    
    print("✅ MAPA CREADO EXITOSAMENTE")
    print(f"   ✅ Popups profesionales: Formato completo")
    print(f"   ✅ Bounds limitados: Sin continentes repetidos")
    print(f"   ✅ Escalabilidad mundial: {len(COORDENADAS_PAISES)} países disponibles")
    
    return mapa

# 🚀 PROCESO PRINCIPAL
if __name__ == "__main__":
    # Obtener datos
    df = get_casos_ia_sindical()
    
    if not df.empty:
        # Crear mapa mejorado
        mapa = create_optimized_map(df)
        
        if mapa:
            # Guardar mapa
            nombre_archivo = 'index.html'  # ← IMPORTANTE: index.html para GitHub Pages
            mapa.save(nombre_archivo)
            print(f"💾 MAPA GUARDADO: {nombre_archivo}")
            print("🎯 LISTO PARA SUBIR A GITHUB Y ACTUALIZAR GAMMA")
            print("🌐 MEJORAS IMPLEMENTADAS:")
            print("   1. ✅ Popups profesionales con diseño completo")
            print("   2. ✅ Bounds limitados (sin continentes repetidos)")
            print("   3. ✅ Escalabilidad mundial (preparado para nuevos países)")
        else:
            print("❌ Error creando mapa")
    else:
        print("❌ No se pudieron obtener datos")
