# -*- coding: utf-8 -*-
import json
from pathlib import Path
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


COLOR_BLUE      = "2E75B6"
COLOR_GRAY      = "A9A9A9"
COLOR_SEPARATOR = "D9D9D9"  # 원복 프로세스 구분선
COLOR_WHITE     = "FFFFFF"
COLOR_BLACK     = "000000"

# 6개 고정 step 정의
FIXED_STEPS = [
    {"no": 1, "label": "사전작업",                       "fixed": False},
    {"no": 2, "label": "작업개시선언",                   "fixed": True},   # 내용/시간 고정
    {"no": 3, "label": "본작업",                         "fixed": False},
    {"no": 4, "label": "서비스 오픈 선언 및 작업 종료",  "fixed": True},   # 내용/시간 고정
    # ── 원복 프로세스 구분선 (2행) ──
    {"no": 5, "label": "원복작업",                       "fixed": False},
    {"no": 6, "label": "점검 및 보고",                   "fixed": False},
]

TOTAL_COLS = 7  # A~G


def _border():
    s = Side(style="thin")
    return Border(left=s, right=s, top=s, bottom=s)

def _fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def _center():
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def _left():
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

def _title_font(size=10):
    return Font(name="맑은 고딕", bold=True, color=COLOR_WHITE, size=size)

def _header_font():
    return Font(name="맑은 고딕", bold=True, color=COLOR_WHITE, size=8)

def _data_font(bold=False):
    return Font(name="맑은 고딕", size=8, color=COLOR_BLACK, bold=bold)


def _set_cell(ws, row, col, value="", bg=COLOR_WHITE, font=None, align=None):
    c = ws.cell(row=row, column=col, value=value)
    c.fill = _fill(bg)
    c.border = _border()
    c.font = font or _data_font()
    c.alignment = align or _center()
    return c


def _merge_set(ws, r1, c1, r2, c2, value="", bg=COLOR_WHITE, font=None, align=None):
    """병합 후 스타일 적용 (border는 전체 셀에)"""
    if r1 != r2 or c1 != c2:
        ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
    _set_cell(ws, r1, c1, value, bg=bg, font=font, align=align or _center())
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ws.cell(r, c).border = _border()


