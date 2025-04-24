format:
		black .


lint: 
		black --check .



run:
		python main.python



setup:
	@echo "Setting up Python environment..."
	@if command -v pyenv >/dev/null 2>&1; then \
		echo "Using pyenv to manage Python versions..."; \
		if pyenv versions | grep -q "3\.10"; then \
			echo "Python 3.10 found in pyenv, using it..."; \
			PYENV_VERSION=3.10.16 pyenv exec python -m venv venv; \
		else \
			echo "Installing Python 3.19 with pyenv..."; \
			pyenv install 3.10.16; \
			PYENV_VERSION=3.10.16 pyenv exec python -m venv venv; \
		fi; \
	elif command -v python3.10 >/dev/null 2>&1; then \
		echo "System Python3.10 found, creating virtual environment..."; \
		python3.10 -m venv venv; \
	else \
		echo "Neither Python3.10 nor pyenv found. Installing pyenv..."; \
		curl https://pyenv.run | bash; \
		export PATH="$$HOME/.pyenv/bin:$$PATH"; \
		eval "$$(pyenv init --path)"; \
		eval "$$(pyenv init -)"; \
		pyenv install 3.10.16; \
		PYENV_VERSION=3.10.16 pyenv exec python -m venv venv; \
	fi
	@echo "Activating virtual environment and installing requirements..."
	@. venv/bin/activate && pip install --upgrade pip && pip install -e ."[dev]"
	@echo "Setup complete ..."
