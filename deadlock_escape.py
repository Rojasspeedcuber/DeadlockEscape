#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEADLOCK ESCAPE - Jogo Educativo de Programação Paralela e Distribuída

Um jogo educativo que ensina conceitos de concorrência, deadlock e gerenciamento
de recursos através de gameplay interativo e estratégico.

Autor: Henrique Rojas Moreno de Almeida
Disciplina: Programação Paralela e Distribuída
Ano: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import List, Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import time


class ResourceType(Enum):
    """Tipos de recursos disponíveis no sistema."""
    CPU = "CPU"
    MEMORIA = "Memória"
    DISCO = "Disco"
    IMPRESSORA = "Impressora"


class ProcessState(Enum):
    """Estados possíveis de um processo."""
    WAITING = "Aguardando"
    RUNNING = "Executando"
    FINISHED = "Finalizado"
    BLOCKED = "Bloqueado"


@dataclass
class Resource:
    """Representa um recurso do sistema."""
    type: ResourceType
    total: int
    available: int

    def allocate(self, amount: int) -> bool:
        """Aloca uma quantidade do recurso se disponível."""
        if self.available >= amount:
            self.available -= amount
            return True
        return False

    def release(self, amount: int):
        """Libera uma quantidade do recurso."""
        self.available = min(self.total, self.available + amount)


@dataclass
class Process:
    """Representa um processo do sistema."""
    id: str
    name: str
    required_resources: Dict[ResourceType, int]
    allocated_resources: Dict[ResourceType, int]
    state: ProcessState = ProcessState.WAITING

    def __post_init__(self):
        if not self.allocated_resources:
            self.allocated_resources = {rt: 0 for rt in ResourceType}

    def is_satisfied(self) -> bool:
        """Verifica se o processo tem todos os recursos necessários."""
        for resource_type, required in self.required_resources.items():
            if self.allocated_resources.get(resource_type, 0) < required:
                return False
        return True

    def can_finish(self, available_resources: Dict[ResourceType, int]) -> bool:
        """Verifica se o processo pode finalizar com os recursos disponíveis."""
        for resource_type, required in self.required_resources.items():
            still_needed = required - self.allocated_resources.get(resource_type, 0)
            if still_needed > available_resources.get(resource_type, 0):
                return False
        return True


