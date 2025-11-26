# API de Sensores FastAPI + SQLite

Esta é uma API REST desenvolvida com FastAPI e SQLite para gerenciamento de dados de sensores IoT.

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional)

## 🚀 Configuração do Ambiente

### 1. Clone o repositório (se aplicável)
```bash
git clone <url-do-repositorio>
cd Backend
```

### 2. Criar e ativar ambiente virtual
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Executando a Aplicação

### 🚀 **Servidor Principal:**
```bash
python3 app.py
```

### 🔧 **Scripts Utilitários:**
```bash
# Recrear banco de dados
python3 scripts/reset_db.py

# Processar dados JSON → Sensores
python3 scripts/Tratar_dados.py
```

### 📡 **Alternativa com uvicorn:**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Acessando a API

Após iniciar o servidor, você pode acessar:

- **API**: http://localhost:8000
- **Documentação interativa (Swagger)**: http://localhost:8000/docs
- **Documentação alternativa (ReDoc)**: http://localhost:8000/redoc

## 🔌 **Integração Raspberry Pi + MQTT**

### 🎯 **Como funciona:**

1. **Raspberry Pi** lê sensores GPIO e publica dados via MQTT
2. **MQTT Service** recebe e salva na tabela `all`
3. **Script processar** lê da tabela `all` e atualiza sensores
4. **Frontend** consulta sensores atualizados

### 📊 **Formato de dados Raspberry Pi:**
```json
{
  "timestamp": "2025-11-06T14:30:00",
  "device_id": "raspberry_pi_001",
  "temperatura": 23.5,
  "umidade": 65.2,
  "luminosidade": 450,
  "botao": false
}
```

### 🔧 **Configuração MQTT:**
- **Broker**: localhost:1883 (Mosquitto)
- **Tópico**: `raspberry/sensores`
- **Formato**: JSON

### 🔌 **Sensores Conectados:**
- **DHT22**: Temperatura e Umidade (GPIO 4)
- **LDR**: Sensor de Luminosidade (GPIO 18)
- **LEDs**: Verde (GPIO 21) e Vermelho (GPIO 20)
- **Botão**: GPIO 16 com pull-up

## �🗄️ Estrutura do Banco de Dados

### Tabela: sensores

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária (auto-incremento) |
| nome | VARCHAR(100) | Nome do sensor |
| tipo | VARCHAR(50) | Tipo do sensor (temperatura, umidade, etc.) |
| valor | FLOAT | Valor atual do sensor |
| unidade | VARCHAR(20) | Unidade de medida (°C, %, hPa, etc.) |

### Tabela: all (dados JSON brutos)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária (auto-incremento) |
| topic | TEXT | Tópico MQTT de origem |
| payload | TEXT | Dados JSON como string |

### Tabela: usuarios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária (auto-incremento) |
| nome | VARCHAR(100) | Nome do usuário |
| email | VARCHAR(100) | Email (único) |
| senha | VARCHAR(100) | Senha do usuário |

## 🔄 Endpoints da API

### GET /
- **Descrição**: Verificar se a API está funcionando
- **Resposta**: Mensagem de confirmação

### GET /sensores
- **Descrição**: Lista todos os sensores
- **Resposta**: Array com todos os sensores

### GET /sensores/{sensor_id}
- **Descrição**: Obtém um sensor específico
- **Parâmetros**: `sensor_id` (int)
- **Resposta**: Dados do sensor

### GET /sensores/tipo/{tipo_sensor}
- **Descrição**: Lista sensores por tipo
- **Parâmetros**: `tipo_sensor` (string)
- **Resposta**: Array com sensores do tipo especificado

### POST /sensores
- **Descrição**: Cria um novo sensor
- **Parâmetros**:
  - `nome` (string, obrigatório)
  - `tipo` (string, obrigatório)
  - `valor` (float, obrigatório)
  - `unidade` (string, obrigatório)
  - `localizacao` (string, opcional)
- **Resposta**: Dados do sensor criado

### PUT /sensores/{sensor_id}
- **Descrição**: Atualiza um sensor existente
- **Parâmetros**: `sensor_id` (int) + campos a atualizar
- **Resposta**: Dados do sensor atualizado

### DELETE /sensores/{sensor_id}
- **Descrição**: Remove um sensor
- **Parâmetros**: `sensor_id` (int)
- **Resposta**: Mensagem de confirmação

## 📁 Estrutura Organizada do Projeto

### 🎯 **Estrutura do Projeto**

