# -*- coding: utf-8 -*-
import customtkinter as ctk
from tkinter import messagebox


class CommandDialog(ctk.CTkToplevel):
    """명령어 추가/수정 다이얼로그"""

    def __init__(self, parent, manager, command: dict = None):
        super().__init__(parent)
        self.manager = manager
        self.command = command
        self.result = None

        self.title("명령어 추가" if command is None else "명령어 수정")
        self.geometry("500x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 500) // 2
        self.geometry(f"500x500+{x}+{y}")

    def _create_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 이름
        ctk.CTkLabel(frame, text="이름:", anchor="w").pack(fill="x", pady=(0, 5))
        self.name_entry = ctk.CTkEntry(frame)
        self.name_entry.pack(fill="x", pady=(0, 15))

        # 명령어
        ctk.CTkLabel(frame, text="명령어:", anchor="w").pack(fill="x", pady=(0, 5))
        self.command_entry = ctk.CTkEntry(frame, font=("Consolas", 13))
        self.command_entry.pack(fill="x", pady=(0, 15))

        # 설명
        ctk.CTkLabel(frame, text="설명:", anchor="w").pack(fill="x", pady=(0, 5))
        self.desc_text = ctk.CTkTextbox(frame, height=80)
        self.desc_text.pack(fill="x", pady=(0, 15))

        # 사용 예시
        ctk.CTkLabel(frame, text="사용 예시:", anchor="w").pack(fill="x", pady=(0, 5))
        self.example_text = ctk.CTkTextbox(frame, height=100, font=("Consolas", 12))
        self.example_text.pack(fill="x", pady=(0, 20))

        # 기존 데이터 채우기
        if self.command:
            self.name_entry.insert(0, self.command["name"])
            self.command_entry.insert(0, self.command["command"])
            self.desc_text.insert("1.0", self.command.get("description", ""))
            self.example_text.insert("1.0", self.command.get("example", ""))

        # 버튼
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x")

        ctk.CTkButton(btn_frame, text="취소", width=100, fg_color="gray",
                      command=self.destroy).pack(side="right", padx=(10, 0))
        ctk.CTkButton(btn_frame, text="저장", width=100,
                      command=self._save).pack(side="right")

    def _save(self):
        name = self.name_entry.get().strip()
        command = self.command_entry.get().strip()
        description = self.desc_text.get("1.0", "end-1c").strip()
        example = self.example_text.get("1.0", "end-1c").strip()

        if not name or not command:
            messagebox.showwarning("입력 오류", "이름과 명령어는 필수입니다.")
            return

        if self.command:
            self.manager.update_command(self.command["id"], name, command, description, example)
        else:
            self.manager.add_command(name, command, description, example)

        self.result = True
        self.destroy()

