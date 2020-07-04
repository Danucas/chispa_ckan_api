#!/usr/bin/python3
template = {
  "swagger": "2.0",
  "info": {
    "title": "Chispa CKAN",
    "description": "An interface to fetch cali.ckan.io datasets",
  },
  "host": "",  # overrides localhost:500
  "basePath": "/",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ]
}