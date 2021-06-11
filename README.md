# USCIS Case Tracker
USCIS Case Tracker and notifier using:
- `requests` - Get details from [USCIS](https://egov.uscis.gov/)
- `BeautifulSoup` - Extract tag values from html response
- `SMTP` - Send email and SMS notification using Simple Mail Transfer Protocol [(choose between TLS or SSL)](emailer.py)

### Commit:
`pip install -U sphinx==4.0.2`<br>
`pip install pre-commit==2.13.0`<br>
`pip install virtualenv==20.0.33`<br>
`pre-commit run --all-files`

### Runbook:
https://thevickypedia.github.io/uscis_case_tracker/

### Docker Setup:
Uses `python:3.8-slim` to reduce build time. Since credentials are passed using `params.json` in run-time, there is no need for `ENV` in [Dockerfile](Dockerfile)

[comment]: <> ( Refer [article on medium]&#40;https://medium.com/swlh/alpine-slim-stretch-buster-jessie-bullseye-bookworm-what-are-the-differences-in-docker-62171ed4531d&#41; to understand difference between `slim`, `alpine` and `buster`)

#### Commands:
- `docker build -t uscis .`
- `docker run uscis`

#### Container sizes and build time comparison:

[comment]: <> (docker pull --quiet python:3.8)
[comment]: <> (docker images)
[comment]: <> (The colons `:` in line #17 decide the text alignment inside the table.)

| Repository   | Tag          | Size    | Build Time |
|:------------ |:------------ |-------: | ----------:|
| `python`     | `3.8-alpine` | 79 MB   | 15.2s      |
| `python`     | `3.8-slim`   | 165 MB  | 18.1s      |
| `python`     | `3.8`        | 934 MB  | 119.5s     |

[comment]: <> (`*/5 * * * * cd $HOME/uscis-case-tracker && source venv/bin/activate && python3 tracker.py >> $HOME/uscis-case-tracker/script_output.log 2>&1 && deactivate`)
