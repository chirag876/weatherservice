from fastapi.responses import FileResponse
from app.utils.excel_generator import generate_excel
from app.utils.pdf_generator import generate_pdf


def export_excel():
    excel_mime = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    path = generate_excel()
    return FileResponse(
        path,
        media_type=excel_mime,
        filename="weather_data.xlsx"
    )


def export_pdf():
    path = generate_pdf()
    return FileResponse(
        path,
        media_type="application/pdf",
        filename="weather_report.pdf"
    )
