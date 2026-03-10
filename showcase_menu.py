#!/usr/bin/env python3
import os
import sys
import time
import random
import importlib.util
from pathlib import Path
from datetime import datetime

# ---------------------------
# ANSI helpers
# ---------------------------
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

USE_COLOR = sys.stdout.isatty()
SESSION_TRACE = []
SESSION_ID = f"demo-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

BASE_DIR = Path.cwd()
DOWNLOADS_DIR = BASE_DIR / "Downloads"
RESULT_HTML = BASE_DIR / "resultados.html"
RESULT_JSON = BASE_DIR / "resultados.json"

RUNTIME_STATE = {
    "module_registry_loaded": False,
    "downloads_dir_exists": False,
    "result_html_exists": False,
    "result_json_exists": False,
    "deps": {},
}

# ---------------------------
# UI helpers
# ---------------------------
def c(text, color):
    return f"{color}{text}{RESET}" if USE_COLOR else text

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.008):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def line(width=108, char="─", color=BRIGHT_BLACK):
    print(c(char * width, color))

def box_title(title, width=108):
    text = f" {title} "
    inner = width - len(text) - 2
    left = inner // 2
    right = inner - left
    print(c("┌" + "─" * left + text + "─" * right + "┐", BRIGHT_CYAN))

def box_end(width=108):
    print(c("└" + "─" * (width - 2) + "┘", BRIGHT_CYAN))

def box_row(text="", color=WHITE, width=108):
    clean = text[: width - 4]
    print(c("│ ", BRIGHT_CYAN) + c(clean.ljust(width - 4), color) + c(" │", BRIGHT_CYAN))

def add_trace(entry):
    timestamp = datetime.now().strftime("%H:%M:%S")
    SESSION_TRACE.append(f"{timestamp}::{entry}")
    if len(SESSION_TRACE) > 6:
        del SESSION_TRACE[0]

# ---------------------------
# Static data
# ---------------------------
BANNER = r"""
███▄    █  ██▓ ███▄    █  ▄▄▄██▀▀▀▄▄▄      ▓█████▄  ▒█████   ██▀███   ██ ▄█▀  ██████
██ ▀█   █ ▓██▒ ██ ▀█   █    ▒██  ▒████▄    ▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒ ▒██    ▒
▓██  ▀█ ██▒▒██▒▓██  ▀█ ██▒   ░██  ▒██  ▀█▄  ░██   █▌▒██░  ██▒▓██ ░▄█ ▒▓███▄░ ░ ▓██▄
▓██▒  ▐▌██▒░██░▓██▒  ▐▌██▒▓██▄██▓ ░██▄▄▄▄██ ░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▓██ █▄   ▒   ██▒
▒██░   ▓██░░██░▒██░   ▓██░ ▓███▒   ▓█   ▓██▒░▒████▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄▒██████▒▒
░ ▒░   ▒ ▒ ░▓  ░ ▒░   ▒ ▒  ▒▓▒▒░   ▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒▒ ▒▓▒ ▒ ░
░ ░░   ░ ▒░ ▒ ░░ ░░   ░ ▒░ ▒ ░▒░    ▒   ▒▒ ░ ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒ ▒░░ ░▒  ░ ░
   ░   ░ ░  ▒ ░   ░   ░ ░  ░ ░ ░    ░   ▒    ░ ░  ░ ░ ░ ░ ▒    ░░   ░ ░ ░░ ░ ░  ░  ░
         ░  ░           ░  ░   ░        ░  ░   ░        ░ ░     ░     ░  ░         ░
                                              ░
"""

MODULES = [
    ("M01", "Dork Query Builder",   "operator chains / presets / filters / filetypes"),
    ("M02", "Search Engine Runner", "google / duckduckgo / selenium automation"),
    ("M03", "Artifact Harvester",   "pdf / docx / txt download workflow"),
    ("M04", "Smart Parser",         "regex extraction / metadata / structured review"),
    ("M05", "Report Generator",     "json / html / evidence packaging"),
    ("M06", "DevOps Hooks",         "logging / reproducibility / dependency checks"),
]

