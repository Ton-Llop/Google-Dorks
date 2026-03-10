#!/usr/bin/env python3
import os
import sys
import time
import random
import importlib.util
from pathlib import Path
from datetime import datetime

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

BASE_DIR = Path.cwd()
DOWNLOADS_DIR = BASE_DIR / "Downloads"
RESULT_HTML = BASE_DIR / "resultados.html"
RESULT_JSON = BASE_DIR / "resultados.json"
ENV_FILE = BASE_DIR / ".env"

RUNTIME_STATE = {
    "module_registry_loaded": False,
    "downloads_dir_exists": False,
    "result_html_exists": False,
    "result_json_exists": False,
    "env_exists": False,
    "core_files": {},
    "deps": {},
}

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
    ("M01", "Query Execution", "run searches with paging, language and export options"),
    ("M02", "Artifact Download", "download target file types from collected result links"),
    ("M03", "Local Smart Search", "inspect local files using regex or AI prompts"),
    ("M04", "Assisted Workflow", "setup, selenium search and dork generation"),
]

TACTICAL_LINES = [
    "query execution",
    "download workflow",
    "local file review",
    "result export",
    "optional selenium automation",
    "configuration via .env",
]


def c(text, color):
    return f"{color}{text}{RESET}" if USE_COLOR else text


def clear():
    if not sys.stdout.isatty():
        return
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


def dependency_status():
    deps = {
        "argparse": importlib.util.find_spec("argparse") is not None,
        "dotenv": importlib.util.find_spec("dotenv") is not None,
        "requests": importlib.util.find_spec("requests") is not None,
        "selenium": importlib.util.find_spec("selenium") is not None,
        "openai": importlib.util.find_spec("openai") is not None,
        "gpt4all": importlib.util.find_spec("gpt4all") is not None,
    }
    RUNTIME_STATE["deps"] = deps
    return deps


def path_status():
    core_files = {
        "ninjadorks.py": (BASE_DIR / "ninjadorks.py").exists(),
        "smartsearch.py": (BASE_DIR / "smartsearch.py").exists(),
        "file_downloader.py": (BASE_DIR / "file_downloader.py").exists(),
        "browserautosearch.py": (BASE_DIR / "browserautosearch.py").exists(),
    }

    RUNTIME_STATE["downloads_dir_exists"] = DOWNLOADS_DIR.exists() and DOWNLOADS_DIR.is_dir()
    RUNTIME_STATE["result_html_exists"] = RESULT_HTML.exists()
    RUNTIME_STATE["result_json_exists"] = RESULT_JSON.exists()
    RUNTIME_STATE["env_exists"] = ENV_FILE.exists()
    RUNTIME_STATE["core_files"] = core_files

    return {
        "downloads": RUNTIME_STATE["downloads_dir_exists"],
        "html": RUNTIME_STATE["result_html_exists"],
        "json": RUNTIME_STATE["result_json_exists"],
        "env": RUNTIME_STATE["env_exists"],
        "core_files_ok": all(core_files.values()),
    }


def prepare_registry():
    RUNTIME_STATE["module_registry_loaded"] = True
    return len(MODULES)


def progress(label, total=22, width=34):
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
    slow_print(c("[boot] launching showcase interface...", BRIGHT_WHITE), 0.01)

    steps = [
        "checking python dependencies",
        "inspecting project workspace",
        "loading menu registry",
    ]

    for step in steps:
        progress(step)

        if step == "checking python dependencies":
            dependency_status()
        elif step == "inspecting project workspace":
            path_status()
        elif step == "loading menu registry":
            prepare_registry()

        time.sleep(0.08)


