from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
import io

def generate_pdf_report(report_data, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='ReportTitle', parent=styles['h1'], alignment=TA_CENTER, spaceAfter=0.5*inch))
    styles.add(ParagraphStyle(name='SectionTitle', parent=styles['h2'], spaceBefore=0.2*inch, spaceAfter=0.1*inch))

    story = []
    title = report_data.get('title', "Data Analysis Report")
    story.append(Paragraph(title, styles['ReportTitle']))

    intro_text = report_data.get('intro_text', "Summary of the data analysis.")
    if intro_text: story.append(Paragraph(intro_text, styles['Justify'])); story.append(Spacer(1, 0.2*inch))

    results_summary = report_data.get('results_summary')
    if results_summary:
        story.append(Paragraph("Analysis Summary", styles['SectionTitle']))
        for line in results_summary.split('\n'): story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

    plot_figure = report_data.get('plot_figure')
    if plot_figure and plot_figure.get_axes():
        story.append(Paragraph("Plot Visualization", styles['SectionTitle']))
        img_buffer = io.BytesIO()
        try:
            plot_figure.savefig(img_buffer, format='PNG', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            max_width = doc.width - 0.5*inch
            img = Image(img_buffer, width=max_width, height=(max_width * plot_figure.get_figheight()) / plot_figure.get_figwidth())
            img.hAlign = 'CENTER'
            story.append(img)
        except Exception as e:
            story.append(Paragraph(f"<i>Error embedding plot: {str(e)}</i>", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    doc.build(story)
