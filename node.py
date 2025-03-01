import json
import socket
import threading
import logging
from blockchain import Blockchain
from transaction import Transaction
from block import Block

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class Node:
    def __init__(self, address="127.0.0.1:5001", wallets=None):
        if wallets is None:
            wallets = {}

        # Проверяем, что адрес задан правильно
        if ":" not in address:
            raise ValueError(f"Некорректный формат адреса: {address} (должен быть в формате 'IP:PORT')")

        self.address = address  # Локальный адрес с портом
        self.blockchain = Blockchain(wallets)
        self.peers = set()  # Множество для хранения адресов других узлов
         self.mempool = []  # Очередь неподтвержденных транзакций
        self.is_node_created_logged = False  # Флаг для логирования создания узла

        self.start_server()

    def add_peer(self, peer_address):
        """Добавляет адрес другого узла в список пиров."""
        if ":" not in peer_address:
            raise ValueError(f"Некорректный формат адреса пира: {peer_address} (должен быть в формате 'IP:PORT')")
        self.peers.add(peer_address)
        logging.info(f"Добавлен новый пир: {peer_address}")

    def broadcast_transaction(self, transaction):
        """Распространяет транзакцию среди всех пиров."""
        transaction_json = json.dumps(transaction.to_dict())
        for peer in self.peers:
            self.send_request(peer, f"TRANSACTION:{transaction_json}")

    def receive_transaction(self, transaction):
        """Обрабатывает полученную транзакцию."""
        if self.blockchain.add_block(transaction):
            logging.info(f"Транзакция {transaction.to_dict()} добавлена в блокчейн")
            self.broadcast_transaction(transaction)

    def get_chain(self):
        """Возвращает текущую цепочку блоков."""
        return self.blockchain.get_blocks()

    def get_balance(self, address):
        """Возвращает баланс указанного адреса."""
        return self.blockchain.get_balance(address)

    def resolve_conflicts(self):
        """Разрешает конфликты, выбирая самую длинную цепочку."""
        longest_chain = None
        current_length = len(self.blockchain.chain)

        for peer in self.peers:
            peer_chain = self.request_chain_from_peer(peer)
            if peer_chain and len(peer_chain) > current_length:
                current_length = len(peer_chain)
                longest_chain = peer_chain

        if longest_chain:
            self.blockchain.chain = longest_chain
            logging.info("Блокчейн обновлен на более длинную цепочку")
            return True
        return False

    def start_server(self):
        """Запускает сервер для обработки входящих соединений."""
        server_thread = threading.Thread(target=self.run_server, daemon=True)
        server_thread.start()

    def run_server(self):
        """Запускает серверный сокет."""
        try:
            ip, port = self.address.split(":")
            port = int(port)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((ip, port))
                server_socket.listen(5)
                logging.info(f"Узел {self.address} запущен и слушает на порту {port}")

                while True:
                    client_socket, addr = server_socket.accept()
                    logging.info(f"Подключен узел {addr}")
                    threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
        except Exception as e:
            logging.error(f"Ошибка в сервере: {e}")

    def handle_client(self, client_socket):
        """Обрабатывает входящие запросы от клиентов."""
        try:
            request = client_socket.recv(1024).decode()
            logging.info(f"Получен запрос: {request}")

            if request.startswith("TRANSACTION:"):
                transaction_data = json.loads(request.split(":", 1)[1])
                transaction = Transaction(**transaction_data)
                self.receive_transaction(transaction)

            elif request == "GET_CHAIN":
                chain_data = json.dumps([block.to_dict() for block in self.blockchain.get_blocks()])
                client_socket.send(chain_data.encode())

        except Exception as e:
            logging.error(f"Ошибка при обработке запроса: {e}")

        finally:
            client_socket.close()

    def send_request(self, peer_address, request):
        """Отправляет запрос другому узлу."""
        try:
            ip, port = peer_address.split(":")
            port = int(port)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))
                client_socket.send(request.encode())

        except Exception as e:
            logging.error(f"Ошибка отправки запроса узлу {peer_address}: {e}")

    def request_chain_from_peer(self, peer):
        """Запрашивает цепочку блоков у другого узла."""
        try:
            ip, port = peer.split(":")
            port = int(port)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((ip, port))
                client_socket.send("GET_CHAIN".encode())
                response = client_socket.recv(4096).decode()

            return json.loads(response) if response else None

        except Exception as e:
            logging.error(f"Ошибка запроса цепочки у {peer}: {e}")
            return None
