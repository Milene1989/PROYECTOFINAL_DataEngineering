# Ingeniería de Datos
# PROYECTO FINAL

# Estructura
- Flujo batch: Un script para obtener datos de la API de Alpha Vantage cada 24 horas.
- Flujo near real-time: Un script en Python para generar logs simulados de operaciones financieras (transacciones de compra/venta, errores de conexión, alertas de precios, etc).

# 1.- Script para flujo batch - Datos financieros (Alpha Vantage)
Este script usará la API de Alpha Vantage para obtener el precio histórico de acciones como por ejemplo Tesla (TSLA).

# Datos obtenidos:
- Fecha
- Precio de apertura
- Precio de cierre
- Volumen

# Código en Python para obtener datos financieros → API_a_CSV.py
¿Cómo funciona?
- Consulta los precios de las acciones en la API.
- Extrae los valores clave (fecha, apertura, cierre, volumen).
- Guarda los datos en un archivo csv: "Datos_financieros.csv", el cual es usado en el flujo batch. Este CSV se lee con Logstash y se envía a Elasticsearch para su análisis.
- También se genera un archivo con logs: "extraccion_finanzas.log", el cual permite ver los registros de los datos extraídos de la API.

# 2.- Script para flujo NRT - Logs de transacciones financieras
Este script genera logs simulados de transacciones en NRT, como si fueran de un sistema de trading.

# Tipos de eventos simulados:
- Compra/venta de acciones.
- Alertas por cambios bruscos de precio.
- Errores en la conexión con la API de mercado.

# Código en Python para generar logs y enviarlos a Kafka → Logs_trans_fin.py
¿Cómo funciona?
- Cada segundo genera un evento financiero (compra/venta de acciones, errores de conexión, etc). 
- Envía los datos a Kafka en el tópico "transacciones_financieras". Logstash lee estos logs desde Kafka y los envía a Elasticsearch para su análisis en tiempo real.
- Al igual que en el script anterior, se genera un archivo con logs para llevar un registro de los datos generados: "logs_transacciones.log".

# 3.- Conexión con Logstash
Como se mencionó anteriormente, una vez que se tiene los datos financieros en batch y los logs en NRT, se usa Logstash para procesarlos.
# Archivo de configuración: LOGSTASH_UNIFICADO_FIN_TRANS.conf
Este archivo hace lo siguiente:
- Lee el CSV generado por Alpha Vantage.
- Convierte los valores en números.
- Envia los datos a Elasticsearch en el índice "finanzas_batch".
- Escucha eventos en tiempo real desde Kafka.
- Realiza transformaciones.
- Guarda los datos en el índice "transacciones_nrt".

# Resumen Final
1.- Batch → Se usa Alpha Vantage para obtener precios de acciones cada 24 horas.

2.- Near real-time → Se genera logs financieros simulados con Python y Kafka.

3.- Logstash → Procesa ambos flujos y envía los datos a Elasticsearch.