def draw_runtime_checks():
    box_title("PROJECT HEALTH")

    deps = RUNTIME_STATE["deps"]
    core_ok = deps.get("argparse", False) and deps.get("dotenv", False) and deps.get("requests", False)
    selenium_ok = deps.get("selenium", False)
    ai_ok = deps.get("openai", False) or deps.get("gpt4all", False)
    core_files_ok = all(RUNTIME_STATE["core_files"].values()) if RUNTIME_STATE["core_files"] else False

    box_row(
        f"core dependencies : {'OK' if core_ok else 'MISSING'} (argparse / python-dotenv / requests)",
        BRIGHT_GREEN if core_ok else BRIGHT_YELLOW,
    )
    box_row(
        f"selenium support  : {'AVAILABLE' if selenium_ok else 'OPTIONAL / NOT INSTALLED'}",
        BRIGHT_GREEN if selenium_ok else BRIGHT_YELLOW,
    )
    box_row(
        f"AI backends       : {'AVAILABLE' if ai_ok else 'OPTIONAL / NOT INSTALLED'}",
        BRIGHT_GREEN if ai_ok else BRIGHT_YELLOW,
    )
    box_row(
        f".env file         : {'PRESENT' if RUNTIME_STATE['env_exists'] else 'MISSING'}",
        BRIGHT_GREEN if RUNTIME_STATE["env_exists"] else BRIGHT_YELLOW,
    )
    box_row(
        f"Downloads/        : {'PRESENT' if RUNTIME_STATE['downloads_dir_exists'] else 'MISSING'}",
        BRIGHT_GREEN if RUNTIME_STATE["downloads_dir_exists"] else BRIGHT_YELLOW,
    )
    box_row(
        f"resultados.html   : {'PRESENT' if RUNTIME_STATE['result_html_exists'] else 'NOT GENERATED'}",
        BRIGHT_GREEN if RUNTIME_STATE["result_html_exists"] else BRIGHT_YELLOW,
    )
    box_row(
        f"resultados.json   : {'PRESENT' if RUNTIME_STATE['result_json_exists'] else 'NOT GENERATED'}",
        BRIGHT_GREEN if RUNTIME_STATE["result_json_exists"] else BRIGHT_YELLOW,
    )
    box_row(
        f"core project files: {'READY' if core_files_ok else 'INCOMPLETE'}",
        BRIGHT_GREEN if core_files_ok else BRIGHT_YELLOW,
    )
    box_end()


