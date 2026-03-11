# -*- coding: utf-8 -*-
import customtkinter as ctk
from tkinter import messagebox

from menual.manager import CommandManager
from menual.ui.dialogs import CommandDialog


class App(ctk.CTk):
    """메인 애플리케이션"""

    def __init__(self):
        super().__init__()
        self.title("서버 명령어 매뉴얼")
        self.geometry("500x100")
        self.minsize(400, 100)

        # 위젯 스타일 설정
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.95)
        self.overrideredirect(True)

        self.manager = CommandManager()
        self.selected_command = None
        self.dropdown_visible = False
        self.detail_visible = False
        self.dropdown_window = None

        self._drag_x = 0
        self._drag_y = 0

        self._create_widgets()
        self._set_position()

    def _set_position(self):
        """창 위치 설정 (화면 오른쪽 상단)"""
        self.update_idletasks()
        x = self.winfo_screenwidth() - 520
        y = 20
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        self._create_titlebar()
        self._create_search_area()
        self._create_detail_area()

    def _create_titlebar(self):
        """타이틀바 생성"""
        titlebar = ctk.CTkFrame(self, height=32, fg_color="gray20", corner_radius=0)
        titlebar.pack(fill="x")
        titlebar.pack_propagate(False)

        titlebar.bind("<Button-1>", self._start_drag)
        titlebar.bind("<B1-Motion>", self._on_drag)

        title_label = ctk.CTkLabel(titlebar, text="  서버 명령어", font=("", 11),
                                   text_color="gray70")
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", self._start_drag)
        title_label.bind("<B1-Motion>", self._on_drag)

        ctk.CTkButton(titlebar, text="✕", width=32, height=32, corner_radius=0,
                      fg_color="transparent", hover_color="red",
                      command=self.quit).pack(side="right")

        self._is_faded = False
        ctk.CTkButton(titlebar, text="─", width=32, height=32, corner_radius=0,
                      fg_color="transparent", hover_color="gray40",
                      command=self._toggle_fade).pack(side="right")

    def _create_search_area(self):
        """검색 영역 생성"""
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=15)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="명령어 입력...",
                                         font=("Consolas", 14), height=40)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search)
        self.search_entry.bind("<FocusOut>", self._on_focus_out)

        ctk.CTkButton(search_frame, text="+", width=40, height=40, font=("", 18),
                      command=self._add_command).pack(side="right")

    def _create_detail_area(self):
        """상세정보 영역 생성"""
        self.detail_frame = ctk.CTkFrame(self)

        # 헤더
        header_frame = ctk.CTkFrame(self.detail_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        self.detail_name = ctk.CTkLabel(header_frame, text="",
                                        font=("", 15, "bold"), anchor="w")
        self.detail_name.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(header_frame, text="✕", width=30, height=26,
                      fg_color="gray30", hover_color="gray40",
                      command=self._close_detail).pack(side="right", padx=(5, 0))

        self.delete_btn = ctk.CTkButton(header_frame, text="삭제", width=50, height=26,
                                        fg_color="red", hover_color="darkred",
                                        command=self._delete_command)
        self.edit_btn = ctk.CTkButton(header_frame, text="수정", width=50, height=26,
                                      command=self._edit_command)

        # 스크롤 가능한 컨텐츠 영역
        content_scroll = ctk.CTkScrollableFrame(self.detail_frame, fg_color="transparent")
        content_scroll.pack(fill="both", expand=True, padx=5, pady=(0, 10))

        # 명령어 박스
        cmd_frame = ctk.CTkFrame(content_scroll, fg_color="gray20", corner_radius=8)
        cmd_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.detail_command = ctk.CTkLabel(cmd_frame, text="", font=("Consolas", 13),
                                           anchor="w")
        self.detail_command.pack(side="left", fill="x", expand=True, padx=15, pady=10)

        self.copy_btn = ctk.CTkButton(cmd_frame, text="복사", width=50, height=26,
                                      command=self._copy_command)
        self.copy_btn.pack(side="right", padx=10, pady=10)

        # 설명
        ctk.CTkLabel(content_scroll, text="설명", font=("", 11), text_color="gray",
                     anchor="w").pack(fill="x", padx=10)
        self.detail_desc = ctk.CTkLabel(content_scroll, text="", anchor="w", justify="left",
                                        wraplength=400)
        self.detail_desc.pack(fill="x", padx=10, pady=(3, 10))

        # 예시
        ctk.CTkLabel(content_scroll, text="사용 예시", font=("", 11), text_color="gray",
                     anchor="w").pack(fill="x", padx=10)
        self.detail_example = ctk.CTkLabel(content_scroll, text="", font=("Consolas", 11),
                                           anchor="w", justify="left", wraplength=420)
        self.detail_example.pack(fill="x", padx=10, pady=(3, 10))

        self._hide_detail_buttons()

    # === 검색 & 드롭다운 ===

    def _on_search(self, event=None):
        query = self.search_entry.get()
        commands = self.manager.search_commands(query)

        if commands:
            self._show_dropdown(commands)
        else:
            self._hide_dropdown()

    def _show_dropdown(self, commands):
        self._hide_dropdown()

        self.dropdown_window = ctk.CTkToplevel(self)
        self.dropdown_window.overrideredirect(True)
        self.dropdown_window.attributes('-topmost', True)
        self.dropdown_window.configure(fg_color="gray25")

        x = self.winfo_x() + 15
        y = self.winfo_y() + 87
        width = self.winfo_width() - 30

        for cmd in commands[:8]:
            item = ctk.CTkFrame(self.dropdown_window, fg_color="transparent", cursor="hand2")
            item.pack(fill="x", padx=5, pady=2)

            cmd_label = ctk.CTkLabel(item, text=cmd["command"], font=("Consolas", 12),
                                     anchor="w", text_color="#7dd3fc")
            cmd_label.pack(side="left", padx=10, pady=6)

            name_label = ctk.CTkLabel(item, text=f"  {cmd['name']}", font=("", 10),
                                      anchor="w", text_color="gray")
            name_label.pack(side="left", pady=6)

            for widget in [item, cmd_label, name_label]:
                widget.bind("<Enter>", lambda e, f=item: f.configure(fg_color="gray35"))
                widget.bind("<Leave>", lambda e, f=item: f.configure(fg_color="transparent"))
                widget.bind("<Button-1>", lambda e, c=cmd: self._select_command(c))

        self.dropdown_window.update_idletasks()
        height = self.dropdown_window.winfo_reqheight()
        self.dropdown_window.geometry(f"{width}x{height}+{x}+{y}")
        self.dropdown_visible = True

    def _hide_dropdown(self):
        if self.dropdown_window and self.dropdown_window.winfo_exists():
            self.dropdown_window.destroy()
            self.dropdown_window = None
        self.dropdown_visible = False

    def _on_focus_out(self, event):
        self.after(150, self._hide_dropdown)

    # === 상세정보 ===

    def _select_command(self, cmd: dict):
        self._hide_dropdown()
        self.selected_command = cmd
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, cmd["command"])

        self.detail_name.configure(text=cmd["name"])
        self.detail_command.configure(text=cmd["command"])
        self.detail_desc.configure(text=cmd.get("description", "-"))
        self.detail_example.configure(text=cmd.get("example", ""))

        self._show_detail_buttons()
        self._show_detail()

    def _show_detail(self):
        if not self.detail_visible:
            self.detail_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
            self.geometry("500x420")
            self.detail_visible = True

    def _close_detail(self):
        if self.detail_visible:
            self.detail_frame.pack_forget()
            self.geometry("500x100")
            self.detail_visible = False
            self.selected_command = None
            self.search_entry.delete(0, "end")
            self._hide_detail_buttons()

    def _show_detail_buttons(self):
        self.edit_btn.pack(side="right", padx=(5, 0))
        self.delete_btn.pack(side="right", padx=(5, 0))

    def _hide_detail_buttons(self):
        self.edit_btn.pack_forget()
        self.delete_btn.pack_forget()

    # === 명령어 CRUD ===

    def _copy_command(self):
        if self.selected_command:
            self.clipboard_clear()
            self.clipboard_append(self.selected_command["command"])
            self.copy_btn.configure(text="복사됨!")
            self.after(1000, lambda: self.copy_btn.configure(text="복사"))

    def _add_command(self):
        dialog = CommandDialog(self, self.manager)
        self.wait_window(dialog)

    def _edit_command(self):
        if self.selected_command:
            dialog = CommandDialog(self, self.manager, self.selected_command)
            self.wait_window(dialog)
            if dialog.result:
                for cmd in self.manager.data["commands"]:
                    if cmd["id"] == self.selected_command["id"]:
                        self._select_command(cmd)
                        break

    def _delete_command(self):
        if self.selected_command:
            if messagebox.askyesno("삭제", f"'{self.selected_command['name']}' 삭제?"):
                self.manager.delete_command(self.selected_command["id"])
                self._close_detail()

    # === 창 드래그 & 투명도 ===

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag(self, event):
        x = self.winfo_x() + event.x - self._drag_x
        y = self.winfo_y() + event.y - self._drag_y
        self.geometry(f"+{x}+{y}")

    def _toggle_fade(self):
        if self._is_faded:
            self.attributes('-alpha', 0.95)
            self._is_faded = False
        else:
            self.attributes('-alpha', 0.3)
            self._is_faded = True

