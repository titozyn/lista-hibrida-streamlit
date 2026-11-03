"""Interface Streamlit da atividade Lista Híbrida."""
import streamlit as st
from lista_hibrida import ListaHibrida

st.set_page_config(page_title="Lista Híbrida", page_icon="🔎", layout="wide")
st.title("🔎 Lista Híbrida — Busca e Reordenação")
st.write("Região ordenada de 1.024 inteiros distintos + cauda não ordenada de até 10 chaves.")

if "lista" not in st.session_state:
    st.session_state.lista = ListaHibrida()
if "historico" not in st.session_state:
    st.session_state.historico = []

with st.sidebar:
    st.header("Configuração")
    semente = st.number_input("Semente aleatória", value=42, step=1)
    if st.button("Reiniciar lista", use_container_width=True):
        st.session_state.lista = ListaHibrida(semente=int(semente))
        st.session_state.historico = []
        st.rerun()
    st.caption("A mesma semente gera a mesma região inicial.")

lista = st.session_state.lista
c1, c2, c3 = st.columns(3)
c1.metric("Região ordenada", len(lista.ordenada))
c2.metric("Cauda", f"{len(lista.cauda)}/{lista.capacidade_cauda}")
c3.metric("Intercalações realizadas", lista.intercalacoes)

aba_inserir, aba_buscar, aba_dados, aba_codigo = st.tabs(["➕ Inserir", "🔍 Buscar", "📋 Visualizar", "🧠 Componentes e código"])

with aba_inserir:
    with st.form("insercao", clear_on_submit=True):
        nova = st.number_input("Número inteiro para inserir", value=0, step=1, format="%d")
        enviar = st.form_submit_button("Inserir chave")
    if enviar:
    ok, mensagem = lista.inserir(int(nova))

    st.session_state.historico.append(
        f"Inserção {int(nova)}: {mensagem}"
    )

    st.session_state.mensagem_insercao = (ok, mensagem)

    st.rerun()

if "mensagem_insercao" in st.session_state:
    ok, mensagem = st.session_state.pop("mensagem_insercao")
    (st.success if ok else st.warning)(mensagem)

    

with aba_buscar:
    with st.form("busca"):
        chave = st.number_input("Chave a buscar", value=0, step=1, format="%d")
        pesquisar = st.form_submit_button("Buscar chave")
    if pesquisar:
        resultado = lista.buscar(int(chave))
        if resultado.encontrado:
            st.success(f"Encontrada na {resultado.local}, índice {resultado.indice} (índice começa em zero).")
        else:
            st.warning("Chave não encontrada.")
        b, s, t = st.columns(3)
        b.metric("Iterações binárias", resultado.iteracoes_binaria)
        s.metric("Iterações sequenciais", resultado.iteracoes_sequencial)
        t.metric("Total de iterações", resultado.total_iteracoes)
        st.session_state.historico.append(f"Busca {int(chave)}: {resultado.local}, {resultado.total_iteracoes} iterações")

with aba_dados:
    st.write("**Região ordenada:**")
    st.dataframe([{"Índice": i, "Chave": valor} for i, valor in enumerate(lista.ordenada)], hide_index=True, use_container_width=True, height=260)
    st.write("**Cauda não ordenada:**")
    st.dataframe([{"Índice": i, "Chave": valor} for i, valor in enumerate(lista.cauda)], hide_index=True, use_container_width=True)
    st.write("**Histórico desta sessão:**")
    st.text("\n".join(st.session_state.historico[-20:]) or "Nenhuma operação ainda.")

with aba_codigo:
    st.markdown("""### Componentes usados
- `random.Random(semente).sample`: gera 1.024 inteiros distintos de forma reprodutível.
- `sorted`: organiza os números iniciais e a cauda no momento da intercalação.
- `buscar`: busca binária na região ordenada, seguida de busca sequencial na cauda.
- `inserir`: rejeita repetidos, adiciona ao final da cauda e dispara a intercalação na 10ª inserção.
- `_intercalar`: combina duas listas já ordenadas preservando a ordem crescente.
- `st.session_state`: mantém os dados entre interações no Streamlit.
- `st.form`, `st.metric`, `st.dataframe`: interface de inserção, indicadores e visualização.
""")
    with st.expander("Código: busca binária e sequencial", expanded=True):
        st.code('''esquerda, direita = 0, len(self.ordenada) - 1
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
        return ResultadoBusca(True, "Cauda não ordenada", indice, binaria, indice + 1)''', language="python")
    with st.expander("Código: inserção e disparo da intercalação"):
        st.code('''if self.buscar(chave).encontrado:
    return False, "Chave repetida: inserção rejeitada."
self.cauda.append(chave)
if len(self.cauda) == self.capacidade_cauda:
    self._intercalar()''', language="python")
    with st.expander("Código: intercalação ordenada"):
        st.code('''cauda_ordenada = sorted(self.cauda)
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
self.cauda.clear()''', language="python")
