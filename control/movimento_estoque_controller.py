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

            # Gravar produto_movimento (sem atualizar estoque ainda)
            for item in produtos_selecionados:
                produto_mov = ProdutoMovimento(item['quantidade'], movimento_salvo._id_movimento, item['produto'])
                self.produto_movimento_dao.save(produto_mov)

            self.view.show_message(f"Movimento criado com sucesso com {len(produtos_selecionados)} produtos!")
        except Exception as e:
            self.view.show_error(f"Erro ao criar movimento: {str(e)}")

    def update_movimento(self, id_movimento=None):
        """Atualiza o status do movimento conforme regras de negócio"""
        try:
            if id_movimento is None:
                id_movimento = self.view.get_id()
            
            if not id_movimento:
                self.view.show_error("Selecione um movimento para atualizar!")
                return

            movimento_existente = self.dao.get_by_id(id_movimento)
            if not movimento_existente:
                self.view.show_error(f"Movimento com id {id_movimento} não encontrado!")
                return

            tipo_movimento = self.tipo_movimento_dao.get_by_id(movimento_existente._tipoMovimento)
            tipo_nome = tipo_movimento._tipo.lower().strip()
            status_atual = movimento_existente._status

            if ("saída" in tipo_nome or "saida" in tipo_nome or "interno" in tipo_nome) and status_atual == "Em separação":
                if self.funcionario_logado and self.funcionario_logado._id != movimento_existente._responsavel:
                    self.view.show_error("Apenas o funcionário responsável pode confirmar o despacho!")
                    return
            
            # Determinar próximo status
            proximo_status = self._obter_proximo_status(tipo_movimento._id, status_atual)
            
            if not proximo_status:
                self.view.show_error("Este movimento já atingiu seu status final!")
                return
            
            # Se for transição para "Despachado" em Saída ou Interno, mostrar confirmação com checkboxes
            if proximo_status == "Despachado" and ("saída" in tipo_nome or "saida" in tipo_nome or "interno" in tipo_nome):
                produtos = self.produto_movimento_dao.get_by_movimento_id(id_movimento)
                if not self._confirmar_produtos(produtos):
                    return
            
            # Atualizar movimento
            movimento_existente._status = proximo_status
            self.dao.update(movimento_existente)
            
            # Aplicar lógica de estoque conforme transição
            self._aplicar_logica_estoque(movimento_existente, tipo_movimento._id, status_atual, proximo_status)
            
            self.view.show_message(f"Movimento atualizado para status: {proximo_status}")
            
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar movimento: {str(e)}")
    
    def _obter_proximo_status(self, tipo_id, status_atual):
        if tipo_id == 1:  # Entrada
            if status_atual == "Pendente":
                return "Efetivado"
        elif tipo_id == 2:  # Saída
            if status_atual == "Pendente":
                return "Em separação"
            elif status_atual == "Em separação":
                return "Despachado"
        elif tipo_id == 3:  # Interno
            if status_atual == "Pendente":
                return "Em separação"
            elif status_atual == "Em separação":
                return "Despachado"
            elif status_atual == "Despachado":
                return "Efetivado"
        
        return None
    
    def _confirmar_produtos(self, produtos):
        """Mostra diálogo de confirmação com checkboxes para todos os produtos"""
        from tkinter import messagebox
        
        if not produtos:
            return messagebox.askyesno("Confirmação", "Nenhum produto neste movimento. Deseja continuar?")
        
        msg = "Confirmar despacho dos seguintes produtos:\n\n"
        for p in produtos:
            msg += f"• {p['nome']} (Qtd: {p['quantidade']})\n"
        msg += "\nDeseja continuar?"
        
        return messagebox.askyesno("Confirmação de Despacho", msg)
    
    def _aplicar_logica_estoque(self, movimento, tipo_id, status_anterior, status_novo):
        """Aplica as mudanças de estoque conforme as regras de negócio"""
        try:
            produtos = self.produto_movimento_dao.get_by_movimento_id(movimento._id_movimento)
            
            for produto in produtos:
                id_produto = produto['produto_id']
                quantidade = produto['quantidade']
                
                # Saída: Remove estoque quando passa para "Despachado"
                if tipo_id == 2 and status_novo == "Despachado":
                    estoque = self.estoque_dao.get_by_id(id_produto, movimento._origem)
                    if estoque:
                        novo_valor = estoque._quantidade - quantidade
                        if novo_valor < 0:
                            novo_valor = 0
                        self.estoque_dao.upsert(id_produto, movimento._origem, novo_valor)
                
                # Entrada: Adiciona estoque quando passa para "Efetivado"
                elif tipo_id == 1 and status_novo == "Efetivado":
                    estoque = self.estoque_dao.get_by_id(id_produto, movimento._destino)
                    quantidade_atual = estoque._quantidade if estoque else 0
                    novo_valor = quantidade_atual + quantidade
                    self.estoque_dao.upsert(id_produto, movimento._destino, novo_valor)
                
                # Interno: Comportamento especial conforme status
                elif tipo_id == 3:
                    if status_novo == "Despachado":
                        # Remove de origem
                        estoque_origem = self.estoque_dao.get_by_id(id_produto, movimento._origem)
                        if estoque_origem:
                            novo_valor = estoque_origem._quantidade - quantidade
                            if novo_valor < 0:
                                novo_valor = 0
                            self.estoque_dao.upsert(id_produto, movimento._origem, novo_valor)
                    
                    elif status_novo == "Efetivado":
                        # Adiciona no destino
                        estoque_destino = self.estoque_dao.get_by_id(id_produto, movimento._destino)
                        quantidade_atual = estoque_destino._quantidade if estoque_destino else 0
                        novo_valor = quantidade_atual + quantidade
                        self.estoque_dao.upsert(id_produto, movimento._destino, novo_valor)
        
        except Exception as e:
            raise Exception(f"Erro ao aplicar lógica de estoque: {str(e)}")

    def cancela_movimento(self, id_movimento=None):
        """Cancela um movimento conforme regras de negócio"""
        try:
            # Verificar permissão: apenas cargo 1, 2, 3 (Diretor, Supervisor, Gerenciador)
            if self.funcionario_logado and self.funcionario_logado._cargo not in [1, 2, 3]:
                self.view.show_error("Apenas supervisor ou diretor podem cancelar movimentos!")
                return

            if id_movimento is None:
                id_movimento = self.view.get_id()
            
            if not id_movimento:
                self.view.show_error("Selecione um movimento para cancelar!")
                return

            movimento = self.dao.get_by_id(id_movimento)
            if not movimento:
                self.view.show_error(f"Movimento com id {id_movimento} não encontrado!")
                return

            # Verificar se pode cancelar
            if not self.dao.pode_cancelar(id_movimento):
                self.view.show_error("Movimentos internos em status 'Efetivado' não podem ser cancelados!")
                return

            tipo_movimento = self.tipo_movimento_dao.get_by_id(movimento._tipoMovimento)
            
            # Reverter estoques conforme regras
            self._reverter_estoque_cancelamento(movimento, tipo_movimento._id)
            
            # Atualizar status para cancelado
            self.dao.cancela_movimento(id_movimento)
            
            self.view.show_message(f"Movimento {id_movimento} cancelado com sucesso!")
            
        except Exception as e:
            self.view.show_error(f"Erro ao cancelar movimento: {str(e)}")
    
    def _reverter_estoque_cancelamento(self, movimento, tipo_id):
        """Reverte os estoques conforme o tipo e status do movimento cancelado"""
        try:
            produtos = self.produto_movimento_dao.get_by_movimento_id(movimento._id_movimento)
            status = movimento._status
            
            for produto in produtos:
                id_produto = produto['produto_id']
                quantidade = produto['quantidade']
                
                # Entrada - Efetivado: Remove itens do estoque
                if tipo_id == 1 and status == "Efetivado":
                    estoque = self.estoque_dao.get_by_id(id_produto, movimento._destino)
                    if estoque:
                        novo_valor = estoque._quantidade - quantidade
                        if novo_valor < 0:
                            novo_valor = 0
                        self.estoque_dao.upsert(id_produto, movimento._destino, novo_valor)
                
                # Saída - Despachado: Adiciona itens novamente ao estoque
                elif tipo_id == 2 and status == "Despachado":
                    estoque = self.estoque_dao.get_by_id(id_produto, movimento._origem)
                    quantidade_atual = estoque._quantidade if estoque else 0
                    novo_valor = quantidade_atual + quantidade
                    self.estoque_dao.upsert(id_produto, movimento._origem, novo_valor)
                
                # Interno - Despachado: Adiciona itens ao estoque (origem)
                elif tipo_id == 3 and status == "Despachado":
                    estoque = self.estoque_dao.get_by_id(id_produto, movimento._origem)
                    quantidade_atual = estoque._quantidade if estoque else 0
                    novo_valor = quantidade_atual + quantidade
                    self.estoque_dao.upsert(id_produto, movimento._origem, novo_valor)
                
                # Interno - Efetivado: Remove itens do destino
                elif tipo_id == 3 and status == "Efetivado":
                    estoque = self.estoque_dao.get_by_id(id_produto, movimento._destino)
                    if estoque:
                        novo_valor = estoque._quantidade - quantidade
                        if novo_valor < 0:
                            novo_valor = 0
                        self.estoque_dao.upsert(id_produto, movimento._destino, novo_valor)
        
        except Exception as e:
            raise Exception(f"Erro ao reverter estoque: {str(e)}")

    def list_movimentos(self):
        try:
            movimentos = self.dao.get_all()
            
            # Se cargo é 4 (operador), filtrar apenas movimentos do funcionário
            if self.funcionario_logado and self.funcionario_logado._cargo == 4:
                movimentos = [
                    m for m in movimentos 
                    if m._responsavel == self.funcionario_logado._nome
                    and m._status in ["Pendente", "Em separação", "Despachado"]
                ]
            
            self.view.show_movimentos(movimentos)

            tipos = self.tipo_movimento_dao.get_all()
            unidades = self.unidade_dao.get_all()
            funcionarios = self._obter_funcionarios_ativos()
            
            self.view.set_tipos_movimento(tipos)
            self.view.set_unidades(unidades)
            self.view.set_funcionarios(funcionarios)

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
            view_detalhe = MovimentoEstoque_Detalhe_View(movimento, tipo_movimento, unidade_origem, unidade_destino, funcionario, produtos_movimento, controller=self)
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
