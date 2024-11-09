"""
AULA - ORIENTADA OBJETOS / TRABALHO - Sistema de estacionamento com reconhencimento de placa

O objetivo deste sistema de estacionamento é automatizar o controle de entrada e saída de veículos, 
proporcionando uma gestão mais eficiente das vagas e simplificando o processo de cobrança. 
Através de reconhecimento automático de placas, o sistema elimina a necessidade de entrada manual de 
informações,reduzindo possíveis erros e aumentando a velocidade do processo de registro.

Conteúdo desse sistema:
 - Interface Gráfica
 - Reconhecimento de Placa
 - Tabela de Registros
 - Controle de Vagas
 - Registro de Entrada e Saída
 - Cálculo de Pagamento e Emissão de Comprovante
 - Configurações Personalizáveis
 - Mensagens de Notificação
 - Funções de Manutenção : Limpar Campos ,Botão de Sair

"""

# Seção 01 -- Importação das bibliotecas e configurações iniciais

import customtkinter as ctk  # Biblioteca para a interface gráfica
import cv2                   # OpenCV para processamento de imagem
import pytesseract           # Tesseract OCR para reconhecimento de texto da placa
from tkinter import ttk      # Importando o ttk para a tabela de histórico de registros
from datetime import datetime # Importa a classe datetime para trabalhar com datas e horas

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

# Configurações iniciais do sistema

registros = [] # List - para armazenar os registros de entrada
vagas_disponiveis = 10  # Número inicial de vagas disponíveis
preco_estacionamento = 5.00  # Preço por hora
hora_entrada = None  # Variável para armazenar a hora da entrada

# Seção 02 -- Estrura do sistema, Funções do sistemas

# Função para reconhecer a placa do veículo!!
# Essa função permite que o sistema reconheça a placa através de uma imagem escolhida

def reconhecer_placa():
    try:
        # Ultilizamos a biblioteca CV2 para processar a imagem da placa do veículo
        image_path = 'ImagemPlacaVeiculo.png'
        image = cv2.imread(image_path)

        # Pré-processamento da imagem
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Usamos OCR (Pytesseract) para fazer extração de texto da imagem
        placa_texto = pytesseract.image_to_string(thresh, config='--psm 8').strip()

        # Atualizar a interface com o texto da placa
        placa_entry.configure(state='normal')  # Habilitar o campo para edição temporária
        placa_entry.delete(0, 'end')           # Limpar campo anterior
        placa_entry.insert(0, placa_texto)     # Inserir placa reconhecida
        placa_entry.configure(state='disabled')  # Desabilitar o campo para evitar edição

    except Exception as e:
        resultado_label.configure(text=f"Erro: {str(e)}")


# Função para limpar campos de entrada
# Essa função permite o usuário limpar os campos ,casa digite errado

def limpar_campos():
    nome_entry.delete(0, 'end')   # Usado para Limpar campo de nome do usuário
    placa_entry.configure(state='normal')  # Usamos para Habilitar campo de placa temporariamente
    placa_entry.delete(0, 'end')  # Usado para Limpar campo de placa
    placa_entry.configure(state='disabled')  # Usado para Desabilitar campo de placa novamente

# Função para registrar entrada
# Essa função permite registrar a entrada do cadastro realizado

def registrar_entrada():
    global hora_entrada, vagas_disponiveis

    nome = nome_entry.get().strip()
    placa = placa_entry.get().strip()
    
    # Verifica se os campos não estão vazios e se há vagas disponíveis
    if nome and placa:
        # Verifica se a placa já está registrada
        for registro in registros:
            if registro[0] == placa:
                resultado_label.configure(text="Erro: Esta placa já está registrada.")
                return

        if vagas_disponiveis > 0:  # Verifica se há vagas disponíveis
            hora_entrada = datetime.now()  # Armazena a hora de entrada
            horario = hora_entrada.strftime("%H:%M")  # Para Formata a hora
            
            # Adiciona o registro na lista
            registros.append((placa, nome, horario))
            atualizar_tabela()
            
            # Atualizar a quantidade de vagas disponíveis
            vagas_disponiveis -= 1
            atualizar_vagas()
            resultado_label.configure(text="Entrada registrada.")
        else:
            resultado_label.configure(text="Não há vagas disponíveis.")
    else:
        resultado_label.configure(text="Preencha todos os campos.")

