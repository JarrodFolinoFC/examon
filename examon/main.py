import sys
print(sys.path)

['/Users/jarrod.folino/Dev/examon-proj/examon/examon',
 '/Users/jarrod.folino/.pyenv/versions/3.9.16/lib/python39.zip',
 '/Users/jarrod.folino/.pyenv/versions/3.9.16/lib/python3.9',
 '/Users/jarrod.folino/.pyenv/versions/3.9.16/lib/python3.9/lib-dynload',
 '/Users/jarrod.folino/Dev/examon-proj/examon/.venv/lib/python3.9/site-packages',
 '/Users/jarrod.folino/Dev/examon-proj/examon']

from view.cli_runtime import CliRuntime

if __name__ == "__main__":
    CliRuntime.run()
