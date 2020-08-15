# Stream Chat Python Token Server

### Quick-start

Clone the repository and run `pip install -r requirements.txt` within the root directory. Create a `.env` file within the main directory with the environment variables found on https://getstream.io/dashboard:

```
USERNAME=
PASSWORD=

STREAM_API_KEY=<YOUR_API_KEY>
STREAM_API_SECRET=<YOUR_API_SECRET>
```

> Note: You can reference `.env.example`.
USERNAME and PASSWORD are used for Basic HTTP Authentication


### Retrieving a Token

To retrieve a token, hit the `/v1/token` endpoint with an HTTP `POST` with the following JSON payload:

```json
{
	"id": userID,
	"name": userName
}
```

```python
# json payload format {"id": " " , "name": " "}
# auth format (username, password)
r = requests.post(url, json=payload, auth=auth)
```