def _make_timetable_sheet(ws, steps_data: list):
    """
    steps_data: 6개 항목 리스트 (FIXED_STEPS 순서 대응)
      각 항목: {
        "start_time": "09:00",
        "duration": "30분",        # fixed step이면 무시하고 "-" 사용
        "tasks": [                 # fixed step이면 무시
          {"content": "...", "reporter": "...", "worker": "...", "scenario": "..."}
        ]
      }
    항목이 부족하면 빈 값으로 채움
    """
    ws.title = "작업계획서"

    # 열 너비
    col_widths = {"A": 8, "B": 12, "C": 10, "D": 40, "E": 12, "F": 12, "G": 45}
    for col, w in col_widths.items():
        ws.column_dimensions[col].width = w

    # ── 제목 row 1 ──
    _merge_set(ws, 1, 1, 1, TOTAL_COLS, "작업계획서",
               bg=COLOR_BLUE, font=_title_font(10))
    ws.row_dimensions[1].height = 22

    # ── 헤더 row 2~3 ──
    # row2: Step | 시간계획(B~C 병합) | 작업 및 점검내용 | 보고자 | 작업자 | 수행시나리오
    _merge_set(ws, 2, 2, 2, 3, "시간계획", bg=COLOR_GRAY, font=_header_font())
    for col, val in [(1, "Step"), (4, "작업 및 점검내용"), (5, "보고자"), (6, "작업자"), (7, "수행시나리오")]:
        _set_cell(ws, 2, col, val, bg=COLOR_GRAY, font=_header_font())

    # row3: 소헤더 (시작시간 / 작업시간)
    for col, val in [(1, ""), (2, "시작시간"), (3, "작업시간"), (4, ""), (5, ""), (6, ""), (7, "")]:
        _set_cell(ws, 3, col, val, bg=COLOR_GRAY, font=_header_font())

    # row2~3 병합: Step, 작업및점검내용, 보고자, 작업자, 수행시나리오
    for col in (1, 4, 5, 6, 7):
        _merge_set(ws, 2, col, 3, col, ws.cell(2, col).value,
                   bg=COLOR_GRAY, font=_header_font())

    ws.row_dimensions[2].height = 18
    ws.row_dimensions[3].height = 18
    ws.freeze_panes = "A4"

    # ── 데이터 행 ──
    cur_row = 4

    for idx, step_def in enumerate(FIXED_STEPS):
        # 구분선: step 4 다음 (idx==3 이후, idx==4 전)
        if idx == 4:
            ws.row_dimensions[cur_row].height = 18
            _merge_set(ws, cur_row, 1, cur_row, TOTAL_COLS,
                       "원복 프로세스 진행",
                       bg=COLOR_SEPARATOR,
                       font=_data_font(bold=True),
                       align=_center())
            cur_row += 1

        # 이 step의 입력 데이터
        d = steps_data[idx] if idx < len(steps_data) else {}
        start_time = d.get("start_time", "")
        duration   = "-" if step_def["fixed"] else d.get("duration", "")
        tasks      = [] if step_def["fixed"] else d.get("tasks", [])

        # 전체 행 수 = 1(label행) + len(tasks)
        span = 1 + len(tasks)

        # 행 초기화
        for i in range(span):
            r = cur_row + i
            ws.row_dimensions[r].height = 25
            for col in range(1, TOTAL_COLS + 1):
                _set_cell(ws, r, col)

        # step no / 시작시간 / 작업시간 → 세로 병합
        _merge_set(ws, cur_row, 1, cur_row + span - 1, 1,
                   step_def["no"], align=_center())
        _merge_set(ws, cur_row, 2, cur_row + span - 1, 2,
                   start_time, align=_center())
        _merge_set(ws, cur_row, 3, cur_row + span - 1, 3,
                   duration, align=_center())

        # label 행
        _set_cell(ws, cur_row, 4, step_def["label"],
                  font=_data_font(bold=True), align=_left())

        # task 행들
        for t_idx, task in enumerate(tasks):
            r = cur_row + 1 + t_idx
            _set_cell(ws, r, 4, task.get("content", ""),   align=_left())
            _set_cell(ws, r, 5, task.get("reporter", ""),  align=_center())
            _set_cell(ws, r, 6, task.get("worker", ""),    align=_center())
            _set_cell(ws, r, 7, task.get("scenario", ""),  align=_left())

        cur_row += span


def _make_workbook(task_name: str, steps_data: list) -> Workbook:
    wb = Workbook()
    wb.remove(wb.active)
    ws = wb.create_sheet("작업계획서")
    _make_timetable_sheet(ws, steps_data)
    return wb


def register(mcp):

    @mcp.tool()
    def create_work_plan_excel(
        task_name: str,
        steps: str = "[]",
        save_dir: str = ""
    ) -> str:
        """엑셀 작업계획서 생성 (6개 고정 step 구조)

        Args:
            task_name: 작업 이름
            steps: 6개 step 데이터 JSON 배열 (순서: 사전작업/작업개시선언/본작업/서비스오픈선언/원복작업/점검및보고)
                각 항목: {"start_time": "09:00", "duration": "30분", "tasks": [{"content": "...", "reporter": "...", "worker": "...", "scenario": "..."}]}
                작업개시선언(2번), 서비스오픈선언(4번)은 start_time만 사용하고 duration/tasks는 무시됨
            save_dir: 저장 폴더 경로 (비우면 바탕화면)
        """
        try:
            steps_data = json.loads(steps)
        except json.JSONDecodeError as e:
            return f"JSON 파싱 오류: {e}"

        out_dir = Path(save_dir) if save_dir else Path.home() / "Desktop"
        out_dir.mkdir(parents=True, exist_ok=True)

        date_str  = datetime.now().strftime("%Y%m%d")
        safe_name = task_name.replace(" ", "_").replace("/", "-")
        out_path  = out_dir / f"작업계획서_{safe_name}_{date_str}.xlsx"

        _make_workbook(task_name, steps_data).save(out_path)
        return f"저장 완료: {out_path}"
