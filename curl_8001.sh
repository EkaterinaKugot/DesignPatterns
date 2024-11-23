#!/bin/bash

curl -X 'POST' \
  'http://localhost:8080/api/filter/range' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "гр",
  "type_filter_name": "EQUALE",
  "id": "",
  "type_filter_id": "EQUALE"
}'

curl -X 'POST' \
  'http://localhost:8080/api/transaction/filter' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "storage": {
    "name": "",
    "type_filter_name": "EQUALE",
    "id": "",
    "type_filter_id": "EQUALE"
  },
  "nomenclature": {
    "name": "мука",
    "type_filter_name": "like",
    "id": "",
    "type_filter_id": "EQUALE"
  }
}'

curl -X 'POST' \
  'http://localhost:8080/api/turnover/filter' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "storage": {
    "name": "Склад 1",
    "type_filter_name": "EQUALE",
    "id": "",
    "type_filter_id": "EQUALE"
  },
  "nomenclature": {
    "name": "Яйцо",
    "type_filter_name": "like",
    "id": "",
    "type_filter_id": "EQUALE"
  },
  "period": {
    "start_period": "2024-01-01T00:00:00Z",
    "end_period": "2024-12-31T23:59:59Z"
  }
}'