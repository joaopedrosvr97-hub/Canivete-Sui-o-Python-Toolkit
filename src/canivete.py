#!/usr/bin/env python3
# canivete_gui.py
# Canivete Suíço - GUI (Tkinter)
# ATENÇÃO: muitas funções alteram o sistema — confirmar antes de executar.

import os
import platform
import subprocess
import sys
import tempfile
from datetime import datetime
import threading
import shutil
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# -----------------------------
# CONFIGURAÇÕES GLOBAIS
# -----------------------------
SYSTEM = platform.system()
BASE_DIR = os.getcwd()
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"toolkit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Encoding para comandos no Windows (evita erro 'utf-8' codec ...)
WIN_ENCODING = "cp850"

# -----------------------------
# UTILITÁRIOS: LOGS e EXEC
# -----------------------------
def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {level}: {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8", errors="ignore") as f:
            f.write(line + "\n")
    except Exception:
        pass

def run_command(cmd, capture=True, shell=False):
    """
    Executa comando. cmd pode ser lista (recomendado) ou string (shell=True).
    Retorna (returncode, stdout+stderr)
    """
    enc = WIN_ENCODING if SYSTEM == "Windows" else "utf-8"
    try:
        if capture:
            proc = subprocess.run(cmd, capture_output=True, text=True, shell=shell, encoding=enc, errors="ignore")
            out = (proc.stdout or "") + (proc.stderr or "")
            log(f"CMD: {cmd} -> RC={proc.returncode}")
            return proc.returncode, out
        else:
            proc = subprocess.run(cmd, shell=shell)
            log(f"CMD(no capture): {cmd} -> RC={proc.returncode}")
            return proc.returncode, ""
    except Exception as e:
        log(f"Erro ao executar: {cmd} -> {e}", level="ERROR")
        return -1, f"Exception: {e}\n{traceback.format_exc()}"

def is_admin():
    if SYSTEM != "Windows":
        return os.geteuid() == 0 if hasattr(os, "geteuid") else False
    # Windows: use ctypes
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def confirm_admin_and_proceed(action_desc):
    if not is_admin():
        if messagebox.askyesno("Permissão necessária", f"A ação '{action_desc}' precisa de privilégios de administrador.\n\nDeseja reiniciar o programa como administrador agora?"):
            # Relaunch as admin (Windows-specific)
            if SYSTEM == "Windows":
                import ctypes
                script = sys.argv[0]
                params = " ".join([f'"{p}"' for p in sys.argv[1:]])
                try:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
                    sys.exit(0)
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao tentar reiniciar como administrador: {e}")
                    return False
            else:
                messagebox.showinfo("Como root", "No Linux/macOS execute o terminal como root e inicie o script.")
                return False
        return False
    return True

# -----------------------------
# FUNÇÕES PRINCIPAIS (equivalentes ao batch)
# -----------------------------

def action_reiniciar():
    if not confirm_admin_and_proceed("Reiniciar sistema"):
        return "Reinício cancelado"
    if messagebox.askyesno("Reiniciar", "Deseja reiniciar o sistema agora?"):
        if SYSTEM == "Windows":
            rc, out = run_command(["shutdown", "/r", "/t", "5", "/c", "Reinicio iniciado pelo Toolkit"], capture=False)
            return "Comando de reinício emitido."
        else:
            rc, out = run_command(["sudo", "shutdown", "-r", "now"], capture=False)
            return out
    return "Ação não confirmada."

def action_flush_dns():
    if SYSTEM == "Windows":
        rc, out = run_command(["ipconfig", "/flushdns"])
        run_command(["ipconfig", "/registerdns"])
        return out or "Flush DNS executado."
    else:
        # Tentativas para diferentes distros
        rc, out = run_command(["sudo", "systemd-resolve", "--flush-caches"])
        if rc != 0:
            rc, out = run_command(["sudo", "resolvectl", "flush-caches"])
        return out

def action_coletar_info_rede():
    temp = os.path.join(tempfile.gettempdir(), f"rede_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    lines = []
    if SYSTEM == "Windows":
        _, ip_all = run_command(["ipconfig", "/all"])
        lines.append(ip_all)
        _, arp = run_command(["arp", "-a"])
        lines.append("\n\n=== ARP ===\n")
        lines.append(arp)
        _, routes = run_command(["route", "print"])
        lines.append("\n\n=== ROUTES ===\n")
        lines.append(routes)
    else:
        _, ifc = run_command(["ifconfig"])
        lines.append(ifc)
        _, routes = run_command(["route", "-n"])
        lines.append("\n\n=== ROUTES ===\n")
        lines.append(routes)
    try:
        with open(temp, "w", encoding="utf-8", errors="ignore") as f:
            f.write("\n".join(lines))
        log(f"Relatório de rede salvo em {temp}")
        return f"Relatório salvo em: {temp}"
    except Exception as e:
        log(f"Erro ao salvar relatório: {e}", level="ERROR")
        return f"Erro ao salvar relatório: {e}"

def action_impressoras_panel():
    if SYSTEM == "Windows":
        rc, out = run_command(["control", "printers"])
        return out or "Painel de impressoras aberto."
    else:
        return "Painel de impressoras não suportado nesta plataforma."

def action_reiniciar_spooler():
    if not confirm_admin_and_proceed("Reiniciar spooler de impressão"):
        return "Cancelado"
    if SYSTEM == "Windows":
        run_command(["net", "stop", "spooler"])
        run_command(["net", "start", "spooler"])
        return "Spooler reiniciado."
    return "Não suportado."

def action_printer_fixes_all():
    if not confirm_admin_and_proceed("Aplicar correções de impressora (registry)"):
        return "Cancelado"
    if not messagebox.askyesno("Confirmação", "As correções alteram o registro do Windows. Deseja continuar?"):
        return "Ação não confirmada."
    if SYSTEM == "Windows":
        cmds = [
            ["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\Print", "/v", "RpcAuthnLevelPrivacyEnabled", "/t", "REG_DWORD", "/d", "0", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Printers\PointAndPrint", "/v", "RestrictDriverInstallationToAdministrators", "/t", "REG_DWORD", "/d", "0", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Printers\RPC", "/v", "RpcUseNamedPipeProtocol", "/t", "REG_DWORD", "/d", "1", "/f"],
            ["net", "stop", "spooler", "/y"],
            ["net", "start", "spooler"]
        ]
        for c in cmds:
            run_command(c)
        return "Correções de impressora aplicadas."
    return "Não suportado."

def action_sfc():
    if not confirm_admin_and_proceed("SFC /scannow"):
        return "Cancelado"
    if SYSTEM == "Windows":
        rc, out = run_command(["sfc", "/scannow"])
        return out
    return "SFC é exclusivo do Windows."

def action_dism():
    if not confirm_admin_and_proceed("DISM /RestoreHealth"):
        return "Cancelado"
    if SYSTEM == "Windows":
        rc, out = run_command(["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"])
        return out
    return "DISM é exclusivo do Windows."

def action_chkdsk():
    if not confirm_admin_and_proceed("CHKDSK"):
        return "Cancelado"
    if SYSTEM == "Windows":
        rc, out = run_command(["chkdsk", "/scan"])
        return out
    return "CHKDSK é exclusivo do Windows."

def action_reset_network():
    if not confirm_admin_and_proceed("Reset de rede (winsock/ip)"):
        return "Cancelado"
    if SYSTEM == "Windows":
        seq = [
            ["netsh", "winsock", "reset"],
            ["netsh", "int", "ip", "reset"],
            ["ipconfig", "/release"],
            ["ipconfig", "/renew"]
        ]
        out_total = []
        for c in seq:
            rc, o = run_command(c)
            out_total.append(o)
        return "\n".join(out_total) or "Reset executado."
    else:
        return "Reset de rede automatizado implementado apenas para Windows."

def action_backup_registry():
    if not confirm_admin_and_proceed("Backup do Registro"):
        return "Cancelado"
    if SYSTEM == "Windows":
        backup_dir = os.path.join("C:\\", f"RegBackup_{datetime.now().strftime('%Y%m%d')}")
        os.makedirs(backup_dir, exist_ok=True)
        rc1, o1 = run_command(["reg", "export", "HKLM", os.path.join(backup_dir, "HKLM.reg"), "/y"])
        rc2, o2 = run_command(["reg", "export", "HKCU", os.path.join(backup_dir, "HKCU.reg"), "/y"])
        rc3, o3 = run_command(["reg", "export", "HKCR", os.path.join(backup_dir, "HKCR.reg"), "/y"])
        return f"Backup salvo em: {backup_dir}"
    return "Backup do registro só no Windows."

def action_process_list():
    if SYSTEM == "Windows":
        rc, out = run_command(["tasklist"])
        return out
    else:
        rc, out = run_command(["ps", "aux"])
        return out

def action_processes_network():
    if SYSTEM == "Windows":
        rc, out = run_command(["netstat", "-ano"])
        return out
    else:
        rc, out = run_command(["ss", "-tulpn"])
        return out

def action_terminate_pid(pid_str):
    if not confirm_admin_and_proceed("Finalizar processo"):
        return "Cancelado"
    try:
        pid = int(pid_str)
    except Exception:
        return "PID inválido"
    if SYSTEM == "Windows":
        rc, out = run_command(["taskkill", "/f", "/pid", str(pid)])
        return out
    else:
        rc, out = run_command(["kill", "-9", str(pid)])
        return out

def action_disable_telemetry_and_apps():
    if not confirm_admin_and_proceed("Desativar Telemetria/Apps"):
        return "Cancelado"
    if not messagebox.askyesno("Confirmar", "Isso altera políticas e serviços. Continua?"):
        return "Cancelado"
    if SYSTEM == "Windows":
        cmds = [
            ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR", "/v", "AllowGameDVR", "/t", "REG_DWORD", "/d", "0", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "/v", "AllowTelemetry", "/t", "REG_DWORD", "/d", "0", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\CloudContent", "/v", "DisableWindowsConsumerFeatures", "/t", "REG_DWORD", "/d", "1", "/f"],
            ["sc", "config", "DiagTrack", "start=", "disabled"],
            ["sc", "config", "dmwappushservice", "start=", "disabled"],
        ]
        for c in cmds:
            run_command(c)
        return "Alterações aplicadas. Reinicie para completar."
    return "Não suportado."

def action_audit_security():
    if SYSTEM == "Windows":
        out_tot = []
        rc, out = run_command(["wmic", "qfe", "list", "brief", "/format:list"])
        out_tot.append("Atualizações:\n" + out)
        rc, out = run_command(["netsh", "advfirewall", "show", "allprofiles"])
        out_tot.append("\nFirewall:\n" + out)
        rc, out = run_command(["sc", "query", "WinDefend"])
        out_tot.append("\nWinDefend:\n" + out)
        rc, out = run_command(["powershell", "-Command", "Get-ExecutionPolicy -List"], shell=False)
        out_tot.append("\nExecutionPolicy:\n" + out)
        return "\n".join(out_tot)
    return "Auditoria só no Windows."

def action_performance_report():
    if SYSTEM == "Windows":
        rc, out = run_command(["start", "perfmon", "/report"], shell=True)
        return "Relatório de desempenho iniciado (Perfmon)."
    return "Perfmon é do Windows."

# Limpeza de temporários (COM CORREÇÃO PARA AMBIENTES UNIX/PYTHONIC)
def action_clean_temp():
    try:
        if SYSTEM == "Windows":
            temp = os.getenv("TEMP") or tempfile.gettempdir()
            run_command(["powershell", "-Command", f"Get-ChildItem -Path '{temp}' -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"])
            run_command(["powershell", "-Command", "Get-ChildItem -Path 'C:\\Windows\\Temp' -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue"])
            run_command(["powershell", "-Command", "Remove-Item -Path 'C:\\Windows\\Prefetch\\*' -Force -ErrorAction SilentlyContinue"])
            run_command(["powershell", "-Command", "Remove-Item -Path '$env:SystemRoot\\SoftwareDistribution\\Download\\*' -Recurse -Force -ErrorAction SilentlyContinue"])
            return "Limpeza de temporários finalizada (Windows)."
        
        else:
            # Lógica Unix/Pythonic (mais segura que 'rm -rf' com shell)
            temp = tempfile.gettempdir()
            for item in os.listdir(temp):
                item_path = os.path.join(temp, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path) # Remove arquivos
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path) # Remove diretórios recursivamente
                except Exception as e:
                    log(f"Não foi possível remover {item_path}: {e}", level="WARNING")
            
            return "Limpeza de temporários finalizada (Unix/Pythonic)."
            
    except Exception as e:
        log(f"Erro clean temp: {e}", level="ERROR")
        return f"Erro: {e}"

