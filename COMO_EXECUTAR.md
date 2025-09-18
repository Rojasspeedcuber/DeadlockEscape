# 🎮 Como Executar o Deadlock Escape

## 📋 Pré-requisitos

- **Python 3.7 ou superior** instalado no sistema
- **tkinter** (incluído por padrão na maioria das instalações Python)

### Verificando se o Python está instalado:
```bash
python --version
```
ou
```bash
python3 --version
```

### Verificando se o tkinter está disponível:
```bash
python -c "import tkinter; print('tkinter está disponível!')"
```

## 🚀 Como Executar

Existem duas formas de executar o jogo:

### Método 1: Execução Direta
```bash
python deadlock_escape.py
```

### Método 2: Script de Execução
```bash
python run_game.py
```

## 📁 Estrutura do Projeto

```
DeadlockEscape/
├── deadlock_escape.py     # Arquivo principal do jogo
├── run_game.py           # Script alternativo de execução
├── requirements.txt      # Dependências (apenas Python padrão)
├── README.md            # Documentação do projeto
├── COMO_EXECUTAR.md     # Este arquivo
├── .gitignore          # Arquivos ignorados pelo Git
└── imgs/               # Mockups e assets (não incluídos no Git)
```

## 🎯 Instruções do Jogo

1. **Execute o jogo** usando um dos métodos acima
2. **Clique em "JOGAR"** na tela inicial
3. **Leia as instruções** clicando em "INSTRUÇÕES" se necessário
4. **Aloque recursos** clicando nos botões "+" ao lado de cada processo
5. **Evite deadlocks** planejando cuidadosamente a ordem de alocação
6. **Complete todos os processos** para avançar de nível

## 🔧 Solução de Problemas

### Erro: "No module named 'tkinter'"
- **Linux/Ubuntu**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter` ou `sudo dnf install python3-tkinter`
- **macOS**: Reinstale o Python ou use: `brew install python-tk`
- **Windows**: Reinstale o Python marcando a opção "tcl/tk and IDLE"

### Erro: "No module named 'dataclasses'"
- **Python < 3.7**: `pip install dataclasses`

### Interface não aparece ou aparece cortada
- Verifique a resolução da tela (mínimo recomendado: 1000x700)
- Alguns gerenciadores de janela podem requerer ajustes de DPI

## 🎓 Conceitos Educativos

Este jogo ensina:
- **Deadlock**: condições e prevenção
- **Algoritmo do Banqueiro** de Dijkstra
- **Gerenciamento de recursos** em sistemas operacionais
- **Concorrência** e **programação paralela**

## 👨‍💻 Desenvolvimento

- **Linguagem**: Python 3.7+
- **Interface**: tkinter (GUI nativa)
- **Paradigma**: Orientação a Objetos
- **Padrões**: MVC, Observer

## 📞 Suporte

Se encontrar problemas:
1. Verifique se todos os pré-requisitos estão instalados
2. Teste com diferentes versões do Python (3.7, 3.8, 3.9+)
3. Verifique as permissões de execução dos arquivos

---

**Desenvolvido por**: Henrique Rojas Moreno de Almeida
**Disciplina**: Programação Paralela e Distribuída
**Ano**: 2025