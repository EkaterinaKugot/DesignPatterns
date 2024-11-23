#!/bin/bash

curl -X 'PUT' \
  'http://localhost:8080/api/api/put_nomenclature' \
  -H 'accept: application/text' \
  -H 'Content-Type: application/json' \
  -d '{
        "full_name": "Перец",
        "group": {
            "id": 91837425884489217160904690353695769402,
            "name": "Сырье"
        },
        "name": "",
        "range": {
            "base_range": null,
            "conversion_factor": 1,
            "id": 91837425963717379676601172628743537466,
            "name": "гр"
        }
    }'

curl -X 'DELETE' \
  'http://localhost:8080/api/api/delete_nomenclature' \
  -H 'accept: application/text' \
  -H 'Content-Type: application/json' \
  -d '{
        "full_name": "Перец",
        "group": {
            "id": 91837425884489217160904690353695769402,
            "name": "Сырье"
        },
        "id": 91837921060504931315277708816139043642,
        "name": "",
        "range": {
            "base_range": null,
            "conversion_factor": 1,
            "id": 91837425963717379676601172628743537466,
            "name": "гр"
        }
    }'

curl -X 'PATCH' \
  'http://localhost:8080/api/api/change_nomenclature' \
  -H 'accept: application/text' \
  -H 'Content-Type: application/json' \
  -d '{
        "full_name": "Белый сахар",
        "group": {
            "id": 41323352302233496525523373456537830202,
            "name": "Сырье"
        },
        "id": 41323352777602471609397186734470611770,
        "name": "",
        "range": {
            "base_range": null,
            "conversion_factor": 1,
            "id": 41323352381461659038287730899190694714,
            "name": "гр"
        }
    }'

curl -X 'GET' \
  'http://localhost:8080/api/api/nomenclature/41323352777602471609397186734470611770' \
  -H 'accept: application/text'
