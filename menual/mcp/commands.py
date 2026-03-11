# -*- coding: utf-8 -*-
from menual.manager import CommandManager

manager = CommandManager()


def register(mcp):
    """명령어 CRUD tools 등록"""

    @mcp.tool()
    def list_commands() -> list[dict]:
        """저장된 모든 명령어 목록 반환"""
        return manager.data["commands"]

    @mcp.tool()
    def search_commands(query: str) -> list[dict]:
        """명령어로 시작하는 항목 검색

        Args:
            query: 검색할 명령어 (예: "df", "docker")
        """
        return manager.search_commands(query)

    @mcp.tool()
    def add_command(name: str, command: str, description: str = "", example: str = "") -> dict:
        """새 명령어 추가

        Args:
            name: 명령어 이름 (예: "디스크 사용량 확인")
            command: 실제 명령어 (예: "df -h")
            description: 설명
            example: 사용 예시
        """
        return manager.add_command(name, command, description, example)

    @mcp.tool()
    def update_command(cmd_id: int, name: str, command: str, description: str = "", example: str = "") -> bool:
        """기존 명령어 수정

        Args:
            cmd_id: 수정할 명령어 ID
            name: 새 이름
            command: 새 명령어
            description: 새 설명
            example: 새 사용 예시
        """
        return manager.update_command(cmd_id, name, command, description, example)

    @mcp.tool()
    def delete_command(cmd_id: int) -> str:
        """명령어 삭제

        Args:
            cmd_id: 삭제할 명령어 ID
        """
        manager.delete_command(cmd_id)
        return f"명령어 ID {cmd_id} 삭제 완료"

