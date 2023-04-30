from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, func, inspect, select, Double
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String(11), nullable=False)
    endereço = Column(String(30), nullable=False)

    conta = relationship("Conta", back_populates="cliente", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereço={self.endereço})"
    
class Conta(Base):
    __tablename__ = 'conta'
    id = Column(Integer, primary_key=True)
    tipo = Column(String(30), nullable=False)
    agencia = Column(String(30), nullable=False)
    numero = Column(String(30), nullable=False)
    saldo = Column(Double, nullable=False)
    id_client = Column(Integer, ForeignKey('cliente.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero={self.numero}, saldo={self.saldo}, id_client={self.id_client})"
    

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inpesctor = inspect(engine)

with Session(engine) as session:
    cliente = Cliente(nome="João", cpf="12345678901", endereço="Rua 1", conta=[Conta(tipo="corrente", agencia="123", numero="123", saldo=1000.00)])
    cliente2 = Cliente(nome="Laura", cpf="12345678902", endereço="Rua 2", conta=[Conta(tipo="Poupança", agencia="321", numero="900", saldo=1000.00)])
    session.add_all([cliente, cliente2])
    session.commit()
    
stmt = select(Cliente)

stmt_conta = select(Conta)

print("Clientes:")
for client in session.scalars(stmt):
    print(client)

print("Contas:")
for conta in session.scalars(stmt_conta):
    print(conta)


join_stmt = select(Cliente.nome, Conta.tipo, Conta.agencia).join_from(Conta, Cliente)

connection = engine.connect()

results = connection.execute(join_stmt).fetchall()
print("Clientes e suas contas:")
for result in results:
    print(result)