# Função para registrar saída
# Essa função permite registrar saida do veículo

def registrar_saida():
    global registros, vagas_disponiveis
    placa = placa_entry.get().strip()
    nome = nome_entry.get().strip() # Obter o nome do proprietário

    if placa:  # Verifica se o campo da placa não está vazio
        for registro in registros:
            if registro[0] == placa:  # Procura o registro correspondente
                if registro[1] == nome:  # Verifica se o nome do proprietário coincidem
                    # Hora da saída
                    hora_saida = datetime.now()
                    # Calcular o tempo de permanência
                    duracao = (hora_saida - hora_entrada).total_seconds() / 3600  # em horas
                    valor_pago = duracao * preco_estacionamento  # Cálculo do valor a ser pago
                    
                    # Abre a janela de pagamento
                    abrir_pagamento(valor_pago, placa, nome)
                    # Remove o registro da lista
                    registros.remove(registro)
                    atualizar_tabela()
                    
                    # Atualiza a quantidade de vagas disponíveis
                    vagas_disponiveis += 1
                    atualizar_vagas()
                    return
                else:
                    resultado_label.configure(text="Erro: Nome do proprietário não coincide.")
                    return

        resultado_label.configure(text="Erro: Placa não encontrada.")
    else:
        resultado_label.configure(text="Preencha o campo da placa.")

# Função para abrir a janela de pagamentos
# Essa função permite abrir uma janela para efetuar o pagamento do estacionamento

def abrir_pagamento(valor_pago, placa, nome):
    pagamento_window = ctk.CTkToplevel(app)
    pagamento_window.title("Pagamento")

    ctk.CTkLabel(pagamento_window, text=f"Valor a ser pago: R${valor_pago:.2f}").pack(pady=10)

    # Opções de pagamentos para o usuário escolher
    ctk.CTkLabel(pagamento_window, text="Método de Pagamento:").pack(pady=5)
    metodo_pagamento = ctk.CTkComboBox(pagamento_window, values=["Dinheiro", "Cartão", "Transferência"])
    metodo_pagamento.pack(pady=5)

    # Função para finalizar pagamento
    # Tem a funcionalidade de um botão para finalizar o pagamento

    def finalizar_pagamento():
        # Comprovante de pagamento
        gerar_comprovante(valor_pago, placa, nome)
        pagamento_window.destroy()

    ctk.CTkButton(pagamento_window, text="Finalizar Pagamento", command=finalizar_pagamento).pack(pady=10)

# Função para gerar o comprovante
# Permite gerar um comprovante de pagaemnto para o usuário

def gerar_comprovante(valor_pago, placa, nome):
    hora_saida = datetime.now().strftime("%H:%M")
    comprovante = f"Comprovante de Pagamento\n\nProprietário: {nome}\nPlaca: {placa}\nValor: R${valor_pago:.2f}\nHora de Saída: {hora_saida}\n"
    
    # Cria uma nova aba para exibir o comprovante
    comprovante_window = ctk.CTkToplevel(app)
    comprovante_window.title("Comprovante de Pagamento")
    
    # Exibe o comprovante
    ctk.CTkLabel(comprovante_window, text=comprovante).pack(pady=10)

# Função para atualizar a tabela com os registros
# tem a funcionalidade de atualizar a tabela conforme vai registrando entrada e saída

def atualizar_tabela():
    for row in tree.get_children():
        tree.delete(row)  # Limpa a tabela existente
    for index, registro in enumerate(registros, start=1):  # Adiciona o índice
        tree.insert("", "end", values=(index, registro[0], registro[1], registro[2]))  # Insere novos registros na tabela

# Função para atualizar a quantidade de vagas disponíveis
# Tem a funcionalidade de alterar a quantidade de vagas disponiveis, conforme vai resgistrando entrada e saída

def atualizar_vagas():
    vagas_label.configure(text=f"Vagas Disponíveis: {vagas_disponiveis}")

