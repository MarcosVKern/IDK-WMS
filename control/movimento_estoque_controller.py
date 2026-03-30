from model.movimento_estoque import MovimentoEstoque
from model.produto_movimento import ProdutoMovimento
from model.dao.produto_movimento_dao import ProdutoMovimento_DAO
from view.movimento_estoque_produtos_view import MovimentoEstoqueProdutos_View
from view.movimento_estoque_detalhe_view import MovimentoEstoque_Detalhe_View

class MovimentoEstoque_Controller:
    def __init__(self, dao, tipo_movimento_dao, unidade_dao, funcionario_dao, view,
                 produto_dao=None, estoque_dao=None, produto_movimento_dao=None, funcionario_logado=None):
        self.dao = dao
        self.tipo_movimento_dao = tipo_movimento_dao
        self.unidade_dao = unidade_dao
        self.funcionario_dao = funcionario_dao
        self.produto_dao = produto_dao
        self.estoque_dao = estoque_dao
        if produto_movimento_dao is None:
            raise ValueError("ProdutoMovimento_DAO deve ser fornecido")
        self.produto_movimento_dao = produto_movimento_dao
        self.view = view
        self.funcionario_logado = funcionario_logado
        self.view.controller = self

    def add_movimento(self):
        try:
            if self.funcionario_logado and self.funcionario_logado._cargo not in [1, 2, 3]:
                self.view.show_error("Você não tem permissão para criar movimentos de estoque!")
                return

            dados = self.view.get_movimento_data()
            if not dados:
                self.view.show_error("Erro ao obter dados do formulário!")
                return

            if not dados['tipo_movimento']:
                self.view.show_error("Tipo de Movimento é obrigatório!")
                return
            
            if not dados['responsavel']:
                self.view.show_error("Funcionário Responsável é obrigatório!")
                return

            try:
                tipo_id = int(dados['tipo_movimento'])
                tipo = self._obter_tipo_movimento(tipo_id)
                if not tipo:
                    self.view.show_error("Tipo de movimento inválido!")
                    return
            except (ValueError, TypeError):
                self.view.show_error("Tipo de movimento inválido!")
                return

            tipo_nome = tipo._tipo.lower().strip()
            
            if "saída" in tipo_nome or "saida" in tipo_nome:
                if not dados['origem']:
                    self.view.show_error("Para movimentos de Saída, Unidade de Origem é obrigatória!")
                    return
            elif "entrada" in tipo_nome:
                if not dados['destino']:
                    self.view.show_error("Para movimentos de Entrada, Unidade de Destino é obrigatória!")
                    return
            elif "interno" in tipo_nome:
                if not dados['origem']:
                    self.view.show_error("Para movimentos Internos, Unidade de Origem é obrigatória!")
                    return
                if not dados['destino']:
                    self.view.show_error("Para movimentos Internos, Unidade de Destino é obrigatória!")
                    return
                if dados['origem'] == dados['destino']:
                    self.view.show_error("Origem e Destino não podem ser iguais!")
                    return

            # Seleção de produtos para o movimento
            produtos_selecionados = self._abrir_selecao_produtos(tipo_nome, dados.get('origem'), dados.get('destino'))
            if produtos_selecionados is None:
                self.view.show_message("Criação de movimento cancelada (sem seleção de produtos).")
                return
            if not produtos_selecionados:
                self.view.show_error("Nenhum produto selecionado para o movimento.")
                return

            try:
                responsavel_id = int(dados['responsavel'])
            except (ValueError, TypeError):
                self.view.show_error("Funcionário responsável inválido!")
                return

            movimento_novo = MovimentoEstoque(
                id_movimento=None,
                origem=dados['origem'] if dados['origem'] else None,
                destino=dados['destino'] if dados['destino'] else None,
                dataSaida=None,
                dataEntrada=None,
                dataAlteracao=None,
                status="Pendente",
                tipoMovimento=tipo_id,
                responsavel=responsavel_id
            )
            movimento_salvo = self.dao.save(movimento_novo)

            # gravar produto_movimento e atualizar estoque
            for item in produtos_selecionados:
                produto_mov = ProdutoMovimento(item['quantidade'], movimento_salvo._id_movimento, item['produto'])
                self.produto_movimento_dao.save(produto_mov)

                if "saída" in tipo_nome or "saida" in tipo_nome or "interno" in tipo_nome:
                    origem = dados['origem']
                    estoque_origem = self.estoque_dao.get_by_id(item['produto'], origem)
                    quantidade_origem = estoque_origem._quantidade if estoque_origem else 0
                    novo_valor_origem = quantidade_origem - item['quantidade']
                    if novo_valor_origem < 0:
                        novo_valor_origem = 0
                    self.estoque_dao.upsert(item['produto'], origem, novo_valor_origem)

                if "entrada" in tipo_nome or "interno" in tipo_nome:
                    destino = dados.get('destino')
                    estoque_destino = self.estoque_dao.get_by_id(item['produto'], destino)
                    quantidade_destino = estoque_destino._quantidade if estoque_destino else 0
                    novo_valor_destino = quantidade_destino + item['quantidade']
                    self.estoque_dao.upsert(item['produto'], destino, novo_valor_destino)

            self.view.show_message(f"Movimento criado com sucesso com {len(produtos_selecionados)} produtos!")
        except Exception as e:
            self.view.show_error(f"Erro ao criar movimento: {str(e)}")

    def update_movimento(self):
        try:
            if self.funcionario_logado and self.funcionario_logado._cargo not in [1, 2, 3]:
                self.view.show_error("Você não tem permissão para atualizar movimentos!")
                return

            id_movimento = self.view.get_id()
            if not id_movimento:
                self.view.show_error("Selecione um movimento para atualizar!")
                return

            movimento_existente = self.dao.get_by_id(id_movimento)
            if not movimento_existente:
                self.view.show_error(f"Movimento com id {id_movimento} não encontrado!")
                return

            dados = self.view.get_movimento_data()
            novo_status = dados.get('status', '')
            
            if novo_status:
                movimento_existente._status = novo_status
                if self.dao.update(movimento_existente):
                    self.view.show_message(f"Movimento {id_movimento} atualizado para status '{novo_status}'!")
                else:
                    self.view.show_error("Erro ao atualizar movimento!")
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar movimento: {str(e)}")

    def cancela_movimento(self):
        try:
            if self.funcionario_logado and self.funcionario_logado._cargo not in [1, 2, 3]:
                self.view.show_error("Você não tem permissão para cancelar movimentos!")
                return

            id_movimento = self.view.get_id()
            if self.dao.cancela_movimento(id_movimento):
                self.view.show_message(f"Movimento {id_movimento} cancelado com sucesso!")
            else:
                self.view.show_message(f"Movimento com id {id_movimento} não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao cancelar movimento: {str(e)}")

    def list_movimentos(self):
        try:
            movimentos = self.dao.get_all()
            
            # Se cargo é 4 (operador), filtrar apenas movimentos do funcionário
            if self.funcionario_logado and self.funcionario_logado._cargo == 4:
                movimentos = [
                    m for m in movimentos 
                    if m._responsavel == self.funcionario_logado._nome
                    and m._status in ["Pendente", "Em Separação"]
                ]
            
            self.view.show_movimentos(movimentos)
            
            # Carregar dados para dropbox
            tipos = self.tipo_movimento_dao.get_all()
            unidades = self.unidade_dao.get_all()
            funcionarios = self._obter_funcionarios_ativos()
            
            self.view.set_tipos_movimento(tipos)
            self.view.set_unidades(unidades)
            self.view.set_funcionarios(funcionarios)
            
            # Habilitar/desabilitar criação conforme cargo
            pode_criar = self.funcionario_logado and self.funcionario_logado._cargo in [1, 2, 3]
            self.view.habilitar_criacao(pode_criar)
            
        except Exception as e:
            self.view.show_error(f"Erro ao listar movimentos: {str(e)}")

    def get_movimento(self):
        try:
            id_movimento = self.view.get_id()
            movimento = self.dao.get_by_id(id_movimento)
            if not movimento:
                self.view.show_error(f"Movimento com id {id_movimento} não encontrado!")
                return
        except Exception as e:
            self.view.show_error(f"Erro ao obter movimento: {str(e)}")

    def abrir_detalhe_movimento(self, id_movimento):
        """Abre uma tela modal com os detalhes do movimento selecionado"""
        try:
            # Buscar movimento pelo ID
            movimento = self.dao.get_by_id(id_movimento)
            if not movimento:
                self.view.show_error(f"Movimento com id {id_movimento} não encontrado!")
                return
            
            # Buscar tipo de movimento
            tipo_movimento = self.tipo_movimento_dao.get_by_id(movimento._tipoMovimento)
            
            # Buscar unidade de origem
            unidade_origem = None
            if movimento._origem:
                unidade_origem = self.unidade_dao.get_by_id(movimento._origem)
            
            # Buscar unidade de destino
            unidade_destino = None
            if movimento._destino:
                unidade_destino = self.unidade_dao.get_by_id(movimento._destino)
            
            # Buscar funcionário responsável
            funcionario = self.funcionario_dao.get_by_id(movimento._responsavel)
            
            # Buscar produtos do movimento usando get_by_movimento_id
            try:
                produtos_movimento = self.produto_movimento_dao.get_by_movimento_id(id_movimento)
            except Exception as e:
                # Se houver erro ao buscar produtos, continuar sem eles
                produtos_movimento = []
            
            # Criar e exibir a view de detalhes
            view_detalhe = MovimentoEstoque_Detalhe_View(movimento, tipo_movimento, unidade_origem, unidade_destino, funcionario, produtos_movimento)
            view_detalhe.show()
            
        except Exception as e:
            self.view.show_error(f"Erro ao abrir detalhes do movimento: {str(e)}")

    def _obter_tipo_movimento(self, tipo_id):
        """Obter objeto tipo movimento pelo ID"""
        try:
            return self.tipo_movimento_dao.get_by_id(tipo_id)
        except:
            return None

    def _abrir_selecao_produtos(self, tipo_nome, origem, destino):
        if "saída" in tipo_nome or "saida" in tipo_nome or "interno" in tipo_nome:
            if not origem:
                self.view.show_error("Origem não informada para seleção de produtos")
                return None
            produtos_disponiveis = self.estoque_dao.get_by_unidade(origem)
        elif "entrada" in tipo_nome:
            produtos_disponiveis = []
            for p in self.produto_dao.get_all():
                produtos_disponiveis.append({'id': p._id, 'nome': p._nome, 'quantidade': 0})
        else:
            produtos_disponiveis = []

        if not produtos_disponiveis:
            if "entrada" not in tipo_nome:
                self.view.show_error("Não há produtos disponíveis para selecionar nessa unidade de origem")
                return []

        view_produtos = MovimentoEstoqueProdutos_View(tipo_nome.capitalize(), origem, destino, produtos_disponiveis)
        produtos_escolhidos = view_produtos.show()
        return produtos_escolhidos

    def _obter_funcionarios_ativos(self):
        try:
            todos_funcionarios = self.funcionario_dao.get_all()
            return [f for f in todos_funcionarios if f._situacao == "Ativo" and f._cargo == 4]
        except:
            return []
