
class Extrato:
    def __init__(self):
        self.transactions = []

    def extrato(self, numeroConta):
        print(f'Extrato: {numeroConta} \n')
        for p in self.transactions:
            print(f"{p[0]:15s} {p[1]:10.2f} {p[2]:10s} {p[3].strftime('%d/%b/%y')}")