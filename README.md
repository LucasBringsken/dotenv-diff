# [dotenv-diff](https://github.com/LucasBringsken/dotenv-diff)

**Lightweight tool for quickly spotting missing keys and differing values in .env files**

`dotenv-diff` helps compare multiple `.env` files and immediately see:

- Which variables are missing in which files
- Which values differ between environments
- A clear matrix overview of all keys and files

It is designed as a simple developer utility for projects that maintain multiple environment configurations (local, staging, production, etc.).

---

## Features

- Compare any number of `.env` files at once
- Detect missing keys across environments
- Detect diverging values
- Show results in human‑friendly tables
- Three different views: summary, values, and presence
- Works with individual files, directories, and glob patterns

---

## Installation

```bash
pip install dotenv-diff
```

---

## Usage

All functionality is available through the command line interface.

You can pass:

- Individual `.env` files
- Directories containing `.env*` files
- Glob patterns like `.env.*`

### Examples

#### summary

Show a high‑level overview of differences.

```bash
dotenv-diff summary /path/to/.env.*
```

```
╭─ SUMMARY ───────────────────╮
│ Total Files:           3    │
│ Unique Keys:          12    │
│ Incomplete Keys:       3    │
│ Diverging Values:      4    │
╰─────────────────────────────╯
Incomplete Key Details
• REDIS_HOST is missing in:
  ↳ .env.production
  ↳ .env.staging

Diverging Value Details
• APP_ENV
  ↳ .env.local: development
  ↳ .env.production: production
  ↳ .env.staging: staging
```

#### values

Show a matrix of actual values for each key and file.

```bash
dotenv-diff values /path/to/.env.*
```

```
╭───────────────────────────────────────────────────────────────╮
│ VARIABLE        │ .env.local │ .env.staging │ .env.production │
├─────────────────┼────────────┼──────────────┼─────────────────┤
│ APP_ENV         │ development│ staging      │ production      │
│ DEBUG           │ true       │ true         │ false           │
│ LOG_LEVEL       │ DEBUG      │ —            │ INFO            │
│ DATABASE_USER   │ dev_user   │ prod_user    │ prod_user       │
│ DATABASE_PASS   │ dev_pass   │ prod_pass    │ prod_pass       │
│ PORT            │ 8000       │ 8000         │ —               │
╰───────────────────────────────────────────────────────────────╯
```

#### presence

Show only whether a variable exists in each file.

```bash
dotenv-diff presence /path/to/.env.*
```

```
╭───────────────────────────────────────────────────────────────╮
│ VARIABLE        │ .env.local │ .env.staging │ .env.production │
├─────────────────┼────────────┼──────────────┼─────────────────┤
│ APP_ENV         │     ✅     │      ✅     │       ✅       │
│ DEBUG           │     ✅     │      ✅     │       ✅       │
│ LOG_LEVEL       │     ✅     │      ❌     │       ✅       │
│ DATABASE_USER   │     ✅     │      ✅     │       ✅       │
│ DATABASE_PASS   │     ✅     │      ✅     │       ✅       │
│ PORT            │     ✅     │      ✅     │       ❌       │
╰───────────────────────────────────────────────────────────────╯
```