# Windows Update via PSWindowsUpdate (tentativa)
def action_update_windows():
    if SYSTEM != "Windows":
        return "Não aplicável"
    rc, out = run_command(["powershell", "-Command", "Install-Module PSWindowsUpdate -Force -Confirm:$false; Get-WindowsUpdate -Install -AcceptAll -IgnoreReboot"], shell=False)
    return out or "Windows Update iniciado (PowerShell)."

# Otimização de energia (powercfg)
def action_optimize_power():
    if not confirm_admin_and_proceed("Otimização de energia"):
        return "Cancelado"
    if SYSTEM == "Windows":
        run_command(["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"])
        run_command(["powercfg", "/change", "standby-timeout-ac", "0"])
        run_command(["powercfg", "/change", "standby-timeout-dc", "0"])
        rc, out = run_command(["powercfg", "/getactivescheme"])
        return out
    return "Não aplicável."

# Diagnóstico completo (sequência)
def action_diagnostico_completo():
    out = []
    out.append("Iniciando diagnóstico completo. Isso pode levar tempo.")
    # É importante garantir que estas funções retornem strings para 'out.append'
    out.append(str(action_sfc()))
    out.append(str(action_dism()))
    out.append(str(action_chkdsk()))
    out.append(str(action_clean_temp()))
    out.append(str(action_update_windows()))
    out.append(str(action_reset_network()))
    out.append(str(action_process_list()))
    return "\n\n".join([str(o) for o in out])


