# AGENTS.md

## 역할 분담

메인 기능 개발은 Claude Code로 진행하고, Codex에서는 품질 점검 및 코드 개선을 수행한다.

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 개발 워크플로우

- **주요 기능 개발**: Claude Code에서 진행
- **품질 점검 및 코드 개선**: Codex에서 수행

## 프로젝트 개요

서버 운영 명령어를 정리하고 조회하는 윈도우 위젯 애플리케이션.
Python + CustomTkinter 기반. MCP 서버로 Codex에서 직접 명령어 관리 가능.

## 실행 명령어

```bash
# 의존성 설치
pip install -e .

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
│       ├── __init__.py      # MCP main() 함수
│       ├── __main__.py      # python -m menual.mcp 진입점
│       ├── server.py        # FastMCP 인스턴스 + tools 등록
│       ├── commands.py      # 명령어 CRUD tools
│       ├── planner.py       # 작업계획서 tools
│       └── excel.py         # 엑셀 작업계획서 생성 tool
├── pyproject.toml
└── requirements.txt
```

## 주요 클래스 및 MCP tools

- `CommandManager` (menual/manager.py): JSON 읽기/쓰기, 검색, CRUD. UI와 MCP가 공유.
- `App` (menual/ui/app.py): 메인 윈도우
- `CommandDialog` (menual/ui/dialogs.py): 명령어 추가/수정 모달

### 명령어 관리 tools (commands.py)

`list_commands` / `search_commands` / `add_command` / `update_command` / `delete_command`

### 엑셀 작업계획서 tool (excel.py)

`create_work_plan_excel` - 4개 시트 엑셀 파일 생성

- **작업계획서**: 6개 고정 step (사전작업/작업개시선언/본작업/서비스오픈선언/원복작업/점검및보고), step별 세부task 세로병합
- **사전작업/본작업/원복작업**: 작업내용 그룹 단위로 연번/작업내용/대상/대상장비 세로병합

## Codex에 MCP 등록

```bash
Codex mcp add --transport stdio menual -- python -m menual.mcp
```

## 데이터 저장 경로

명령어 데이터: `%APPDATA%\menual\commands.json` (UI/MCP 공유)

## 데이터 구조 (commands.json)

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
