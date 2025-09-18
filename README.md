# 🎮 Deadlock Escape

## 📌 Descrição do Jogo
**Deadlock Escape** é um jogo educativo digital no estilo **puzzle/estratégia**, cujo objetivo é ensinar e consolidar conceitos fundamentais de concorrência e gerenciamento de recursos na **programação paralela e distribuída**.  

No jogo, o jogador assume o papel de um **gerente de processos** que deve alocar recursos (CPU, impressoras, memória e discos) a diferentes tarefas.  
A cada rodada, múltiplos processos solicitam recursos simultaneamente, e o jogador precisa decidir a ordem de alocação para **evitar condições de corrida e deadlocks**.  

- ✅ Alocação correta → Sistema flui sem bloqueios  
- ❌ Alocação incorreta → Deadlock (“Game Over”)  

---

## 🎓 Conceitos Ensinados
O jogo aborda os seguintes conceitos de programação paralela e distribuída:

- Concorrência entre processos e threads  
- **Deadlock**: condições, detecção e prevenção  
- Semáforos, locks e controle de acesso a recursos compartilhados  
- Alocação segura de recursos (baseado no **Algoritmo do Banqueiro de Dijkstra**)  

---

## 🎯 Objetivos do Jogo
- Evitar **deadlocks** ao gerenciar corretamente múltiplos processos que competem por recursos limitados  
- **Maximizar a eficiência do sistema**, garantindo a execução de todos os processos sem bloqueios  
- Ensinar, de forma lúdica, como decisões incorretas em sistemas paralelos e distribuídos podem levar a falhas críticas  

---

## 🕹️ Mecânica, Regras e Dinâmica

### 🔹 Mecânica
- O jogador visualiza uma lista de processos ativos, cada um solicitando recursos (CPU, memória, disco, impressora).  
- Os recursos são limitados e devem ser distribuídos entre os processos.  
- O jogador escolhe a ordem de alocação:  
  - **Alocação correta** → processos finalizam sem deadlock (Vitória).  
  - **Alocação incorreta** → ocorre espera circular → Deadlock (Game Over).  

### 🔹 Regras
- Um processo só finaliza se receber **todos os recursos** que solicitou.  
- Recursos alocados permanecem ocupados até a finalização do processo.  
- Se houver **espera circular** (condição de Coffman) → Deadlock.  
- O tempo de resposta é limitado (por turnos ou cronômetro).  

### 🔹 Dinâmica
- **Fase 1**: Poucos processos e muitos recursos (nível introdutório).  
- **Fase 2**: Recursos mais escassos → decisões estratégicas.  
- **Fase 3**: Muitos processos competindo, exigindo raciocínio avançado (similar ao **Algoritmo do Banqueiro**).  
- Em caso de derrota (**Deadlock – Game Over**), o jogador deve retornar ao nível inicial.  

---

## 🎨 Protótipo Visual (Mockups)

### Tela Inicial
![Tela Inicial](./imgs/tela_inicial.png)

### Tela de Jogo – Interface Principal
![Tela de Jogo](./imgs/tela_jogo.png)

### Tela de Vitória
![Tela de Vitória](./imgs/tela_vitória.png)

### Tela de Game Over (Deadlock)
![Tela Game Over](./imgs/tela_game_over.png)

### Tela de Instruções
![Tela de Instruções](./imgs/tela_instruções.png)

---

## 👨‍💻 Autor
- **Aluno**: Henrique Rojas Moreno de Almeida  
- **Disciplina**: Programação Paralela e Distribuída  

---
