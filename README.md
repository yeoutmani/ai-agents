# Environnement Python pour apprendre les agents IA

Ce dossier contient un mini-parcours pour apprendre a creer des agents IA avec Python et l'OpenAI Agents SDK.

## 1. Activer l'environnement

```bash
source .venv/bin/activate
```

Si `.venv` n'existe pas encore:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Configurer la cle API

Copie le fichier d'exemple:

```bash
cp .env.example .env
```

Puis ajoute ta cle OpenAI dans `.env`:

```bash
OPENAI_API_KEY=sk-...
```

## 3. Lancer les exercices

Agent simple:

```bash
python examples/01_agent_simple.py
```

Agent avec un outil Python:

```bash
python examples/02_agent_avec_outil.py
```

Agent routeur avec plusieurs specialistes:

```bash
python examples/03_multi_agents.py
```

## Ce que tu vas apprendre

- Creer un agent avec un nom et des instructions.
- Donner des outils Python a un agent.
- Lancer un agent avec `Runner.run`.
- Router une question vers plusieurs agents specialistes.
- Garder un projet propre avec `.env`, `.venv` et `requirements.txt`.

Documentation utile:

- [OpenAI Agents SDK Python](https://openai.github.io/openai-agents-python/)
- [Quickstart Agents SDK](https://openai.github.io/openai-agents-python/quickstart/)
