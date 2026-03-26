from model.cargo import Cargo
from model.dao.cargo_dao import Cargo_DAO

if __name__ == "__main__":
    cargo_dao = Cargo_DAO()
    cargos = cargo_dao.get_all()
    for cargo in cargos:
        print(f"ID: {cargo._id}, Cargo: {cargo._cargo}")