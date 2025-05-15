# Chordsnip API

Simple backend API for detecting chords from uploaded MP3 files using FastAPI and Madmom.

### Endpoint
`POST /detect_chords`

### Payload
Upload a file via multipart/form-data with field name: `file`

### Returns
JSON with timestamps and detected chords
