```bash
docker exec -it savannah-airflow-webserver-1  bash
```


```bash
airflow users create --username airflow --firstname savannah --lastname savannah --role Admin --email admin@example.com --password <new_password>
```
airflow users create --username savannah --firstname savannah --lastname savannah --role Admin --email admin@example.com --password admin


generate the secret key for

```bash
openssl rand -base64 32

```