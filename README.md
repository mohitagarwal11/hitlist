# hitlist

`hitlist` is a small command-line tool for tracking job applications in a local SQLite database.

## features

- add jobs
- update jobs by id
- list all jobs or filter by status
- delete by id, role and company, or status
- truncate the table and reset ids back to `1`

## install locally

Run these commands from the project folder:

```powershell
python -m pip install -e .
```

That installs the `hitlist` command on your machine.

If `hitlist` is not recognized right away, open a new terminal and try again.

## important note

`hitlist.db` is created in the folder where you run the `hitlist` command.

If you want to keep using the same database, run `hitlist` from the same folder each time.

## usage

Show all commands:

```powershell
hitlist --help
```

Add a job:

```powershell
hitlist add --role software_engineer --company openai --location remote --pay 5000 --status p
```

List all jobs:

```powershell
hitlist list
```

List by status:

```powershell
hitlist list --status i
```

Update a job by id:

```powershell
hitlist update 1 --status a --pay 7000
```

Delete a job by id:

```powershell
hitlist delete 1
```

Delete by role and company:

```powershell
hitlist delete --role software_engineer --company openai
```

Delete by status:

```powershell
hitlist delete --status g
```

Truncate the table and reset ids:

```powershell
hitlist truncate --choice y
```

## status values

You can use either the shortcut or the full word:

- `p` = `applied`
- `i` = `interviewed`
- `r` = `rejected`
- `a` = `accepted`
- `d` = `declined`
- `g` = `ghosted`

## quick start

```powershell
hitlist add --role backend_developer --company stripe --location remote --pay 8000 --status p
hitlist list
hitlist update 1 --status i
hitlist delete 1
```
