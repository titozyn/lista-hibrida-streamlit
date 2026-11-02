# Lista Híbrida com Busca e Reordenação

Projeto da atividade extra de Estruturas de Dados: Python + Streamlit.

## Executar localmente

1. Instale Python 3.10 ou superior.
2. Abra o terminal na pasta do projeto.
3. Instale dependências: `python -m pip install -r requirements.txt`
4. Execute: `python -m streamlit run app.py`
5. Acesse a URL local indicada no terminal.

## Testes automatizados

`python -m unittest discover -v`

## Publicar no Streamlit Community Cloud

1. Crie um repositório no GitHub e envie `app.py`, `lista_hibrida.py`, `test_lista_hibrida.py`, `requirements.txt` e `README.md`.
2. Acesse https://share.streamlit.io/ e entre com sua conta.
3. Escolha **Create app** / **Deploy**, selecione seu repositório, branch e arquivo principal `app.py`.
4. Confirme o deploy e copie o link público gerado.

**Atenção:** o link público não pode ser gerado apenas a partir deste ZIP. É necessário publicar o projeto na sua conta.

## Explicação resumida

- `ListaHibrida.__init__`: gera 1.024 números distintos com `random.Random(semente).sample` e ordena.
- `buscar`: usa busca binária primeiro; se não encontrar, percorre a cauda sequencialmente; contabiliza comparações/iterações.
- `inserir`: impede duplicatas, insere na cauda e, na décima inserção, chama `_intercalar`.
- `_intercalar`: ordena somente a cauda, intercala as duas regiões ordenadas e esvazia a cauda.
- `st.session_state`: preserva a lista e o histórico durante as interações no navegador.
- `test_lista_hibrida.py`: verifica geração, buscas, duplicatas, intercalação e novas inserções.

## Demonstração sugerida

1. Abra a aba **Visualizar** para mostrar os 1.024 valores ordenados.
2. Busque um valor existente na região ordenada.
3. Insira um valor que não exista (por exemplo, `-1`) e busque-o na cauda.
4. Tente inserir `-1` novamente e observe a rejeição.
5. Insira mais nove valores distintos e observe a intercalação e a cauda vazia.
6. Insira mais um valor e mostre que o processo continua.
7. Mostre a aba **Componentes e código** e execute os testes no terminal.

## Observações

- Os índices exibidos começam em zero, como é padrão no Python.
- A semente é aplicada ao clicar em **Reiniciar lista**.
- O estado é mantido por sessão de navegador, não em banco de dados.
