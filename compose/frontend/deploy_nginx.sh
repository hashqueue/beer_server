#!/bin/bash

while ! nc -z backend 8000 ; do
    echo "Waiting for the Django backend service to be deployed. 🌿 🌿 🌿"
    sleep 3
done

echo "The Django backend service is deployed. ✅ The Nginx service will be deployed soon. 🌿 🌿 🌿"

