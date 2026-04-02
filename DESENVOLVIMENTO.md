# Guia de Desenvolvimento - IDK-WMS

Este documento fornece orientações para desenvolvedores que desejam contribuir ao projeto IDK-WMS.

## 📚 Entendendo a Arquitetura

### Camada Model
Representa entidades do sistema:
```python
# model/produto.py
class Produto:
    def __init__(self, id, nome, descricao, imagem):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._imagem = imagem
```

### Camada DAO (Data Access Object)
Abstração de acesso a dados:
```python
# model/dao/produto_dao.py
class Produto_DAO(Base_DAO):
    def save(self, produto: Produto):
        # Inserir no banco
        
    def get_by_id(self, id):
        # Recuperar do banco
        
    def update(self, produto: Produto):
        # Atualizar no banco
```

### Camada Controller
Orquestração de lógica de negócio:
```python
# control/produto_controller.py
class Produto_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        
    def add_produto(self):
        # Validar entrada
        # Chamar DAO
        # Atualizar view
```

### Camada View
Interface gráfica:
```python
# view/produto_view.py
class Produto_View:
    def __init__(self, parent=None):
        self.root = tk.Toplevel() if parent is None else tk.Frame(parent)
        # Criar widgets
```

---

## 🎨 Padrões de Código

### Criação de Nova Funcionalidade

1. **Criar Model** (`model/minha_entidade.py`)
```python
class MinhaEntidade:
    def __init__(self, id, nome, valor):
        self._id = id
        self._nome = nome
        self._valor = valor
```

2. **Criar DAO** (`model/dao/minha_entidade_dao.py`)
```python
class MinhaEntidade_DAO(Base_DAO):
    def save(self, entidade):
        sql = "INSERT INTO tabela (nome, valor) VALUES (%s, %s)"
        # ... executar
        
    def get_all(self):
        sql = "SELECT * FROM tabela"
        # ... executar
```

3. **Criar Controller** (`control/minha_entidade_controller.py`)
```python
class MinhaEntidade_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        
    def listar(self):
        dados = self.dao.get_all()
        self.view.popular_tabela(dados)
```

4. **Criar View** (`view/minha_entidade_view.py`)
```python
class MinhaEntidade_View:
    def __init__(self, parent=None):
        # Inicializar UI
        
    def popular_tabela(self, dados):
        # Preencher widgets
```

5. **Registrar em Main Controller** (`control/main_controller.py`)
```python
def exibir_minha_entidade(self, parent_frame=None):
    dao = MinhaEntidade_DAO(self.db_config)
    view = MinhaEntidade_View(parent=parent_frame)
    control = MinhaEntidade_Controller(dao, view)
    if parent_frame:
        view.display()
    else:
        view.run()
```

---

## 🎯 Convenções de Nomenclatura

### Arquivos e Classes
- Use **PascalCase** para nomes de classe: `ProdutoController`, `EstoqueView`
- Use **snake_case** para nomes de arquivo: `produto_controller.py`, `estoque_view.py`

### Variáveis e Métodos
- Use **snake_case**: `id_produto`, `exibir_detalhes()`, `validar_entrada()`
- Prefixo privado com `_`: `_validar_nome()`, `_get_pasta_imagens_absoluta()`

### Propriedades de Classe
- Use `_` no início: `self._nome`, `self._id`, `self._descricao`

### Cores
Sempre use a paleta em `Cores_Padrao`:
```python
from view.cores_padrao import Cores_Padrao

# Buttons
fg_color=Cores_Padrao.COR_BOTAO_SALVAR
hover_color=Cores_Padrao.COR_BOTAO_SALVAR_HOVER
text_color=Cores_Padrao.COR_TEXTO_BOTAO

# Backgrounds
bg=Cores_Padrao.COR_FUNDO
```

---

## 🎪 Notificações ao Usuário

Sempre use o sistema de notificações:
```python
from view.notificacao import Notificacao

# Sucesso
Notificacao.sucesso("Sucesso", "Produto salvo!", parent=self.root)

# Erro
Notificacao.erro("Erro", "Não foi possível salvar!", parent=self.root)
```

---

## 🖼️ Sistema de Imagens

### Padrão de Armazenamento
- Apenas **nomes de arquivo** são salvos no banco de dados
- Exemplo: `"fotoProduto.png"` (não o caminho completo)

### Carregamento Dinâmico
```python
def _get_pasta_imagens_absoluta(self):
    """Resolve o caminho absoluto dinamicamente"""
    return self._get_caminho_absoluto("imagens/produtos")

def _exibir_imagem(self, nome_arquivo):
    """Exibe imagem usando o path dinâmico"""
    caminho_absoluto = os.path.join(self._get_pasta_imagens_absoluta(), nome_arquivo)
    # ... carregar e exibir
```

