# LAB 1 — Sistema de Chat com Deteção de Dados Pessoais (GDPR)

Sistema de chat multiutilizador em Python com deteção automática de dados pessoais (GDPR) e registo de tentativas de engenharia social.

---

## Estrutura do Projeto

```
laboratorio1/
├── servidor.py     # Servidor de chat (iniciar primeiro)
├── cliente.py      # Cliente de chat (pode-se correr o mesmo ficheiro várias vezes)
├── capturas.json   # Criado automaticamente — todos os registos de deteção
└── README.md
```

---

## Como Executar

### 1. Iniciar o Servidor

```bash
python3 servidor.py
```

O servidor fica à escuta na porta **5555**. Manter este terminal aberto.

### 2. Ligar Clientes (em terminais separados)

```bash
python3 cliente.py
```

Abrir vários terminais com `python3 cliente.py` para simular múltiplos utilizadores.

---

## Funcionalidades

### Chat Multiutilizador
- Múltiplos clientes ligam-se simultaneamente ao servidor
- Cada cliente corre numa thread independente (sem bloquear os outros)
- Mensagens de broadcast chegam a todos os utilizadores ligados
- Notificação automática quando alguém entra ou sai do chat

### Comandos disponíveis no cliente

| Comando | Descrição |
|---|---|
| `/users` | Lista os utilizadores online |
| `/w <username> <mensagem>` | Envia mensagem privada (DM) |
| `/consent on\|off` | Ativa/desativa o consentimento GDPR |
| `/help` | Mostra a lista de comandos |
| `exit` | Desliga do servidor |

### Deteção de Dados Pessoais (GDPR)

O servidor usa **regex** para detetar automaticamente:

| Tipo | Exemplo |
|---|---|
| E-mail | `pedro@email.com` |
| Telefone (PT) | `912 345 678` / `+351912345678` / `912-345-678` |
| Endereço IP | `192.168.1.1` |
| Nome completo | `Pedro Mota` |
| Data de nascimento | `01/01/2000` |
| Cartão de crédito | Validado pelo algoritmo de Luhn |
| Divulgação de credenciais | `password é abc123`, `iban: PT50...`, `pin=1234` |

Quando dados pessoais são detetados:
- A mensagem é **bloqueada** — não chega aos outros utilizadores
- O remetente recebe um **alerta GDPR** com os dados detetados
- Se tiver consentimento ativo, o evento é guardado em `capturas.json`

### Deteção de Divulgação de Credenciais

O sistema deteta mensagens onde o utilizador está a revelar ativamente um valor sensível através do padrão **palavra-chave + conector + valor**:

- Palavras-chave: `password`, `palavra-passe`, `iban`, `pin`, `otp`, `token`, `codigo`, `cvv`, `nib`
- Conectores aceites: `é`, `e`, `eh`, `:`, `=`, `->`, `sera`, `será`, `is`, `foi`

Exemplos bloqueados: `"password é abc123"`, `"o meu iban: PT50..."`, `"pin=1234"`

### Engenharia Social

O servidor analisa **todas** as mensagens à procura de padrões suspeitos, independentemente de terem dados GDPR ou não:

- Palavras-chave de manipulação: `urgente`, `password`, `pin`, `otp`, `token`, `iban`, etc.
- Múltiplos tipos de dados pessoais na mesma mensagem
- Pedido de dados de cartão combinado com código/pin

Quando detetado, o evento é registado em `capturas.json` e um aviso aparece nos logs do servidor.

### Consentimento GDPR
No início da ligação, o utilizador é questionado se aceita que os dados detetados sejam guardados. Pode alterar a qualquer momento com `/consent on|off`. Sem consentimento, a mensagem continua a ser bloqueada mas **não é persistida** em disco.

### Ficheiro de Capturas (`capturas.json`)

Todos os eventos são guardados no mesmo ficheiro. O campo `"tipo"` distingue a origem de cada registo:

```json
[
  {
    "tipo": "gdpr",
    "timestamp": "2024-01-15T10:30:00Z",
    "username": "pedro",
    "canal": "broadcast",
    "mensagem": "o meu email é pedro@email.com",
    "deteções": { "emails": ["pedro@email.com"] }
  },
  {
    "tipo": "gdpr",
    "timestamp": "2024-01-15T10:31:00Z",
    "username": "pedro",
    "canal": "broadcast",
    "mensagem": "password é abc123",
    "deteções": { "divulgacao_credenciais": ["password é abc123"] }
  },
  {
    "tipo": "engenharia_social",
    "timestamp": "2024-01-15T10:32:00Z",
    "username": "pedro",
    "razoes": ["palavras-chave suspeitas: urgente, password"],
    "mensagem": "urgente! envia a tua password"
  }
]
```

---

## Tecnologias Utilizadas

- **Python 3** — linguagem principal
- **`socket`** — comunicação TCP entre cliente e servidor
- **`threading`** — suporte a múltiplos clientes simultâneos
- **`re` (regex)** — deteção de dados pessoais e padrões suspeitos
- **`logging`** — logs de conexões e eventos no terminal do servidor
- **`json`** — persistência das capturas em `capturas.json`
