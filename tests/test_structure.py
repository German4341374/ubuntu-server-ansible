"""Fast repository structure checks that do not require a virtual machine."""

from pathlib import Path
import re

import yaml
from jinja2 import Environment


ROOT = Path(__file__).parents[1]
REQUIRED_ROLES = {
    "admin_user",
    "common",
    "directories",
    "docker",
    "fail2ban",
    "firewall",
    "logrotate",
    "ssh_hardening",
    "sysctl",
    "timesync",
    "unattended_upgrades",
}


def test_required_roles_have_tasks_and_defaults():
    roles = ROOT / "roles"
    assert REQUIRED_ROLES <= {path.name for path in roles.iterdir() if path.is_dir()}
    for role in REQUIRED_ROLES:
        assert (roles / role / "tasks" / "main.yml").is_file()
        assert (roles / role / "defaults" / "main.yml").is_file()


def test_yaml_files_parse():
    excluded = {".cache", ".venv", ".molecule"}
    for path in ROOT.rglob("*.yml"):
        if excluded.intersection(path.parts):
            continue
        with path.open(encoding="utf-8") as stream:
            list(yaml.safe_load_all(stream))


def test_jinja_templates_parse():
    environment = Environment(autoescape=False)  # Templates produce configuration, not HTML.
    for path in (ROOT / "roles").rglob("*.j2"):
        environment.parse(path.read_text(encoding="utf-8"))


def test_site_playbook_references_every_role():
    play = yaml.safe_load((ROOT / "playbooks/site.yml").read_text(encoding="utf-8"))[0]
    configured_roles = {
        entry["role"] if isinstance(entry, dict) else entry for entry in play["roles"]
    }
    assert configured_roles == REQUIRED_ROLES


def test_inventory_uses_documentation_addresses_only():
    inventory = (ROOT / "inventories/example/hosts.yml").read_text(encoding="utf-8")
    addresses = set(re.findall(r"(?:\d{1,3}\.){3}\d{1,3}", inventory))
    assert addresses == {"192.0.2.10", "198.51.100.20"}


def test_repository_documents_safety_and_demo_workflows():
    for relative_path in [
        "README.md",
        "DEMO.md",
        "docs/design-notes.md",
        "SECURITY.md",
        "docs/runbooks/ssh-recovery.md",
    ]:
        assert (ROOT / relative_path).is_file()
