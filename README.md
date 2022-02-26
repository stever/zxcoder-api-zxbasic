![Boriel ZX Basic](img/zxbasic_logo.png)

# ZX Play API for ZX Basic

## Development start

### Initial project setup

```bash
git clone git@git.tiepy.dev:zxplay/zxplay-api-zxbasic.git
cd zxplay-api-zxbasic/
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Run app

```bash
uvicorn app.main:app --reload
```

## Docker Build & Push

```bash
docker build -t steverobertson/zxplay-api-zxbasic .
docker push steverobertson/zxplay-api-zxbasic
```

## Run Locally

```bash
docker run \
  --env=API_URL=https://zxplay.org/api/v1/graphql \
  --publish=80:8000 \
  --detach=true \
  --name=zxplay-api-zxbasic \
  steverobertson/zxplay-api-zxbasic
```

## Environment Variables

* API_URL

```powershell
$env:API_URL='https://zxplay.org/api/v1/graphql'
```

## GraphQL Configuration

Using the GraphQL JS plugin for WebStorm. Download the schemas for the two endpoints using the GraphQL JS UI.

Create a file named `.graphqlconfig` with the following:

```json
{
  "name": "Hasura GraphQL Schema",
  "schemaPath": "schema.graphql",
  "extensions": {
    "endpoints": {
      "Default GraphQL Endpoint": {
        "url": "https://zxplay.org/api/v1/graphql",
        "headers": {
          "user-agent": "JS GraphQL",
          "x-hasura-admin-secret": "<secret>"
        },
        "introspect": false
      }
    }
  }
}
```

## Hasura Deployment Configuration

### Compile Action Service

Tick option to "Forward client headers to webhook".

#### Action definition

```graphql
type Mutation {
  compile (
    basic: String!
  ): CompileResult
}
```

#### New types definition

```graphql
type CompileResult {
  base64Encoded: String!
}
```

#### Handler

```
http://zxbasic/compile/
```
