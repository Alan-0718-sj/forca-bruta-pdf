"""Ataque de Força Bruta para Senhas de PDFs"""

import itertools
from string import digits, punctuation, ascii_letters
from PyPDF2 import PdfReader
from datetime import datetime
import time
import os
from pyfiglet import Figlet
from tkinter import Tk, filedialog


def clear():
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_titulo():
    """Exibe o título formatado do programa."""
    preview_text = Figlet(font='slant')
    print(preview_text.renderText("Senha PDF".upper()))


def escolher_arquivo():
    """Abre uma janela para selecionar o arquivo PDF e retorna o caminho do arquivo selecionado."""
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Escolha o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )


def obter_tipo_caracteres():
    """Solicita ao usuário o tipo de caracteres para a senha e retorna o conjunto correspondente."""
    opcoes = {
        '1': digits,
        '2': ascii_letters,
        '3': digits + ascii_letters,
        '4': digits + ascii_letters + punctuation
    }

    while True:
        print("Escolha o tipo de caracteres da senha:")
        print("1. Apenas números")
        print("2. Apenas letras")
        print("3. Números e letras")
        print("4. Números, letras e símbolos especiais")
        escolha = input("Opção: ").strip()

        if escolha in opcoes:
            return opcoes[escolha]

        print("Opção inválida. Tente novamente.")


def obter_comprimento_senha():
    """Solicita ao usuário o comprimento da senha e retorna os valores mínimo e máximo."""
    while True:
        try:
            faixa = input("Digite o comprimento da senha (Ex: 3-7): ")
            min_len, max_len = map(int, faixa.split('-'))
            if min_len > 0 and max_len >= min_len:
                return min_len, max_len
        except (ValueError, IndexError):
            pass
        print("Dados inseridos incorretos. Use o formato correto (ex: 3-7).")


def tentar_senha(reader, senha):
    """Tenta abrir o PDF com a senha fornecida."""
    try:
        if reader.is_encrypted:
            return reader.decrypt(senha)
    except Exception as e:
        print(f"Erro ao tentar senha {senha}: {e}")
    return False


def ataque_brute_force():
    """Executa o ataque de força bruta para encontrar a senha do arquivo PDF."""
    clear()
    exibir_titulo()
    print("Hello friend!".center(30, '*'))

    # Solicita as informações necessárias
    min_len, max_len = obter_comprimento_senha()
    caracteres = obter_tipo_caracteres()
    arquivo_pdf = escolher_arquivo()

    if not arquivo_pdf:
        print("Nenhum arquivo selecionado.")
        return

    # Inicia o processo de força bruta
    inicio = time.time()
    print(f"Início do processo: {datetime.now().strftime('%H:%M:%S')}")
    total_tentativas = 0

    reader = PdfReader(arquivo_pdf)

    for comprimento in range(min_len, max_len + 1):
        for tentativa in itertools.product(caracteres, repeat=comprimento):
            senha = "".join(tentativa)
            total_tentativas += 1

            if tentar_senha(reader, senha):
                print(f"Senha encontrada: {senha} na tentativa #{total_tentativas}")
                print(f"Finalizado em: {datetime.now().strftime('%H:%M:%S')}")
                print(f"Tempo total: {time.time() - inicio:.2f} segundos")
                return f"Senha correta: {senha}"

            # Reduz a frequência de atualização do progresso para melhor desempenho
            if total_tentativas % 1000 == 0:
                print(f"Tentativa #{total_tentativas}: {senha} (não é a senha correta)")

    print("Nenhuma senha encontrada dentro do intervalo fornecido.")
    return None


def main():
    """Função principal do programa."""
    resultado = ataque_brute_force()
    if resultado:
        print(resultado)


if __name__ == '__main__':
    main()


