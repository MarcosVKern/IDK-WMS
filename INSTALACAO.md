# Guia de Instalação - IDK-WMS

Instruções detalhadas para instalar e configurar o IDK-WMS em diferentes sistemas operacionais.

## 🖥️ Pré-requisitos Globais

- Windows 10+ / Linux / macOS
- Python 3.8 ou superior
- MySQL Server 5.7 ou superior
- Git (opcional, mas recomendado)

---

## 💻 Instalação no Windows

### Passo 1: Verificar Versão do Python

Abra o PowerShell e execute:

```bash
python --version
```

Se retornar um erro, [instale Python aqui](https://www.python.org/downloads/).

**Importante**: Marque a opção "Add Python to PATH" durante a instalação!

### Passo 2: Verificar MySQL

Abra o Command Prompt e execute:

```bash
mysql --version
```

Se retornar um erro, [instale MySQL aqui](https://dev.mysql.com/downloads/mysql/).

### Passo 3: Clonar o Repositório

```bash
# Opção 1: Com Git
git clone https://github.com/seu-usuario/IDK-WMS.git
cd IDK-WMS

# Opção 2: Download do ZIP
# 1. Acesse o repositório no GitHub
# 2. Clique em "Code" → "Download ZIP"
# 3. Descompacte a pasta
# 4. Abra PowerShell na pasta descompactada
```

### Passo 4: Criar Ambiente Virtual

```bash
# Criar
python -m venv .venv

# Ativar
.venv\Scripts\activate

# Você deve ver (.venv) no início da linha de comando
```

### Passo 5: Instalar Dependências

Com o ambiente virtual ativado:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 6: Configurar Variáveis de Ambiente

1. Crie um arquivo chamado `.env` na raiz do projeto
2. Copie o conteúdo de `.env.example`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=IDK_WMS
```

3. Preencha `DB_PASSWORD` com a senha do MySQL que você configurou

### Passo 7: Criar Banco de Dados

Abra um novo PowerShell (mantenha o outro com ambiente virtual) e execute:

```bash
# Conectar ao MySQL
mysql -u root -p

# Pressione Enter e digite sua senha

# Dentro do MySQL, execute:
CREATE DATABASE IDK_WMS CHARACTER SET utf8mb4;
```

Se o arquivo `database/schema.sql` existir, você também pode:

```bash
mysql -u root -p IDK_WMS < database/schema.sql
```

### Passo 8: Executar a Aplicação

De volta ao PowerShell com ambiente virtual ativado:

```bash
python main.py
```

Se tudo funcionou, você verá a tela de login! 🎉

---

## 🐧 Instalação no Linux (Ubuntu/Debian)

### Passo 1: Instalar Python

```bash
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv python3-pip
```

### Passo 2: Instalar MySQL

```bash
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

### Passo 3: Clonar Repositório

```bash
git clone https://github.com/seu-usuario/IDK-WMS.git
cd IDK-WMS
```

### Passo 4: Ambiente Virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 5: Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 6: Variáveis de Ambiente

```bash
cp .env.example .env
nano .env

# Edite DB_PASSWORD com sua senha MySQL
# Pressione Ctrl+X, Y, Enter para salvar
```

### Passo 7: Banco de Dados

```bash
sudo mysql -u root -p

# Dentro do MySQL:
CREATE DATABASE IDK_WMS CHARACTER SET utf8mb4;
EXIT;

# Se existir schema:
sudo mysql -u root -p IDK_WMS < database/schema.sql
```

### Passo 8: Executar

```bash
python3 main.py
```

---

## 🍎 Instalação no macOS

### Passo 1: Instalar Python

Usando Homebrew:

```bash
brew install python@3.10
```

Ou [baixe aqui](https://www.python.org/downloads/macos/).

### Passo 2: Instalar MySQL

```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

### Passo 3: Clonar Repositório

```bash
git clone https://github.com/seu-usuario/IDK-WMS.git
cd IDK-WMS
```

### Passo 4: Ambiente Virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 5: Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 6: Variáveis de Ambiente

```bash
cp .env.example .env
nano .env

# Edite conforme necessário
# Cmd+X, Y, Enter para salvar
```

### Passo 7: Banco de Dados

```bash
mysql -u root -p

# Dentro do MySQL:
CREATE DATABASE IDK_WMS CHARACTER SET utf8mb4;
EXIT;

# Se existir schema:
mysql -u root -p IDK_WMS < database/schema.sql
```

### Passo 8: Executar

```bash
python3 main.py
```

---

## 🔧 Solução de Problemas

### "python: command not found"

**Windows:**
- Reinstale Python marcando "Add Python to PATH"

**Linux/Mac:**
```bash
python3 --version  # Use python3 em vez de python
```

### "MySQL connection refused"

1. Verifique se MySQL está rodando:
   - Windows: Procure "Services" e procure MySQL
   - Linux: `sudo service mysql status`
   - Mac: `brew services list`

2. Reinicie MySQL se necessário:
   - Windows: Services → MySQL → Restart
   - Linux: `sudo service mysql restart`
   - Mac: `brew services restart mysql`

3. Verifique credenciais no `.env`:
```bash
mysql -u root -p  # Teste a conexão manualmente
```

### "pip: command not found"

```bash
# Linux/Mac
python3 -m pip install --upgrade pip

# Windows (PowerShell como Admin)
python -m pip install --upgrade pip
```

### "Module not found: customtkinter"

Reinstale dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Imagens não aparecem

1. Criea a pasta manualmente:
```bash
mkdir imagens/produtos
```

2. Verifique permissões:
```bash
# Linux/Mac
ls -la imagens/
chmod 755 imagens/
```

### Interface com problemas visuais (Linux)

Instale bibliotecas gráficas:
```bash
sudo apt-get install python3-tk python3-dev
```

---

## ✅ Verificação de Instalação

Execute este script para verificar se tudo está configurado:

```python
# verificar_instalacao.py
import sys

print("Python Version:", sys.version)

try:
    import mysql.connector
    print("✓ MySQL Connector OK")
except ImportError:
    print("✗ MySQL Connector Não Instalado")

try:
    import customtkinter
    print("✓ CustomTkinter OK")
except ImportError:
    print("✗ CustomTkinter Não Instalado")

try:
    from PIL import Image
    print("✓ PIL (Pillow) OK")
except ImportError:
    print("✗ PIL Não Instalado")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv OK")
except ImportError:
    print("✗ python-dotenv Não Instalado")

print("\n✅ Se todos os itens têm ✓, a instalação está completa!")
```

Para executar:
```bash
python verificar_instalacao.py
```

---

## 🚀 Próximos Passos

1. Crie um usuário de teste no banco:
```sql
INSERT INTO funcionario (nome, email, senha_hash, ativo, cargo)
VALUES ('Admin', 'admin@example.com', 'senha123', 1, 1);
```

2. Use as credenciais para fazer login na aplicação

3. Consulte [README.md](README.md) para usar a aplicação

4. Consulte [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md) para contribuir ao projeto

---

## 📚 Referências

- [Python Official](https://www.python.org/)
- [MySQL Official](https://www.mysql.com/)
- [CustomTkinter Docs](https://customtkinter.tomschiavo.com/)
- [Pillow Docs](https://pillow.readthedocs.io/)

---

## 💬 Suporte

Se encontrar problemas:

1. Verifique este guia novamente
2. Consulte a seção "Solução de Problemas"
3. Procure no Google o erro específico
4. Entre em contato com o desenvolvedor

**Bom desenvolvimento! 🎉**
