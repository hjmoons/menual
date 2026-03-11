# -*- coding: utf-8 -*-
from menual.manager import CommandManager

manager = CommandManager()


def register(mcp):
    """작업계획서 관련 tools 등록"""

    @mcp.tool()
    def create_work_plan(task: str) -> str:
        """작업 내용을 바탕으로 명령어 목록을 포함한 작업계획서 생성

        Args:
            task: 작업 내용 설명 (예: "nginx 서버 점검 및 재시작")
        """
        commands = manager.data["commands"]

        # 작업과 관련된 명령어 수집
        related = [
            cmd for cmd in commands
            if any(keyword in task for keyword in cmd["name"].split())
            or any(keyword in cmd["description"] for keyword in task.split())
        ]

        lines = [f"# 작업계획서: {task}", ""]

        if related:
            lines.append("## 관련 명령어")
            for cmd in related:
                lines.append(f"\n### {cmd['name']}")
                lines.append(f"```\n{cmd['command']}\n```")
                if cmd.get("description"):
                    lines.append(f"> {cmd['description']}")
                if cmd.get("example"):
                    lines.append(f"\n**예시:**\n```\n{cmd['example']}\n```")
        else:
            lines.append("_관련 명령어가 없습니다. 명령어를 먼저 등록해주세요._")

        return "\n".join(lines)

