# openapi-ext-tools

extended tools for openapi spec

## bundle multiple yaml files into single openapi.yaml

```bash
$ openapi-spec-cli --help
usage: openapi-spec-cli [-h] --spec-path SPEC_PATH
                        [--bundled-spec-path BUNDLED_SPEC_PATH] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --spec-path SPEC_PATH
                        set path to openapi spec file
  --bundled-spec-path BUNDLED_SPEC_PATH
                        set path to bundled spec file
  --verbose             set verbose mode
```

### How to use

**Currently, bundling only support components object.**

The `tests/fixtures/simple/openapi.yaml` is openapi specification file and a part of schemas is defined in `tests/fixtures/simple/schemas.yaml`.

```yaml
...
    content:
      application/json:
        schema:
          $ref: 'schemas.yaml#/components/schemas/User'
...
```

For example, *User* schema is defined like this.

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          format: int64
        username:
          type: string
        firstName:
          type: string
        lastName:
          type: string
        birthday:
          type: string
          format: date
        email:
          type: string
        password:
          type: string
        phone:
          type: string
        userStatus:
          type: integer
          description: User Status
          format: int32
```

Run `openapi-spec-cli` to bundle yaml files and create single `openapi.yaml`.

```bash
$ openapi-spec-cli --spec-path tests/fixtures/simple/openapi.yaml
2019-05-11 11:56:12,337 openapi.spec.ext INFO wrote bundled spec file to "bundled_openapi.yaml"
2019-05-11 11:56:12,402 openapi.spec.ext INFO validating bundled spec: OK
```

You can confirm `bundled_openapi.yaml` in current directory. Then, all schemas in `schemas.yaml` are moved to `bundled_openapi.yaml` and a `$ref` field also reffers as Local Reference.

```yaml
...
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
...
```
