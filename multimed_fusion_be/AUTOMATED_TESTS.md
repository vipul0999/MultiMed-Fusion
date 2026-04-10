# Automated Test Runbook

## Backend API and Unit Tests

Run all sheet-aligned backend tests from WSL:

```bash
cd "/home/anil/gdp 2/backend_test"
source venv/bin/activate
python manage.py test accounts portal medfiles
```

Run a single sheet:

```bash
python manage.py test medfiles.test_tc1
python manage.py test portal.test_tc31
python manage.py test accounts.test_tc40
```

The backend helpers use the provided sample files from:

`/mnt/c/Users/s576701/Documents/gdp files`

You can override that path with:

```bash
export GDP_TEST_DATA_DIR="/mnt/c/Users/s576701/Documents/gdp files"
```

## Frontend UI Tests

Run from Windows PowerShell or Command Prompt using `pushd` so Playwright can work with the WSL path:

```bat
pushd \\wsl.localhost\Ubuntu-22.04\home\anil\gdp 2\gdp_fe
set UI_BASE_URL=http://127.0.0.1:5173
set UI_DOCTOR_USERNAME=doctor 11
set UI_PATIENT_USERNAME=patient 11
set UI_PASSWORD=password
set GDP_UI_TEST_DATA_DIR=C:\Users\s576701\Documents\gdp files
npm run test:ui
```

If Playwright browsers are not installed yet:

```bat
npx playwright install
```
