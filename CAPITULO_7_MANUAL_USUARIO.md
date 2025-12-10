# CAPÍTULO 7: MANUAL DE USUARIO

## 7.1 Instalación y configuración

Para ejecutar el sistema "Terminal Terrestre" en un entorno local, se requieren los siguientes componentes previos:

### Requisitos del Sistema
1.  **Base de Datos:** SQL Server 2019 o superior.
2.  **Lenguaje Backend:** Python 3.9 o superior.
3.  **Frontend Runtime:** Node.js (v18+) y NPM.
4.  **Controlador ODBC:** ODBC Driver 18 for SQL Server.

### Pasos de Instalación

1.  **Clonar el Proyecto:**
    Descargue el código fuente en su directorio de trabajo.

2.  **Configurar Base de Datos:**
    *   Ejecute el script `database_setup.sql` en SQL Server Management Studio (SSMS) para crear la estructura de tablas.
    *   Ejecute los scripts de procedimientos almacenados ubicados en la carpeta `/sql`.
    *   Configure la cadena de conexión en `config.py` o mediante variables de entorno.

3.  **Configurar Entorno Python:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Configurar Frontend (Angular):**
    ```bash
    cd frontend
    npm install
    ```

## 7.2 Guía de despliegue

El sistema está diseñado para ejecutarse en dos procesos simultáneos: el servidor API y el servidor de desarrollo del cliente.

### Iniciar el Backend
Desde la terminal en la carpeta raíz del proyecto:
```bash
python app.py
```
*Se confirmará el inicio en: http://127.0.0.1:5000*

### Iniciar el Frontend
Desde una nueva terminal en la carpeta `/frontend`:
```bash
ng serve -o
```
*El navegador se abrirá automáticamente en: http://localhost:4200*

## 7.3 Ejemplos de uso del sistema

### A. Registro de una Empresa
1.  El administrador del sistema crea un usuario con rol "Empresa".
2.  La empresa inicia sesión y accede al **Dashboard de Empresa**.
3.  En la pestaña "General", puede actualizar su banner y agregar **Redes Sociales** haciendo clic en el botón (+).
4.  En "Vehículos", registra su flota de buses ingresando placa y capacidad.

### B. Programación de Viajes
1.  La empresa accede a la sección "Rutas" para definir orígenes y destinos (ej. Chachapoyas -> Lima).
2.  En la sección "Viajes", selecciona un bus, un conductor asignado y una ruta.
3.  Define la fecha, hora de salida y el precio del boleto.
4.  Al guardar, el viaje queda disponible inmediatamente para la venta pública.

### C. Compra de Pasajes (Cliente)
1.  El usuario ingresa a la página principal (Pública).
2.  Busca viajes seleccionando su destino.
3.  Elige una empresa y un horario conveniente.
4.  Selecciona sus asientos en el mapa interactivo del bus.
5.  Completa sus datos personales y realiza el pago simulado.
6.  El sistema genera un boleto virtual y marca los asientos como ocupados.

## 7.4 Solución de problemas comunes

| Problema | Causa Probable | Solución |
| :--- | :--- | :--- |
| **Error "Login failed for user..."** | Credenciales de SQL Server incorrectas en `config.py`. | Verifique usuario/clave en la cadena de conexión. |
| **Error "Driver not found"** | Falta instalar el driver ODBC 18. | Descargue e instale el driver desde el sitio de Microsoft. |
| **Página en blanco o "Not Found"** | El frontend no se ha compilado o conectado al puerto correcto. | Asegúrese de correr `ng serve` y verifique que el proxy apunte a las rutas `/api` del backend. |
| **CORS Policy Error** | El navegador bloquea la petición al backend. | Flask-CORS está configurado, pero verifique que accede desde `localhost:4200`. |
| **Asientos no se actualizan** | Problema de concurrencia o caché. | Refresque la página. El sistema valida la disponibilidad en tiempo real antes de la compra. |
