
# prerequisites
- python 3.11
- pdm (https://pdm.fming.dev/)
- (optional) direnv (to just set stuff up for you)
- (optional) pipx (to isolate the PDM install)

**direnv** can be installed with `brew install direnv`, same with `pipx`.

run `direnv allow` (with pdm installed already) to get things running. otherwise, follow the instructions below.



# installation

1. clone this repo to another directory
2. `python -m venv .venv`
3. `pip install .` (or alternatively, `pdm install`)
4. run `invoke edge` to generate code based on edgedb schema

# usage

1. ensure you set the right directories in `tasks.py`.

## notes

this is useful for me to not think about fastAPI/routing, literally just code the API via input/output queries and fastAPI handles all the typing/routing.