```
Backend/
├── 📄 app.py                 # Aplicação principal FastAPI
├── 📄 sensores.db           # Banco de dados SQLite
├── 📄 requirements.txt      # Dependências Python
├── 📄 README.md            # Este arquivo
│
├── 📁 config/              # Configurações do banco de dados
│   └── databaseConfig.py
│
├── 📁 model/               # Modelos de dados (sensores, usuarios)
│   ├── sensoresModel.py
│   └── usuariosModel.py
│
├── 📁 service/             # Serviços de negócio
│   ├── SensoresService.py
│   └── UsuariosService.py
│
├── 📁 controller/          # Controladores REST
│   ├── SensoresController.py
│   └── UsuariosController.py
│
├── 📁 routes/              # Rotas da API
│   ├── sensores_router.py
│   ├── usuarios_router.py
│   └── geral_router.py
│
├── 📁 scripts/             # Scripts utilitários
│   ├── router.py           # Configuração central de rotas
│   ├── reset_db.py         # Recrear banco de dados
│   └── Tratar_dados.py     # Processar dados da tabela 'all'
│
├── 📁 all_module/          # 📦 Módulo dedicado à tabela 'all'
│   ├── __init__.py
│   ├── allModel.py         # Modelo da tabela 'all'
│   ├── AllService.py       # Serviço para dados JSON
│   ├── AllController.py    # Controller REST
│   └── all_router.py       # Rotas da API
│
├── 📁 mqtt_module/         # 📡 Módulo dedicado ao MQTT
│   ├── __init__.py
│   └── MQTTService.py      # Serviço MQTT para Raspberry Pi
│
└── 📁 venv/               # Ambiente virtual Python
```

### 📋 **Funcionalidades por Módulo**

#### 🎯 **Core (Raiz)**
- `app.py`: Aplicação FastAPI principal
- `sensores.db`: Banco SQLite

#### 📊 **Sensores & Usuários**
- **model/**: Definições das tabelas
- **service/**: Lógica de negócio (CRUD)
- **controller/**: Endpoints REST
- **routes/**: Configuração de rotas

#### 📦 **ALL Module** 
- **Propósito**: Gerenciar dados JSON brutos do Raspberry Pi
- **Tabela**: `all` (id, topic, payload)
- **Fluxo**: MQTT → Tabela ALL → Processamento

#### 📡 **MQTT Module**
- **Propósito**: Comunicação com Raspberry Pi
- **Tópico**: `raspberry/sensores`
- **Formato**: `{"temperatura": 50, "umidade": 20}`

#### 🔧 **Scripts**
- **router.py**: Configuração central de todas as rotas
- **reset_db.py**: Limpar e recriar banco
- **Tratar_dados.py**: Processar JSON → Atualizar sensores

### 🔄 **Fluxo de Dados**

```
Raspberry Pi GPIO → MQTT → all_module → scripts/Tratar_dados.py → Sensores
```

1. **Raspberry Pi** lê sensores GPIO e publica no tópico `raspberry/sensores`
2. **MQTT Service** salva JSON na tabela `all`
3. **Tratar_dados.py** processa e atualiza sensores
4. **Frontend** consulta sensores atualizados

### 🚀 **Executar Leitura de Sensores**
```bash
# Script para ler sensores GPIO e publicar via MQTT
python3 sensores_raspberry.py
```

### ✅ **Vantagens da Nova Estrutura**

- ✅ **Organização clara** por responsabilidade
- ✅ **Módulos independentes** (all, mqtt)
- ✅ **Scripts separados** da lógica principal
- ✅ **Fácil manutenção** e extensão
- ✅ **Imports limpos** e organizados

## 🧪 Testando a API

### Exemplos com curl:

1. **Listar todos os sensores:**
```bash
curl -X GET "http://localhost:8000/sensores"
```

2. **Criar um novo sensor:**
```bash
curl -X POST "http://localhost:8000/sensores" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "nome=Sensor Teste&tipo=temperatura&valor=25.0&unidade=°C&localizacao=Sala"
```

3. **Obter sensor específico:**
```bash
curl -X GET "http://localhost:8000/sensores/1"
```

4. **Atualizar sensor:**
```bash
curl -X PUT "http://localhost:8000/sensores/1" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "valor=26.5"
```

5. **Deletar sensor:**
```bash
curl -X DELETE "http://localhost:8000/sensores/1"
```

## 🔧 Desenvolvimento

### Dados de exemplo
O sistema insere automaticamente alguns sensores de exemplo na primeira execução:
- Sensor de temperatura (23.5°C)
- Sensor de umidade (65.2%)
- Sensor de pressão atmosférica (1013.25 hPa)

### Expandindo a API
- Para adicionar novos endpoints, edite o arquivo `app.py`
- Para modificar o modelo de dados, edite `model/sensoresModel.py`
- Para alterar configurações do banco, edite `config/databaseConfig.py`

## 🐛 Resolução de Problemas

### Erro: "python: command not found"
Use `python3` em vez de `python`:
```bash
python3 app.py
```

### Erro de permissão no arquivo de banco
Certifique-se de que o diretório tem permissões de escrita:
```bash
chmod 755 .
```

### Porta já em uso
Altere a porta no arquivo `app.py` ou termine o processo:
```bash
pkill -f "python.*app"
```

## 📝 Notas

- O banco de dados SQLite (`sensores.db`) é criado automaticamente na primeira execução
- O modo `reload=True` permite que mudanças no código sejam aplicadas automaticamente
- Para produção, desabilite o modo debug e configure adequadamente o host

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request