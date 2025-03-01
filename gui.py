import tkinter as tk
from tkinter import messagebox
from blockchain import Blockchain
from asymmetric_encryption import AsymmetricEncryption
from transaction import Transaction
import threading
import time
import random
import json
import socket
import logging
from node import Node

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class WalletApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Кошелек")
        self.wallets = {}
        self.blockchain = Blockchain(self.wallets)
        self.create_scrollable_frame()
        self.create_widgets()
        self.is_blockchain_loaded = False  
        self.load_blockchain()

        self.node_address = '127.0.0.1:5001'  
        self.node = Node(self.node_address, self.wallets)
        logging.info(f" Узел создан с адресом: {self.node_address}")

        self.update_thread = threading.Thread(target=self.update_data, daemon=True)
        self.update_thread.start()
        self.block_list = tk.Listbox(master)  # Пример списка для отображения блоков
        self.block_list.pack()

    def create_scrollable_frame(self):
        self.canvas = tk.Canvas(self.master) 
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        def create_widgets(self):
        self.hot_wallet_var = tk.BooleanVar(value=True)
        tk.Radiobutton(self.master, text="Горячий кошелек", variable=self.hot_wallet_var, value=True).pack()
        tk.Radiobutton(self.master, text="Холодный кошелек", variable=self.hot_wallet_var, value=False).pack()

        tk.Label(self.master, text="Создать кошелек").pack()
        tk.Button(self.master, text="Создать", command=self.create_wallet).pack()

        tk.Label(self.master, text="Адрес:").pack()
        self.address_entry = tk.Entry(self.master)
        self.address_entry.pack()

        tk.Button(self.master, text="Показать баланс", command=self.show_balance).pack()

        tk.Label(self.master, text="Получатель:").pack()
        self.recipient_entry = tk.Entry(self.master)
        self.recipient_entry.pack()

        tk.Label(self.master, text="Сумма:").pack()
        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        tk.Button(self.master, text="Инициировать транзакцию", command=self.initiate_transaction).pack()

        tk.Button(self.master, text="Показать блоки", command=self.show_blocks).pack()

        tk.Button(self.master, text="Показать ключи", command=self.show_keys).pack()

        tk.Button(self.master, text="Сохранить блокчейн", command=self.save_blockchain).pack()
        self.load_button = tk.Button(self.master, text="Загрузить блокчейн", command=self.load_blockchain)
        self.load_button.pack()

    def save_blockchain(self):
        self.blockchain.save_to_file('blockchain.json')
        messagebox.showinfo("Сохранение", "Блокчейн успешно сохранен!")

    def load_blockchain(self):
        if not self.is_blockchain_loaded:
            try:
                self.blockchain.load_from_file('blockchain.json')
                messagebox.showinfo("Загрузка", "Блокчейн успешно загружен!")
                self.is_blockchain_loaded = True
                self.load_button.config(state=tk.DISABLED)
            except FileNotFoundError:
                messagebox.showwarning("Загрузка", "Файл блокчейна не найден. Начинаем с пустого блокчейна.")
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Ошибка при чтении файла блокчейна. Проверьте формат JSON.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке блокчейна: {str(e)}")

    def create_wallet(self):
        wallet_type = 'hot' if self.hot_wallet_var.get() else 'cold'
        wallet = AsymmetricEncryption(wallet_type)
        public_key = wallet.get_public_key()

        while True:
            port = random.randint(5002, 6000)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('127.0.0.1', port)) != 0:
                    break
        address = f"127.0.0.1:{port}"
        self.wallets[address] = wallet
        self.blockchain.utxo.utxos[address] = self.blockchain.utxo.initial_balance

        new_node = Node(address, self.wallets)
        logging.info(f"Узел создан с адресом: {address}")

        self.node.add_peer(address)
        messagebox.showinfo("Кошелек создан", f"Ваш адрес: {address}")

    def show_balance(self):
        address = self.address_entry.get()
        if address in self.blockchain.utxo.utxos:
            balance = self.blockchain.get_balance(address)  # Получение баланса через UTXO
            messagebox.showinfo("Баланс", f"Баланс для {address}: {balance}")
        else:
            messagebox.showerror("Ошибка", "Кошелек не найден.")

    def initiate_transaction(self):
        sender = self.address_entry.get()
        recipient = self.recipient_entry.get()
        try:
            amount = float(self.amount_entry.get())
            fee = 1

            # Запускаем обработку транзакции в отдельном потоке
            transaction_thread = threading.Thread(target=self.process_transaction, args=(sender, recipient, amount, fee))
            transaction_thread.start()
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное значение для суммы.")

    def process_transaction(self, sender, recipient, amount, fee):
        balance = self.blockchain.get_balance(sender)
        if balance < amount + fee:
            self.show_error("Недостаточно средств для транзакции.")
            return

        if sender in self.wallets:
            private_key = self.wallets[sender].get_private_key()
            transaction = Transaction(sender, recipient, amount, fee)
            transaction.sign_transaction(private_key)

            # Проверяем, можно ли добавить транзакцию в mempool
            if self.node.add_transaction_to_mempool(transaction):
                self.mine_block()  # Создаем блок после добавления транзакции
                self.show_info("Транзакция успешно добавлена!")
            else:
                self.show_error("Не удалось добавить транзакцию в mempool.")
        else:
            self.show_error("Кошелек не найден.")

    def show_error(self, message):
        # Обновление интерфейса должно происходить в основном потоке
        self.master.after(0, lambda: messagebox.showerror("Ошибка", message))

    def show_info(self, message):
        # Обновление интерфейса должно происходить в основном потоке
        self.master.after(0, lambda: messagebox.showinfo("Успех", message))


    def mine_block(self):
        if self.node.mempool:  # Проверяем, есть ли транзакции в mempool
            new_block = Block(transactions=self.node.mempool, previous_hash=self.blockchain.get_last_block_hash())
            difficulty = 4  # Установите уровень сложности

            miner_address = self.address_entry.get()  # Получаем адрес майнера из интерфейса

            for tx in new_block.transactions:
                logging.info(f"Транзакция: {tx.sender} -> {tx.recipient}, сумма: {tx.amount}")

            if self.blockchain.add_block(new_block, difficulty, miner_address):  # Передаем miner_address
                self.node.mempool.clear()  # Очищаем mempool после добавления блока
                logging.info("Блок успешно добавлен в блокчейн.")
            else:
                logging.error("Не удалось добавить блок в блокчейн.")
        else:
            logging.info("Нет транзакций для майнинга.")

    def update_data(self):
        while True:
            time.sleep(10)
            self.refresh_data()

    def refresh_data(self):
        new_blocks = self.node.get_chain()
        # Используем after для обновления интерфейса в основном потоке
        self.master.after(0, self.show_blocks)  # Обновляем отображение блоков

    def show_blocks(self):
        blocks = self.blockchain.get_blocks()
        self.display_blocks(blocks)

    def display_blocks(self, blocks):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, block in enumerate(blocks):
            frame = tk.Frame(self.scrollable_frame, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(frame, text=f"Блок {index}", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(frame, text=f"Время: {block.timestamp}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Предыдущий хэш: {block.previous_hash}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Меркле корень: {block.merkle_root}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Хэш блока: {block.hash}", font=("Arial", 10)).pack(anchor="w")

            for tx in block.transactions:
                tk.Label(frame,
                         text=f"Транзакция: {tx.transaction_hash}, Отправитель: {tx.sender}, Получатель: {tx.recipient}, "
                              f"Сумма: {tx.amount}, Комиссия: {tx.fee}, Подпись: {tx.signature}",
                         font=("Arial", 10)).pack(anchor="w")

    def show_keys(self):
        keys_info = "\n".join(
            [f"Адрес: {address}, Закрытый ключ: {self.wallets[address].get_private_key()[0]}" for address in
             self.wallets])
        messagebox.showinfo("Ключи", keys_info if keys_info else "Нет ключей.")


if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()
