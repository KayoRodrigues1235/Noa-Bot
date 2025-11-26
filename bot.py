"""
Bot para servidor do discord do Bastards
    Desenvolvido por Kayo Rodrigues, o bot consiste em um algoritmo que guarda as informações dos usuarios cadastrado
    e transforma em "xp" de acordo com o valor daquele jogador; 
"""

import discord

class bot:
    def __init__(self, nome, value):
        self.nome = nome
        self.value = value
        
        
        