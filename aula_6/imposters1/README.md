# Aula 6 - Imposter 1

## Escopo
- Exercícios 0 a 15 (stubs HTTP com predicados específicos + fallbacks)
- Porta: `4545`

## Ficheiros
- `imposter_empty.json` (Ex. 0)
- `imposter.json` (configuração final)
- `test_imposter.sh` (matriz de testes)

## Execução
```bash
cd /Users/pedro/Documents/pedro_mota_exercicios_pac2025/aula_6/imposters1
mb restart --configfile imposter.json
./test_imposter.sh
```

## Verificação Ex. 0
```bash
mb restart --configfile imposter_empty.json
curl -i http://localhost:4545/qualquer/caminho
```

## Resultado
- Matriz validada: `PASS=16` `FAIL=0`
