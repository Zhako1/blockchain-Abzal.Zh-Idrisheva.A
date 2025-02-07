import tkinter as tk
from tkinter import messagebox
from blockchain import Blockchain
from asymmetric_encryption import AsymmetricEncryption
from transaction import Transaction
import random
import json


class WalletApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Кошелек")
        self.blockchain = Blockchain()
        self.wallets = {}
        self.create_scrollable_frame()
        self.create_widgets()

        self.is_blockchain_loaded = False
        self.load_blockchain()



    def create_scrollable_frame(self):
        self.canvas = tk.Canvas(self.master)  # Изменено на self.master
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
        # Создание кошелька
        tk.Label(self.master, text="Создать кошелек").pack()
        tk.Button(self.master, text="Создать", command=self.create_wallet).pack()

        # Ввод адреса
        tk.Label(self.master, text="Адрес:").pack()
        self.address_entry = tk.Entry(self.master)
        self.address_entry.pack()

        # Показать баланс
        tk.Button(self.master, text="Показать баланс", command=self.show_balance).pack()

        # Инициировать транзакцию
        tk.Label(self.master, text="Получатель:").pack()
        self.recipient_entry = tk.Entry(self.master)
        self.recipient_entry.pack()

        tk.Label(self.master, text="Сумма:").pack()
        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        tk.Button(self.master, text="Инициировать транзакцию", command=self.initiate_transaction).pack()

        # Показать блоки
        tk.Button(self.master, text="Показать блоки", command=self.show_blocks).pack()

        # Показать ключи
        tk.Button(self.master, text="Показать ключи", command=self.show_keys).pack()

        tk.Button(self.master, text="Сохранить блокчейн", command=self.save_blockchain).pack()
        self.load_button = tk.Button(self.master, text="Загрузить блокчейн", command=self.load_blockchain)
        self.load_button.pack()

    def save_blockchain(self):
        self.blockchain.save_to_file('blockchain.json')
        messagebox.showinfo("Сохранение", "Блокчейн успешно сохранен!")

    def load_blockchain(self):
        if not self.is_blockchain_loaded:  # Проверяем, был ли загружен блокчейн
            try:
                self.blockchain.load_from_file('blockchain.json')
                messagebox.showinfo("Загрузка", "Блокчейн успешно загружен!")
                self.is_blockchain_loaded = True  # Устанавливаем флаг
                self.load_button.config(state=tk.DISABLED)  # Делаем кнопку неактивной
            except FileNotFoundError:
                messagebox.showwarning("Загрузка", "Файл блокчейна не найден. Начинаем с пустого блокчейна.")
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Ошибка при чтении файла блокчейна. Проверьте формат JSON.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке блокчейна: {str(e)}")

    def create_wallet(self):
        address = str(random.randint(1000, 9999))
        self.wallets[address] = AsymmetricEncryption()
        self.blockchain.utxo.utxos[address] = self.blockchain.utxo.initial_balance  # Начальный баланс
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
        recipient = self.recipient_entry.get()  # Получаем адрес получателя из поля ввода
        try:
            amount = float(self.amount_entry.get())  # Получаем сумму из поля ввода
            fee = 1  # Замените на фактическую комиссию

            # Проверка баланса перед инициализацией транзакции
            balance = self.blockchain.get_balance(sender)
            if balance < amount + fee:
                messagebox.showerror("Ошибка", "Недостаточно средств для транзакции.")
                return

            if sender in self.wallets:
                private_key = self.wallets[sender].get_private_key()  # Получение закрытого ключа
                transaction = Transaction(sender, recipient, amount, fee)
                transaction.sign_transaction(private_key)

                if self.blockchain.add_block(transaction):
                    messagebox.showinfo("Успех", "Транзакция успешно добавлена!")
                else:
                    messagebox.showerror("Ошибка", "Не удалось добавить транзакцию.")
            else:
                messagebox.showerror("Ошибка", "Кошелек не найден.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректное значение для суммы.")

    def show_blocks(self):
        # Очищаем предыдущие блоки
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        blocks = self.blockchain.get_blocks()
        for index, block in enumerate(blocks):  # Используем enumerate для получения индекса
            frame = tk.Frame(self.scrollable_frame, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(frame, text=f"Блок {index}", font=("Arial", 12, "bold")).pack(anchor="w")  # Используем index
            tk.Label(frame, text=f"Время: {block.timestamp}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Предыдущий хэш: {block.previous_hash}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Меркле корень: {block.merkle_root}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Хэш блока: {block.hash}", font=("Arial", 10)).pack(anchor="w")
            for tx in block.transactions:
                tk.Label(frame,
                         text=f"Транзакция: {tx.transaction_hash}, Отправитель: {tx.sender}, Получатель: {tx.recipient}, Сумма: {tx.amount}, Комиссия: {tx.fee}, Подпись: {tx.signature}",
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
