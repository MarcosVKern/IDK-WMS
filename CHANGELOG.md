# Changelog - IDK-WMS

Todos os mudanças notáveis neste projeto estão documentadas neste arquivo.

## [1.0.0] - 2026-04-02

### Adicionado - Versão Final Completa

#### Gerenciamento de Produtos
- ✅ CRUD completo de produtos
- ✅ Suporte a imagens com sistema dinâmico (filenames apenas no BD)
- ✅ Placeholder automático para imagens não encontradas
- ✅ Visualização de imagens em tempo real
- ✅ Validação de tipos de arquivo (PNG, JPG)

#### Gerenciamento de Estoque
- ✅ Consulta de níveis de estoque em tempo real
- ✅ Filtros por produto, armazém e unidade de armazenamento
- ✅ Detalhes do estoque com visualização de produto e imagem
- ✅ Treeview com zebra striping para melhor legibilidade
- ✅ Busca dinâmica com múltiplos filtros

#### Movimentações de Estoque
- ✅ Três tipos de movimento: Entrada (1), Saída (2), Interno (3)
- ✅ Fluxo de status completo para cada tipo:
  - **Entrada**: Pendente → Efetivado
  - **Saída**: Pendente → Em separação → Despachado
  - **Interno**: Pendente → Em separação → Despachado → Efetivado
- ✅ Atualização automática de estoque baseada em tipo e status
- ✅ Cancelamento de movimentos com reversão de estoque
- ✅ Detalhes de movimento com lista de produtos
- ✅ Validação de permissões por cargo para operações
- ✅ Histórico completo de movimentações

#### Gerenciamento de Usuários
- ✅ Sistema de autenticação email/senha
- ✅ Gestão de cargos com diferentes permissões
- ✅ Ativar/Bloquear funcionários
- ✅ Rastreamento de responsáveis por operações
- ✅ Validação de credenciais no login

#### Estrutura de Armazém
- ✅ Múltiplos armazéns
- ✅ Unidades de armazenamento organizadas por armazém
- ✅ Mapeamento completo de localização de estoque

#### Sistema de Auditoria
- ✅ Log automático de todas as alterações
- ✅ Rastreamento de data/hora de atualizações
- ✅ Identificação do responsável pelas operações
- ✅ Tabela `log_atualizacao` com histórico completo

#### Interface e UX
- ✅ Design consistent com `Cores_Padrao` em todo o projeto
- ✅ Sistema de notificações (sucesso, erro)
- ✅ Theming customizado com CustomTkinter
- ✅ Layouts responsivos e bem organizados
- ✅ Zebra striping em tabelas para melhor legibilidade
- ✅ Botões com hover color dinâmico

### Refatorações Recentes

#### Imagens de Produtos
- Refatoração de armazenamento: Apenas filenames no BD, caminhos resolvidos em runtime
- Criação de helpers para reutilização de código:
  - `_carregar_placeholder()`
  - `_restaurar_imagem_anterior()`
  - `_exibir_imagem()`
  - `_get_pasta_imagens_absoluta()`

#### Código Limpo
- Remova de imports não utilizados
- Consolidação de código duplicado em helpers
- Remova de métodos não utilizados
- Padronização de naming conventions

#### Botões e Cores
- Correção de `hover=` para `hover_color=` em todos os buttons
- Adição de hovers consistentes em todas as views
- Uso padronizado de paleta de cores

#### Movimentos de Estoque
- Nova view `MovimentoEstoque_Detalhe_View` para detalhes completos
- Nova view `MovimentoEstoque_Produtos_View` para listar produtos do movimento
- Refatoração total do fluxo de status
- Implementação de regras de cancelamento

### Documentação

- ✅ README.md completo com instruções de setup
- ✅ DESENVOLVIMENTO.md com guia para contribuidores
- ✅ .env.example para configuração fácil
- ✅ CHANGELOG.md (este arquivo)
- ✅ Docstrings em todas as classes principais

### Banco de Dados

#### Tabelas Principais
- `produto`: Armazena produtos com metadados
- `estoque`: Relaciona produtos com unidades e quantidades
- `movimento_estoque`: Registra movimentações
- `produto_movimento`: Detalha produtos em cada movimento
- `funcionario`: Usuários do sistema com autenticação
- `cargo`: Papéis e permissões
- `armazem`: Localizações de armazém
- `unidade_armazenamento`: Unidades dentro de armazéns
- `tipo_movimento`: Tipos de movimento (Entrada, Saída, Interno)
- `log_atualizacao`: Auditoria de todas as operações

### Arquitetura

- ✅ MVC completo: Model, View, Controller
- ✅ DAO Pattern para acesso a dados
- ✅ Separação clara de responsabilidades
- ✅ MySQL para persistência
- ✅ Tkinter + CustomTkinter para UI

### Testes Realizados

- ✅ CRUD de produtos com imagens
- ✅ Filtros de estoque com múltiplos critérios
- ✅ Fluxos de movimentação para todos os tipos
- ✅ Cancelamento com reversão de estoque
- ✅ Autenticação de usuários
- ✅ Validação de permissões
- ✅ Criação automática de placeholder
- ✅ Tratamento de imagens não encontradas

---

## [0.9.0] - 2026-03-XX

### Adicionado
- Suporte a movimentos internos (origem e destino)
- Nova view para detalhes de movimentos
- Sistema de notificações toast

### Corrigido
- Fluxo de status para movimentos internos
- Validação de permissões para operações

---

## [0.8.0] - 2026-03-XX

### Adicionado
- Suporte a imagens de produtos
- Sistema dinâmico de placeholder

### Corrigido
- Armazenamento de imagens em BD
- Carregamento de imagens em runtime

---

## [0.7.0] - 2026-03-XX

### Adicionado
- Gerenciamento de estoque
- Filtros por produto, armazém, unidade

### Corrigido
- Queries para estoque

---

## [0.6.0] - 2026-03-XX

### Adicionado
- Movimentações de estoque básicas
- Fluxo de status inicial
- Log de auditoria

---

## [0.5.0] - 2026-03-XX

### Adicionado
- Sistema de autenticação
- Gestão de usuários
- Cargos e permissões

---

## [0.4.0] - 2026-03-XX

### Adicionado
- CRUD de produtos
- Gerenciamento de armazéns
- Unidades de armazenamento

---

## [0.3.0] - 2026-03-XX

### Adicionado
- Conexão com MySQL
- DAOs básicos
- Models de entidades

---

## [0.2.0] - 2026-03-XX

### Adicionado
- Interface principal com Tkinter
- Menu de navegação
- Estrutura básica MVC

---

## [0.1.0] - 2026-03-XX

### Adicionado
- Projeto inicial
- Estrutura de pastas
- Configuração de ambiente
- Banco de dados MySQL

---

## Notas de Versão

### Como Usar Este Changelog

- **Adicionado**: Nova funcionalidade
- **Corrigido**: Correção de bug
- **Alterado**: Mudança em funcionalidade existente
- **Depreciado**: Feature que será removida em breve
- **Removido**: Feature removida
- **Segurança**: Em caso de vulnerabilidades

### Versionamento Semântico

Seguimos [Semantic Versioning](https://semver.org/):
- **MAJOR**: Alterações incompatíveis (1.0.0)
- **MINOR**: Novas funcionalidades compatíveis (1.1.0)
- **PATCH**: Correções de bugs compatíveis (1.0.1)

---

**Data de Início**: 2026-03-XX
**Data da Versão 1.0.0**: 2026-04-02
**Status**: ✅ Completo e Funcional
