from model.movimento_estoque import MovimentoEstoque

class MovimentoEstoque_Controller:
    def __init__(self, dao, tipo_movimento_dao, unidade_dao, funcionario_dao, view, funcionario_logado=None):
        self.dao = dao
        self.tipo_movimento_dao = tipo_movimento_dao
        self.unidade_dao = unidade_dao
        self.funcionario_dao = funcionario_dao
        self.view = view
        self.funcionario_logado = funcionario_logado
        self.view.controller = self

    def add_movimento(self):
        try:
            # Validar permissão: apenas cargos 1, 2, 3 podem criar
            if self.funcionario_logado and self.funcionario_logado._cargo not in [1, 2, 3]:
                self.view.show_error("Você não tem permissão para criar movimentos de estoque!")
                return

            dados = self.view.get_movimento_data()
            if not dados:
                self.view.show_error("Erro ao obter dados do formulário!")
                return

            # Validar campos obrigatórios
            if not dados['tipo_movimento']:
                self.view.show_error("Tipo de Movimento é obrigatório!")
                return
            
            if not dados['responsavel']:
                self.view.show_error("Funcionário Responsável é obrigatório!")
                return

            # Validar campos conforme tipo de movimento
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

            movimento_novo = MovimentoEstoque(
                id_movimento=None,
                origem=dados['origem'] if dados['origem'] else None,
                destino=dados['destino'] if dados['destino'] else None,
                dataSaida=None,
                dataEntrada=None,
                dataAlteracao=None,
                status="Pendente",
                tipoMovimento=int(dados['tipo_movimento']),
                responsavel=int(dados['responsavel'])
            )
            movimento_salvo = self.dao.save(movimento_novo)
            self.view.show_message(f"Movimento criado com sucesso! ID: {movimento_salvo._id_movimento}")
        except Exception as e:
            self.view.show_error(f"Erro ao criar movimento: {str(e)}")

    def update_movimento(self):
        try:
            # Validar permissão
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

    def delete_movimento(self):
        try:
            # Validar permissão
            if self.funcionario_logado and self.funcionario_logado._cargo not in [1, 2, 3]:
                self.view.show_error("Você não tem permissão para cancelar movimentos!")
                return

            id_movimento = self.view.get_id()
            if self.dao.delete(id_movimento):
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
                    if m._responsavel == self.funcionario_logado._id 
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

    def _obter_tipo_movimento(self, tipo_id):
        """Obter objeto tipo movimento pelo ID"""
        try:
            return self.tipo_movimento_dao.get_by_id(tipo_id)
        except:
            return None

    def _obter_funcionarios_ativos(self):
        """Obter apenas funcionários ativos com cargo 4 (operador)"""
        try:
            todos_funcionarios = self.funcionario_dao.get_all()
            return [f for f in todos_funcionarios if f._situacao == "Ativo" and f._cargo == 4]
        except:
            return []
