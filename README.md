# Proyecto de Análisis de Algoritmos

Este proyecto utiliza Gemini 2.5 Flash para analizar la eficiencia de algoritmos y convertir descripciones en lenguaje natural a pseudocódigo.

## Características

- **Análisis de Complejidad**: Analiza la complejidad temporal y espacial de algoritmos
- **Conversión NL a Pseudocódigo**: Convierte descripciones en lenguaje natural a pseudocódigo estructurado
- **Visualización**: Genera gráficos de complejidad usando matplotlib
- **Cálculos Matemáticos**: Utiliza sympy para análisis matemático avanzado

## Requisitos Previos

- Python 3.8 o superior
- Una clave de API de Google Gemini

## Instalación

1. **Clona el repositorio**:
    ```bash
    git clone https://github.com/MauroGc19/Proyecto-Algoritmos.git
    cd Proyecto-Algoritmos
    ```

2. **Crea un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate   # En Windows
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:
   ```bash
   cp .env.example .env
   ```
   
   Edita el archivo `.env` y añade tu clave de API de Gemini:
   ```
   GEMINI_API_KEY=tu_clave_api_aqui
   MODEL=gemini-2.5-flash
   ```

## Obtener una Clave de API de Gemini

1. Ve a [Google AI Studio](https://aistudio.google.com/)
2. Inicia sesión con tu cuenta de Google
3. Crea un nuevo proyecto o selecciona uno existente
4. Ve a la sección de "API Keys"
5. Genera una nueva clave de API
6. Copia la clave y pégala en tu archivo `.env`

## Uso

Para ejecutar la aplicación:

```bash
python main.py
```

## Dependencias

- **google-genai**: Cliente oficial de Google para la API de Gemini
- **python-dotenv**: Manejo de variables de entorno
- **matplotlib**: Visualización de gráficos de complejidad
- **sympy**: Cálculos matemáticos simbólicos

## Contribuir

1. Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto es parte del curso de Análisis de Algoritmos - Universidad de Caldas.
