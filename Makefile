SHELL := /bin/bash
PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
ANSIBLE_GALAXY := $(VENV)/bin/ansible-galaxy
ANSIBLE_PLAYBOOK := $(VENV)/bin/ansible-playbook

.PHONY: setup lint test molecule syntax up down provision verify clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --disable-pip-version-check -r requirements.txt
	$(ANSIBLE_GALAXY) collection install -r collections/requirements.yml -p .cache/ansible/collections

lint:
	$(VENV)/bin/yamllint .
	$(VENV)/bin/ansible-lint

syntax:
	$(ANSIBLE_PLAYBOOK) --syntax-check playbooks/bootstrap.yml
	$(ANSIBLE_PLAYBOOK) --syntax-check playbooks/site.yml
	$(ANSIBLE_PLAYBOOK) --syntax-check playbooks/verify.yml

test: lint syntax
	$(VENV)/bin/pytest -q

molecule:
	PATH="$(CURDIR)/$(VENV)/bin:$$PATH" $(VENV)/bin/molecule test

up:
	vagrant up

provision:
	vagrant provision

verify:
	vagrant ssh -c "cd /vagrant && sudo /opt/ansible-venv/bin/ansible-playbook -i inventories/local/hosts.yml playbooks/verify.yml"

down:
	vagrant destroy -f

clean:
	rm -rf $(VENV) .cache .molecule .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
