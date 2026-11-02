"""Estrutura de dados híbrida: região ordenada e cauda de inserção."""
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoBusca:
    encontrado: bool
    local: str
    indice: int | None
    iteracoes_binaria: int
    iteracoes_sequencial: int

    @property
    def total_iteracoes(self) -> int:
        return self.iteracoes_binaria + self.iteracoes_sequencial


class ListaHibrida:
    def __init__(self, semente: int = 42, tamanho_inicial: int = 1024, capacidade_cauda: int = 10):
        if tamanho_inicial < 0 or capacidade_cauda < 1:
            raise ValueError("Tamanho inicial deve ser não negativo e capacidade deve ser positiva")
        self.semente = semente
        self.capacidade_cauda = capacidade_cauda
        gerador = random.Random(semente)
        self.ordenada = sorted(gerador.sample(range(0, 100_000), tamanho_inicial))
        self.cauda: list[int] = []
        self.intercalacoes = 0

    def buscar(self, chave: int) -> ResultadoBusca:
        esquerda, direita = 0, len(self.ordenada) - 1
        binaria = 0
        while esquerda <= direita:
            binaria += 1
            meio = (esquerda + direita) // 2
            if self.ordenada[meio] == chave:
                return ResultadoBusca(True, "Região ordenada", meio, binaria, 0)
            if self.ordenada[meio] < chave:
                esquerda = meio + 1
            else:
                direita = meio - 1
        for indice, valor in enumerate(self.cauda):
            if valor == chave:
                return ResultadoBusca(True, "Cauda não ordenada", indice, binaria, indice + 1)
        return ResultadoBusca(False, "Não encontrada", None, binaria, len(self.cauda))

    def inserir(self, chave: int) -> tuple[bool, str]:
        if type(chave) is not int:
            return False, "A chave deve ser um número inteiro."
        if self.buscar(chave).encontrado:
            return False, "Chave repetida: inserção rejeitada."
        self.cauda.append(chave)
        if len(self.cauda) == self.capacidade_cauda:
            self._intercalar()
            return True, "Cauda cheia: chaves ordenadas, intercaladas e cauda esvaziada."
        return True, f"Chave inserida na cauda ({len(self.cauda)}/{self.capacidade_cauda})."

    def _intercalar(self) -> None:
        cauda_ordenada = sorted(self.cauda)
        resultado = []
        i = j = 0
        while i < len(self.ordenada) and j < len(cauda_ordenada):
            if self.ordenada[i] < cauda_ordenada[j]:
                resultado.append(self.ordenada[i]); i += 1
            else:
                resultado.append(cauda_ordenada[j]); j += 1
        resultado.extend(self.ordenada[i:])
        resultado.extend(cauda_ordenada[j:])
        self.ordenada = resultado
        self.cauda.clear()
        self.intercalacoes += 1
