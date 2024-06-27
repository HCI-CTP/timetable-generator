# timetable-generator

[comment]: <> (write the actual instructions here)

## Required File Organisation (Hidden Files)
```
data
|-- hcihs_24t2_cleaned.db (or other relevant files)
|
secrets
|-- isphs-auth.json
!-- service-credentials.json
```

### Hidden Files
#### `hcihs_24t2_cleaned.db`
Cleaned Timetable Data 

#### `isphs-auth.json`
JSON File for authentication and retrieval of cookies

```json
{
    "username": <your username>,
    "password": <your password>
}
```

#### `service-credentials.json`
Contact me to create a service account to use the Google Calendar. 

I will send you a JSON File for the OAuth2.0 JSON Credentials, rename to `service-credentials.json`