def draw_dashboard():
    clear()
    print(c(BANNER, BRIGHT_RED))

    box_title("NINJADORKS :: SHOWCASE")
    box_row("project type   : educational search automation toolkit", BRIGHT_WHITE)
    box_row("interface      : terminal showcase aligned with the real CLI", BRIGHT_WHITE)
    box_row("focus          : functionality, reproducibility and clean execution flow", BRIGHT_WHITE)
    box_row("author         : Antoni Llop", BRIGHT_WHITE)
    box_row("status         : READY", BRIGHT_GREEN)
    box_end()

    print()
    draw_runtime_checks()

    print()
    box_title("MODULE MAP")
    for mid, name, desc in MODULES:
        left = c(f"[{mid}]", BRIGHT_RED) if USE_COLOR else f"[{mid}]"
        text = f"{left}  {name:<18} -> {desc}"
        box_row(text, BRIGHT_WHITE)
    box_end()

    print()
    box_title("SUPPORTED CLI AREAS")
    box_row("query / pages / language / html export / json export", BRIGHT_WHITE)
    box_row("download by extension from result links", BRIGHT_WHITE)
    box_row("smart-search over local files with regex or AI prompt", BRIGHT_WHITE)
    box_row(".env configuration / selenium search / dork generation", BRIGHT_WHITE)
    box_end()

    print()
    box_title("MENU")
    box_row("(1) Show validated command examples", BRIGHT_WHITE)
    box_row("(2) Inspect module map", BRIGHT_WHITE)
    box_row("(3) Show workflow summary", BRIGHT_WHITE)
    box_row("(4) Exit", BRIGHT_WHITE)
    box_row("", WHITE)
    box_row("aliases: M01 M02 M03 M04", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_end()


def run_demo():
    print()
    box_title("VALIDATED COMMAND EXAMPLES")
    commands = [
        "$ python ninjadorks.py -c",
        "$ python ninjadorks.py -q 'site:example.com filetype:pdf' --pages 1 --lang lang_es --html resultados.html --json resultados.json",
        "$ python ninjadorks.py -q 'site:example.com filetype:pdf' --download pdf",
        "$ python ninjadorks.py --smart-search ./Downloads --regex '(?i)password|token|secret'",
        "$ python ninjadorks.py -q 'site:example.com login' --selenium",
    ]
    for cmd in commands:
        box_row(cmd, BRIGHT_WHITE)
        time.sleep(0.20)

    box_row("notes:", BRIGHT_WHITE)
    box_row("   - option -c creates or updates .env", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   - html/json export requires an active query", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   - download uses links returned by the search results", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   - smart-search works over an existing local directory", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   - selenium support is optional and environment-dependent", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_end()


def inspect_modules():
    print()
    box_title("MODULE DETAILS + REAL USAGE")

    module_blocks = [
        ("[M01] Query Execution", [
            "capabilities -> -q / --pages / --start-page / --lang / --html / --json",
            "example      -> python ninjadorks.py -q 'site:example.com report' --pages 2",
            "example      -> python ninjadorks.py -q 'filetype:pdf budget' --html resultados.html --json resultados.json",
        ]),
        ("[M02] Artifact Download", [
            "capabilities -> --download pdf,docx,sql,txt after collecting result links",
            "example      -> python ninjadorks.py -q 'site:example.com filetype:pdf' --download pdf",
            "example      -> python ninjadorks.py -q 'site:example.com filetype:sql' --download sql",
        ]),
        ("[M03] Local Smart Search", [
            "capabilities -> --smart-search PATH with --regex or --prompt",
            "example      -> python ninjadorks.py --smart-search ./Downloads --regex '(?i)admin|password'",
            "example      -> python ninjadorks.py --smart-search ./Downloads --prompt 'Resume el contenido principal'",
        ]),
        ("[M04] Assisted Workflow", [
            "capabilities -> -c / --selenium / --generate-dork",
            "example      -> python ninjadorks.py -c",
            "example      -> python ninjadorks.py -q 'site:example.com login' --selenium",
            "example      -> python ninjadorks.py --generate-dork 'Busca documentos PDF públicos de presupuestos'",
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
        "M01": "QUERY EXECUTION",
        "M02": "ARTIFACT DOWNLOAD",
        "M03": "LOCAL SMART SEARCH",
        "M04": "ASSISTED WORKFLOW",
    }

    data = {
        "M01": [
            "capabilities -> -q / --pages / --start-page / --lang / --html / --json",
            "usage        -> python ninjadorks.py -q 'site:example.com report' --pages 2",
            "usage        -> python ninjadorks.py -q 'filetype:pdf budget' --html resultados.html --json resultados.json",
            "output       -> console results plus optional html/json files",
        ],
        "M02": [
            "capabilities -> --download EXT[,EXT...] using search result links",
            "usage        -> python ninjadorks.py -q 'site:example.com filetype:pdf' --download pdf",
            "usage        -> python ninjadorks.py -q 'site:example.com filetype:txt' --download txt",
            "output       -> downloaded files under Downloads/",
        ],
        "M03": [
            "capabilities -> --smart-search PATH with --regex or --prompt",
            "usage        -> python ninjadorks.py --smart-search ./Downloads --regex '(?i)token|secret'",
            "usage        -> python ninjadorks.py --smart-search ./Downloads --prompt 'Resume los hallazgos'",
            "output       -> terminal matches or AI summaries by file",
        ],
        "M04": [
            "capabilities -> configuration, selenium-assisted search, dork generation",
            "usage        -> python ninjadorks.py -c",
            "usage        -> python ninjadorks.py -q 'site:example.com login' --selenium",
            "usage        -> python ninjadorks.py --generate-dork 'Busca PDFs públicos sobre presupuestos'",
            "output       -> configured environment or guided search workflow",
        ],
    }

    print()
    box_title(f"MODULE VIEW :: {titles[module_id]}")
    box_row(f"module_id     : {module_id}", BRIGHT_WHITE)
    for item in data[module_id]:
        box_row(item, BRIGHT_BLACK if USE_COLOR else WHITE)
    box_end()


def summary_panel():
    print()
    box_title("WORKFLOW SUMMARY")
    box_row("focus areas   : " + " / ".join(TACTICAL_LINES), BRIGHT_WHITE)
    box_row("architecture  : search -> optional download -> local review -> export", BRIGHT_WHITE)
    box_row("runtime       : terminal workflow backed by ninjadorks.py arguments", BRIGHT_WHITE)
    box_row("configuration : .env for engine and API settings when required", BRIGHT_WHITE)
    box_row("", WHITE)
    box_row("recommended demo flow:", BRIGHT_WHITE)
    box_row("   1) python ninjadorks.py -c", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   2) python ninjadorks.py -q 'site:example.com filetype:pdf' --html resultados.html --json resultados.json", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   3) python ninjadorks.py -q 'site:example.com filetype:pdf' --download pdf", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_row("   4) python ninjadorks.py --smart-search ./Downloads --regex '(?i)password|token|secret'", BRIGHT_BLACK if USE_COLOR else WHITE)
    box_end()


def capture_mode():
    boot_runtime()
    draw_dashboard()
    print()
    run_demo()
    print()
    summary_panel()
    print()
    line()
    print(c("[tip] this showcase only prints commands that exist in ninjadorks.py.", BRIGHT_YELLOW))
    print(c("[tip] runtime checks are based on local files and installed python modules.", BRIGHT_YELLOW))
    line()


def interactive_mode():
    boot_runtime()

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
        elif choice in {"M01", "M02", "M03", "M04"}:
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