TACTICAL_LINES = [
    "public data discovery",
    "search automation",
    "artifact triage",
    "metadata review",
    "structured outputs",
    "reproducible workflow",
]

# ---------------------------
# Real checks
# ---------------------------
def dependency_status():
    deps = {
        "json": importlib.util.find_spec("json") is not None,
        "re": importlib.util.find_spec("re") is not None,
        "pathlib": importlib.util.find_spec("pathlib") is not None,
        "selenium": importlib.util.find_spec("selenium") is not None,
    }
    RUNTIME_STATE["deps"] = deps
    return deps

def path_status():
    RUNTIME_STATE["downloads_dir_exists"] = DOWNLOADS_DIR.exists() and DOWNLOADS_DIR.is_dir()
    RUNTIME_STATE["result_html_exists"] = RESULT_HTML.exists()
    RUNTIME_STATE["result_json_exists"] = RESULT_JSON.exists()
    return {
        "downloads": RUNTIME_STATE["downloads_dir_exists"],
        "html": RUNTIME_STATE["result_html_exists"],
        "json": RUNTIME_STATE["result_json_exists"],
    }

def prepare_registry():
    RUNTIME_STATE["module_registry_loaded"] = True
    return len(MODULES)

# ---------------------------
# Boot / dashboard
# ---------------------------
def progress(label, total=24, width=34):
    for i in range(total + 1):
        filled = int(width * i / total)
        bar = "█" * filled + "░" * (width - filled)
        pct = int(100 * i / total)
        print(
            "\r"
            + c("[", BRIGHT_BLACK)
            + c("*", BRIGHT_RED)
            + c("] ", BRIGHT_BLACK)
            + c(label.ljust(34), BRIGHT_WHITE)
            + c("[", BRIGHT_BLACK)
            + c(bar, BRIGHT_RED if pct < 100 else BRIGHT_GREEN)
            + c("]", BRIGHT_BLACK)
            + " "
            + c(f"{pct:>3}%", BRIGHT_WHITE),
            end="",
            flush=True,
        )
        time.sleep(0.02 + random.uniform(0.0, 0.01))
    print()

def boot_runtime():
    clear()
    print(c(BANNER, BRIGHT_RED))
    slow_print(c("[boot] launching NINJADORKS runtime environment...", BRIGHT_WHITE), 0.01)

    steps = [
        "initializing runtime context",
        "validating local dependencies",
        "inspecting local workspace",
        "preparing module registry",
    ]

    for step in steps:
        progress(step)

        if step == "initializing runtime context":
            add_trace("boot::runtime-context-ready")

        elif step == "validating local dependencies":
            deps = dependency_status()
            ok = [name for name, state in deps.items() if state]
            missing = [name for name, state in deps.items() if not state]
            add_trace(f"boot::deps-ok={','.join(ok)}")
            if missing:
                add_trace(f"boot::deps-missing={','.join(missing)}")

        elif step == "inspecting local workspace":
            paths = path_status()
            add_trace(
                "boot::workspace="
                f"Downloads:{'available' if paths['downloads'] else 'on-demand'},"
                f"HTML:{'available' if paths['html'] else 'not-generated'},"
                f"JSON:{'available' if paths['json'] else 'not-generated'}"
            )

        elif step == "preparing module registry":
            count = prepare_registry()
            add_trace(f"boot::modules-loaded={count}")

        time.sleep(0.08)

def draw_trace_box():
    box_title("SESSION TRACE")
    if not SESSION_TRACE:
        box_row("no commands executed yet", BRIGHT_BLACK if USE_COLOR else WHITE)
    else:
        for item in SESSION_TRACE:
            box_row(item, BRIGHT_WHITE)
    box_end()

