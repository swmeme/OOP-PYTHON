from Conta import Conta
from Cliente import Cliente

cliente1 = Cliente(123, 'Joao', 'Rua 1')
cliente2 = Cliente(345, 'Maria','Rua 2')
conta1 = Conta(1, [cliente1], 0)
conta2 = Conta(2, cliente2, 2000 )
conta1.gerar_extrato()
conta1.depositar(1500)
conta1.sacar(500)
print(30 * '-')
conta1.gerar_extrato()