import unittest
from lista_hibrida import ListaHibrida

class TestListaHibrida(unittest.TestCase):
    def setUp(self):
        self.lista = ListaHibrida()

    def test_geracao_reprodutivel(self):
        self.assertEqual(self.lista.ordenada, ListaHibrida(semente=42).ordenada)
        self.assertEqual(len(self.lista.ordenada), 1024)
        self.assertEqual(len(set(self.lista.ordenada)), 1024)
        self.assertEqual(self.lista.ordenada, sorted(self.lista.ordenada))

    def test_busca_na_regiao_ordenada(self):
        resultado = self.lista.buscar(self.lista.ordenada[100])
        self.assertTrue(resultado.encontrado)
        self.assertEqual(resultado.local, "Região ordenada")
        self.assertEqual(resultado.iteracoes_sequencial, 0)

    def test_insercao_e_busca_na_cauda(self):
        self.lista.inserir(-1)
        self.lista.inserir(-2)
        resultado = self.lista.buscar(-2)
        self.assertEqual(resultado.local, "Cauda não ordenada")
        self.assertEqual(resultado.iteracoes_sequencial, 2)
        self.assertEqual(resultado.total_iteracoes, resultado.iteracoes_binaria + 2)

    def test_rejeita_repetidas(self):
        self.assertFalse(self.lista.inserir(self.lista.ordenada[0])[0])
        self.lista.inserir(-1)
        self.assertFalse(self.lista.inserir(-1)[0])
        self.assertEqual(self.lista.cauda, [-1])

    def test_decima_insercao_intercala(self):
        for chave in range(-10, 0):
            self.assertTrue(self.lista.inserir(chave)[0])
        self.assertEqual(len(self.lista.ordenada), 1034)
        self.assertEqual(self.lista.cauda, [])
        self.assertEqual(self.lista.ordenada, sorted(self.lista.ordenada))
        self.assertEqual(self.lista.intercalacoes, 1)
        self.assertTrue(self.lista.inserir(-11)[0])
        self.assertEqual(self.lista.cauda, [-11])

    def test_nao_encontrada(self):
        self.lista.inserir(-1)
        resultado = self.lista.buscar(-100)
        self.assertFalse(resultado.encontrado)
        self.assertEqual(resultado.iteracoes_sequencial, 1)

    def test_intercalacao_com_valores_intermediarios(self):
        candidatos = [x for x in range(100_000) if x not in set(self.lista.ordenada)][:10]
        for chave in reversed(candidatos):
            self.lista.inserir(chave)
        self.assertEqual(self.lista.ordenada, sorted(self.lista.ordenada))
        self.assertEqual(len(set(self.lista.ordenada)), 1034)

if __name__ == "__main__":
    unittest.main()
