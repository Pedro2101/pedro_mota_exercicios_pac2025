#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost:4546"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

PASS=0
FAIL=0

req() {
  local name="$1" expected="$2" method="$3" path="$4" data="${5:-}" extra_header="${6:-}"
  local out="$TMP_DIR/resp.txt"
  local headers="$TMP_DIR/headers.txt"
  local body="$TMP_DIR/body.json"

  local -a args=("-sS" "-i" "-X" "$method" "$BASE_URL$path")
  if [[ -n "$extra_header" ]]; then args+=("-H" "$extra_header"); fi
  if [[ -n "$data" ]]; then
    args+=("-H" "Content-Type: application/json" "-d" "$data")
  fi

  curl "${args[@]}" > "$out"
  awk 'BEGIN{h=1} h&&/^\r?$/{h=0;next} h{print > hf; next} {print > bf}' hf="$headers" bf="$body" "$out"
  local got
  got="$(head -n1 "$headers" | awk '{print $2}')"
  if [[ "$got" == "$expected" ]]; then
    echo "[OK] $name ($got)"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $name esperado=$expected obtido=$got"
    FAIL=$((FAIL + 1))
  fi
}

echo "A correr testes REST (imposters2)..."

req "GET /api/alunos" 200 GET /api/alunos
req "POST /api/alunos idade invalida" 400 POST /api/alunos '{"nome":"Z","idade":9,"curso":"Engenharia"}'
req "DELETE /api/alunos/1 sem admin" 403 DELETE /api/alunos/1
req "DELETE /api/alunos/1 com admin" 200 DELETE /api/alunos/1 '' 'x-role: admin'

req "GET /api/produtos/10" 200 GET /api/produtos/10
req "POST /api/produtos quantidade negativa" 400 POST /api/produtos '{"nome":"X","preco":1,"quantidade":-2}'
req "DELETE /api/produtos/10 stock>0" 409 DELETE /api/produtos/10
req "DELETE /api/produtos/11 stock=0" 200 DELETE /api/produtos/11

req "POST /api/reservas datas erradas" 400 POST /api/reservas '{"cliente":"A","checkin":"2026-05-10","checkout":"2026-05-01","tipo_quarto":"duplo"}'
req "POST /api/reservas quarto cheio" 409 POST /api/reservas '{"cliente":"A","checkin":"2026-07-01","checkout":"2026-07-02","tipo_quarto":"suite"}'
req "POST /api/reservas valida" 201 POST /api/reservas '{"cliente":"A","checkin":"2026-07-01","checkout":"2026-07-02","tipo_quarto":"duplo"}'

req "POST /api/emprestimos livro emprestado" 409 POST /api/emprestimos '{"cliente":"A","livro_id":302,"data_emprestimo":"2026-05-06"}'
req "PUT devolucao sem emprestimo" 404 PUT /api/emprestimos/999/devolucao
req "DELETE /api/livros/302 emprestado" 409 DELETE /api/livros/302

req "POST /api/funcionarios salario baixo" 400 POST /api/funcionarios '{"nome":"A","cargo":"Dev","salario":700}'
req "PUT salario abaixo minimo" 400 PUT /api/funcionarios/501/salario '{"salario":700}'
req "DELETE funcionario pendente" 409 DELETE /api/funcionarios/501

req "POST /api/tarefas titulo vazio" 400 POST /api/tarefas '{"titulo":"","descricao":"x"}'
req "DELETE tarefa pendente" 409 DELETE /api/tarefas/601
req "DELETE tarefa concluida" 200 DELETE /api/tarefas/602

req "POST /api/pedidos cliente inexistente" 404 POST /api/pedidos '{"cliente_id":999,"produto":"Livro","quantidade":1}'
req "POST /api/pedidos quantidade invalida" 400 POST /api/pedidos '{"cliente_id":701,"produto":"Livro","quantidade":0}'
req "PUT /api/pedidos/802 estado invalido" 400 PUT /api/pedidos/802 '{"estado":"Cancelado"}'
req "DELETE /api/pedidos/802 em processamento" 200 DELETE /api/pedidos/802

echo "Resumo PASS=$PASS FAIL=$FAIL"
[[ "$FAIL" -eq 0 ]]
