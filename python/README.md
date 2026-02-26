# Šablony pro IPP projekt – Python

## Nástroje pro kontrolu kvalitu kódu

V obou šablonách jsou pomocí souboru `pyproject.toml` nakonfigurovány nástroje ruff a mypy, které
máte využít pro kontrolu kvality kódu a pro kontrolu typových anotací. Do této konfigurace je
**zakázáno zasahovat** (bude kontrolováno).

Jakmile jsou nástroje nainstalovány ve vašem pythonovém prostředí, lze je spustit z kořenového 
adresáře projektu pomocí `ruff` a `mypy` (viz níže). Doporučujeme oba nástroje spouštět **pravidelně**
v průběhu vývoje – jinak se chyby zvládnou velice rychle nahromadit. Také doporučujeme využít rozšíření
pro různá IDE či editory kódu existují rozšíření, která umí ruff integrovat přímo do svých kontrol kódu
(např. pro IntelliJ PyCharm doporučuji rozšíření [RyeCharm](https://plugins.jetbrains.com/plugin/25230-ryecharm)).

Velmi doporučujeme využít nástroj [pre-commit](https://pre-commit.com/), který se integruje s gitem
a při každém commitu automaticky spustí kontroly oběma nástroji. V případě, že kontroly selžou,
nedovolí (bez použití přepínače `--no-verify`) commit ani vytvořit. Příklad konfiguračího souboru
pro tento nástroj najdete v tomto adresáři v souboru `example-pre-commit-config.yaml`.

## Správa projektu a závislostí

V obou šablonách jsou povinně využity knihovny třetích stran ([Pydantic](https://docs.pydantic.dev/latest/),
v případě interpretu taky [pydantic-xml](https://pydantic-xml.readthedocs.io/en/latest/)). 
Požadované nástroje ruff a mypy se také instalují jako pythonové balíčky. Z tohoto důvodu budete
muset zvolit nějaký způsob správy pythonového prostředí, které budou k dispozici i při běhu
(v kontejneru). V tomto směru doporučujeme zvolit jednu z možností:
- klasická systémová instalace Pythonu a správce balíčků **pip**, přičemž využijete tzv.
  **virtuální prostředí** (venv) – viz [dokumentaci](https://docs.python.org/3/library/venv.html);
- správce projektu [**uv**](https://docs.astral.sh/uv/), který poskytuje kompletní správu projektu 
  i závislostí.

V obou šablonách jsou předpřipraveny soubory `requirements.txt` (závislosti nutné při běhu)
a `requirements-dev.txt` (závislosti nutné jen pro vývoj – ruff a mypy), zároveň je připraven také
projektový soubor `pyproject.toml`, který lze přímo využít se správcem projektu **uv**.

Příklad vytvoření a použití virtuálního prostředí:

```bash
# vytvoří virtuální prostředí
python3 -m venv .venv
# upraví aktuální sezení shellu tak, že používá Python z virtuálního prostředí
source .venv/bin/activate
# nainstaluje balíčky
pip install -r requirements.txt requirements-dev.txt
# ruff a mypy
ruff check
ruff format
mypy .
# spustí skript
python src/tester.py
```

Příklad použití **uv**:

```bash
# nainstaluje v automaticky spravovaném virtuálním prostředí závislosti podle pyproject.toml
uv sync
# příkazy lze ve virtuálním prostředí spouštět přímo skrz uv run
uv run ruff check
uv run python src/tester.py
# případně lze také aktivovat vytvořené virtuální prostředí jako výše
```

## Spuštění v kontejneru

Je na vás, jak zajistíte, že se vaše programy budou spouštět v prostředí, které má nainstalované 
všechny potřebné závislosti – záleží, jaký způsob správy projektu zvolíte.

Uživatel bude testovací nástroj spouštět pouze v kontejneru, který bude vytvořen na 
základě vašeho Containerfile (Dockerfile). Při použití virtuálních prostředí (venv) je jedním
z možných postupů, že využijete shellový skript, který si aktivuje prostředí a předá argumenty.
Váš Containerfile by tedy obsahoval např. direktivu:

```Dockerfile
ENTRYPOINT ["/app/docker-entrypoint.sh"]
```

přičemž skript `docker-entrypoint.sh` bude obsahovat příkazy pro spuštění testovacího nástroje
a předání parametrů, např.:

```bash
#!/bin/bash
source .venv/bin/activate
python src/tester.py "$@"
```

Při použití správce projektů **uv** doporučujeme následovat [instrukce v dokumentaci](https://docs.astral.sh/uv/guides/integration/docker/),
odkazován tam je i repozitář s ukázkami Containerfile souborů pro použití s **uv**.
