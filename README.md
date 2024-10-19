# Senzil Challenge

Simple (MUY simple) Shop utilizando exclusivamente Django y Django Admin. 
Como el desafio lo pedía, no se utilizó ningún framework frontend, sino que simplemente se utilizo el template de Django Admin con algunas modificaciones.

Mi interpretacion del manejo de roles es la siguiente: 
- Superuser: Puede hacer cualquier cosa (full Django Admin powers).
- Admin: Puede crear nuevos productos.
- User/Client: Puede ver el historial de compras y los detalles de una orden. Y tambien puede crear nuevas ordenes. Para esto se utiliza un carrito de compras MUY basico.

En cuanto a la seguridad, se maneja con permisos de usuario y grupos.

En cuanto al uso de API, se utilizo una API muy simple para obtener una lista de productos y detalles de cada uno. Tambien como pedia el desafio, se utiliza un unico POST para crear una orden (con items del carrito y stock actualizado).

Tests unitarios y de integración utilizando Pytest.

Finalmente la aplicacion se puede correr con Docker o directamente con Python. La version de Python es mucho mas basica dado que no se utilizan herramientas externas como Postgres, Redis, Celery, etc.

La version final y completa de este desafio necesita de Docker para funcionar correctamente.


## Table of Contents

- [Instalacion](#instalacion)
- [Uso](#uso)
- [Consideraciones](#consideraciones)

## Instalacion con Docker, Redis, Celery, Postgres

1. Clonar el repositorio:
   ```
   git clone https://github.com/Kraw-Codehorde/challengecurse.git
   ```
2. Acceder al directorio del proyecto:
   ```   
   cd challengecurse
   ```
3. Crear las imagenes y levantar:
   ```
   docker compose up -d --build
   ```
## Instalacion sin Docker, Redis, Celery, Postgres

1. Clonar el repositorio:
   ```
   git clone https://github.com/Kraw-Codehorde/challengecurse.git
   ```
2. Cambiar al commit con la version stable sin Docker:
   ```
   git checkout 02fbd5e0ea0b3ec9d83f39493d2a72f05e637354
   ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Una vez que docker esta corriendo, acceder al admin:
```
http://localhost:8000/admin
```
Distintos usuarios con distintos permisos:
- Superuser: admin / admin (full Django Admin powers)
- Admin: admin / admin (puede crear nuevos productos)
- Client: client / client (puede ver el historial de compras y los detalles de una orden. Y tambien puede crear nuevas ordenes)

##Testing

Para correr los tests:
```
docker-compose exec web pytest
```

## Consideraciones

Pense que el challenge iba a ser mas sencillo, pero setear bien el Admin y las vistas fue un poco mas complejo de lo que esperaba (con el tiempo disponible).

No se si suponia que habia que hacerlo asi, pero la distincion entre Superuser y Admin tambien tuvo un desafio extra.

Asi y todo fue muy interesante el challenge y aprendi bastante sobre el Admin de Django, que en general no es algo que haya utilizado demasiado.

Desde ya que hay muchas cosas que se pueden mejorar y agregar, y algunas que faltaron por completarse, pero asi y todo deberia cumplir con lo pedido y demostrar un poco mis capacidades/habilidades. Saludos!

Nico.