### Placeholder
- Criado automaticamente se não existir
- Localizado em: `imagens/produtos/placeholder.png`
- Exibido quando: arquivo não encontrado, null, ou erro

---

## 🔄 Fluxos de Movimentação

### Estrutura de Transição de Status

Cada tipo tem seu próprio fluxo:
```python
# Entrada: 1
# Pendente → Efetivado
# Ao Efetivado: += quantidade

# Saída: 2
# Pendente → Em separação → Despachado
# Ao Despachado: -= quantidade

# Interno: 3
# Pendente → Em separação → Despachado → Efetivado
# Ao Despachado: -= origem
# Ao Efetivado: += destino
```

### Implementação
```python
def _obter_proximo_status(self, tipo_id, status_atual):
    """Determina próximo status baseado no tipo"""
    if tipo_id == 1:  # Entrada
        return "Efetivado"
    elif tipo_id == 2:  # Saída
        # Lógica para Saída
    elif tipo_id == 3:  # Interno
        # Lógica para Interno

def _aplicar_logica_estoque(self, movimento, tipo_id, status_novo):
    """Aplica mudanças de estoque baseado no tipo e status"""
    if tipo_id == 1 and status_novo == "Efetivado":
        # Adicionar estoque
    elif tipo_id == 2 and status_novo == "Despachado":
        # Remover estoque
```

---

## 🧪 Testing e Debug

### Debug Print
Para debug rápido durante desenvolvimento:
```python
print(f"[DEBUG] Variável: {valor}")
```

**Importante**: Remova todos os debugs antes de fazer commit!

### Validação de Sintaxe
```bash
python -m py_compile arquivo.py
```

### Teste em Desenvolvimento
```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Rodar aplicação
python main.py
```

---

## 📋 Checklist para Novas Features

- [ ] Model criado (`model/minha_entidade.py`)
- [ ] DAO criado (`model/dao/minha_entidade_dao.py`)
- [ ] Controller criado (`control/minha_entidade_controller.py`)
- [ ] View criada (`view/minha_entidade_view.py`)
- [ ] Registrado em `main_controller.py`
- [ ] Usa cores de `Cores_Padrao`
- [ ] Usa `Notificacao` para feedback
- [ ] Sem debug prints
- [ ] Sintaxe validada com `py_compile`
- [ ] Testado manualmente

---

## 🐛 Corrigindo Bugs

1. **Reproduzir o bug**: Encontre passos claros para reproduzir
2. **Adicionar debug**: Use `print()` para rastrear a execução
3. **Identificar causa**: Veja onde exatamente ocorre o erro
4. **Implementar fix**: Corrija o código
5. **Testar**: Certifique-se que o bug foi resolvido
6. **Remover debugs**: Limpe todos os prints antes de commit

---

## 📚 Recursos Úteis

### CustomTkinter
- [Documentação Oficial](https://customtkinter.tomschiavo.com/)
- Buttons, Labels, Entry, Combobox, etc

### Tkinter
- [Python tkinter Tutorial](https://realpython.com/tkinter-gui-tutorial-python/)
- Widgets base e layout managers

### MySQL Python
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
- Conexão e queries com banco

### PIL (Pillow)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- Manipulação e carregamento de imagens

---

## 🚀 Commits e Versionamento

### Formato de Commit
```
git commit -m "Tipo: Descrição breve"

# Exemplos:
# Fix: Corrige bug de imagem não aparecer
# Feature: Adiciona filtro por data em movementos
# Refactor: Simplifica lógica de validação
# Docs: Atualiza README com instruções de setup
```

### Branch Naming
```
feature/nome-da-feature
fix/descricao-do-bug
refactor/o-que-foi-refatorado
```

---

## 💡 Boas Práticas

✅ **Faça:**
- Use nomes descritivos para funções e variáveis
- Mantenha métodos pequenos e focados
- Valide entrada do usuário
- Trate exceções apropriadamente
- Use constantes em vez de magic numbers
- Escriva código legível e bem organizado

❌ **Evite:**
- Hard-coded values
- Funções muito longas
- Nomes genéricos como `x`, `temp`, `data`
- Validação apenas no controller
- Deixar debugs no código
- Fazer múltiplas responsabilidades em uma função

---

## 📞 Dúvidas?

Consulte:
1. Código existente similar
2. Esta documentação
3. Docstrings das funções
4. Comentários no código

Happy coding! 🎉