def draw_runtime_checks():
    box_title("RUNTIME CHECKS")

    deps = RUNTIME_STATE["deps"]
    core_ok = deps.get("json", False) and deps.get("re", False) and deps.get("pathlib", False)
    selenium_ok = deps.get("selenium", False)

    downloads_state = "AVAILABLE" if RUNTIME_STATE["downloads_dir_exists"] else "ON-DEMAND"
    html_state = "AVAILABLE" if RUNTIME_STATE["result_html_exists"] else "NOT GENERATED"
    json_state = "AVAILABLE" if RUNTIME_STATE["result_json_exists"] else "NOT GENERATED"

    box_row(
        f"core_deps       : {'OK' if core_ok else 'MISSING'} (json / re / pathlib)",
        BRIGHT_GREEN if core_ok else BRIGHT_YELLOW
    )
    box_row(
        f"selenium        : {'AVAILABLE' if selenium_ok else 'OPTIONAL / NOT INSTALLED'}",
        BRIGHT_GREEN if selenium_ok else BRIGHT_YELLOW
    )
    box_row(
        f"downloads_dir   : {downloads_state}",
        BRIGHT_GREEN if RUNTIME_STATE["downloads_dir_exists"] else BRIGHT_YELLOW
    )
    box_row(
        f"resultados.html : {html_state}",
        BRIGHT_GREEN if RUNTIME_STATE["result_html_exists"] else BRIGHT_YELLOW
    )
    box_row(
        f"resultados.json : {json_state}",
        BRIGHT_GREEN if RUNTIME_STATE["result_json_exists"] else BRIGHT_YELLOW
    )
    box_row(
        f"module_registry : {'READY' if RUNTIME_STATE['module_registry_loaded'] else 'NOT READY'}",
        BRIGHT_GREEN if RUNTIME_STATE["module_registry_loaded"] else BRIGHT_YELLOW
    )
    box_end()

