#!/usr/bin/env bash
#应用不经过 Nginx直接抛出外网的启动脚本
python manage.py runserver --host=0.0.0.0 --port=8080