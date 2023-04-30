import pprint
import pymongo as pm

client = pm.MongoClient('localhost', 27017)

db = client.banco

novos_clientes = [{
   "nome": "João",
    "cpf": "12345678901",
    "endereço": "Rua 1",
    "conta": [
        {
            "tipo": "corrente",
            "agencia": "123",
            "numero": "123",
            "saldo": 1000.00
        },
        {
            "tipo": "Poupança",
            "agencia": "321",
            "numero": "900",
            "saldo": 31540.00
        }
    ]
},
{
    "nome": "Laura",
    "cpf": "12345678902",
    "endereço": "Rua 2",
    "conta": [
        {
            "tipo": "corrente",
            "agencia": "4563",
            "numero": "123123",
            "saldo": 1000.00
        }
    ]
}]

clients = db.banco

result = clients.insert_many(novos_clientes)

print("Id inseridos")
print(result.inserted_ids)

print("Clientes:")
for client in clients.find():
    pprint.pprint(client)

print(clients.count_documents({}))
