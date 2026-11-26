# 🚇 MetroDemand Analytics

![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white) ![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white) ![Delta Lake](https://img.shields.io/badge/Delta%20Lake-00ADD8?style=for-the-badge) ![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)

![Líneas](https://img.shields.io/badge/Líneas-5-00843D) ![WAPE julio](https://img.shields.io/badge/WAPE%20julio-10.01%25-00843D) ![Modelo](https://img.shields.io/badge/Modelo-Mediana%20histórica-087F8C)

**Diseño e implementación de una solución Big Data para el análisis y predicción de la demanda horaria de pasajeros del Metro de Medellín.**

**Universidad Autónoma Latinoamericana (UNAULA)**  
Especialización en Analítica de Datos · Big Data · 2026

### Integrantes

- Isis Valentina Palacio Taborda
- Yuliana Estrada Calle
- Dora Milena Estrada Muñoz
- Maria Antonia Pino Giraldo

## ✨ Resultados destacados

| 🟢 Afluencia histórica consolidada | 🔵 Demanda futura estimada | 🟣 Cobertura histórica final |
| :---: | :---: | :---: |
| **479,24 millones** | **128,47 millones** | **100 %** |
| Enero 2025 – julio 2026 | Agosto – diciembre 2026 | Tras la reconstrucción |

| Registros históricos | Predicciones horarias | WAPE de prueba | R² de prueba |
| :---: | :---: | :---: | :---: |
| **57.700** | **15.300** | **10,01 %** | **0,9737** |

El proyecto transforma datos públicos de movilidad en información histórica trazable, estimaciones de demanda y un servicio de predicción consultable. La afluencia consolidada incluye valores imputados; la demanda futura es una estimación, no una medición. Las métricas corresponden a julio de 2026.

## 🎯 1. Contexto y propósito

La demanda del transporte masivo presenta variaciones por línea, hora y tipo de día. Contar con información histórica consistente y estimaciones de demanda permite identificar patrones de movilidad y aportar evidencia a la planificación operativa. El proyecto aborda, además, la ausencia de registros históricos mediante una reconstrucción controlada y trazable.

### Objetivo general

Implementar una solución integral de ingeniería de datos y analítica predictiva que permita consolidar, analizar y estimar la demanda horaria de cinco líneas del Metro de Medellín.

### Objetivos específicos

- Integrar y transformar las fuentes originales mediante una arquitectura Medallion.
- Identificar faltantes, evaluar estrategias de imputación y reconstruir la serie histórica sin utilizar información futura.
- Comparar modelos predictivos mediante validación temporal y una prueba independiente.
- Registrar y desplegar el modelo seleccionado para consultar predicciones mediante una API REST.
- Comunicar los resultados mediante un dashboard interactivo.

## 📂 2. Alcance y fuentes de datos

| Característica | Descripción |
|---|---|
| Fuentes | Afluencia_Metro_2025.xlsx y Afluencia_Metro_2026.xlsx |
| Cobertura histórica | Enero de 2025 a julio de 2026 |
| Brecha principal | Octubre a diciembre de 2025 |
| Líneas objetivo | A, B, 1, 2 y T-A |
| Granularidad | Fecha, línea y franja horaria |
| Franjas de análisis | 04:00 a 23:00; no equivalen al horario efectivo de servicio |
| Horizonte predictivo | Agosto a diciembre de 2026 |

### Fuentes oficiales de información

Los datos de afluencia y los horarios de operación se obtuvieron de información pública del Metro de Medellín. El calendario de festivos nacionales complementa las variables temporales.

| Recurso | Fuente |
|---|---|
| Horarios de operación | [Metro de Medellín – Usuarios](https://www.metrodemedellin.gov.co/usuarios) |
| Portal de datos abiertos | [Afluencia de pasajeros](https://datosabiertos-metrodemedellin.opendata.arcgis.com/search?tags=afluencia) |
| Afluencia 2025 | [Descargar desde la fuente oficial](https://datosabiertos-metrodemedellin.opendata.arcgis.com/documents/d6bb62fc46db490db6f8783736969d15/about) |
| Afluencia 2026 | [Descargar desde la fuente oficial](https://datosabiertos-metrodemedellin.opendata.arcgis.com/documents/b9f146a80d1d41b498dac9bdc2838104/about) |

Consulte las [instrucciones de carga](data/README.md).

## 🏗️ 3. Arquitectura de la solución

![Infografía de arquitectura MetroDemand Analytics](docs/arquitectura_visual.png)

### Diagrama técnico complementario

![Arquitectura técnica](docs/arquitectura.svg)

El diagrama técnico representa el flujo de datos y las dos rutas de consumo: visualización mediante tablas analíticas y consulta del modelo mediante un endpoint. El despliegue se realiza en un notebook separado del Job principal.

Las métricas de la infografía corresponden a la prueba independiente de julio, no a resultados observados del horizonte futuro; los beneficios son potenciales. La descripción técnica siguiente detalla las responsabilidades de cada capa.

| Componente | Función |
|---|---|
| Databricks | Entorno de ejecución y análisis |
| Apache Spark / PySpark | Transformación y procesamiento de datos |
| Delta Lake | Persistencia de tablas y resultados |
| Unity Catalog | Organización de volúmenes, tablas y modelos |
| Lakeflow Jobs | Orquestación del notebook principal |
| Spark MLlib | Evaluación de Random Forest |
| MLflow | Seguimiento de experimentos y empaquetado del modelo |
| Model Serving | Exposición del modelo registrado mediante API REST |
| SQL Warehouse y Dashboards | Consulta y visualización interactiva |

### Arquitectura Medallion

| Capa | Responsabilidad | Tabla principal |
|---|---|---|
| Bronze | Ingesta y conservación de datos originales | `metrodemanda_afluencia_raw` |
| Silver | Normalización y transformación a formato horario | `metrodemanda_afluencia` |
| Gold | Enriquecimiento de calendario y operación, reconstrucción histórica | `metrodemanda_afluencia_horaria_base`, `metrodemanda_afluencia_horaria_completa` |
| Esquema analítica | Comparación, evaluación, medianas persistidas y pronósticos | `metrodemanda_comparacion_modelos`, `metrodemanda_evaluacion_julio2026`, `metrodemanda_predicciones_ago_dic2026` |

## 🔎 4. Calidad y reconstrucción histórica

Se diferencian observaciones válidas, observaciones excepcionales fuera de horario, faltantes operativos y ceros estructurales. Se preservan los registros observados y se reconstruyen faltantes mediante métodos evaluados temporalmente: mediana histórica, mediana móvil estacional y Random Forest. Los cortes mensuales impiden que los datos del mes reconstruido participen en el ajuste.

| Indicador | Resultado |
|---|---:|
| Registros históricos consolidados | 57.700 |
| Registros imputados | 8.615 |
| Registros de pronóstico | 15.300 |

La reconstrucción permitió completar la cuadrícula de fechas, líneas y franjas horarias sin confundir ausencia de servicio con ausencia de información. Los 8.615 registros imputados representan aproximadamente el 14,93 % del histórico consolidado. La imputación se distingue explícitamente de las observaciones originales. Consulte la [metodología](docs/metodologia.md) y el [diccionario de datos](docs/diccionario_datos.md).

## 📈 5. Modelado y evaluación predictiva

Se compararon tres escenarios: mediana histórica con observaciones, Random Forest con observaciones y Random Forest con observaciones e imputaciones. La selección se realizó por WAPE en junio de 2026; julio se reservó como prueba independiente. Posteriormente se reajustó el modelo ganador con información disponible hasta julio.

### Diseño de la evaluación temporal

| Etapa | Periodo | Propósito |
|---|---|---|
| Entrenamiento | Enero 2025 – mayo 2026 | Ajuste de candidatos |
| Validación | Junio 2026 | Selección por WAPE |
| Prueba independiente | Julio 2026 | Evaluación fuera de muestra |
| Reajuste definitivo | Hasta julio 2026 | Preparación del pronóstico |
| Predicción | Agosto – diciembre 2026 | Estimación de demanda futura |

**Modelo seleccionado: mediana histórica sobre registros observados**, con niveles de respaldo por línea, hora y calendario. La selección favorece el desempeño observado, no la complejidad del algoritmo.

| Métrica de prueba independiente (julio de 2026) | Resultado |
|---|---:|
| WAPE | 10,01 % |
| MAE | 830,05 |
| RMSE | 2.143,69 |
| R² | 0,9737 |
| Registros evaluados | 2.885 |

El resultado muestra que un modelo estadístico sencillo puede superar alternativas más complejas para este problema. El WAPE mide el error absoluto agregado respecto a la demanda observada; el R² refleja el ajuste en la prueba independiente. Ninguna de estas métricas garantiza el desempeño futuro.

[Experimentos MLflow](docs/evidencias/08_Experimentos_MLflow.png) · [Ajuste definitivo](docs/evidencias/09_Ajuste_Definitivo.png)

## ⚙️ 6. Orquestación y ejecución

El Job `MetroDemand_Analytics_Pipeline` ejecuta la ingesta, transformación, reconstrucción y predicción mediante una tarea de notebook en cómputo Serverless. La ejecución documentada fue manual y terminó satisfactoriamente en **17 minutos y 21 segundos**. No incluye despliegue automático del modelo.

![Ejecución satisfactoria](docs/evidencias/06_Pipeline_Ejecucion.png)

[Configuración del Job](pipelines/job_config.json) · [Tarea de procesamiento](docs/evidencias/07_Pipeline_Tareas.png)

## 🚀 7. Registro, despliegue y API REST

El modelo definitivo se persiste en tablas Delta de medianas y se empaqueta como MLflow PyFunc. Se verifica su equivalencia con los 15.300 registros de pronóstico y se registra en Unity Catalog como `workspace.analitica.metrodemanda_modelo_definitivo`, versión 1. El endpoint `metrodemanda-serving` se documentó en estado Ready.

![Servicio desplegado](docs/evidencias/10_Serving_Endpoint.png)

Ejemplo de solicitud:

```json
{"dataframe_records": [{"linea": "LÍNEA A", "hora_num": 7, "dia_semana_num": 2, "es_festivo": 0, "en_horario_operacion": 1}]}
```

Respuesta obtenida para ese escenario:

```json
{"predictions": [{"demanda_predicha": 54879}]}
```

El servicio recibe variables de calendario y operación precalculadas. La prueba funcional múltiple devolvió cinco predicciones; no sustituye la evaluación estadística.

[Registro del modelo](docs/evidencias/13_Registro_Unity_Catalog.png) · [Prueba API](docs/evidencias/11_API_Predicciones.png) · [Instrucciones de consumo](serving/README.md)

## 📊 8. Visualización y análisis

El dashboard interactivo se diseñó y publicó directamente en Databricks, utilizando las tablas Delta de la solución como fuentes de información. La versión publicada `MetroDemand_Analytics_V1` integra cinco módulos:

| Módulo | Propósito |
|---|---|
| Centro de control | Resumen histórico y predictivo |
| Inteligencia de movilidad | Patrones horarios y por tipo de día |
| Calidad y trazabilidad | Cobertura, procedencia e imputación |
| Inteligencia predictiva | Comparación y evaluación del modelo |
| Planificación operativa | Exploración de la demanda futura estimada |

![Dashboard con filtro de Línea A](docs/evidencias/12_Dashboard_Interactivo.png)

[Dashboard publicado en PDF](dashboards/dashboard_publicado.pdf) · [Descripción del dashboard](dashboards/README.md)

## 💡 9. Aportes y conclusiones

MetroDemand Analytics integra el ciclo de ingeniería de datos, experimentación, predicción y consumo de resultados en una misma solución. Los principales aportes son:

- **Calidad y trazabilidad:** reconstrucción de faltantes con identificación de su procedencia y preservación de las observaciones originales.
- **Rigor predictivo:** selección de modelos mediante validación temporal y evaluación independiente, evitando utilizar información futura en el ajuste.
- **Implementación funcional:** ejecución satisfactoria del pipeline, persistencia del modelo, registro en Unity Catalog y consulta de predicciones mediante Model Serving.
- **Inteligencia de movilidad:** exploración de patrones por línea, hora y tipo de día, con estimaciones que pueden apoyar la planificación operativa y las decisiones basadas en datos.

El alcance es predictivo y analítico: no se estiman frecuencias óptimas, capacidad disponible ni ahorros efectivos. Los beneficios operativos son aplicaciones potenciales que requieren información y evaluación adicionales.

## 📚 10. Recursos y reproducción

| Recurso | Acceso |
|---|---|
| Procesamiento y modelado | [Notebook principal](notebooks/MetroDemand_Analytics.ipynb) |
| Registro y despliegue | [Notebook de despliegue](notebooks/MetroDemand_Model_Deployment.ipynb) |
| Orquestación | [Configuración del Job](pipelines/job_config.json) |
| Datos | [Fuentes e instrucciones de carga](data/README.md) |
| Documentación | [Metodología](docs/metodologia.md) · [Diccionario de datos](docs/diccionario_datos.md) |
| Visualización | [Dashboard publicado](dashboards/dashboard_publicado.pdf) |
| API | [Instrucciones de consumo](serving/README.md) |
| Evidencias | [13 capturas de implementación](docs/evidencias/) |

<details>
<summary>Instrucciones técnicas y condiciones de reproducción</summary>

1. Cargar los Excel oficiales en `/Volumes/workspace/default/data`.
2. Importar el notebook principal como `MetroDemand_Analytics_Version_Final` y ejecutarlo en Serverless, en un entorno aislado porque crea esquemas y sobrescribe tablas.
3. Crear un Job nuevo con la configuración suministrada, ajustando la ruta del notebook al usuario.
4. Ejecutar el notebook de despliegue, ajustar las referencias al experimento y al run definitivo y crear el endpoint con la versión registrada.
5. Configurar `DATABRICKS_HOST` y `DATABRICKS_TOKEN` para consumir la API sin publicar credenciales.

Las versiones publicadas de los notebooks se adaptaron para retirar salidas y metadatos de sesión y parametrizar referencias del entorno. Se validaron localmente, sin una nueva ejecución en Databricks. Las pruebas del endpoint se realizaron desde su interfaz; el cliente REST externo no se ejecutó contra el servicio. El PDF es evidencia de la visualización publicada, no una configuración importable.

</details>

---

**MetroDemand Analytics · UNAULA · 2026**
