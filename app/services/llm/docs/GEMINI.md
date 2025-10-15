# Documentación del Servicio Gemini

Esta documentación explica la implementación y uso del servicio Gemini 2.5 Flash para el análisis de algoritmos y conversión de lenguaje natural a pseudocódigo.

## Estructura de Archivos

```
app/services/llm/src/
├── config/
│   └── config_gemini.py    # Configuración del cliente Gemini
├── prompts/
│   └── SYSTEMPROMPT.md     # Prompt del sistema
└── gemini.py              # Funciones principales del servicio
```

## config_gemini.py

### Propósito
Este archivo se encarga de la configuración inicial del cliente de Google Gemini AI.

### Componentes

#### Importaciones
- `google.genai`: Cliente oficial de Google para la API Gemini
- `os`: Manejo de variables de entorno
- `dotenv`: Carga de variables de entorno desde archivo `.env`

#### Configuración del Cliente
```python
client = genai.Client(os.getenv("GEMINI_API_KEY"))
```

- **Función**: Inicializa el cliente de Gemini usando la clave API desde las variables de entorno
- **Requisito**: La variable `GEMINI_API_KEY` debe estar definida en el archivo `.env`
- **Seguridad**: La clave API se mantiene fuera del código fuente

## gemini.py

### Propósito
Contiene las funciones principales para interactuar con Gemini AI, incluyendo análisis de algoritmos y conversión de lenguaje natural.

### Componentes

#### Variables Globales
- `MODEL`: Modelo de IA a utilizar (por defecto: "gemini-2.5-flash")
- `SYSTEM_PROMPT`: Instrucciones del sistema cargadas desde `SYSTEMPROMPT.md`

#### Funciones Disponibles

##### 1. `ask_gemini(prompt: str) -> str`
**Propósito**: Realizar consultas básicas a Gemini sin instrucciones del sistema.

**Parámetros**:
- `prompt`: Consulta o pregunta para Gemini

**Retorna**: Respuesta de texto de Gemini

**Uso típico**: Consultas generales sin contexto específico de algoritmos

##### 2. `ask_gemini_system(prompt: str) -> str`
**Propósito**: Realizar consultas con el contexto del sistema (experto en algoritmos).

**Parámetros**:
- `prompt`: Consulta específica sobre algoritmos

**Retorna**: Respuesta especializada en análisis de algoritmos

**Características**:
- Utiliza el `SYSTEM_PROMPT` para mantener contexto de especialización
- Ideal para análisis de complejidad y consultas técnicas

##### 3. `parse_nl_code(prompt: str) -> str`
**Propósito**: Convertir descripciones en lenguaje natural a pseudocódigo siguiendo una sintaxis específica.

**Parámetros**:
- `prompt`: Descripción en lenguaje natural del algoritmo

**Retorna**: Pseudocódigo estructurado

**Características**:
- Carga y utiliza el archivo `Proyecto_Gramatica.pdf` como referencia de sintaxis
- Mantiene consistencia en la estructura del pseudocódigo generado
- Utiliza la API de archivos de Gemini para procesar el PDF de referencia

##### 4. `analisys_code(prompt: str, code: str) -> str`
**Propósito**: Analizar la eficiencia y complejidad de código o pseudocódigo existente.

**Parámetros**:
- `prompt`: Instrucciones específicas para el análisis
- `code`: Código o pseudocódigo a analizar

**Retorna**: Análisis detallado de complejidad temporal y espacial

**Características**:
- Proporciona análisis de Big O notation
- Identifica operaciones dominantes
- Explica escenarios de mejor, promedio y peor caso

## Flujo de Trabajo Típico

### 1. Análisis de Algoritmo Existente
```python
from app.services.llm.src.gemini import analisys_code

code = """
for i in range(n):
    for j in range(n):
        print(i, j)
"""

result = analisys_code("Analiza la complejidad de este algoritmo", code)
```

### 2. Conversión de Lenguaje Natural
```python
from app.services.llm.src.gemini import parse_nl_code

description = "Crear un algoritmo que ordene una lista usando el método burbuja"
pseudocode = parse_nl_code(description)
```

### 3. Consulta General sobre Algoritmos
```python
from app.services.llm.src.gemini import ask_gemini_system

question = "¿Cuál es la diferencia entre O(n) y O(log n)?"
answer = ask_gemini_system(question)
```

## Consideraciones Importantes

### Manejo de Errores
- Las funciones no incluyen manejo de errores explícito
- Se recomienda implementar try-catch en el código que las utilice
- Verificar conexión a internet y validez de la API key

### Performance
- Las llamadas a la API tienen latencia variable
- Considerar implementar cache para consultas frecuentes
- El procesamiento de archivos PDF puede tomar tiempo adicional

### Limitaciones
- Dependiente de la disponibilidad del servicio Gemini
- Limitado por los tokens y rate limits de la API
- La calidad del análisis depende de la claridad del input

## Variables de Entorno Requeridas

```bash
GEMINI_API_KEY=your_gemini_api_key_here
MODEL=gemini-2.5-flash
```

## Dependencias

- `google-genai>=1.39.1`
- `python-dotenv>=1.1.1`