def draw_dashboard():
    clear()
    print(c(BANNER, BRIGHT_RED))

    box_title("NINJADORKS :: OSINT / SEARCH AUTOMATION / PARSING TOOLKIT")
    box_row(f"session_id      : {SESSION_ID}", BRIGHT_WHITE)
    box_row("operator        : Antoni Llop", BRIGHT_WHITE)
    box_row("track           : cybersecurity / devops beginner", BRIGHT_WHITE)
    box_row("project_scope   : educational tooling for public-data discovery workflows", BRIGHT_WHITE)
    box_row("runtime_profile : interactive terminal interface", BRIGHT_WHITE)
    status_text = c("OPERATIONAL", BRIGHT_GREEN) if USE_COLOR else "OPERATIONAL"
    box_row(f"status          : {status_text}", BRIGHT_WHITE)
    box_end()

    print()
    draw_trace_box()

    print()
    draw_runtime_checks()

    print()
    box_title("MODULE MAP")
    for mid, name, desc in MODULES:
        left = c(f"[{mid}]", BRIGHT_RED) if USE_COLOR else f"[{mid}]"
        text = f"{left}  {name:<22} -> {desc}"
        box_row(text, BRIGHT_WHITE)
    box_end()

    print()
    box_title("ACTIVE FLAGS / OUTPUT")
    box_row("--smart-search   --download pdf   --selenium   --generate-dork", BRIGHT_WHITE)
    box_row("outputs: resultados.html / resultados.json / Downloads/", BRIGHT_WHITE)
    box_row("signals: logs / extracted links / downloadable artifacts / parsed metadata", BRIGHT_WHITE)
    box_end()

    print()
    box_title("CURRENT MENU")
    box_row("(1) Run smart-search demo", BRIGHT_WHITE)
    box_row("(2) Inspect module map with examples", BRIGHT_WHITE)
    box_row("(3) Generate operational summary", BRIGHT_WHITE)
    box_row("(4) Exit", BRIGHT_WHITE)
    box_row("", WHITE)
    box_row("aliases: M01 M02 M03 M04 M05 M06", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_end()

# ---------------------------
# Views
# ---------------------------
def run_demo():
    add_trace("menu::smart-search-demo")
    print()
    box_title("SMART-SEARCH DEMO")
    commands = [
        "$ python ninjadorks.py --smart-search -q 'site:example.com filetype:pdf'",
        "$ python ninjadorks.py --download pdf --selenium",
        "$ python ninjadorks.py --parse resultados.html --export json",
    ]
    for cmd in commands:
        box_row(cmd, BRIGHT_WHITE)
        time.sleep(0.4)

    box_row(c("[ok] query preset generated", BRIGHT_GREEN), BRIGHT_WHITE)
    box_row(c("[ok] search pipeline initialized", BRIGHT_GREEN), BRIGHT_WHITE)
    box_row(c("[ok] public artifacts queued for review", BRIGHT_GREEN), BRIGHT_WHITE)
    box_row(c("[ok] structured output written to resultados.json", BRIGHT_GREEN), BRIGHT_WHITE)
    box_end()

def inspect_modules():
    add_trace("menu::module-map-with-examples")
    print()
    box_title("MODULE DETAILS + USAGE EXAMPLES")

    module_blocks = [
        ("[M01] Dork Query Builder", [
            "capabilities -> operator chains / presets / filters / filetypes",
            "example      -> python ninjadorks.py --generate-dork 'intitle:index of pdf passwords'",
            "example      -> python ninjadorks.py --smart-search -q 'site:gov filetype:pdf report'",
        ]),
        ("[M02] Search Engine Runner", [
            "capabilities -> google / duckduckgo / selenium automation",
            "example      -> python ninjadorks.py --engine google -q 'site:example.com login'",
            "example      -> python ninjadorks.py --engine duckduckgo --selenium -q 'filetype:docx invoice'",
        ]),
        ("[M03] Artifact Harvester", [
            "capabilities -> pdf / docx / txt download workflow",
            "example      -> python ninjadorks.py --download pdf --limit 10",
            "example      -> python ninjadorks.py --download docx --output Downloads/",
        ]),
        ("[M04] Smart Parser", [
            "capabilities -> regex extraction / metadata / structured review",
            "example      -> python ninjadorks.py --parse resultados.html",
            "example      -> python ninjadorks.py --parse Downloads/ --extract emails,urls,metadata",
        ]),
        ("[M05] Report Generator", [
            "capabilities -> json / html / evidence packaging",
            "example      -> python ninjadorks.py --export json",
            "example      -> python ninjadorks.py --export html --report-name findings_report",
        ]),
        ("[M06] DevOps Hooks", [
            "capabilities -> logging / reproducibility / dependency checks",
            "example      -> python ninjadorks.py --check-deps --verbose",
            "example      -> python ninjadorks.py --log-file run.log --save-config config.json",
        ]),
    ]

    for title, lines in module_blocks:
        box_row(title, BRIGHT_WHITE)
        for item in lines:
            box_row(f"   {item}", BRIGHT_BLACK if USE_COLOR else WHITE)
        box_row("", WHITE)

    box_end()

def module_view(module_id):
    titles = {
        "M01": "DORK QUERY BUILDER",
        "M02": "SEARCH ENGINE RUNNER",
        "M03": "ARTIFACT HARVESTER",
        "M04": "SMART PARSER",
        "M05": "REPORT GENERATOR",
        "M06": "DEVOPS HOOKS",
    }

    data = {
        "M01": [
            "capabilities -> operator chains / presets / filters / filetypes",
            "usage        -> python ninjadorks.py --generate-dork 'intitle:index of pdf passwords'",
            "usage        -> python ninjadorks.py --smart-search -q 'site:gov filetype:pdf report'",
            "output       -> normalized search query presets",
        ],
        "M02": [
            "capabilities -> google / duckduckgo / selenium automation",
            "usage        -> python ninjadorks.py --engine google -q 'site:example.com login'",
            "usage        -> python ninjadorks.py --engine duckduckgo --selenium -q 'filetype:docx invoice'",
            "output       -> collected search result pages",
        ],
        "M03": [
            "capabilities -> pdf / docx / txt download workflow",
            "usage        -> python ninjadorks.py --download pdf --limit 10",
            "usage        -> python ninjadorks.py --download docx --output Downloads/",
            "output       -> downloaded artifacts under target directory",
        ],
        "M04": [
            "capabilities -> regex extraction / metadata / structured review",
            "usage        -> python ninjadorks.py --parse resultados.html",
            "usage        -> python ninjadorks.py --parse Downloads/ --extract emails,urls,metadata",
            "output       -> extracted indicators and metadata",
        ],
        "M05": [
            "capabilities -> json / html / evidence packaging",
            "usage        -> python ninjadorks.py --export json",
            "usage        -> python ninjadorks.py --export html --report-name findings_report",
            "output       -> structured report artifacts",
        ],
        "M06": [
            "capabilities -> logging / reproducibility / dependency checks",
            "usage        -> python ninjadorks.py --check-deps --verbose",
            "usage        -> python ninjadorks.py --log-file run.log --save-config config.json",
            "output       -> logs / runtime state / reusable config",
        ],
    }

    add_trace(f"module::{module_id}")
    print()
    box_title(f"MODULE VIEW :: {titles[module_id]}")
    box_row(f"module_id     : {module_id}", BRIGHT_WHITE)
    for item in data[module_id]:
        box_row(item, BRIGHT_BLACK if USE_COLOR else WHITE)
    box_end()

def summary_panel():
    add_trace("menu::operational-summary")
    print()
    box_title("OPERATIONAL SUMMARY")
    box_row("focus areas   : " + " / ".join(TACTICAL_LINES), BRIGHT_WHITE)
    box_row("architecture  : modular pipeline with search / collection / parsing / reporting", BRIGHT_WHITE)
    box_row("runtime       : terminal-oriented workflow with reproducible outputs", BRIGHT_WHITE)
    box_row("execution     : local workspace + optional downloads + exportable reports", BRIGHT_WHITE)
    box_row("", WHITE)
    box_row("example flow  :", BRIGHT_WHITE)
    box_row("   1) generate or refine query presets", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   2) execute search and collect result pages", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   3) download public artifacts for local inspection", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   4) parse extracted content and export structured reports", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("", WHITE)
    box_row("example usage :", BRIGHT_WHITE)
    box_row("   python ninjadorks.py --smart-search -q 'site:example.com filetype:pdf'", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   python ninjadorks.py --download pdf --selenium", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   python ninjadorks.py --parse resultados.html --export json", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_end()

# ---------------------------
# Modes
# ---------------------------
def capture_mode():
    boot_runtime()
    add_trace("boot::capture-mode")
    draw_dashboard()
    print()
    run_demo()
    print()
    summary_panel()
    print()
    line()
    print(c("[tip] take the screenshot now — this frame is the cleanest one.", BRIGHT_YELLOW))
    print(c("[tip] runtime checks are based on local dependency and workspace inspection.", BRIGHT_YELLOW))
    line()

def interactive_mode():
    boot_runtime()
    add_trace("boot::interactive-mode")

    while True:
        draw_dashboard()
        print()
        choice = input(c("Select option > ", BRIGHT_CYAN)).strip().upper()

        if choice == "1":
            run_demo()
        elif choice == "2":
            inspect_modules()
        elif choice == "3":
            summary_panel()
        elif choice == "4":
            print()
            print(c("[bye] closing showcase session.", BRIGHT_RED))
            break
        elif choice in {"M01", "M02", "M03", "M04", "M05", "M06"}:
            module_view(choice)
        else:
            print(c("[warn] invalid option.", BRIGHT_YELLOW))

        print()
        input(c("Press Enter to continue...", BRIGHT_BLACK))

def main():
    if "--capture" in sys.argv:
        capture_mode()
    else:
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(c("[bye] interrupted by operator.", BRIGHT_RED))