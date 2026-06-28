import customtkinter as ctk
from datetime import datetime


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ERP Order Messenger")
        self.geometry("900x650")
        self.resizable(False, False)

        self._criar_layout()

    def _criar_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, height=90)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        titulo = ctk.CTkLabel(
            header,
            text="ERP ORDER MESSENGER",
            font=("Segoe UI", 28, "bold")
        )
        titulo.pack(side="left", padx=25, pady=20)

        self.lbl_status = ctk.CTkLabel(
            header,
            text="🟢 Online",
            font=("Segoe UI", 16, "bold")
        )
        self.lbl_status.pack(side="right", padx=25)

        painel = ctk.CTkFrame(self)
        painel.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        painel.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_pedido = self._criar_card(painel, "📄 Pedido", "-")
        self.card_pedido.grid(row=0, column=0, padx=10, pady=15, sticky="ew")

        self.card_valor = self._criar_card(painel, "💰 Valor", "R$ -")
        self.card_valor.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        self.card_status = self._criar_card(painel, "📦 Status", "Aguardando PDF")
        self.card_status.grid(row=0, column=2, padx=10, pady=15, sticky="ew")

        detalhes = ctk.CTkFrame(self)
        detalhes.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        detalhes.grid_columnconfigure(0, weight=1)
        detalhes.grid_columnconfigure(1, weight=1)

        info = ctk.CTkFrame(detalhes)
        info.grid(row=0, column=0, sticky="nsew", padx=(15, 8), pady=15)

        ctk.CTkLabel(
            info,
            text="Último pedido processado",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 15))

        self.lbl_cliente = ctk.CTkLabel(
            info,
            text="Cliente: -",
            font=("Segoe UI", 16),
            anchor="w"
        )
        self.lbl_cliente.pack(fill="x", padx=20, pady=8)

        self.lbl_cidade = ctk.CTkLabel(
            info,
            text="Cidade: -",
            font=("Segoe UI", 16),
            anchor="w"
        )
        self.lbl_cidade.pack(fill="x", padx=20, pady=8)

        self.lbl_emissao = ctk.CTkLabel(
            info,
            text="Emissão: -",
            font=("Segoe UI", 16),
            anchor="w"
        )
        self.lbl_emissao.pack(fill="x", padx=20, pady=8)

        self.lbl_condicao = ctk.CTkLabel(
            info,
            text="Condição: -",
            font=("Segoe UI", 16),
            anchor="w"
        )
        self.lbl_condicao.pack(fill="x", padx=20, pady=8)

        self.lbl_produto = ctk.CTkLabel(
            info,
            text="Produto: -",
            font=("Segoe UI", 16),
            anchor="w",
            wraplength=350,
            justify="left"
        )
        self.lbl_produto.pack(fill="x", padx=20, pady=8)

        log_frame = ctk.CTkFrame(detalhes)
        log_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 15), pady=15)

        ctk.CTkLabel(
            log_frame,
            text="Atividade do sistema",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        self.txt_log = ctk.CTkTextbox(
            log_frame,
            height=350,
            font=("Consolas", 13)
        )
        self.txt_log.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.txt_log.configure(state="disabled")

        rodape = ctk.CTkFrame(self, height=60)
        rodape.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 20))

        self.lbl_resumo = ctk.CTkLabel(
            rodape,
            text="Pedidos processados nesta sessão: 0",
            font=("Segoe UI", 14)
        )
        self.lbl_resumo.pack(side="left", padx=20)

        self.total_processados = 0

        self.adicionar_log("Interface iniciada.")
        self.adicionar_log("Aguardando integração com o monitor.")

    def _criar_card(self, master, titulo, valor):
        frame = ctk.CTkFrame(master)

        ctk.CTkLabel(
            frame,
            text=titulo,
            font=("Segoe UI", 14)
        ).pack(anchor="w", padx=18, pady=(15, 5))

        label_valor = ctk.CTkLabel(
            frame,
            text=valor,
            font=("Segoe UI", 22, "bold")
        )
        label_valor.pack(anchor="w", padx=18, pady=(0, 15))

        frame.valor = label_valor

        return frame

    def adicionar_log(self, mensagem):
        horario = datetime.now().strftime("%H:%M:%S")

        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", f"[{horario}] {mensagem}\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def atualizar_ultimo_pedido(self, dados):
        self.total_processados += 1

        self.card_pedido.valor.configure(
            text=dados.get("pedido") or "-"
        )

        self.card_valor.valor.configure(
            text=f"R$ {dados.get('valor_pedido') or '-'}"
        )

        self.card_status.valor.configure(
            text="Processado"
        )

        self.lbl_cliente.configure(
            text=f"Cliente: {dados.get('cliente') or '-'}"
        )

        cidade = dados.get("cidade") or "-"
        uf = dados.get("uf") or ""

        self.lbl_cidade.configure(
            text=f"Cidade: {cidade} - {uf}"
        )

        self.lbl_emissao.configure(
            text=f"Emissão: {dados.get('emissao') or '-'}"
        )

        self.lbl_condicao.configure(
            text=f"Condição: {dados.get('condicao_pagamento') or '-'}"
        )

        self.lbl_produto.configure(
            text=f"Produto: {dados.get('produto') or '-'}"
        )

        self.lbl_resumo.configure(
            text=f"Pedidos processados nesta sessão: {self.total_processados}"
        )

        self.adicionar_log(
            f"Pedido {dados.get('pedido')} processado com sucesso."
        )