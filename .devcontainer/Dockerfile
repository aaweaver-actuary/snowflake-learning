FROM debian:latest

WORKDIR /app

# This allows me to store .pyiceberg.yaml in the root of the project
ENV PYICEBERG_HOME=/app/.pyiceberg

RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        python3-setuptools \
        python3-wheel \
        git \
        zsh \
        curl \  
    && rm -rf /var/lib/apt/lists/* \
    && exec zsh \
    && if [ ! -d "/app/.venv" ]; then python3 -m venv .venv; fi \
    && . .venv/bin/activate \
    && pip install --upgrade pip \
    && if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi \
    && if [ -f "requirements-dev.txt" ]; then pip install -r requirements-dev.txt; fi \
    && pip install ipython ipykernel dbt-core dbt-snowflake duckdb snowflake pyiceberg[duckdb,snappy] \
\
    && git clone http://github.com/aaweaver-actuary/dotfiles \
    && cp ./dotfiles/install_dotfiles /usr/bin/install_dotfiles \
    && chmod +x /usr/bin/install_dotfiles \
    && rm -rf ./dotfiles \
    && install_dotfiles /app install_oh_my_zsh \
    && chmod +x /app/install_oh_my_zsh \
    && /app/install_oh_my_zsh \
    && rm -rf /app/install_oh_my_zsh \
    && exec zsh \
\
    && install_dotfiles $HOME .zshrc .zsh_aliases \
    && install_dotfiles /app .ruff.toml .mypy.ini .prettierrc pytest.ini

CMD ["/bin/zsh"]
