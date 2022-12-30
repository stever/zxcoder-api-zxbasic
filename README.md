![Boriel ZX Basic](img/zxbasic_logo.png)

# ZX Play API for ZX Basic

## Development start

### Initial project setup

```bash
git clone https://github.com/stever/zxplay-api-zxbasic.git
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
docker build -t ghcr.io/stever/zxplay-api-zxbasic .
docker push ghcr.io/stever/zxplay-api-zxbasic
```

## Run Locally

```bash
docker run \
  --env=API_URL=https://zxplay.org/api/v1/graphql \
  --publish=80:8000 \
  --detach=true \
  --name=zxplay-api-zxbasic \
  ghcr.io/stever/zxplay-api-zxbasic
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
