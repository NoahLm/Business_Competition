from fpdf import FPDF
import pandas as pd
import math

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Competition Assessment Report', 0, 1, 'C')


def create_pdf_report(business_data, competition_data):
    pdf = PDF("P", "mm", "A4")
    pdf.set_margins(left= 10, top= 10)
    pdf.set_font("Helvetica", style= "", size= 8)
    pdf.set_text_color(r= 0, g= 0, b= 0)
    pdf.add_page()

    # Add business metrics
    #pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Business Name: {business_data['name']}", ln=True)
    pdf.cell(0, 10, f"Score: {business_data['score']}", ln=True)
    pdf.cell(0, 10, f"Type of Place: {business_data['type']}", ln=True)
    pdf.cell(0, 10, f"Competition metrics:", ln=True)
    pdf.cell(0, 10, f"\n", ln=True)
    comp_df = pd.DataFrame(competition_data)
    comp_df.drop(["geometry","icon", "icon_background_color","icon_mask_base_uri","photos", "place_id", "plus_code", "reference"], axis = 1, inplace=True)
    pdf.cell(0, 10, f"Number of competing businesses: {len(comp_df)}", ln=True)
    pdf.cell(0, 10, f"Competition metrics:", ln=True)
    # Creating our table headers
    cell_width = (210 -10 -10) / len(comp_df.columns)
    line_height = pdf.font_size
    number_lines = 1
    for i in comp_df.columns:
        new_number_lines = math.ceil(pdf.get_string_width(str(i)) / cell_width)
        if new_number_lines > number_lines:
            number_lines = new_number_lines   
    
    for i in comp_df.columns:
        pdf.multi_cell(w= cell_width,
                    txt=str(i), align="C", border="L,R,B",h=line_height)
    pdf.ln(line_height * 1.5 * number_lines)   
    
        # Changing font style

    # Creating our table row by row
    for index, row in comp_df.iterrows():
        number_lines = 1
        for i in range(len(comp_df.columns)):
            new_number_lines = math.ceil(pdf.get_string_width(str(row[i])) / cell_width)
            if new_number_lines > number_lines:
                number_lines = new_number_lines

        for i in range(len(comp_df.columns)):
            pdf.multi_cell(w=cell_width,
                    txt=str(row[i]), align="C", border="L,R,B",h=line_height)
    pdf.ln(line_height * 1.5 * number_lines)
                  # go to next line after each row

    # ... add other business metrics

    # Add competition metrics
    # ... add competition metrics

    # Save PDF to file
    pdf.output('report.pdf')

    return 'report.pdf'