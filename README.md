# Files manager utilities in python

## Installation

```bash
pip install pyfilesmanager
```

## Usage

```bash
pyfilesmanager [--debug] COMMAND
```

### Commands

#### `version`

Prints the installed version of pyfilesmanager.

```bash
pyfilesmanager version
```

#### `find-duplicates`

Finds duplicate files in a given directory.

```bash
pyfilesmanager find-duplicates DIR_PATH [--output-dir OUTPUT_DIR]
```

| Argument / Option | Description                                            |
|-------------------|--------------------------------------------------------|
| `DIR_PATH`        | Directory to scan for duplicates                       |
| `--output-dir`    | Directory where debug files are written (default: `.`) |

### Global options

| Option       | Description                  |
|--------------|------------------------------|
| `--debug`    | Enable debug mode            |
| `--no-debug` | Disable debug mode (default) |
