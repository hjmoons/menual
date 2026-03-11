# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 개발 워크플로우

- **주요 기능 개발**: Claude Code에서 진행
- **품질 점검 및 코드 개선**: Codex에서 수행

## 프로젝트 개요

서버 운영 명령어를 정리하고 조회하는 윈도우 위젯 애플리케이션.
Python + CustomTkinter 기반. MCP 서버로 Claude에서 직접 명령어 관리 가능.

## 실행 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# UI 실행
python -m menual

# MCP 서버 실행
python -m menual.mcp
```

## 빌드 (exe)

```bash
# PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed --name menual menual/__main__.py
```

## 프로젝트 구조

```text
menual/
├── menual/
│   ├── __init__.py
│   ├── __main__.py          # UI 진입점 (python -m menual)
│   ├── manager.py           # CommandManager - UI/MCP 공통 데이터 레이어
│   ├── ui/
│   │   ├── app.py           # App (메인 윈도우)
│   │   └── dialogs.py       # CommandDialog (추가/수정 모달)
│   └── mcp/
│       ├── __init__.py      # MCP 진입점 (python -m menual.mcp)
│       └── server.py        # MCP 서버 (tools: list/search/add/update/delete)
├── data/
│   └── commands.json
├── pyproject.toml
└── requirements.txt
```

## 주요 클래스 및 MCP tools

- `CommandManager` (menual/manager.py): JSON 읽기/쓰기, 검색, CRUD. UI와 MCP가 공유.
- `App` (menual/ui/app.py): 메인 윈도우
- `CommandDialog` (menual/ui/dialogs.py): 명령어 추가/수정 모달

MCP tools: `list_commands` / `search_commands` / `add_command` / `update_command` / `delete_command`

## Claude Code에 MCP 등록

```bash
claude mcp add --transport stdio menual -- python -m menual.mcp
```

## 데이터 구조 (data/commands.json)

```json
{
  "commands": [
    {
      "id": 1,
      "name": "명령어 이름",
      "command": "실제 명령어",
      "description": "설명",
      "example": "사용 예시"
    }
  ]
}
```
