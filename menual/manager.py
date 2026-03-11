# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path


def _get_data_file() -> Path:
    # exe/MCP/개발 환경 모두 같은 경로 사용 (AppData)
    base = Path.home() / "AppData" / "Roaming" / "menual"
    base.mkdir(parents=True, exist_ok=True)
    return base / "commands.json"


DATA_FILE = _get_data_file()


class CommandManager:
    """명령어 데이터 관리"""

    def __init__(self):
        self.data = self.load_data()

    def _normalize_data(self, data) -> dict:
        if not isinstance(data, dict):
            return {"commands": []}

        commands = data.get("commands")
        if not isinstance(commands, list):
            return {"commands": []}

        normalized = []
        for item in commands:
            if not isinstance(item, dict):
                continue

            name = str(item.get("name", "")).strip()
            command = str(item.get("command", "")).strip()
            if not name or not command:
                continue

            try:
                cmd_id = int(item.get("id", 0))
            except (TypeError, ValueError):
                continue

            normalized.append({
                "id": cmd_id,
                "name": name,
                "command": command,
                "description": str(item.get("description", "")),
                "example": str(item.get("example", ""))
            })

        return {"commands": normalized}

    def load_data(self) -> dict:
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return self._normalize_data(data)
            except (json.JSONDecodeError, OSError):
                return {"commands": []}
        return {"commands": []}

    def save_data(self):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp_file = DATA_FILE.with_suffix(".tmp")
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_file, DATA_FILE)

    def search_commands(self, query: str) -> list:
        if not query:
            return []
        query = query.lower()
        return [c for c in self.data["commands"] if c["command"].lower().startswith(query)]

    def add_command(self, name: str, command: str, description: str, example: str) -> dict:
        max_id = max([c["id"] for c in self.data["commands"]], default=0)
        new_cmd = {
            "id": max_id + 1,
            "name": name,
            "command": command,
            "description": description,
            "example": example
        }
        self.data["commands"].append(new_cmd)
        self.save_data()
        return new_cmd

    def update_command(self, cmd_id: int, name: str, command: str, description: str, example: str):
        for cmd in self.data["commands"]:
            if cmd["id"] == cmd_id:
                cmd["name"] = name
                cmd["command"] = command
                cmd["description"] = description
                cmd["example"] = example
                self.save_data()
                return True
        return False

    def delete_command(self, cmd_id: int):
        self.data["commands"] = [c for c in self.data["commands"] if c["id"] != cmd_id]
        self.save_data()
