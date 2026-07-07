import streamlit as st
import pandas as pd

# 1. Configuración visual de la página
st.set_page_config(page_title="Portal de Vacaciones", page_icon="🌴", layout="centered")

st.title("Sistema de Consulta de Vacaciones")
st.write("Departamento de Talento Humano - Prefectura del Azuay")
st.divider()

# 2. Función para leer las hojas del Excel
@st.cache_data
def cargar_datos_locales():
    df_base = pd.read_excel('Prototipo_Vacaciones_Nombre.xlsx', sheet_name='Base_Historica')
    df_cons = pd.read_excel('Prototipo_Vacaciones_Nombre.xlsx', sheet_name='Consolidado')
    
    # TRUCO DE ORO: Convertir a texto, quitar decimales si se crearon y rellenar con ceros hasta tener 10 dígitos
    df_cons['Cédula'] = df_cons['Cédula'].astype(str).str.split('.').str[0].str.zfill(10)
    df_base['Cédula'] = df_base['Cédula'].astype(str).str.split('.').str[0].str.zfill(10)
    
    return df_base, df_cons

try:
    df_base, df_cons = cargar_datos_locales()
except Exception as e:
    st.error("⚠️ No se pudo cargar el archivo Excel. Asegúrate de que 'Prototipo_Vacaciones_Nombre.xlsx' esté subido en tu repositorio de GitHub.")
    st.stop()

# 3. Interfaz de búsqueda por Cédula
st.subheader("Consulta tu saldo")
cedula_input = st.text_input("Ingrese su número de cédula:", max_chars=10, placeholder="Ej: 0102030405")

if cedula_input:
    # Limpiar el texto que ingresa el usuario por si acaso tenga espacios
    cedula_input = str(cedula_input).strip().zfill(10)

    # Buscar coincidencia en el Consolidado
    empleado_info = df_cons[df_cons['Cédula'] == cedula_input]

    if not empleado_info.empty:
        nombre = empleado_info.iloc[0]['Empleado']
        regimen = empleado_info.iloc[0]['Régimen Laboral']
        saldo = empleado_info.iloc[0]['Saldo Disponible']

        # Mostrar resultados en pantalla
        st.success(f"Funcionario encontrado: **{nombre}**")

        col1, col2 = st.columns(2)
        col1.metric(label="Régimen Laboral", value=regimen)
        col2.metric(label="Saldo Disponible", value=f"{saldo:.2f} Días")

        st.divider()
        st.write("### Historial de Peticiones Aprobadas")
        
        # Filtrar el historial de la Hoja 1 por la cédula
        historial = df_base[df_base['Cédula'] == cedula_input]

        if not historial.empty:
            columnas_vista = ['Desde', 'Hasta', 'Tiempo (Odoo)', 'Días Consumidos (Calculado)', 'Aprobado por']
            st.dataframe(historial[columnas_vista], use_container_width=True, hide_index=True)
        else:
            st.info("No tienes peticiones de vacaciones registradas.")
    else:
        st.error("❌ Cédula no encontrada en el simulador. Intenta con las cédulas del prototipo: 0102030405, 0102030406, 0102030407, 0102030408 o 0102030409")
