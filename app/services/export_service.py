import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from sqlalchemy.orm import Session
from app.services.weather_service import WeatherService
import logging

logger = logging.getLogger(__name__)


class ExportService:

    @staticmethod
    def generate_excel(db: Session, latitude: float = None, longitude: float = None):
        try:
            weather_data = WeatherService.get_last_48_hours_data(
                db, latitude, longitude)

            if not weather_data:
                raise Exception("No weather data found for the specified parameters")

            data = []
            for record in weather_data:
                data.append({
                    'timestamp': record.timestamp,
                    'temperature_2m': record.temperature_2m,
                    'relative_humidity_2m': record.relative_humidity_2m,
                    'latitude': record.latitude,
                    'longitude': record.longitude
                })

            df = pd.DataFrame(data)

            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Weather Data', index=False)

            excel_buffer.seek(0)
            return excel_buffer.getvalue()

        except Exception as e:
            logger.error(f"Error generating Excel file: {e}")
            raise Exception(f"Failed to generate Excel file: {e}")

    @staticmethod
    def generate_pdf_report(db: Session, latitude: float = None, longitude: float = None):
        try:
            weather_data = WeatherService.get_last_48_hours_data(
                db, latitude, longitude)

            if not weather_data:
                raise Exception("No weather data found for the specified parameters")

            # Prepare data for plotting
            timestamps = [record.timestamp for record in weather_data]
            temperatures = [record.temperature_2m for record in weather_data]
            humidity = [record.relative_humidity_2m for record in weather_data]

            # Create the plot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

            ax1.plot(timestamps, temperatures, 'r-', linewidth=2, label='Temperature (°C)')
            ax1.set_ylabel('Temperature (°C)', color='red')
            ax1.tick_params(axis='y', labelcolor='red')
            ax1.grid(True, alpha=0.3)
            ax1.legend()

            ax2.plot(timestamps, humidity, 'b-', linewidth=2, label='Relative Humidity (%)')
            ax2.set_ylabel('Relative Humidity (%)', color='blue')
            ax2.set_xlabel('Time')
            ax2.tick_params(axis='y', labelcolor='blue')
            ax2.grid(True, alpha=0.3)
            ax2.legend()

            plt.xticks(rotation=45)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            ax2.xaxis.set_major_locator(mdates.HourLocator(interval=6))

            plt.tight_layout()

            # Save plot image
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=120, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()

            # Build PDF
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            # Title
            elements.append(Paragraph("Weather Data Report", styles['Title']))
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph("Time-Series Analysis of Temperature and Humidity", styles['Heading2']))
            elements.append(Spacer(1, 0.3 * inch))

            # Metadata table
            location_info = f"Latitude: {latitude}, Longitude: {longitude}" if latitude and longitude else "Multiple Locations"
            date_range = f"{timestamps[0].strftime('%Y-%m-%d %H:%M')} to {timestamps[-1].strftime('%Y-%m-%d %H:%M')}"

            metadata = [
                ["Location:", location_info],
                ["Date Range:", date_range],
                ["Data Points:", str(len(weather_data))],
                ["Generated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            table = Table(metadata, colWidths=[100, 350])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.3 * inch))

            # Chart image
            elements.append(Paragraph("Temperature and Humidity Chart", styles['Heading2']))
            img = Image(img_buffer, width=6*inch, height=4*inch)
            elements.append(img)

            # Build PDF
            doc.build(elements)
            pdf_buffer.seek(0)

            return pdf_buffer.getvalue()

        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise Exception(f"Failed to generate PDF report: {e}")