class GameState:
    """Gerencia o estado atual do jogo."""

    def __init__(self, level: int = 1):
        self.level = level
        self.resources = self._initialize_resources()
        self.processes = self._generate_processes()
        self.game_log = []
        self.moves = 0
        self.max_moves = 20

    def _initialize_resources(self) -> Dict[ResourceType, Resource]:
        """Inicializa os recursos baseado no nível."""
        base_amounts = {
            ResourceType.CPU: 4,
            ResourceType.MEMORIA: 4,
            ResourceType.DISCO: 3,
            ResourceType.IMPRESSORA: 2
        }

        # Reduz recursos conforme o nível aumenta
        multiplier = max(0.7, 1.2 - (self.level * 0.1))

        resources = {}
        for resource_type, base_amount in base_amounts.items():
            total = max(2, int(base_amount * multiplier))
            resources[resource_type] = Resource(resource_type, total, total)

        return resources

    def _generate_processes(self) -> List[Process]:
        """Gera processos baseado no nível."""
        process_count = min(2 + self.level, 6)
        processes = []

        process_templates = [
            ("Editor de Texto", {ResourceType.CPU: 1, ResourceType.MEMORIA: 2}),
            ("Compilador", {ResourceType.CPU: 2, ResourceType.MEMORIA: 1, ResourceType.DISCO: 1}),
            ("Backup", {ResourceType.DISCO: 2, ResourceType.MEMORIA: 1}),
            ("Impressão", {ResourceType.IMPRESSORA: 1, ResourceType.MEMORIA: 1}),
            ("Antivírus", {ResourceType.CPU: 1, ResourceType.DISCO: 1, ResourceType.MEMORIA: 1}),
            ("Navegador", {ResourceType.CPU: 2, ResourceType.MEMORIA: 3}),
            ("Streaming", {ResourceType.CPU: 2, ResourceType.MEMORIA: 2, ResourceType.DISCO: 1}),
            ("Banco de Dados", {ResourceType.CPU: 1, ResourceType.MEMORIA: 2, ResourceType.DISCO: 2})
        ]

        selected_templates = random.sample(process_templates, min(process_count, len(process_templates)))

        for i, (name, requirements) in enumerate(selected_templates):
            # Adiciona variação nos requisitos baseado no nível
            varied_requirements = {}
            for resource_type, amount in requirements.items():
                variation = random.randint(-1, 1) if self.level > 2 else 0
                varied_requirements[resource_type] = max(1, amount + variation)

            processes.append(Process(
                id=f"P{i+1}",
                name=name,
                required_resources=varied_requirements,
                allocated_resources={rt: 0 for rt in ResourceType}
            ))

        return processes

    def get_available_resources(self) -> Dict[ResourceType, int]:
        """Retorna recursos disponíveis no sistema."""
        return {rt: resource.available for rt, resource in self.resources.items()}

    def detect_deadlock(self) -> bool:
        """Detecta se há deadlock no sistema usando algoritmo de detecção."""
        # Cria cópia dos recursos disponíveis
        available = self.get_available_resources()

        # Lista de processos que ainda não finalizaram
        unfinished_processes = [p for p in self.processes if p.state != ProcessState.FINISHED]

        if not unfinished_processes:
            return False

        # Algoritmo de detecção de deadlock
        # Tenta encontrar pelo menos um processo que pode terminar
        changed = True
        while changed and unfinished_processes:
            changed = False

            for process in unfinished_processes[:]:
                if process.can_finish(available):
                    # Este processo pode terminar, libera seus recursos
                    for resource_type, allocated in process.allocated_resources.items():
                        available[resource_type] += allocated
                    unfinished_processes.remove(process)
                    changed = True
                    break

        # Se ainda há processos não finalizados, há deadlock
        return len(unfinished_processes) > 0

    def allocate_resource(self, process_id: str, resource_type: ResourceType, amount: int = 1) -> bool:
        """Aloca recurso para um processo."""
        process = next((p for p in self.processes if p.id == process_id), None)
        if not process or process.state == ProcessState.FINISHED:
            return False

        resource = self.resources[resource_type]
        if resource.allocate(amount):
            process.allocated_resources[resource_type] += amount
            self.moves += 1

            # Verifica se o processo pode finalizar
            if process.is_satisfied():
                self._finish_process(process)

            self.game_log.append(f"Alocado {amount} {resource_type.value} para {process.id}")
            return True

        return False

    def _finish_process(self, process: Process):
        """Finaliza um processo e libera seus recursos."""
        process.state = ProcessState.FINISHED

        # Libera todos os recursos do processo
        for resource_type, allocated in process.allocated_resources.items():
            if allocated > 0:
                self.resources[resource_type].release(allocated)
                process.allocated_resources[resource_type] = 0

        self.game_log.append(f"Processo {process.id} ({process.name}) finalizado!")

    def is_level_complete(self) -> bool:
        """Verifica se o nível foi completado."""
        return all(p.state == ProcessState.FINISHED for p in self.processes)

    def is_game_over(self) -> bool:
        """Verifica se o jogo terminou (deadlock ou sem movimentos)."""
        return self.detect_deadlock() or self.moves >= self.max_moves


