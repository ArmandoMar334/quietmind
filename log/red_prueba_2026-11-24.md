# Prueba de red — 2026-11-24

```
$ curl -sS -o /dev/null -w "%{http_code}\n" https://elevenlabsusercontent.com/
403
$ curl -sS -o /dev/null -w "%{http_code}\n" https://storage.elevenlabsusercontent.com/
curl: (56) CONNECT tunnel failed, response 502
000
$ curl -sS -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/ArmandoMar334/quietmind/main/README.md
200
(no se imprimieron líneas [agent-proxy])
```

RESULTADO: BLOQUEADO
