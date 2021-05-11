# 基于Django和Django REST framework的自动化测试平台后端仓库
## Celery测试环境启动
```bash
docker start ramq
celery -A beer_server worker -l INFO
```
