#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost:4545"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

PASS=0
FAIL=0

req() {
  local name="$1" expected_status="$2" method="$3" path="$4" data="${5:-}" ctype="${6:-application/json}" auth="${7:-}"
  local body_file="$TMP_DIR/body.json"
  local head_file="$TMP_DIR/headers.txt"

  local -a curl_args=("-sS" "-i" "-X" "$method" "$BASE_URL$path")
  if [[ -n "$auth" ]]; then
    curl_args+=("-H" "Authorization: $auth")
  fi
  if [[ -n "$ctype" ]]; then
    curl_args+=("-H" "Content-Type: $ctype")
  fi
  if [[ -n "$data" ]]; then
    curl_args+=("-d" "$data")
  fi

  curl "${curl_args[@]}" > "$TMP_DIR/resp.txt"
  awk 'BEGIN{h=1} h&&/^\r?$/{h=0;next} h{print} !h{print > body}' body="$body_file" "$TMP_DIR/resp.txt" > "$head_file"

  local status
  status="$(head -n1 "$head_file" | awk '{print $2}')"

  if [[ "$status" != "$expected_status" ]]; then
    echo "[FAIL] $name: esperado $expected_status, obtido $status"
    ((FAIL++))
    return 1
  fi

  echo "[OK] $name ($status)"
  ((PASS++))
  return 0
}

json_has() {
  local expr="$1"
  jq -e "$expr" "$TMP_DIR/body.json" >/dev/null
}

contains_header() {
  local header="$1"
  grep -qi "^$header" "$TMP_DIR/headers.txt"
}

echo "A correr matriz de testes..."

req "1 GET /api/marcas" "200" "GET" "/api/marcas"
json_has '.marcas | type=="array" and length>0'

req "2 GET /api/cars?brand=Toyota" "200" "GET" "/api/cars?brand=Toyota"
json_has '.brand=="Toyota" and (.results|length>0)'

req "3 GET /api/cars" "200" "GET" "/api/cars"
json_has '.results|type=="array" and length==0'

req "4 POST /api/login válido" "200" "POST" "/api/login" '{"username":"admin","password":"secret"}'
json_has 'has("token")'

req "5 POST /api/login inválido" "401" "POST" "/api/login" '{"username":"admin","password":"wrong"}'
json_has '.error=="invalid_credentials"'

req "6 POST /api/users duplicado" "409" "POST" "/api/users" '{"name":"x","email":"exists@example.com","age":20}'
json_has '.error=="email_exists"'

req "7 POST /api/users sucesso" "201" "POST" "/api/users" '{"name":"x","email":"new@example.com","age":20}'
contains_header 'Location: /api/users/'
json_has '.id and .status=="created"'

req "8 POST /api/temperature sem value" "400" "POST" "/api/temperature" '{"sensor_id":"s1"}'
json_has '.error=="missing_field"'

req "9 POST /api/temperature com value" "201" "POST" "/api/temperature" '{"sensor_id":"s1","value":22.5}'
json_has '.status=="created"'

req "10 POST /api/tasks duplicada" "409" "POST" "/api/tasks" '{"title":"duplicate"}'
json_has '.error=="duplicate_task"'

req "11 POST /api/tasks sucesso" "201" "POST" "/api/tasks" '{"title":"normal"}'
contains_header 'Location: /api/tasks/'
json_has '.id and .status=="created"'

req "12 POST /api/auth válido" "200" "POST" "/api/auth" '{"username":"user1","password":"pass1"}'
json_has 'has("token") and has("expires_in")'

req "13 GET /api/profile com token" "200" "GET" "/api/profile" "" "application/json" "Bearer validtoken"
json_has '.username and .email'

req "14 GET /api/profile sem token" "403" "GET" "/api/profile"
json_has '.error=="forbidden"'

req "15 POST sem Content-Type" "415" "POST" "/api/qualquer" '{"a":1}' ""
json_has '.error=="unsupported_media_type"'

req "16 GET fallback" "404" "GET" "/nao-definido"
json_has '.error=="not_found"'

echo ""
echo "Resumo: PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" -eq 0 ]]