# -----------------------------
# GUI - Tkinter
# -----------------------------
class ToolkitGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Canivete Suíço - Toolkit (GUI)")
        self.geometry("1100x700")
        self.is_running = False # Novo estado para controlar a execução
        self.create_widgets()
        log("Aplicação GUI iniciada")

    def create_widgets(self):
        # MENU superior
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exportar log...", command=self.export_log)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self.show_about)
        menubar.add_cascade(label="Ajuda", menu=help_menu)

        self.config(menu=menubar)

        # Frames
        left_frame = ttk.Frame(self, width=340)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Botões / Grupos no left_frame (Chamadas permanecem as mesmas)
        self.add_section(left_frame, "Sistema", [
            ("Reiniciar sistema", lambda: self.run_threaded(self.do_and_print, action_reiniciar)),
            ("Backup registro", lambda: self.run_threaded(self.do_and_print, action_backup_registry)),
            ("Relatório desempenho (Perfmon)", lambda: self.run_threaded(self.do_and_print, action_performance_report)),
            ("Otimização de energia", lambda: self.run_threaded(self.do_and_print, action_optimize_power)),
        ])

        self.add_section(left_frame, "Rede", [
            ("Testar conexão (ping)", self.ping_prompt),
            ("Flush DNS", lambda: self.run_threaded(self.do_and_print, action_flush_dns)),
            ("Reset de rede", lambda: self.run_threaded(self.do_and_print, action_reset_network)),
            ("Coletar info de rede", lambda: self.run_threaded(self.do_and_print, action_coletar_info_rede)),
        ])

        self.add_section(left_frame, "Impressão", [
            ("Painel de impressoras", lambda: self.run_threaded(self.do_and_print, action_impressoras_panel)),
            ("Reiniciar spooler", lambda: self.run_threaded(self.do_and_print, action_reiniciar_spooler)),
            ("Reparos impressora (todos)", lambda: self.run_threaded(self.do_and_print, action_printer_fixes_all)),
        ])

        self.add_section(left_frame, "Diagnóstico", [
            ("SFC /scannow", lambda: self.run_threaded(self.do_and_print, action_sfc)),
            ("DISM Restore", lambda: self.run_threaded(self.do_and_print, action_dism)),
            ("CHKDSK (scan)", lambda: self.run_threaded(self.do_and_print, action_chkdsk)),
            ("Diagnóstico completo", lambda: self.run_threaded(self.do_and_print, action_diagnostico_completo)),
        ])

        self.add_section(left_frame, "Processos e Segurança", [
            ("Listar processos", lambda: self.run_threaded(self.do_and_print, action_process_list)),
            ("Conexões de rede (netstat/ss)", lambda: self.run_threaded(self.do_and_print, action_processes_network)),
            ("Finalizar processo (por PID)", self.terminate_pid_prompt),
            ("Auditoria de segurança", lambda: self.run_threaded(self.do_and_print, action_audit_security)),
            ("Desativar telemetria/apps", lambda: self.run_threaded(self.do_and_print, action_disable_telemetry_and_apps)),
        ])

        self.add_section(left_frame, "Limpeza & Atualização", [
            ("Limpar temporários", lambda: self.run_threaded(self.do_and_print, action_clean_temp)),
            ("Windows Update (PowerShell)", lambda: self.run_threaded(self.do_and_print, action_update_windows)),
        ])

        # Console de saída no right_frame
        top_label = ttk.Label(right_frame, text="Saída / Console")
        top_label.pack(anchor="w")
        self.txt = tk.Text(right_frame, wrap="none", state="disabled") # Começa como disabled
        self.txt.pack(fill="both", expand=True, side=tk.LEFT)
        scroll_y = ttk.Scrollbar(right_frame, orient="vertical", command=self.txt.yview)
        scroll_y.pack(side=tk.LEFT, fill=tk.Y)
        self.txt.configure(yscrollcommand=scroll_y.set)
        
        # Save/clear buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Salvar saída", command=self.save_output).pack(side=tk.LEFT, padx=4, pady=4)
        ttk.Button(btn_frame, text="Limpar saída", command=lambda: self.txt.configure(state="normal") or self.txt.delete("1.0", tk.END) or self.txt.configure(state="disabled")).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Abrir pasta de logs", command=self.open_log_dir).pack(side=tk.RIGHT, padx=4)

    def add_section(self, parent, title, buttons):
        lab = ttk.Label(parent, text=title, font=("Segoe UI", 10, "bold"))
        lab.pack(anchor="w", pady=(8,0))
        fr = ttk.Frame(parent)
        fr.pack(fill="x", pady=(2,6))
        for i, (label, cmd) in enumerate(buttons):
            b = ttk.Button(fr, text=label, command=cmd)
            b.grid(row=i, column=0, sticky="ew", pady=2)
            fr.grid_columnconfigure(0, weight=1)

    def run_threaded(self, target, *args, **kwargs):
        t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
        t.start()
    
    # -----------------------------
    # MÉTODOS DE VISUALIZAÇÃO AVANÇADA
    # -----------------------------

    def _do_search(self, entry, text_area):
        # Função auxiliar de busca para o advanced viewer
        term = entry.get()
        text_area.tag_remove("highlight", "1.0", tk.END)
        if not term:
            return
        
        text_area.configure(state="normal")
        start = "1.0"
        while True:
            pos = text_area.search(term, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(term)}c"
            text_area.tag_add("highlight", pos, end)
            start = end
        text_area.tag_config("highlight", background="yellow", foreground="black")
        text_area.configure(state="disabled")
        
    def open_advanced_viewer(self, text):
        # Implementação do viewer avançado (terminal-like)
        viewer = tk.Toplevel(self)
        viewer.title("Visualização Avançada (Modo Terminal)")
        viewer.geometry("900x700")

        # Campo de busca e botões
        search_frame = ttk.Frame(viewer)
        search_frame.pack(fill="x")
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Button(search_frame, text="Buscar", command=lambda: self._do_search(search_entry, text_area)).pack(side="left", padx=5)

        # Caixa de texto
        text_area = tk.Text(viewer, wrap="none", font=("Consolas", 10))
        text_area.pack(fill="both", expand=True)

        # Scrollbars
        scroll_y = ttk.Scrollbar(viewer, orient="vertical", command=text_area.yview)
        scroll_y.pack(side="right", fill="y")
        text_area.configure(yscrollcommand=scroll_y.set)

        text_area.insert("1.0", text)
        text_area.configure(state="disabled") # Trava edição
        
    def open_table_viewer(self, raw_text):
        # Implementação do visualizador tabular
        win = tk.Toplevel(self)
        win.title("Visualização em Tabela")
        win.geometry("1000x600")

        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Treeview e Scrollbars
        table = ttk.Treeview(frame)
        table.pack(side="left", fill="both", expand=True)
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        scroll_y.pack(side="right", fill="y")
        table.configure(yscrollcommand=scroll_y.set)

        lines = raw_text.strip().split("\n")
        
        if not lines or len(lines) < 2:
            messagebox.showwarning("Aviso", "Saída da tabela incompleta. Exibindo como texto simples.")
            win.destroy()
            self.append_output(raw_text)
            return
            
        # 1. Obter e processar cabeçalhos (separa por múltiplos espaços)
        header_line = lines[0]
        # Usamos regex para splitar em 2 ou mais espaços para melhor precisão, mas mantendo a simplicidade:
        import re
        headers = [h for h in re.split(r'\s{2,}', header_line) if h.strip()]
        
        # 2. Configurar a tabela
        table["columns"] = headers
        table["show"] = "headings"

        for h in headers:
            table.column(h, width=120, anchor='w')
            table.heading(h, text=h.strip())
            
        # 3. Inserir dados
        for line in lines[1:]:
             # Tenta splitar os dados de forma similar ao cabeçalho
            row_data = [d.strip() for d in re.split(r'\s{2,}', line) if d.strip()]
            
            row_data = row_data + [""] * (len(headers) - len(row_data))
            
            table.insert("", "end", values=row_data[:len(headers)])

    # -----------------------------
    # MÉTODO CORE REVISADO (do_and_print)
    # -----------------------------
    
    def do_and_print(self, func):
        try:
            self.is_running = True
            
            self.append_output(f"\n>> Executando {func.__name__ if hasattr(func, '__name__') else func} ...\n")
            res = func() if callable(func) else func
            
            if res is None:
                res = "Concluído."
            
            if not isinstance(res, str):
                res = str(res)
                
            # Se resultado tem mais de 20 mil caracteres → abrir viewer avançado
            if len(res) > 20000:
                self.open_advanced_viewer(res)
                log(f"Resultado de {func.__name__} enviado para viewer avançado.")
                return 

            # Se parecer tabela → abrir viewer tabular
            # Critério: mais de 2 linhas e presença de espaçamento grande (típico de saídas de console tabulares)
            if "\n" in res and res.count('\n') > 2 and "  " in res:
                 # Comandos como tasklist, netstat, ps aux se beneficiam disso
                 self.open_table_viewer(res)
                 log(f"Resultado de {func.__name__} enviado para viewer tabular.")
                 return

            # Caso normal → exibir no console
            self.append_output(res + "\n")
            log(f"Executado: {func.__name__ if hasattr(func, '__name__') else func}")
            
        except Exception as e:
            err = f"Erro ao executar ação: {e}\n{traceback.format_exc()}"
            self.append_output(err)
            log(err, level="ERROR")
            
        finally:
            self.is_running = False

    # -----------------------------
    # MÉTODOS DE UTILIDADE DA GUI
    # -----------------------------

    def append_output(self, text):
        self.txt.configure(state="normal")
        self.txt.insert(tk.END, text)
        self.txt.see(tk.END)
        self.txt.configure(state="disabled")

    def save_output(self):
        # Onde a saída do console principal (se houver) é salva
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if not path:
            return
        with open(path, "w", encoding="utf-8", errors="ignore") as f:
            self.txt.configure(state="normal")
            f.write(self.txt.get("1.0", tk.END))
            self.txt.configure(state="disabled")
        messagebox.showinfo("Salvo", f"Saída salva em:\n{path}")

    def export_log(self):
        path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log files","*.log")])
        if not path:
            return
        try:
            shutil.copyfile(LOG_FILE, path)
            messagebox.showinfo("Exportado", f"Log exportado para:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar log: {e}")

    def open_log_dir(self):
        try:
            if SYSTEM == "Windows":
                os.startfile(LOG_DIR)
            elif SYSTEM == "Darwin":
                subprocess.run(["open", LOG_DIR])
            else:
                subprocess.run(["xdg-open", LOG_DIR])
        except Exception:
            messagebox.showinfo("Logs", f"Pasta de logs:\n{LOG_DIR}")

    def show_about(self):
        messagebox.showinfo("Sobre", "Canivete Suíço - Toolkit GUI\nAdaptado para Python/Tkinter\nUse com responsabilidade.")

    def ping_prompt(self):
        # Prompt simples para ping
        def do():
            ip = ent.get().strip()
            if not ip:
                messagebox.showwarning("Aviso", "Digite IP ou domínio.")
                return
            self.win_ping.destroy()
            self.run_threaded(self.do_and_print, lambda: self.action_ping(ip))
            
        self.win_ping = tk.Toplevel(self)
        self.win_ping.title("Ping")
        self.win_ping.geometry("380x120")
        self.win_ping.resizable(False, False)
        ttk.Label(self.win_ping, text="IP ou domínio:").pack(padx=8, pady=(8,0))
        ent = ttk.Entry(self.win_ping, width=40)
        ent.pack(padx=8, pady=6)
        ent.bind("<Return>", lambda e: do())
        ttk.Button(self.win_ping, text="Executar", command=do).pack(padx=8, pady=6)
        self.win_ping.focus_set()
        ent.focus_set()

    def action_ping(self, ip):
        # Execute ping with correct encoding and return output
        if SYSTEM == "Windows":
            rc, out = run_command(["ping", "-n", "4", ip])
        else:
            rc, out = run_command(["ping", "-c", "4", ip])
        return out

    def terminate_pid_prompt(self):
        def do():
            pid = ent.get().strip()
            self.win_pid.destroy()
            self.run_threaded(self.do_and_print, lambda: action_terminate_pid(pid))
            
        self.win_pid = tk.Toplevel(self)
        self.win_pid.title("Finalizar processo")
        self.win_pid.geometry("250x120")
        self.win_pid.resizable(False, False)
        ttk.Label(self.win_pid, text="Informe PID:").pack(padx=8, pady=(8,0))
        ent = ttk.Entry(self.win_pid, width=20)
        ent.pack(padx=8, pady=6)
        ent.bind("<Return>", lambda e: do())
        ttk.Button(self.win_pid, text="Finalizar", command=do).pack(padx=8, pady=6)
        self.win_pid.focus_set()
        ent.focus_set()

# -----------------------------
# ENTRYPOINT
# -----------------------------
def main():
    app = ToolkitGUI()
    app.mainloop()

if __name__ == "__main__":
    # Importar 're' que é usado na open_table_viewer
    import re
    main()