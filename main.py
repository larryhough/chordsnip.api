from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from madmom.features.chords import CNNChordFeatureProcessor, CRFChordRecognitionProcessor
import os
import uuid

app = FastAPI()

@app.post("/detect_chords")
async def detect_chords(file: UploadFile = File(...)):
    try:
        input_id = str(uuid.uuid4())
        mp3_path = f"temp_{input_id}.mp3"
        wav_path = f"temp_{input_id}.wav"

        with open(mp3_path, "wb") as f:
            f.write(await file.read())

        audio = AudioSegment.from_file(mp3_path)
        audio.export(wav_path, format="wav")

        chord_proc = CNNChordFeatureProcessor()
        crf_proc = CRFChordRecognitionProcessor()
        chords = crf_proc(chord_proc(wav_path))

        chord_list = []
        for start_time, end_time, chord in chords:
            minutes = int(start_time // 60)
            seconds = int(start_time % 60)
            chord_list.append({
                "start": f"{minutes:02}:{seconds:02}",
                "chord": chord
            })

        os.remove(mp3_path)
        os.remove(wav_path)

        return JSONResponse(content=chord_list)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
