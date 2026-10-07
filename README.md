# MARPOL-SAFE Major Project — UI/UX Enhanced Edition

This is the original MARPOL-SAFE Streamlit project with its existing database, records, alerts, approval queue, reports, audit trail, MARPOL library and offline synchronization retained. The UI layer adds:

- Login/logout with four shipboard roles
- Attractive ship-themed login screen
- Local ship artwork included in `assets/` (works offline)
- Live clock refresh
- Realistic vessel latitude/longitude prototype feed
- GPS values pre-filled into operation records
- Vessel banner and status cards

## Demo login
`chief / marpol123`
`second / marpol123`
`officer / marpol123`
`cadet / marpol123`

## Run without PowerShell activation
```powershell
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501`.

### GPS note
The included coordinates are a **realistic prototype/simulated live feed** around the Arabian Sea/Mangalore route. They are not a real onboard GPS sensor. For deployment on a vessel, connect the position field to an approved GPS/NMEA gateway and apply the required cybersecurity/access controls.
