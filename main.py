from fastapi import FastAPI, UploadFile, File
import shutil
from parseybaby.pdfpurrse import gettexthehe, get_layout, get_tables
from pipelines.signals import Find_headers

from meowdels.intermeowdiate import IntermeowdiateRep, LayoutBlock, TableData, DetectedHeader
app = FastAPI()

@app.get("/")
def home():
    return {"message": "meow backend alive"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    


    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #get it raw ... hehehehe

    rawtext = gettexthehe(filepath)
    rawlayout = get_layout(filepath)
    rawtables = get_tables(filepath)

    #see signals

    rawheaders = Find_headers(rawlayout)

    #convert to meowdels

    layout_blocks = [LayoutBlock(**block) for block in rawlayout]

    tables = [TableData(**table) for table in tables]

    headers_found = [DetectedHeader(**header) for header in rawheaders]

    intermediate = IntermeowdiateRep(
        rawtext = rawtext,
        layout_blocks = layout_blocks,
        tables = tables,
        headers_found = headers_found
    )

    return intermediate.model_dump()