class DeadlockEscapeGame:
    """Classe principal do jogo Deadlock Escape."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Deadlock Escape")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)

        # Estado do jogo
        self.game_state = None
        self.current_frame = None

        # Cores do tema
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'success': '#27ae60'
        }

        # Inicializa na tela inicial
        self.show_main_menu()

    def clear_frame(self):
        """Remove o frame atual."""
        if self.current_frame:
            self.current_frame.destroy()

    def show_main_menu(self):
        """Exibe a tela inicial do jogo."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.colors['dark'])
        self.current_frame.pack(fill='both', expand=True)

        # Título principal
        title_label = tk.Label(
            self.current_frame,
            text="DEADLOCK ESCAPE",
            font=('Arial', 32, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['dark']
        )
        title_label.pack(pady=(50, 20))

        # Subtítulo
        subtitle_label = tk.Label(
            self.current_frame,
            text="Jogo Educativo de Programação Paralela e Distribuída",
            font=('Arial', 14),
            fg=self.colors['light'],
            bg=self.colors['dark']
        )
        subtitle_label.pack(pady=(0, 30))

        # Texto de boas-vindas
        welcome_text = """Bem-vindo ao Deadlock Escape!

Assuma o papel de um gerente de processos e evite deadlocks
alocando recursos de forma inteligente e estratégica.

Gerencie CPU, Memória, Disco e Impressoras para manter
o sistema funcionando sem bloqueios."""

        welcome_label = tk.Label(
            self.current_frame,
            text=welcome_text,
            font=('Arial', 12),
            fg=self.colors['light'],
            bg=self.colors['dark'],
            justify='center'
        )
        welcome_label.pack(pady=(0, 40))

        # Botões do menu
        button_frame = tk.Frame(self.current_frame, bg=self.colors['dark'])
        button_frame.pack(pady=20)

        play_btn = tk.Button(
            button_frame,
            text="JOGAR",
            font=('Arial', 16, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            width=15,
            height=2,
            command=self.start_game,
            cursor='hand2'
        )
        play_btn.pack(pady=5)

        instructions_btn = tk.Button(
            button_frame,
            text="INSTRUÇÕES",
            font=('Arial', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            width=15,
            height=2,
            command=self.show_instructions,
            cursor='hand2'
        )
        instructions_btn.pack(pady=5)

        exit_btn = tk.Button(
            button_frame,
            text="SAIR",
            font=('Arial', 16, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            width=15,
            height=2,
            command=self.root.quit,
            cursor='hand2'
        )
        exit_btn.pack(pady=5)

        # Rodapé
        footer_label = tk.Label(
            self.current_frame,
            text="© 2025 - Equipe de Desenvolvimento",
            font=('Arial', 10),
            fg=self.colors['light'],
            bg=self.colors['dark']
        )
        footer_label.pack(side='bottom', pady=20)

    def show_instructions(self):
        """Exibe a tela de instruções."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.colors['dark'])
        self.current_frame.pack(fill='both', expand=True)

        # Título
        title_label = tk.Label(
            self.current_frame,
            text="COMO JOGAR - DEADLOCK ESCAPE",
            font=('Arial', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['dark']
        )
        title_label.pack(pady=(30, 20))

        # Frame scrollável para instruções
        canvas = tk.Canvas(self.current_frame, bg=self.colors['dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.current_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['dark'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Instruções detalhadas
        instructions = [
            ("OBJETIVO:", "Evitar deadlocks gerenciando recursos do sistema de forma eficiente."),
            ("RECURSOS:", "• CPU: Processamento\n• Memória: Armazenamento temporário\n• Disco: Armazenamento permanente\n• Impressora: Dispositivo de saída"),
            ("REGRAS:", "• Processos precisam de recursos específicos para funcionar\n• Aloque recursos clicando nos botões correspondentes\n• Um processo só termina quando tem TODOS os recursos necessários\n• Recursos ocupados não podem ser usados por outros processos"),
            ("DEADLOCK:", "Ocorre quando processos ficam esperando uns pelos outros indefinidamente.\nEvite criar dependências circulares!"),
            ("VITÓRIA:", "Complete todos os processos sem criar deadlocks."),
            ("DERROTA:", "Deadlock detectado ou muitos movimentos sem progresso."),
            ("DICAS:", "• Analise os requisitos antes de alocar\n• Prefira finalizar processos com menos recursos primeiro\n• Use o algoritmo do banqueiro: sempre mantenha o sistema em estado seguro")
        ]

        for title, content in instructions:
            section_frame = tk.Frame(scrollable_frame, bg=self.colors['dark'])
            section_frame.pack(fill='x', padx=40, pady=(10, 5))

            title_label = tk.Label(
                section_frame,
                text=title,
                font=('Arial', 14, 'bold'),
                fg=self.colors['warning'],
                bg=self.colors['dark'],
                anchor='w'
            )
            title_label.pack(anchor='w')

            content_label = tk.Label(
                section_frame,
                text=content,
                font=('Arial', 11),
                fg=self.colors['light'],
                bg=self.colors['dark'],
                anchor='w',
                justify='left',
                wraplength=800
            )
            content_label.pack(anchor='w', padx=(20, 0))

        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 20))

        # Botão voltar
        back_btn = tk.Button(
            self.current_frame,
            text="Voltar ao Menu",
            font=('Arial', 14, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            width=20,
            height=2,
            command=self.show_main_menu,
            cursor='hand2'
        )
        back_btn.pack(side='bottom', pady=20)

    def start_game(self):
        """Inicia um novo jogo."""
        self.game_state = GameState(level=1)
        self.show_game_screen()

    def show_game_screen(self):
        """Exibe a tela principal do jogo."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.colors['dark'])
        self.current_frame.pack(fill='both', expand=True)

        # Header com informações do jogo
        header_frame = tk.Frame(self.current_frame, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)

        level_label = tk.Label(
            header_frame,
            text=f"NÍVEL {self.game_state.level}",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        level_label.pack(side='left', padx=20, pady=15)

        moves_label = tk.Label(
            header_frame,
            text=f"Movimentos: {self.game_state.moves}/{self.game_state.max_moves}",
            font=('Arial', 12),
            fg='white',
            bg=self.colors['primary']
        )
        moves_label.pack(side='right', padx=20, pady=15)

        # Frame principal dividido em colunas
        main_frame = tk.Frame(self.current_frame, bg=self.colors['dark'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Coluna esquerda: Recursos e Processos
        left_frame = tk.Frame(main_frame, bg=self.colors['light'], width=600)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        left_frame.pack_propagate(False)

        # Seção de recursos
        self.create_resources_section(left_frame)

        # Seção de processos
        self.create_processes_section(left_frame)

        # Coluna direita: Log e controles
        right_frame = tk.Frame(main_frame, bg=self.colors['light'], width=300)
        right_frame.pack(side='right', fill='both', padx=(5, 0))
        right_frame.pack_propagate(False)

        # Log do sistema
        self.create_log_section(right_frame)

        # Botões de controle
        self.create_control_buttons(right_frame)

        # Atualiza a interface
        self.update_game_display()

    def create_resources_section(self, parent):
        """Cria a seção de recursos disponíveis."""
        resources_frame = tk.LabelFrame(
            parent,
            text="Recursos Disponíveis",
            font=('Arial', 14, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['dark']
        )
        resources_frame.pack(fill='x', padx=10, pady=10)

        self.resource_labels = {}
        resource_icons = {
            ResourceType.CPU: "🖥️",
            ResourceType.MEMORIA: "💾",
            ResourceType.DISCO: "💿",
            ResourceType.IMPRESSORA: "🖨️"
        }

        for i, (resource_type, resource) in enumerate(self.game_state.resources.items()):
            frame = tk.Frame(resources_frame, bg=self.colors['light'])
            frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky='w')

            icon_label = tk.Label(
                frame,
                text=resource_icons[resource_type],
                font=('Arial', 16),
                bg=self.colors['light']
            )
            icon_label.pack(side='left')

            name_label = tk.Label(
                frame,
                text=resource_type.value + ":",
                font=('Arial', 12, 'bold'),
                bg=self.colors['light'],
                fg=self.colors['dark']
            )
            name_label.pack(side='left', padx=(5, 10))

            self.resource_labels[resource_type] = tk.Label(
                frame,
                text="",
                font=('Arial', 12),
                bg=self.colors['light'],
                fg=self.colors['primary']
            )
            self.resource_labels[resource_type].pack(side='left')

    def create_processes_section(self, parent):
        """Cria a seção de processos ativos."""
        processes_frame = tk.LabelFrame(
            parent,
            text="Processos Ativos",
            font=('Arial', 14, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['dark']
        )
        processes_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Canvas scrollável para processos
        canvas = tk.Canvas(processes_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(processes_frame, orient="vertical", command=canvas.yview)
        self.processes_scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])

        self.processes_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.processes_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.process_frames = {}

    def create_log_section(self, parent):
        """Cria a seção de log do sistema."""
        log_frame = tk.LabelFrame(
            parent,
            text="Log do Sistema",
            font=('Arial', 14, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['dark']
        )
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Text widget com scrollbar para o log
        log_text_frame = tk.Frame(log_frame, bg=self.colors['light'])
        log_text_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.log_text = tk.Text(
            log_text_frame,
            font=('Consolas', 9),
            bg='#1e1e1e',
            fg='#00ff00',
            height=15,
            state='disabled',
            wrap='word'
        )

        log_scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")

    def create_control_buttons(self, parent):
        """Cria os botões de controle do jogo."""
        control_frame = tk.Frame(parent, bg=self.colors['light'])
        control_frame.pack(fill='x', padx=10, pady=10)

        check_deadlock_btn = tk.Button(
            control_frame,
            text="Verificar Deadlock",
            font=('Arial', 11, 'bold'),
            bg=self.colors['warning'],
            fg='white',
            command=self.check_deadlock_manual,
            cursor='hand2'
        )
        check_deadlock_btn.pack(fill='x', pady=2)

        restart_btn = tk.Button(
            control_frame,
            text="Reiniciar Nível",
            font=('Arial', 11, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            command=self.restart_level,
            cursor='hand2'
        )
        restart_btn.pack(fill='x', pady=2)

        menu_btn = tk.Button(
            control_frame,
            text="Menu Principal",
            font=('Arial', 11, 'bold'),
            bg=self.colors['dark'],
            fg='white',
            command=self.show_main_menu,
            cursor='hand2'
        )
        menu_btn.pack(fill='x', pady=2)

    def update_game_display(self):
        """Atualiza toda a interface do jogo."""
        self.update_resources_display()
        self.update_processes_display()
        self.update_log_display()

        # Verifica condições de fim de jogo
        if self.game_state.is_level_complete():
            self.root.after(500, self.show_victory_screen)
        elif self.game_state.is_game_over():
            self.root.after(500, self.show_game_over_screen)

    def update_resources_display(self):
        """Atualiza a exibição dos recursos."""
        for resource_type, resource in self.game_state.resources.items():
            available_blocks = "■" * resource.available
            used_blocks = "□" * (resource.total - resource.available)
            display_text = f"{available_blocks}{used_blocks} ({resource.available}/{resource.total})"
            self.resource_labels[resource_type].config(text=display_text)

    def update_processes_display(self):
        """Atualiza a exibição dos processos."""
        # Limpa frames existentes
        for frame in self.process_frames.values():
            frame.destroy()
        self.process_frames.clear()

        for i, process in enumerate(self.game_state.processes):
            if process.state == ProcessState.FINISHED:
                continue

            process_frame = tk.Frame(
                self.processes_scrollable_frame,
                bg='white',
                relief='solid',
                bd=1
            )
            process_frame.pack(fill='x', padx=5, pady=5)
            self.process_frames[process.id] = process_frame

            # Header do processo
            header_frame = tk.Frame(process_frame, bg=self.colors['primary'])
            header_frame.pack(fill='x')

            process_title = tk.Label(
                header_frame,
                text=f"{process.id}: {process.name}",
                font=('Arial', 11, 'bold'),
                fg='white',
                bg=self.colors['primary']
            )
            process_title.pack(side='left', padx=10, pady=5)

            status_color = self.colors['success'] if process.is_satisfied() else self.colors['warning']
            status_label = tk.Label(
                header_frame,
                text=process.state.value,
                font=('Arial', 10),
                fg='white',
                bg=status_color
            )
            status_label.pack(side='right', padx=10, pady=5)

            # Recursos do processo
            resources_frame = tk.Frame(process_frame, bg='white')
            resources_frame.pack(fill='x', padx=10, pady=5)

            for j, (resource_type, required) in enumerate(process.required_resources.items()):
                allocated = process.allocated_resources.get(resource_type, 0)

                resource_row = tk.Frame(resources_frame, bg='white')
                resource_row.grid(row=j//2, column=j%2, sticky='w', padx=(0, 20))

                resource_label = tk.Label(
                    resource_row,
                    text=f"{resource_type.value}:",
                    font=('Arial', 10),
                    bg='white'
                )
                resource_label.pack(side='left')

                progress_text = f"{allocated}/{required}"
                progress_color = self.colors['success'] if allocated >= required else self.colors['danger']

                progress_label = tk.Label(
                    resource_row,
                    text=progress_text,
                    font=('Arial', 10, 'bold'),
                    fg=progress_color,
                    bg='white'
                )
                progress_label.pack(side='left', padx=(5, 10))

                # Botão de alocação
                if allocated < required and self.game_state.resources[resource_type].available > 0:
                    alloc_btn = tk.Button(
                        resource_row,
                        text="+",
                        font=('Arial', 8, 'bold'),
                        bg=self.colors['secondary'],
                        fg='white',
                        width=3,
                        command=lambda pid=process.id, rt=resource_type: self.allocate_resource(pid, rt),
                        cursor='hand2'
                    )
                    alloc_btn.pack(side='left')

    def update_log_display(self):
        """Atualiza o log do sistema."""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)

        # Adiciona informações do sistema
        self.log_text.insert(tk.END, f"=== SISTEMA DEADLOCK ESCAPE ===\n")
        self.log_text.insert(tk.END, f"Nível: {self.game_state.level}\n")
        self.log_text.insert(tk.END, f"Movimentos: {self.game_state.moves}/{self.game_state.max_moves}\n")
        self.log_text.insert(tk.END, f"Processos ativos: {len([p for p in self.game_state.processes if p.state != ProcessState.FINISHED])}\n\n")

        # Adiciona log de ações
        for entry in self.game_state.game_log[-10:]:  # Últimas 10 entradas
            timestamp = time.strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {entry}\n")

        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def allocate_resource(self, process_id: str, resource_type: ResourceType):
        """Aloca um recurso para um processo."""
        if self.game_state.allocate_resource(process_id, resource_type):
            self.update_game_display()
        else:
            messagebox.showwarning(
                "Recurso Indisponível",
                f"Não há {resource_type.value} disponível para alocação."
            )

    def check_deadlock_manual(self):
        """Verifica deadlock manualmente a pedido do usuário."""
        has_deadlock = self.game_state.detect_deadlock()
        if has_deadlock:
            messagebox.showwarning(
                "Deadlock Detectado!",
                "O sistema está em deadlock. Os processos estão esperando uns pelos outros indefinidamente."
            )
        else:
            messagebox.showinfo(
                "Sistema Seguro",
                "Nenhum deadlock detectado. O sistema está em um estado seguro."
            )

    def restart_level(self):
        """Reinicia o nível atual."""
        if messagebox.askyesno("Reiniciar Nível", "Deseja reiniciar o nível atual?"):
            self.game_state = GameState(level=self.game_state.level)
            self.show_game_screen()

    def show_victory_screen(self):
        """Exibe a tela de vitória."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.colors['success'])
        self.current_frame.pack(fill='both', expand=True)

        # Título de vitória
        title_label = tk.Label(
            self.current_frame,
            text="SISTEMA ESTÁVEL!",
            font=('Arial', 36, 'bold'),
            fg='white',
            bg=self.colors['success']
        )
        title_label.pack(pady=(100, 30))

        # Mensagem de parabéns
        message_text = f"""Parabéns! Você completou o Nível {self.game_state.level}!

Todos os processos foram executados com sucesso
sem causar deadlocks no sistema.

Movimentos utilizados: {self.game_state.moves}/{self.game_state.max_moves}

Você demonstrou excelente compreensão de:
• Gerenciamento de recursos
• Prevenção de deadlocks
• Algoritmos de alocação segura"""

        message_label = tk.Label(
            self.current_frame,
            text=message_text,
            font=('Arial', 14),
            fg='white',
            bg=self.colors['success'],
            justify='center'
        )
        message_label.pack(pady=(0, 50))

        # Botões
        button_frame = tk.Frame(self.current_frame, bg=self.colors['success'])
        button_frame.pack()

        next_level_btn = tk.Button(
            button_frame,
            text="Próximo Nível",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg=self.colors['success'],
            width=15,
            height=2,
            command=self.next_level,
            cursor='hand2'
        )
        next_level_btn.pack(pady=5)

        menu_btn = tk.Button(
            button_frame,
            text="Menu Principal",
            font=('Arial', 14),
            bg=self.colors['dark'],
            fg='white',
            width=15,
            height=2,
            command=self.show_main_menu,
            cursor='hand2'
        )
        menu_btn.pack(pady=5)

    def show_game_over_screen(self):
        """Exibe a tela de game over."""
        self.clear_frame()

        self.current_frame = tk.Frame(self.root, bg=self.colors['danger'])
        self.current_frame.pack(fill='both', expand=True)

        # Título de game over
        title_label = tk.Label(
            self.current_frame,
            text="DEADLOCK DETECTADO!",
            font=('Arial', 36, 'bold'),
            fg='white',
            bg=self.colors['danger']
        )
        title_label.pack(pady=(100, 30))

        # Explicação do deadlock
        explanation_text = f"""O sistema entrou em deadlock!

Os processos estão esperando uns pelos outros indefinidamente,
criando uma dependência circular que impede o progresso.

Nível: {self.game_state.level}
Movimentos realizados: {self.game_state.moves}

CAUSAS COMUNS DE DEADLOCK:
• Alocação inadequada de recursos
• Dependências circulares entre processos
• Falta de planejamento na ordem de alocação

DICA: Use o algoritmo do banqueiro para verificar
se o sistema permanece em estado seguro após cada alocação."""

        explanation_label = tk.Label(
            self.current_frame,
            text=explanation_text,
            font=('Arial', 12),
            fg='white',
            bg=self.colors['danger'],
            justify='center'
        )
        explanation_label.pack(pady=(0, 50))

        # Botões
        button_frame = tk.Frame(self.current_frame, bg=self.colors['danger'])
        button_frame.pack()

        restart_btn = tk.Button(
            button_frame,
            text="Reiniciar",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg=self.colors['danger'],
            width=15,
            height=2,
            command=self.restart_level,
            cursor='hand2'
        )
        restart_btn.pack(pady=5)

        menu_btn = tk.Button(
            button_frame,
            text="Menu Principal",
            font=('Arial', 14),
            bg=self.colors['dark'],
            fg='white',
            width=15,
            height=2,
            command=self.show_main_menu,
            cursor='hand2'
        )
        menu_btn.pack(pady=5)

    def next_level(self):
        """Avança para o próximo nível."""
        self.game_state = GameState(level=self.game_state.level + 1)
        self.show_game_screen()

    def run(self):
        """Executa o jogo."""
        self.root.mainloop()


def main():
    """Função principal do programa."""
    print("Iniciando Deadlock Escape...")
    print("Jogo Educativo de Programação Paralela e Distribuída")
    print("Autor: Henrique Rojas Moreno de Almeida")
    print("=" * 50)

    try:
        game = DeadlockEscapeGame()
        game.run()
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        messagebox.showerror("Erro", f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()