#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de execução simplificado para o Deadlock Escape

Este arquivo pode ser usado como ponto de entrada alternativo para o jogo.
"""

import sys
import os

# Adiciona o diretório atual ao path para importar o módulo do jogo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from deadlock_escape import main

    if __name__ == "__main__":
        print("Iniciando Deadlock Escape...")
        print("=" * 50)
        main()

except ImportError as e:
    print(f"Erro ao importar o jogo: {e}")
    print("Certifique-se de que o arquivo 'deadlock_escape.py' está no mesmo diretório.")
    sys.exit(1)

except Exception as e:
    print(f"Erro inesperado: {e}")
    sys.exit(1)