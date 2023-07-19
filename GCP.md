How to deploy to Google App Engine using Google SDK
===

Init SDK.
```
gcloud init
```

Create project. Need go to console for linking billing account.
```
gcloud projects create <project-id>
```

Set working project.
```
gcloud config set project <project-id>
```

Create app engine. Remember your selected region for later use when creating Cloud SQL instance.
```
gcloud app create
```

Create postgres instance.
```
gcloud sql instances create <CLOUD-SQL-INSTANCE-NAME> \
    --project <PROJECT-ID> \
    --database-version POSTGRES_14 \
    --tier db-f1-micro \
    --region <REGION>
```

Create database.
```
gcloud sql databases create <DBNAME> \
    --instance <CLOUD-SQL-INSTANCE-NAME>
```

Create database user.
```
gcloud sql users create <DBUSER> \
    --instance <CLOUD-SQL-INSTANCE-NAME> \
    --password <DBPASS>
```

Install psql cli if needed, then try to access your databse.
```
sudo apt-get install -y postgresql-client
gcloud sql connect <CLOUD-SQL-INSTANCE-NAME> --user <DBUSER> --database <DBNAME>
```

Download Cloud SQL Auth proxy to connect to Cloud SQL from your local machine [Link](https://cloud.google.com/python/django/flexible-environment#connect_sql_locally). Enable proxy for local development. Then, run db migration.
```
./cloud-sql-proxy <PROJECT-ID>:<REGION>:<CLOUD-SQL-INSTANCE-NAME>
flask init-db
```

Deploy our application to GAE. Remember to update `app.yaml` configuration before deploying.
```
gcloud app deploy
```

Get the URL to access our web application.
```
gcloud app describe --format "value(defaultHostname)"
```

Delete everything after use.
```
gcloud projects delete <PROJECT-ID>
```
