# Sistema de Votação Blockchain

Este projeto implementa um sistema de votação descentralizado utilizando blockchain, desenvolvido em Python com Flask para a API e uma interface gráfica em Tkinter. O sistema garante integridade e transparência ao processo de votação.

---

## Funcionalidades

1. **Registrar votos**: Alunos podem votar em um candidato específico.
2. **Mineração de blocos**: Minerar blocos para adicionar votos à blockchain.
3. **Visualizar blockchain**: Exibir toda a blockchain para auditoria.
4. **Encerrar votação e exibir resultados**: Contabilizar os votos e apresentar o resultado da eleição.

---

## Requisitos

1. Python 3.8 ou superior.
2. Bibliotecas necessárias (listadas no `requirements.txt`):
   - Flask
   - requests
   - tkinter

Para instalar as dependências:
```bash
pip install -r requirements.txt
```

---

## Como executar o sistema

### 1. Iniciar o servidor Flask
Este servidor gerencia a blockchain, permitindo a votação, mineração e sincronização de nós.

No terminal, execute:
```bash
python server.py
```

O servidor será iniciado no endereço padrão `http://127.0.0.1:5000`.

### 2. Executar a interface gráfica (Tkinter)
A interface gráfica permite interações simplificadas com o sistema.

Em outro terminal, execute:
```bash
python interface.py
```

A janela principal da aplicação será aberta com as seguintes opções:
- **Votar**: Registrar um voto.
- **Minerar**: Adicionar os votos pendentes à blockchain.
- **Ver Blockchain**: Visualizar a blockchain completa.
- **Encerrar Votação**: Contabilizar e exibir o resultado da votação.

---

## Detalhes da API

### Endpoints disponíveis

1. **`/vote` (POST)**  
   Registra um novo voto.  
   **Payload esperado**:
   ```json
   {
       "voter_id": "string",
       "candidate": "string"
   }
   ```
   **Resposta**:
   - Sucesso: `201 Created` com mensagem indicando o bloco onde o voto será registrado.

2. **`/mine` (GET)**  
   Realiza a mineração de um novo bloco.  
   **Resposta**:
   - Sucesso: `200 OK` com informações do bloco minerado.

3. **`/chain` (GET)**  
   Exibe a blockchain completa.  
   **Resposta**:
   - Sucesso: `200 OK` com a cadeia completa e seu comprimento.

4. **`/nodes/register` (POST)**  
   Registra novos nós na rede blockchain.  
   **Payload esperado**:
   ```json
   {
       "nodes": ["http://127.0.0.1:5000"]
   }
   ```
   **Resposta**:
   - Sucesso: `201 Created` com a lista atualizada de nós.

5. **`/nodes/resolve` (GET)**  
   Resolve conflitos entre blockchains dos nós da rede.  
   **Resposta**:
   - Sucesso: `200 OK` indicando se a cadeia foi substituída.

---

## Fluxo do sistema

1. **Registro do voto**:
   - O voto é registrado como uma transação pendente.
   - A interface ou API `/vote` é usada para este processo.

2. **Mineração**:
   - Ao minerar, todos os votos pendentes são adicionados a um novo bloco.
   - Este bloco é validado e adicionado à blockchain.

3. **Consulta à blockchain**:
   - A cadeia completa pode ser consultada a qualquer momento para auditoria.

4. **Encerramento da votação**:
   - Todos os votos são contabilizados a partir da blockchain.
   - O resultado final é apresentado na interface gráfica.

---

## Observações

- O sistema foi projetado para ser usado em uma rede local, mas pode ser adaptado para redes distribuídas.
- Certifique-se de que todos os nós na rede estão sincronizados para evitar discrepâncias na blockchain.

---

## Licença

Este projeto é de uso educacional e pode ser modificado livremente para atender às suas necessidades.