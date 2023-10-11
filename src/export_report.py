from fpdf import FPDF
import pandas as pd
import math

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Competition Assessment Report', 0, 1, 'C')

def get_required_height(pdf, content, width):
    """Determine required height for content in specified width"""
    lines = pdf.multi_cell(width, 0, content, split_only=True)
    return len(lines) * pdf.font_size

def draw_headers(pdf, comp_df, cell_width, line_height):
    header_height = max([get_required_height(pdf, col, cell_width) for col in comp_df.columns])
    y_before = pdf.get_y()
    for col in comp_df.columns:
        x_pos = 10 + comp_df.columns.get_loc(col) * cell_width
        pdf.set_x(x_pos)
        
        # Drawing the cell borders with the determined header height
        pdf.cell(cell_width, header_height, border="L,R,B")
        
        # Placing the text in the center of the cell
        text_lines = pdf.multi_cell(cell_width, 0, col, split_only=True)
        text_height = len(text_lines) * line_height
        pdf.set_xy(x_pos, y_before + (header_height - text_height) / 2)
        pdf.multi_cell(w=cell_width, txt=col, align="C", h=line_height, border=0)
        
        pdf.set_y(y_before)
    pdf.set_y(y_before + header_height)

def create_pdf_report(business_data, competition_data):
    pdf = PDF("P", "mm", "A4")
    pdf.set_margins(left=10, top=10)
    pdf.set_font("Helvetica", style="", size=8)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.add_page()

    # Add business metrics
    pdf.cell(0, 10, f"Business Name: {business_data['name']}", ln=True)
    pdf.cell(0, 10, f"Score: {business_data['score']}", ln=True)
    pdf.cell(0, 10, f"Type of Place: {business_data['type']}", ln=True)
    pdf.cell(0, 10, f"Price level: {business_data['price_level']}", ln=True)
    pdf.cell(0, 10, f"Vicinity: {business_data['vicinity']}", ln=True)
    pdf.cell(0, 10, f"Number of reviews: {business_data['number_of_reviews']}", ln=True)
    pdf.cell(0, 10, f"\n", ln=True)
    
    comp_df = pd.DataFrame(competition_data)
    comp_df.drop(["geometry", "icon", "icon_background_color", "icon_mask_base_uri", "opening_hours", "photos", "place_id", "plus_code", "reference", "scope"], axis=1, inplace=True)
    
    pdf.cell(0, 10, f"Number of competing businesses: {len(comp_df)}", ln=True)
    pdf.cell(0, 10, f"Competition metrics:", ln=True)

    # Creating our table headers
    cell_width = (210 - 10 - 10) / len(comp_df.columns)
    line_height = pdf.font_size
    draw_headers(pdf, comp_df, cell_width, line_height)


    # Creating our table row by row
    for _, row in comp_df.iterrows():
        row_height = max([get_required_height(pdf, str(item), cell_width) for item in row])
        if pdf.get_y() + row_height > 297 - pdf.b_margin:  # Check if row fits on the remaining page
            pdf.add_page()
            draw_headers(pdf, comp_df, cell_width, line_height)
        y_before = pdf.get_y()
        for i, item in enumerate(row):
            pdf.set_x(10 + i * cell_width)
            pdf.multi_cell(w=cell_width, txt=str(item), align="C", border="L,R,B", h=row_height / len(pdf.multi_cell(cell_width, 0, str(item), split_only=True)))
            pdf.set_y(y_before)
        pdf.set_y(y_before + row_height)


    pdf.output('report.pdf')
    return 'report.pdf'