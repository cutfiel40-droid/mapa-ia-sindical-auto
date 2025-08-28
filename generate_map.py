# 🗺️ MAPA INTERACTIVO IA SINDICAL - SOLUCIÓN CONTINENTES + DESCRIPCIÓN COMPLETA
# FECHA: 28 Agosto 2025 - CORRECCIÓN BOUNDS + TEXTO COMPLETO
# MEJORAS: Sin continentes repetidos + Descripción completa visible

import pandas as pd
import folium
import requests
import os
import json  # ← Agregar esta línea después de "import os"


print("🚀 INICIANDO MAPA IA SINDICAL - SOLUCIÓN BOUNDS + DESCRIPCIÓN")
print("=" * 65)

# 🔑 CONFIGURACIÓN API AIRTABLE
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TOKEN = os.environ.get('AIRTABLE_TOKEN')
AIRTABLE_TABLE_NAME = "Casos IA Sindical"

# 🌍 COORDENADAS MUNDIALES
COORDENADAS_PAISES = {
    # EUROPA
    'España': [40.4168, -3.7038],
    'Francia': [46.6034, 1.8883],
    'Alemania': [51.1657, 10.4515],
    'Reino Unido': [55.3781, -3.4360],
    'Italia': [41.8719, 12.5674],
    'Portugal': [39.3999, -8.2245],
    'Países Bajos': [52.1326, 5.2913],
    'Bélgica': [50.5039, 4.4699],
    'Suiza': [46.8182, 8.2275],
    'Austria': [47.5162, 14.5501],
    'Suecia': [60.1282, 18.6435],
    'Noruega': [60.4720, 8.4689],
    'Dinamarca': [56.2639, 9.5018],
    'Finlandia': [61.9241, 25.7482],
    'Islandia': [64.9631, -19.0208],
    'Irlanda': [53.1424, -7.6921],
    'Polonia': [51.9194, 19.1451],
    'República Checa': [49.8175, 15.4730],
    'Eslovaquia': [48.6690, 19.6990],
    'Hungría': [47.1625, 19.5033],
    'Rumania': [45.9432, 24.9668],
    'Bulgaria': [42.7339, 25.4858],
    'Grecia': [39.0742, 21.8243],
    'Croacia': [45.1000, 15.2000],
    'Serbia': [44.0165, 21.0059],
    'Eslovenia': [46.1512, 14.9955],
    'Bosnia y Herzegovina': [43.9159, 17.6791],
    'Montenegro': [42.7087, 19.3744],
    'Albania': [41.1533, 20.1683],
    'Macedonia del Norte': [41.6086, 21.7453],
    'Estonia': [58.5953, 25.0136],
    'Letonia': [56.8796, 24.6032],
    'Lituania': [55.1694, 23.8813],
    'Ucrania': [48.3794, 31.1656],
    'Bielorrusia': [53.7098, 27.9534],
    'Moldavia': [47.4116, 28.3699],
    'Rusia': [61.5240, 105.3188],
    
    # AMÉRICA DEL NORTE
    'Estados Unidos': [37.0902, -95.7129],
    'Canadá': [56.1304, -106.3468],
    'México': [23.6345, -102.5528],
    'Guatemala': [15.7835, -90.2308],
    'Belice': [17.1899, -88.4976],
    'Honduras': [15.2000, -86.2419],
    'El Salvador': [13.7942, -88.8965],
    'Nicaragua': [12.2650, -85.2072],
    'Costa Rica': [9.7489, -83.7534],
    'Panamá': [8.5380, -80.7821],
    
    # AMÉRICA DEL SUR
    'Brasil': [-14.2350, -51.9253],
    'Argentina': [-38.4161, -63.6167],
    'Chile': [-35.6751, -71.5430],
    'Colombia': [4.5709, -74.2973],
    'Perú': [-9.1900, -75.0152],
    'Venezuela': [6.4238, -66.5897],
    'Ecuador': [-1.8312, -78.1834],
    'Bolivia': [-16.2902, -63.5887],
    'Paraguay': [-23.4425, -58.4438],
    'Uruguay': [-32.5228, -55.7658],
    'Guyana': [4.8604, -58.9302],
    'Suriname': [3.9193, -56.0278],
    'Guyana Francesa': [3.9339, -53.1258],
    
    # ASIA
    'China': [35.8617, 104.1954],
    'India': [20.5937, 78.9629],
    'Japón': [36.2048, 138.2529],
    'Corea del Sur': [35.9078, 127.7669],
    'Corea del Norte': [40.3399, 127.5101],
    'Indonesia': [-0.7893, 113.9213],
    'Tailandia': [15.8700, 100.9925],
    'Vietnam': [14.0583, 108.2772],
    'Filipinas': [12.8797, 121.7740],
    'Malasia': [4.2105, 101.9758],
    'Singapur': [1.3521, 103.8198],
    'Brunéi': [4.5353, 114.7277],
    'Myanmar': [21.9162, 95.9560],
    'Camboya': [12.5657, 104.9910],
    'Laos': [19.8563, 102.4955],
    'Mongolia': [46.8625, 103.8467],
    'Kazajistán': [48.0196, 66.9237],
    'Uzbekistán': [41.3775, 64.5853],
    'Kirguistán': [41.2044, 74.7661],
    'Tayikistán': [38.8610, 71.2761],
    'Turkmenistán': [38.9697, 59.5563],
    'Afganistán': [33.9391, 67.7100],
    'Pakistán': [30.3753, 69.3451],
    'Bangladesh': [23.6850, 90.3563],
    'Sri Lanka': [7.8731, 80.7718],
    'Maldivas': [3.2028, 73.2207],
    'Nepal': [28.3949, 84.1240],
    'Bután': [27.5142, 90.4336],
    'Irán': [32.4279, 53.6880],
    'Irak': [33.2232, 43.6793],
    'Siria': [34.8021, 38.9968],
    'Turquía': [38.9637, 35.2433],
    'Armenia': [40.0691, 45.0382],
    'Georgia': [42.3154, 43.3569],
    'Azerbaiyán': [40.1431, 47.5769],
    'Israel': [31.0461, 34.8516],
    'Palestina': [31.9522, 35.2332],
    'Jordania': [30.5852, 36.2384],
    'Líbano': [33.8547, 35.8623],
    'Kuwait': [29.3117, 47.4818],
    'Arabia Saudí': [23.8859, 45.0792],
    'Emiratos Árabes Unidos': [23.4241, 53.8478],
    'Qatar': [25.3548, 51.1839],
    'Baréin': [25.9304, 50.6378],
    'Omán': [21.4735, 55.9754],
    'Yemen': [15.5527, 48.5164],
    
    # ÁFRICA
    'Sudáfrica': [-30.5595, 22.9375],
    'Nigeria': [9.0820, 8.6753],
    'Egipto': [26.0975, 30.0444],
    'Kenia': [-0.0236, 37.9062],
    'Etiopía': [9.1450, 40.4897],
    'Ghana': [7.9465, -1.0232],
    'Marruecos': [31.7917, -7.0926],
    'Argelia': [28.0339, 1.6596],
    'Túnez': [33.8869, 9.5375],
    'Libia': [26.3351, 17.2283],
    'Sudán': [12.8628, 30.2176],
    'Chad': [15.4542, 18.7322],
    'Níger': [17.6078, 8.0817],
    'Mali': [17.5707, -3.9962],
    'Burkina Faso': [12.2383, -1.5616],
    'Senegal': [14.4974, -14.4524],
    'Guinea': [9.9456, -9.6966],
    'Sierra Leona': [8.4606, -11.7799],
    'Liberia': [6.4281, -9.4295],
    'Costa de Marfil': [7.5400, -5.5471],
    'Camerún': [7.3697, 12.3547],
    'República Centroafricana': [6.6111, 20.9394],
    'República Democrática del Congo': [-4.0383, 21.7587],
    'República del Congo': [-0.2280, 15.8277],
    'Gabón': [-0.8037, 11.6094],
    'Guinea Ecuatorial': [1.6508, 10.2679],
    'Santo Tomé y Príncipe': [0.1864, 6.6131],
    'Angola': [-11.2027, 17.8739],
    'Zambia': [-13.1339, 27.8493],
    'Zimbabue': [-19.0154, 29.1549],
    'Botswana': [-22.3285, 24.6849],
    'Namibia': [-22.9576, 18.4904],
    'Tanzania': [-6.3690, 34.8888],
    'Uganda': [1.3733, 32.2903],
    'Ruanda': [-1.9403, 29.8739],
    'Burundi': [-3.3731, 29.9189],
    'Mozambique': [-18.6657, 35.5296],
    'Madagascar': [-18.7669, 46.8691],
    'Mauricio': [-20.3484, 57.5522],
    'Seychelles': [-4.6796, 55.4920],
    'Comoras': [-11.6455, 43.3333],
    'Yibuti': [11.8251, 42.5903],
    'Somalia': [5.1521, 46.1996],
    'Eritrea': [15.1794, 39.7823],
    
    # OCEANÍA
    'Australia': [-25.2744, 133.7751],
    'Nueva Zelanda': [-40.9006, 174.8860],
    'Papúa Nueva Guinea': [-6.3150, 143.9555],
    'Fiji': [-16.5780, 179.4144],
    'Vanuatu': [-15.3767, 166.9592],
    'Samoa': [-13.7590, -172.1046],
    'Tonga': [-21.1789, -175.1982],
    'Kiribati': [-3.3704, -168.7340],
    'Tuvalu': [-7.1095, 177.6493],
    'Nauru': [-0.5228, 166.9315],
    'Palau': [7.5150, 134.5825],
    'Islas Marshall': [7.1315, 171.1845],
    'Micronesia': [7.4256, 150.5508],
    'Islas Salomón': [-9.6457, 160.1562],
    
    # CASOS ESPECIALES/REGIONES
    'Global': [20.0, 0.0],
    'Internacional': [0.0, 0.0],
    'Multinacional': [30.0, 0.0],
    'Varios países': [40.0, 10.0],
    'Unión Europea': [50.1109, 9.2522],
    'No especificado': [0.0, 0.0]
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
                    'Titulo': fields.get('Título del Caso', 'Sin título'),
                    'País': pais,
                    'Latitud': lat,
                    'Longitud': lon,
                    'Organización_Sindical': fields.get('Organización Sindical', 'No especificada'),
                    'Tipo_IA': fields.get('Tipo de IA', 'No especificado'),
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

def aplicar_offset_automatico(df):
    """Sistema para separar casos del mismo país"""
    if df.empty:
        return df
        
    # ✅ CORRECCIÓN: Convertir DataFrame a lista de diccionarios
    casos = df.to_dict('records')     
    
    # Agrupar casos por país
    casos_por_pais = {}
    for caso in casos:
        pais = caso.get('País', 'Desconocido')
        if pais not in casos_por_pais:
            casos_por_pais[pais] = []
        casos_por_pais[pais].append(caso)
    
    casos_con_offset = []
    
    for pais, casos_pais in casos_por_pais.items():
        if len(casos_pais) == 1:
            # Un solo caso - mantener igual
            casos_con_offset.extend(casos_pais)
        else:
            # Múltiples casos - separar un poco
            for i, caso in enumerate(casos_pais):
                if i == 0:
                    casos_con_offset.append(caso)
                else:
                    caso_nuevo = caso.copy()
                    caso_nuevo['Latitud'] = caso_nuevo.get('Latitud', 0) + (0.1 * i)
                    caso_nuevo['Longitud'] = caso_nuevo.get('Longitud', 0) + (0.05 * i)
                    casos_con_offset.append(caso_nuevo)
    
      # Convertir de vuelta a DataFrame
    return pd.DataFrame(casos_con_offset)

def create_fixed_map(df):
    """Crear mapa SIN continentes repetidos + descripción completa"""
    
    print("🗺️ Creando mapa con BOUNDS LIMITADOS + DESCRIPCIÓN COMPLETA...")
    
    # Filtrar casos válidos
    df_valid = df.dropna(subset=['Latitud', 'Longitud'])
    
    if len(df_valid) == 0:
        print("❌ No hay casos con coordenadas válidas")
        return None
    
    # SOLUCIÓN CONTINENTES REPETIDOS: BOUNDS ESTRICTOS
    mapa = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles='OpenStreetMap',
        # CRÍTICO: Configuración que evita continentes repetidos
        world_copy_jump=False,  # ← CLAVE: Evita saltos mundiales
        no_wrap=True,           # ← CLAVE: No permite wrap horizontal
        min_zoom=2,             # ← Zoom mínimo para evitar over-zoom out
        max_zoom=15,
        max_bounds=True
    )
    
    # Configurar bounds mundiales estrictos (sin repetición)
    southwest = [-60, -180]  # Límite suroeste
    northeast = [85, 180]    # Límite noreste
    mapa.fit_bounds([southwest, northeast], padding=(10, 10))
    
    print(f"📍 Procesando {len(df_valid)} casos...")
    
    # Agregar marcadores con DESCRIPCIÓN COMPLETA
    for index, row in df_valid.iterrows():
        if pd.notna(row['Latitud']) and pd.notna(row['Longitud']):
            
            # POPUP FORMATO EXACTO + DESCRIPCIÓN COMPLETA
            popup_html = f"""
            <div style="width: 380px; font-family: 'Courier New', monospace; 
                       background: white; border: 2px solid #333; padding: 0; border-radius: 5px;">
                
                <!-- TÍTULO -->
                <div style="background: #f0f0f0; padding: 10px; border-bottom: 1px solid #333; 
                           font-weight: bold; text-align: center; border-radius: 3px 3px 0 0;">
                    Caso IA Sindical - {row['País']}
                </div>
                
                <!-- CONTENIDO -->
                <div style="padding: 12px; font-size: 13px; line-height: 1.5;">
                    <div style="margin-bottom: 4px;">🏢 <strong>Organización:</strong> {row['Organización_Sindical']}</div>
                    <div style="margin-bottom: 4px;">🤖 <strong>Tipo IA:</strong> {row['Tipo_IA']}</div>
                    <div style="margin-bottom: 4px;">📊 <strong>Estado:</strong> {row['Estado']}</div>
                    <div style="margin-bottom: 4px;">📄 <strong>Fuente:</strong> {row['Fuente']}</div>
                    <div style="margin-bottom: 8px;">👥 <strong>Actores:</strong> {row['Actores']}</div>
                    
                    <!-- SEPARADOR -->
                    <div style="border-top: 1px solid #ccc; margin: 10px 0;"></div>
                    
                    <!-- DESCRIPCIÓN COMPLETA (SIN LÍMITE) -->
                    <div style="margin-bottom: 10px;">
                        <div style="margin-bottom: 5px;"><strong>📝 Descripción:</strong></div>
                        <div style="font-size: 12px; color: #555; line-height: 1.4; text-align: justify; 
                                   max-height: 150px; overflow-y: auto; padding-right: 5px;">
                            {str(row['Descripción'])}
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
                popup=folium.Popup(popup_html, max_width=400),
                tooltip=f"{row['Titulo']} - {row['País']}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
    
    print("✅ MAPA CREADO CON CORRECCIONES:")
    print("   ✅ BOUNDS LIMITADOS: Sin continentes repetidos")
    print("   ✅ DESCRIPCIÓN COMPLETA: Texto completo visible con scroll")
    print("   ✅ POPUP FORMATO EXACTO: Según especificaciones")
    
    return mapa
def crear_filtros_html():
    """Generar HTML para filtros temáticos"""
    return """
    <div id="filtros-panel" style="position: fixed; top: 10px; left: 10px; 
                                   background: white; border: 2px solid #333; 
                                   border-radius: 10px; padding: 15px; z-index: 1000; 
                                   width: 280px; max-height: 500px; overflow-y: auto;
                                   box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h3 style="margin: 0 0 15px 0; color: #333; text-align: center;">🔍 Filtros Temáticos</h3>
        
        <!-- Filtro por País -->
        <div style="margin-bottom: 12px;">
            <label style="font-weight: bold; color: #555;">🌍 País:</label>
            <select id="filtro-pais" onchange="aplicarFiltros()" style="width: 100%; padding: 5px; margin-top: 3px;">
                <option value="">Todos los países</option>
            </select>
        </div>
        
        <!-- Filtro por Tipo IA -->
        <div style="margin-bottom: 12px;">
            <label style="font-weight: bold; color: #555;">🤖 Tipo de IA:</label>
            <select id="filtro-tipo-ia" onchange="aplicarFiltros()" style="width: 100%; padding: 5px; margin-top: 3px;">
                <option value="">Todos los tipos</option>
            </select>
        </div>
        
        <!-- Filtro por Estado -->
        <div style="margin-bottom: 12px;">
            <label style="font-weight: bold; color: #555;">📊 Estado:</label>
            <select id="filtro-estado" onchange="aplicarFiltros()" style="width: 100%; padding: 5px; margin-top: 3px;">
                <option value="">Todos los estados</option>
            </select>
        </div>
        
        <!-- Filtro por Organización -->
        <div style="margin-bottom: 15px;">
            <label style="font-weight: bold; color: #555;">🏢 Organización:</label>
            <select id="filtro-organizacion" onchange="aplicarFiltros()" style="width: 100%; padding: 5px; margin-top: 3px;">
                <option value="">Todas las organizaciones</option>
            </select>
        </div>
        
        <!-- Botón Limpiar -->
        <button onclick="limpiarFiltros()" style="width: 100%; padding: 8px; background: #f0f0f0; 
                                                   border: 1px solid #ccc; border-radius: 5px; 
                                                   cursor: pointer; font-weight: bold;">
            🔄 Limpiar Filtros
        </button>
        
        <!-- Contador casos visibles -->
        <div id="contador-casos" style="text-align: center; margin-top: 10px; 
                                       font-size: 12px; color: #666; font-weight: bold;">
            Mostrando: 0 casos
        </div>
    </div>
    
    <script>
    // Variables globales
    let todosLosMarcadores = [];
    let mapaGlobal = null;
    
    // Función para inicializar filtros
    function inicializarFiltros(casos, mapa) {
        mapaGlobal = mapa;
        
        // Extraer valores únicos para cada filtro
        const paises = [...new Set(casos.map(c => c.pais))].sort();
        const tiposIA = [...new Set(casos.map(c => c.tipo_ia))].sort();
        const estados = [...new Set(casos.map(c => c.estado))].sort();
        const organizaciones = [...new Set(casos.map(c => c.organizacion))].sort();
        
        // Poblar selectores
        poblarSelector('filtro-pais', paises);
        poblarSelector('filtro-tipo-ia', tiposIA);
        poblarSelector('filtro-estado', estados);
        poblarSelector('filtro-organizacion', organizaciones);
        
        // Actualizar contador inicial
        actualizarContador(casos.length);
    }
    
    function poblarSelector(idSelector, valores) {
        const selector = document.getElementById(idSelector);
        valores.forEach(valor => {
            if (valor && valor.trim() !== '') {
                const option = document.createElement('option');
                option.value = valor;
                option.textContent = valor;
                selector.appendChild(option);
            }
        });
    }
    
    function aplicarFiltros() {
        const filtroPais = document.getElementById('filtro-pais').value;
        const filtroTipoIA = document.getElementById('filtro-tipo-ia').value;
        const filtroEstado = document.getElementById('filtro-estado').value;
        const filtroOrganizacion = document.getElementById('filtro-organizacion').value;
        
        let casosVisibles = 0;
        
        todosLosMarcadores.forEach(marcador => {
            const datos = marcador.options.datos;
            let mostrar = true;
            
            if (filtroPais && datos.pais !== filtroPais) mostrar = false;
            if (filtroTipoIA && datos.tipo_ia !== filtroTipoIA) mostrar = false;
            if (filtroEstado && datos.estado !== filtroEstado) mostrar = false;
            if (filtroOrganizacion && datos.organizacion !== filtroOrganizacion) mostrar = false;
            
            if (mostrar) {
                mapaGlobal.addLayer(marcador);
                casosVisibles++;
            } else {
                mapaGlobal.removeLayer(marcador);
            }
        });
        
        actualizarContador(casosVisibles);
    }
    
    function limpiarFiltros() {
        document.getElementById('filtro-pais').value = '';
        document.getElementById('filtro-tipo-ia').value = '';
        document.getElementById('filtro-estado').value = '';
        document.getElementById('filtro-organizacion').value = '';
        
        // Mostrar todos los marcadores
        todosLosMarcadores.forEach(marcador => {
            mapaGlobal.addLayer(marcador);
        });
        
        actualizarContador(todosLosMarcadores.length);
    }
    
    function actualizarContador(cantidad) {
        document.getElementById('contador-casos').textContent = `Mostrando: ${cantidad} casos`;
    }
    </script>
    """

def create_fixed_map_with_filters(df):
    """Crear mapa CON filtros temáticos integrados"""
    
    print("🗺️ Creando mapa CON FILTROS TEMÁTICOS...")
    
    # Filtrar casos válidos
    df_valid = df.dropna(subset=['Latitud', 'Longitud'])
    
    if len(df_valid) == 0:
        print("❌ No hay casos con coordenadas válidas")
        return None
    
    # Crear mapa base
    mapa = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles='OpenStreetMap',
        world_copy_jump=False,
        no_wrap=True,
        min_zoom=2,
        max_zoom=15,
        max_bounds=True
    )
    
    # Configurar bounds mundiales
    southwest = [-60, -180]
    northeast = [85, 180]
    mapa.fit_bounds([southwest, northeast], padding=(10, 10))
    
    print(f"📍 Procesando {len(df_valid)} casos con filtros...")
    
    # Lista para JavaScript
    casos_js = []
    
    # Agregar marcadores
    for index, row in df_valid.iterrows():
        if pd.notna(row['Latitud']) and pd.notna(row['Longitud']):
            
            # Popup HTML (mismo formato que antes)
            popup_html = f"""
            <div style="width: 380px; font-family: 'Courier New', monospace; 
                       background: white; border: 2px solid #333; padding: 0; border-radius: 5px;">
                
                <div style="background: #f0f0f0; padding: 10px; border-bottom: 1px solid #333; 
                           font-weight: bold; text-align: center; border-radius: 3px 3px 0 0;">
                    Caso IA Sindical - {row['País']}
                </div>
                
                <div style="padding: 12px; font-size: 13px; line-height: 1.5;">
                    <div style="margin-bottom: 4px;">🏢 <strong>Organización:</strong> {row['Organización_Sindical']}</div>
                    <div style="margin-bottom: 4px;">🤖 <strong>Tipo IA:</strong> {row['Tipo_IA']}</div>
                    <div style="margin-bottom: 4px;">📊 <strong>Estado:</strong> {row['Estado']}</div>
                    <div style="margin-bottom: 4px;">📄 <strong>Fuente:</strong> {row['Fuente']}</div>
                    <div style="margin-bottom: 8px;">👥 <strong>Actores:</strong> {row['Actores']}</div>
                    
                    <div style="border-top: 1px solid #ccc; margin: 10px 0;"></div>
                    
                    <div style="margin-bottom: 10px;">
                        <div style="margin-bottom: 5px;"><strong>📝 Descripción:</strong></div>
                        <div style="font-size: 12px; color: #555; line-height: 1.4; text-align: justify; 
                                   max-height: 150px; overflow-y: auto; padding-right: 5px;">
                            {str(row['Descripción'])}
                        </div>
                    </div>
                    
                    {f'<div style="text-align: center; margin-top: 8px;"><a href="{row["URL"]}" target="_blank" style="color: #0066cc; text-decoration: none; font-weight: bold;">🔗 Ver más información</a></div>' if row['URL'] and str(row['URL']).strip() else ''}
                </div>
            </div>
            """
            
            # Crear marcador con datos para filtros
            marcador = folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=folium.Popup(popup_html, max_width=400),
                tooltip=f"{row['Titulo']} - {row['País']}",
                icon=folium.Icon(color='blue', icon='info-sign')
            )
            
            # Agregar al mapa
            marcador.add_to(mapa)
            
            # Datos para JavaScript
            casos_js.append({
                'pais': str(row['País']),
                'tipo_ia': str(row['Tipo_IA']),
                'estado': str(row['Estado']),
                'organizacion': str(row['Organización_Sindical'])
            })
    
    # Agregar filtros HTML
    filtros_html = crear_filtros_html()
    mapa.get_root().html.add_child(folium.Element(filtros_html))
    
    # Script de inicialización
    init_script = f"""
    <script>
    // Inicializar filtros cuando el mapa esté listo
    document.addEventListener('DOMContentLoaded', function() {{
        const casos = {casos_js};
        
        // Obtener referencia al mapa Leaflet
        setTimeout(function() {{
            const mapas = Object.keys(window).filter(key => key.startsWith('map_'));
            if (mapas.length > 0) {{
                const mapa = window[mapas[0]];
                
                // Guardar marcadores
                mapa.eachLayer(function(layer) {{
                    if (layer instanceof L.Marker) {{
                        const index = todosLosMarcadores.length;
                        if (casos[index]) {{
                            layer.options.datos = casos[index];
                        }}
                        todosLosMarcadores.push(layer);
                    }}
                }});
                
                inicializarFiltros(casos, mapa);
            }}
        }}, 1000);
    }});
    </script>
    """
    
    mapa.get_root().html.add_child(folium.Element(init_script))
    
    print("✅ MAPA CON FILTROS CREADO:")
    print("   ✅ 4 filtros temáticos: País, Tipo IA, Estado, Organización")
    print("   ✅ Contador de casos visible")
    print("   ✅ Botón limpiar filtros")
    print("   ✅ JavaScript interactivo integrado")
    
    return mapa

# 🚀 PROCESO PRINCIPAL
if __name__ == "__main__":
    df = get_casos_ia_sindical()
    df = aplicar_offset_automatico(df) 
    
    if not df.empty:
        mapa = create_fixed_map_with_filters(df)
       
        if mapa:
            nombre_archivo = 'index.html'
            mapa.save(nombre_archivo)
            print(f"💾 MAPA GUARDADO: {nombre_archivo}")
            print("🎯 PROBLEMAS SOLUCIONADOS:")
            print("   1. ✅ Continentes NO repetidos")
            print("   2. ✅ Descripción COMPLETA visible")
            print("🚀 LISTO PARA GAMMA")
        else:
            print("❌ Error creando mapa")
    else:
        print("❌ No se pudieron obtener datos")