# Função para sair do aplicativo
# Tem funcionalidade de um botão para encerrar o programa ou sistema

def sair():
    app.quit()

# Função para abrir configurações
# Funcionalidade de um botão de configurações,para alter algumas coisas do programa

def abrir_configuracoes():
    configuracoes_window = ctk.CTkToplevel(app)  # Cria uma nova janela para configurações
    configuracoes_window.title("Configurações")
    
    # Campo para alterar o número de vagas
    ctk.CTkLabel(configuracoes_window, text="Número de Vagas:").pack(pady=5)
    vagas_entry = ctk.CTkEntry(configuracoes_window)
    vagas_entry.pack(pady=5)
    vagas_entry.insert(0, str(vagas_disponiveis))  # Preenche o campo com o valor atual
    
    # Campo para alterar o preço do estacionamento
    ctk.CTkLabel(configuracoes_window, text="Preço do Estacionamento:").pack(pady=5)
    preco_entry = ctk.CTkEntry(configuracoes_window)
    preco_entry.pack(pady=5)
    preco_entry.insert(0, str(preco_estacionamento))  # Preenche o campo com o valor atual

    # Função para salvar as configurações
    # Funcionalidade de um botão para salvar as configurações do usuário

    def salvar_configuracoes():
        global vagas_disponiveis, preco_estacionamento
        try:
            vagas_disponiveis = int(vagas_entry.get())  # Altera o número de vagas
            preco_estacionamento = float(preco_entry.get())  # Altera o preço
            atualizar_vagas()  # Atualiza a exibição das vagas
            resultado_label.configure(text="Configurações salvas.")
            configuracoes_window.destroy()  # Fecha a janela de configurações
        except ValueError:
            resultado_label.configure(text="Erro: Valores inválidos.")

    ctk.CTkButton(configuracoes_window, text="Salvar", command=salvar_configuracoes).pack(pady=10)

# Seção 03 -- Interface Gráfica e suas configurações

# Configuração da interface
app = ctk.CTk()  # Cria a janela principal
app.title("Sistema de Estacionamento")

# Label do título
titulo_label = ctk.CTkLabel(app, text="Sistema de Reconhecimento de Placas", font=("Arial", 20))  
titulo_label.pack(pady=10)

# Campos de entrada
ctk.CTkLabel(app, text="Nome do Proprietário:").pack(pady=5)
nome_entry = ctk.CTkEntry(app)
nome_entry.pack(pady=5)

ctk.CTkLabel(app, text="Placa do Veículo:").pack(pady=5)
placa_entry = ctk.CTkEntry(app, state='disabled')  # Inicialmente desabilitado
placa_entry.pack(pady=5)

# Botões de ação
ctk.CTkButton(app, text="Reconhecer Placa", command=reconhecer_placa).pack(pady=8)
ctk.CTkButton(app, text="Limpar Campos", command=limpar_campos).pack(pady=8)
ctk.CTkButton(app, text="Registrar Entrada", command=registrar_entrada).pack(pady=8)
ctk.CTkButton(app, text="Registrar Saída", command=registrar_saida).pack(pady=8)


# Exibição de vagas
vagas_label = ctk.CTkLabel(app, text=f"Vagas Disponíveis: {vagas_disponiveis}")
vagas_label.pack(pady=5)

# Tabela de registros
tree = ttk.Treeview(app, columns=("Index", "Placa", "Proprietário", "Hora de Entrada"), show='headings')
tree.heading("Index", text="Índice")
tree.heading("Placa", text="Placa")
tree.heading("Proprietário", text="Proprietário")
tree.heading("Hora de Entrada", text="Hora de Entrada")
tree.pack(pady=5)

# Label para mensagens de resultado
resultado_label = ctk.CTkLabel(app, text="")
resultado_label.pack(pady=5)

# Botões de configurações e sair
ctk.CTkButton(app, text="Configurações", command=abrir_configuracoes).pack(side='right', padx=10, pady=5)
ctk.CTkButton(app, text="Sair", command=sair).pack(side='right', padx=10, pady=5)

# Inicia a aplicação
app.mainloop()


