# IDK-WMS - Sistema de Gerenciamento de Warehouse

Um sistema completo de gerenciamento de armazém desenvolvido em Python com interface gráfica Tkinter + CustomTkinter, designed para otimizar operações de estoque, movimentações e gestão de produtos.

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Fluxos de Negócio](#fluxos-de-negócio)
- [License](#license)

---

## 🎯 Funcionalidades

### Gerenciamento de Produtos
- ✅ Criar, atualizar e deletar produtos
- ✅ Suporte a imagens de produtos com sistema de placeholder dinâmico
- ✅ Descrição e metadados de produtos
- ✅ Armazenamento de apenas nomes de arquivo (paths resolvidas dinamicamente)

### Gerenciamento de Estoque
- ✅ Visualizar níveis de estoque em tempo real
- ✅ Filtrar por produto, armazém e unidade de armazenamento
- ✅ Detalhes completos do estoque com imagem do produto
- ✅ Consulta rápida de disponibilidade

### Movimentações de Estoque
- ✅ Três tipos de movimento: **Entrada**, **Saída**, **Interno**
- ✅ Fluxo de status completo para cada tipo
- ✅ Atualização automática de estoque baseada no tipo e status
- ✅ Cancelamento de movimentos com reversão automática
- ✅ Histórico de movimentações
- ✅ Detalhes com visualização de produtos movimentados

### Gerenciamento de Usuários
- ✅ Autenticação com email/senha
- ✅ Sistema de cargos (Gerente, Operador Entrada, Operador Saída, etc)
- ✅ Ativar/Bloquear funcionários
- ✅ Rastreamento de responsáveis por operações

### Estrutura de Armazém
- ✅ Múltiplos armazéns
- ✅ Unidades de armazenamento por armazém
- ✅ Melhor organização de espaço
- ✅ Suporte para diferentes tipos de unidades

### Logs e Auditoria
- ✅ Log automático de todas as alterações
- ✅ Rastreamento de data/hora de atualizações
- ✅ Identificação do responsável pelas operações

---

## 🔧 Pré-requisitos

- Python >= 3.8
- MySQL Server 5.7+
- Conexão de internet (para instalação de dependências)

---

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone <seu-repositorio>
cd IDK-WMS
```

### 2. Criar e ativar ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Criar arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=IDK_WMS
```

### 5. Criar banco de dados

```bash
mysql -u root -p < database/schema.sql
```

### 6. Executar a aplicação

```bash
python main.py
```

---

## 🚀 Uso

### Login
- Acesse a tela de login com email e senha de um funcionário cadastrado
- O sistema validará as credenciais no banco de dados

### Navegação Principal
A interface principal oferece acesso via menu a:
- **Produtos**: CRUD completo de produtos com imagens
- **Estoque**: Consulta e visualização de níveis
- **Movimentações**: Gerenciar entradas, saídas e movimentos internos
- **Funcionários**: Gerenciar usuários do sistema
- **Armazéns**: Configurar estrutura de armazém
- **Unidades de Armazenamento**: Organizar espaços
- **Cargos**: Gerenciar permissões por cargo

### Fluxo de Movimentação
1. Criar novo movimento
2. Selecionar tipo (Entrada/Saída/Interno)
3. Adicionar produtos com quantidades
4. Atualizar status conforme necessário
5. Sistema atualiza estoque automaticamente
6. Visualizar histórico completo

---

## 📁 Estrutura do Projeto

```
IDK-WMS/
├── main.py                          # Ponto de entrada da aplicação
├── requirements.txt                 # Dependências do projeto
├── .env.example                     # Template de variáveis de ambiente
│
├── control/                         # Controllers (Business Logic)
│   ├── __init__.py
│   ├── main_controller.py          # Orquestração principal
│   ├── produto_controller.py       # Lógica de produtos
│   ├── estoque_controller.py       # Lógica de estoque
│   ├── movimento_estoque_controller.py  # Lógica de movimentos
│   ├── funcionarios_controller.py  # Lógica de usuários
│   ├── armazem_controller.py       # Lógica de armazéns
│   ├── unidade_armazenamento_controller.py
│   └── cargos_controller.py        # Lógica de cargos
│
├── model/                           # Models (Data Objects)
│   ├── __init__.py
│   ├── produto.py
│   ├── estoque.py
│   ├── movimento_estoque.py
│   ├── funcionario.py
│   ├── armazem.py
│   ├── cargo.py
│   ├── unidade_armazenamento.py
│   ├── tipo_movimento.py
│   ├── log_atualizacao.py
│   └── dao/                        # Data Access Objects
│       ├── __init__.py
│       ├── base_dao.py            # Base DAO com conexão
│       ├── produto_dao.py
│       ├── estoque_dao.py
│       ├── movimento_estoque_dao.py
│       ├── funcionario_dao.py
│       ├── armazem_dao.py
│       ├── cargo_dao.py
│       ├── unidade_armazenamento_dao.py
│       ├── tipo_movimento_dao.py
│       ├── log_atualizacao_dao.py
│       └── produto_movimento_dao.py
│
├── view/                            # Views (UI)
│   ├── __init__.py
│   ├── main_view.py                # Tela principal
│   ├── produto_view.py             # CRUD de produtos
│   ├── estoque_view.py             # Consulta de estoque
│   ├── estoque_detalhe_view.py     # Detalhes do estoque
│   ├── movimento_estoque_view.py   # Movimentações
│   ├── movimento_estoque_detalhe_view.py
│   ├── movimento_estoque_produtos_view.py
│   ├── funcionarios_view.py        # Gerenciar usuários
│   ├── armazem_view.py             # Gerenciar armazéns
│   ├── unidade_armazenamento_view.py
│   ├── cargos_view.py              # Gerenciar cargos
│   ├── cores_padrao.py             # Paleta de cores
│   └── notificacao.py              # Sistema de notificações
│
├── imagens/                         # Recursos de mídia
│   └── produtos/                   # Imagens de produtos
│       └── placeholder.png         # Placeholder padrão
│
└── database/                        # Scripts de banco de dados
    └── schema.sql                  # Schema inicial
```

---

## 🏗️ Arquitetura

### Padrão MVC (Model-View-Controller)

A aplicação segue o padrão arquitetural MVC:

- **Model**: Objetos que representam entidades do sistema
- **View**: Interface gráfica Tkinter
- **Controller**: Lógica de negócio e orquestração
- **DAO**: Camada de acesso a dados

### Fluxo de Dados

```
User Interface (View)
        ↓
   Controller (Business Logic)
        ↓
   DAO (Data Access)
        ↓
   Database (MySQL)
```

### Gerenciamento de Imagens

- **Sistema Dinâmico**: Apenas nomes de arquivo são armazenados no BD
- **Resolução de Path**: Caminhos são resolvidos em runtime
- **Placeholder Automático**: Se arquivo não existir, exibe placeholder
- **Validação**: Apenas PNG e JPG aceitos

---

## 🛠️ Tecnologias

### Backend
- **Python 3.8+**: Linguagem principal
- **MySQL**: Banco de dados relacional
- **python-dotenv**: Gerenciamento de variáveis de ambiente

### Frontend
- **Tkinter**: Framework GUI padrão Python
- **CustomTkinter**: Extensão moderna do Tkinter
- **Pillow (PIL)**: Processamento de imagens

### Padrões de Design
- **MVC Pattern**: Separação de responsabilidades
- **DAO Pattern**: Abstração de acesso a dados
- **Singleton Pattern**: Conexão com banco de dados

---

## 📊 Fluxos de Negócio

### Fluxo de Entrada

```
Criar Movimento (Tipo: Entrada)
    ↓
Status: Pendente
    ↓
Clicar "Atualizar"
    ↓
Status: Efetivado
    ↓
Estoque Aumenta (+ quantidade)
```

### Fluxo de Saída

```
Criar Movimento (Tipo: Saída)
    ↓
Status: Pendente
    ↓
Clicar "Atualizar"
    ↓
Status: Em separação
    ↓
Clicar "Atualizar" + Confirmação
    ↓
Status: Despachado
    ↓
Estoque Diminui (- quantidade)
```

### Fluxo Interno

```
Criar Movimento (Tipo: Interno)
    ↓
Status: Pendente → Em separação → Despachado → Efetivado
    ↓
Estoque Remove da Origem (em Despachado)
    ↓
Estoque Adiciona no Destino (em Efetivado)
```

### Cancelamento

Regras de cancelamento por tipo e status:
- **Entrada/Efetivado**: Remove do destino
- **Saída/Despachado**: Adiciona em origem
- **Interno/Despachado**: Adiciona em origem
- **Interno/Efetivado**: ❌ NÃO PERMITIDO

---

## 🔐 Segurança

- ✅ Autenticação obrigatória
- ✅ Validação de cargos para operações
- ✅ Rastreamento de quem fez cada alteração
- ✅ Validação de entrada em todos os campos
- ✅ Proteção contra operações inválidas

---

## 📝 Logs e Auditoria

Todos os eventos são registrados em `log_atualizacao`:
- Usuário responsável
- Data/hora precisa
- Tipo de operação
- Entidade modificada
- Valor anterior e novo

---

## 🐛 Troubleshooting

### Erro de Conexão ao Banco

```bash
# Verificar se MySQL está rodando
mysql -u root -p

# Verificar variáveis de ambiente
# Certifique-se de que .env existe com credenciais corretas
```

### Imagens não aparecem

1. Verifique se a pasta `imagens/produtos/` existe
2. Certifique-se de que placeholder.png foi criado
3. Valide se os arquivos têm permissão de leitura

### Interface com problemas visuais

```bash
# Reinstale CustomTkinter
pip install --upgrade customtkinter
```

---

## 👥 Contribuições

Relatórios de bugs e sugestões são bem-vindos! Por favor, abra uma issue no repositório.

---

## 📄 License

Projeto desenvolvido como trabalho integrador SENAC - 2026

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação interna ou entre em contato com o time de desenvolvimento.
