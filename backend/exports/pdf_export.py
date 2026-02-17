"""
PDF Export - Generate PDF itineraries
"""

from typing import Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os
from backend.config import settings
from loguru import logger

class PDFExporter:
    """Export travel itineraries to PDF format"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12
        )
        
        self.day_style = ParagraphStyle(
            'DayStyle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#16A085'),
            spaceAfter=10
        )
    
    def export_itinerary(self, travel_plan: Dict[str, Any], filename: str = None) -> str:
        """
        Export travel plan to PDF
        
        Args:
            travel_plan: Complete travel plan dictionary
            filename: Optional custom filename
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Generate filename if not provided
            if not filename:
                destination = travel_plan.get('plan', {}).get('destination', 'trip')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"itinerary_{destination}_{timestamp}.pdf"
            
            # Ensure exports directory exists
            output_path = settings.EXPORTS_DIR / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build PDF content
            story = []
            plan = travel_plan.get('plan', {})
            
            # Title
            title = Paragraph(
                f"Travel Itinerary: {plan.get('destination', 'Your Trip')}",
                self.title_style
            )
            story.append(title)
            story.append(Spacer(1, 0.2*inch))
            
            # Summary
            summary = plan.get('summary', 'Your personalized travel plan')
            story.append(Paragraph(summary, self.styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Budget Summary
            budget = plan.get('budget_breakdown', {})
            if budget:
                story.append(Paragraph("Budget Summary", self.heading_style))
                budget_data = [
                    ['Category', 'Amount (USD)'],
                    ['Total Estimated', f"${budget.get('total_estimated', 'N/A')}"],
                    ['Daily Average', f"${budget.get('daily_average', 'N/A')}"],
                ]
                
                budget_table = Table(budget_data, colWidths=[3*inch, 2*inch])
                budget_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(budget_table)
                story.append(Spacer(1, 0.3*inch))
            
            # Daily Itinerary
            story.append(PageBreak())
            story.append(Paragraph("Day-by-Day Itinerary", self.heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            itinerary = plan.get('itinerary', {})
            days = itinerary.get('days', [])
            
            for day in days:
                # Day header
                day_title = f"Day {day.get('day_number', 'N/A')}: {day.get('theme', '')}"
                story.append(Paragraph(day_title, self.day_style))
                
                # Morning, Afternoon, Evening
                for period in ['morning', 'afternoon', 'evening']:
                    activity = day.get(period, {})
                    if activity:
                        period_text = f"<b>{period.capitalize()}:</b> "
                        if isinstance(activity, dict):
                            period_text += f"{activity.get('location', 'Activity')} "
                            period_text += f"({activity.get('time', 'TBD')})"
                            if activity.get('description'):
                                period_text += f"<br/>{activity.get('description')}"
                        else:
                            period_text += str(activity)
                        
                        story.append(Paragraph(period_text, self.styles['Normal']))
                        story.append(Spacer(1, 0.1*inch))
                
                # Meals
                meals = day.get('meals', {})
                if meals:
                    meal_text = f"<b>Meals:</b> {', '.join([f'{k}: {v}' for k, v in meals.items() if v])}"
                    story.append(Paragraph(meal_text, self.styles['Normal']))
                
                # Notes
                notes = day.get('notes', '')
                if notes:
                    story.append(Paragraph(f"<i>{notes}</i>", self.styles['Italic']))
                
                story.append(Spacer(1, 0.3*inch))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF exported successfully: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error exporting PDF: {e}")
            raise

# Global exporter instance
pdf_exporter = PDFExporter()
