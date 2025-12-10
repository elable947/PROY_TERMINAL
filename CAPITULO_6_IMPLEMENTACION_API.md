# CAPÍTULO 6: IMPLEMENTACIÓN DE LA API

## 6.1 Arquitectura de la API REST

El sistema backend del "Terminal Terrestre" está construido utilizando una arquitectura **RESTful** (Representational State Transfer) sobre el framework **Flask** de Python. Esta arquitectura desacopla completamente el frontend y el backend, permitiendo una comunicación eficiente mediante peticiones HTTP estándar (GET, POST, PUT, DELETE) y respuestas en formato JSON.

### Componentes Principales:
1.  **Framework Web (Flask):** Maneja el enrutamiento, las solicitudes HTTP y las respuestas. Se utilizan **Blueprints** para modularizar las rutas por funcionalidad (Auth, Company, Public, etc.).
2.  **ORM y Base de Datos (SQLAlchemy + PyODBC):** La interacción con la base de datos **SQL Server** se realiza principalmente mediante **procedimientos almacenados (Stored Procedures)** ejecutados a través de `SQLAlchemy`. Esto asegura que la lógica de negocio pesada y la integridad de los datos se mantengan en el motor de base de datos, cumpliendo con los requisitos de la asignatura Base de Datos I.
3.  **Seguridad:** Se implementa autenticación basada en sesiones y hash de contraseñas para proteger los accesos.

## 6.2 Endpoints implementados

La API se divide en varios módulos funcionales. A continuación se detallan los endpoints más relevantes:

### 6.2.1 Autenticación (`/api/auth`)
*   `POST /login`: Valida credenciales y crea la sesión del usuario.
*   `POST /logout`: Cierra la sesión activa.
*   `POST /register`: Registra nuevos usuarios/clientes.

### 6.2.2 Módulo Público (`/api/public`)
Accesible sin autenticación para usuarios visitantes.
*   `GET /companies`: Lista todas las empresas de transporte activas.
*   `GET /destinations`: Lista los destinos disponibles.
*   `GET /trips`: Busca viajes filtrados por origen, destino y fecha.

### 6.2.3 Panel de Empresa (`/api/company`)
Exclusivo para usuarios con rol de "Empresa de Transporte".
*   `GET /my-company/<id>`: Obtiene información del perfil de la empresa.
*   `POST /banner`: Sube y actualiza el banner promocional.
*   **Gestión de Flota:**
    *   `GET/POST /vehicles`: CRUD de vehículos (buses).
    *   `GET/POST /drivers`: Gestión de conductores.
    *   `POST /drivers/assign`: Asigna un usuario conductor a la empresa.
*   **Gestión de Viajes:**
    *   `POST /trips`: Programación de nuevos viajes (salidas).
    *   `POST /routes`: Creación de rutas (Origen -> Destino).
*   **Redes Sociales:**
    *   `GET/POST/DELETE /socials`: Gestión de enlaces sociales (Facebook, Instagram, etc.).

### 6.2.4 Panel de Conductor (`/api/driver`)
*   `GET /assigned-trips`: Lista los viajes asignados al conductor logueado.
*   `POST /start-trip`: Marca el inicio de un viaje.
*   `GET /history`: Historial de viajes realizados.

### 6.2.5 Módulo de Clientes/Ventas (`/api/client`)
*   `GET /seats/<trip_id>`: Obtiene el mapa de asientos (libres/ocupados) de un viaje.
*   `POST /purchase`: Procesa la compra de pasajes, generando boletos y actualizando el estado de los asientos.

## 6.4 Documentación de la API

La API sigue el estándar de respuestas JSON.
*   **Éxito (200/201):** Retorna el objeto solicitado o un mensaje de confirmación.
*   **Error (400/404/500):** Retorna un objeto JSON con la clave `error` describiendo el problema.

**Formato General de Respuesta:**
```json
// Éxito
{
    "idViaje": 12,
    "destino": "Chachapoyas",
    "precio": 50.00
}

// Error
{
    "error": "Usuario no encontrado o contraseña incorrecta"
}
```

## 6.5 Ejemplos de consumo

A continuación se muestran ejemplos de cómo consumir la API utilizando `curl` o JavaScript (Fetch API).

### Ejemplo 1: Listar Empresas (Público)
**Petición:**
`GET http://localhost:5000/api/public/companies`

**Respuesta JSON:**
```json
[
    {
        "idEmpresaTransporte": 1,
        "nombreEmpresa": "Transportes Zelada",
        "telefonoEmpresa": "987654321",
        "redesSociales": [
            { "red": "Facebook", "url": "https://fb.com/zelada" }
        ]
    }
]
```

### Ejemplo 2: Programar un Viaje (Empresa)
**JavaScript (Angular Service):**
```typescript
const payload = {
    idEmpresaTransporte: 1,
    idVehiculo: 5,
    idConductorEmpresa: 3,
    idRuta: 10,
    fechaSalida: "2024-12-15T08:00:00",
    precio: 45.00
};

this.http.post('/api/company/trips', payload).subscribe(response => {
    console.log('Viaje creado:', response);
});
```

### Ejemplo 3: Iniciar Sesión
**Request:**
```json
POST /api/auth/login
{
    "email": "admin@zelada.com",
    "password": "securePass123"
}
```
