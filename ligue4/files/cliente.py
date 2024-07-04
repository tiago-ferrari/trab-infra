import grpc
import connectfour_pb2
import connectfour_pb2_grpc
import threading

# Criação de um lock para garantir que o tabuleiro e as mensagens sejam impressos sem interrupção
print_lock = threading.Lock()

def connect(server_address, client_name):
    channel = grpc.insecure_channel(server_address)
    stub = connectfour_pb2_grpc.ConnectFourStub(channel)
    response = stub.Connect(connectfour_pb2.PlayerInfo(name=client_name))
    return response.connected, response.player_id, stub

def make_move(stub, player_id, col):
    response = stub.MakeMove(connectfour_pb2.Move(player_id=player_id, col=col))
    return response

def get_updates(stub, client_name):
    for update in stub.GetUpdates(connectfour_pb2.PlayerInfo(name=client_name)):
        with print_lock:
            print_board(update.board)
            print(update.message)
            if update.game_over:
                print(f"Fim de jogo. Vencedor: {'Empate' if update.winner == 0 else 'Jogador ' + str(update.winner)}")
                break

def print_board(board):
    print("\n" + "-" * (len(board.rows[0].cells) * 4 + 1))
    for row in board.rows:
        print("|", end="")
        for cell in row.cells:
            print(f" {cell} |", end="")
        print("\n" + "-" * (len(row.cells) * 4 + 1))

def main():
    server_address = '100.10.0.10:50051'
    client_name = input("Digite seu nome: ")

    connected, player_id, stub = connect(server_address, client_name)
    if connected:
        print(f"{client_name} conectado ao servidor como jogador {player_id}!")
        threading.Thread(target=get_updates, args=(stub, client_name)).start()
        while True:
            command = input("Digite 'sair' para sair ou 'jogar' para fazer um movimento: ").lower()
            if command == 'sair':
                break
            elif command == 'jogar':
                try:
                    col = int(input("Digite a coluna (0-6): "))
                    if 0 <= col <= 6:
                        response = make_move(stub, player_id, col)
                        with print_lock:
                            print(response.message)
                        if response.game_over:
                            break
                    else:
                        with print_lock:
                            print("Coluna inválida. Tente novamente.")
                except ValueError:
                    with print_lock:
                        print("Entrada inválida. Por favor, digite um número entre 0 e 6.")
            else:
                with print_lock:
                    print("Comando inválido. Tente novamente.")
    else:
        print("Falha ao conectar ao servidor.")

if __name__ == '__main__':
    main()
