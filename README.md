# vecindario
### Los commits recientes son agregados por la rama master
### Para hacer el despliegue se necesita que la maquina anfitrión tenga instalado y configurado docker y docker-compose
## Clonar repositorio
- git clone https://github.com/softkra/vecindario.git
#### *No deberia presentar problemas al momento de clonarlo ya que el repositorio es publico*
## Iniciar despliegue del proyecto mediante docker
- Una vez clonado el repositorio, se ingresa al directorio 'vecindario'
- Con `docker-compose up --build -d` se iniciará la construccion de los contenedores docker que estan configurados para trabajar con la última version de Python 3 y la ultima de Django soportada por la version de python

```
backend_1  | System check identified no issues (0 silenced).
backend_1  | July 06, 2022 - 14:34:03
backend_1  | Django version 4.0.6, using settings 'vecindario.settings'
backend_1  | Starting development server at http://0.0.0.0:5000/
backend_1  | Quit the server with CONTROL-C.
```

- Una vez se creen los contenedores se puede hacer seguimiento a los logs con el comando `docker-compose logs -f`
## Seguimiento
- El admin de django se puede ver en el endpoint `localhost:8000/admin`, (usuario: `superuser` contraseña: `superpass`)

##### _El código almacenado en este GitHub fue desarrollado por Christian David Porres_
