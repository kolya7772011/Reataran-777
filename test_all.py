#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Django backend + frontend integration test script

Usage:
  python test_all.py
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from urllib.request import Request, urlopen

# Configuration
BASE_DIR = Path(__file__).parent
DJANGO_BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:8000"

# Colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
END = "\033[0m"
SUCCESS = "✓"
FAILURE = "✗"
INFO = "ℹ"


def log_success(msg):
    print(f"{GREEN}{SUCCESS}{END} {msg}")


def log_failure(msg):
    print(f"{RED}{FAILURE}{END} {msg}")


def log_info(msg):
    print(f"{YELLOW}{INFO}{END} {msg}")


def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=120)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def test_django_migrations():
    print("\n📦 Testing Django migrations...")
    code, out, err = run_command(f'"{BASE_DIR / "venv\Scripts\python.exe"}" manage.py migrate')
    if code == 0:
        log_success("Migrations applied successfully")
        return True
    else:
        log_failure(f"Migrations failed: {err}")
        return False


def test_django_staticfiles():
    print("\n📁 Testing Django static files setup...")
    from config.settings import STATICFILES_DIRS, STATIC_ROOT
    checks = [
        ("STATICFILES_DIRS", BASE_DIR / "static"),
        ("STATIC_ROOT", BASE_DIR / "staticfiles"),
        ("WhiteNoise in MIDDLEWARE", any("whitenoise" in m for m in globals().get("MIDDLEWARE", [])))
    ]
    all_ok = True
    for name, path in checks:
        if os.path.exists(path):
            log_success(f"{name}: {path}")
        else:
            log_failure(f"{name}: {path} (MISSING)")
            all_ok = False
    return all_ok


def test_static_file_server():
    print("\n🌐 Testing static file server...")
    test_files = [
        ("/static/frontend/globals.css", "text/css"),
        ("/static/frontend/config.js", "application/javascript"),
        ("/static/frontend/index.html", "text/html"),
    ]
    all_ok = True
    for path, expected_type in test_files:
        try:
            req = Request(f"{FRONTEND_URL}{path}")
            with urlopen(req, timeout=10) as resp:
                content_type = resp.info().get("Content-Type", "")
                if expected_type in content_type:
                    log_success(f"GET {path} ({content_type})")
                else:
                    log_failure(f"GET {path} (wrong type: {content_type})")
                    all_ok = False
        except Exception as e:
            log_failure(f"GET {path} ({e})")
            all_ok = False
    return all_ok


def test_frontend_routes():
    print("\n🖥️ Testing frontend routes...")
    pages = [
        ("/", "Home"),
        ("/login", "Login"),
        ("/register", "Register"),
        ("/menu-page", "Menu"),
        ("/news-page", "News"),
        ("/about", "About"),
        ("/contact-page", "Contact"),
        ("/admin-panel", "Admin panel"),
    ]
    all_ok = True
    for path, name in pages:
        try:
            req = Request(f"{FRONTEND_URL}{path}")
            with urlopen(req, timeout=10) as resp:
                if resp.getcode() == 200 and resp.getheader("Content-Type", "").startswith("text/html"):
                    length = len(resp.read())
                    log_success(f"{name} ({path}): {length} bytes")
                else:
                    log_failure(f"{name} ({path}): {resp.getcode()}")
                    all_ok = False
        except Exception as e:
            log_failure(f"{name} ({path}): {e}")
            all_ok = False
    return all_ok


def test_api_endpoints():
    print("\n🧪 Testing API endpoints...")
    apis = [
        ("/api/schema/", "GET", None, "OpenAPI schema"),
        ("/api/docs/", "GET", None, "Swagger UI"),
        ("/api/token/", "POST", {"username": "test", "password": "test"}, "JWT token (bad credentials)"),
    ]
    all_ok = True
    for path, method, body, desc in apis:
        try:
            req = Request(f"{DJANGO_BACKEND_URL}{path}", data=json.dumps(body).encode() if body else None)
            req.add_header("Content-Type", "application/json")
            if method != "GET":
                req.get_method = lambda: method
            with urlopen(req, timeout=10) as resp:
                if resp.getcode() == 200 or ("bad credentials" in desc and resp.getcode() == 401):
                    log_success(f"{desc} ({method} {path}): {resp.getcode()}")
                else:
                    log_failure(f"{desc} ({method} {path}): {resp.getcode()}")
                    all_ok = False
        except Exception as e:
            if "bad credentials" in desc and ("401" in str(e) or "401" in str(e).lower()):
                log_success(f"{desc} ({method} {path}): 401 (expected)")
            else:
                log_failure(f"{desc} ({method} {path}): {e}")
                all_ok = False
    return all_ok


def test_admin_access():
    print("\n👤 Testing admin panel access...")
    try:
        req = Request(f"{FRONTEND_URL}/admin/", headers={"User-Agent": "Test"})
        with urlopen(req, timeout=10) as resp:
            if resp.getcode() == 200:
                log_success("Admin panel accessible")
                return True
            else:
                log_failure(f"Admin panel: {resp.getcode()}")
                return False
    except Exception as e:
        log_failure(f"Admin panel: {e}")
        return False


def main():
    print("=" * 70)
    print("Backend + Frontend Integration Test Suite")
    print("=" * 70)

    # Backup plan: try to find if the venv path is correct
    venv_path = BASE_DIR / "venv" / "Scripts" / "python.exe"
    if not venv_path.exists():
        # Try another possible location
        possible_paths = [
            BASE_DIR / "venv" / "bin" / "python",
            BASE_DIR / "env" / "Scripts" / "python.exe",
            BASE_DIR / "env" / "bin" / "python",
        ]
        for path in possible_paths:
            if path.exists():
                venv_path = path
                break

    if not venv_path.exists():
        log_failure("Python virtual environment not found")
        log_info("Available in venv directory:")
        for root, dirs, files in os.walk(BASE_DIR):
            if "venv" in root or "env" in root:
                print(f"  {root}/")
        return 1

    # Set DJANGO_SETTINGS_MODULE
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

    # Run all tests
    results = []
    results.append(("Django migrations", test_django_migrations()))
    results.append(("Static files setup", test_django_staticfiles()))
    results.append(("Static file server", test_static_file_server()))
    results.append(("Frontend routes", test_frontend_routes()))
    results.append(("API endpoints", test_api_endpoints()))
    results.append(("Admin access", test_admin_access()))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary:")
    print("=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "PASS" if result else "FAIL"
        color = GREEN if result else RED
        print(f"{color}{status}{END} {name}")

    print("=" * 70)
    print(f"Total: {passed}/{total} passed")

    if passed == total:
        log_success("All tests passed! The Django + Frontend integration is ready.")
        return 0
    else:
        log_failure("Some tests failed. Please check the configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
