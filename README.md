# Tablero-Update


Configuracion para que funcione con docker

antes de ejecutar el docker asegurese de que en

tablero-update/manager.py

la linea de configuracion este en docker para q se ajusten las configuraciones pertinentes para su correcto funcinamiento

Como hacer el mongorestore en docker

crear todos los containers con /bin/bash run_docker.sh

luego abrir otra terminar y agregar docker exec -it tablero-update_mongodb_1 bash

asi se lograra acceder a mongo dentro de docker ahora usamos un cd y nos dirigimos a la ruta siguiente cd data/

al estar en esa direccion ejecutamos el siguiente comando 

mongorestore -d python_test python_test/

y listo ya se puede usar la base de datos

