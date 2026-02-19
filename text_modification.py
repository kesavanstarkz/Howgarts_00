from text_extraction import extract_entities
import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Input text containing project details
input_text = """
    
Project Name 

BOCE Advanced Information Portal   

Name of Client  

Alexion Pharmaceuticals, Inc. 

Effective Date 

25th May 2024 

Type 

Fixed Bid 

Scope & Timeline 

Development, Launch and Hypercare of the Application (25th Apr’24 - 31st July’24)  
Operational Support of the Application as detailed in Section 16 (1st Aug’24 - 31st Dec’24) 


"""

def create_docx_sow(data, output_path):
    """Creates a professionally formatted DOCX Statement of Work."""
    doc = Document()

    # --- Header Section ---
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("STATEMENT OF WORK")
    run.bold = True
    run.underline = True
    run.font.size = Pt(16)

    confidential = doc.add_paragraph()
    confidential.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = confidential.add_run("CONFIDENTIALITY: HIGH")
    run.bold = True
    run.underline = True
    run.font.size = Pt(12)

    doc.add_paragraph("\nThe information contained in this document shall be deemed Confidential Information to both parties. It shall not be disclosed, duplicated, or used for any purpose other than that stated herein, in whole or in part, without prior written consent of the other party.\n")

    # --- Summary Table ---
    table = doc.add_table(rows=0, cols=2)
    table.style = 'Table Grid'
    
    summary_data = [
        ("Project Name", data.get("project_name", "")),
        ("Name of Client", data.get("client_name", "")),
        ("Effective Date", data.get("effective_date", "")),
        ("Type", data.get("type", "")),
    ]
    
    for label, value in summary_data:
        row_cells = table.add_row().cells
        row_cells[0].text = label
        row_cells[0].paragraphs[0].runs[0].bold = True
        row_cells[1].text = str(value)

    # Add Scope to table
    scope_cells = table.add_row().cells
    scope_cells[0].text = "Scope & Timeline"
    scope_cells[0].paragraphs[0].runs[0].bold = True
    scope_text = "\n".join(data.get("scope_timeline", []))
    scope_cells[1].text = scope_text

    doc.add_page_break()

    # --- Detailed Content ---
    doc.add_heading("STATEMENT OF WORK #4", level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER

    p = doc.add_paragraph()
    p.add_run(f"This Statement of Work (“SOW”) is entered into as of {data.get('effective_date')} (Effective Date) by and between {data.get('client_name')}, a Delaware corporation having a principal place of business at 121 Seaport Blvd., Boston, MA 02210 (“Alexion”), and AGILISIUM CONSULTING LLC with its principal place of business located at 6200 Canoga Ave, Suite 315, Woodland Hills, CA 91367 (“Service Provider”)").italic = False

    doc.add_heading("1. BACKGROUND:", level=2)
    doc.add_paragraph("Agilisium and the Client entered into a Master Service Agreement (the Agreement) on 19th day of July 2023, under which the Client engages Agilisium to perform the services as detailed in this SOW and Agilisium agrees to perform the same on the terms and conditions set out in the Agreement and this SOW.")
    
    doc.add_paragraph(f"{data.get('project_name')} (English Language only) will be setup as a platform to bring key pieces of data from various sources of data that drives significant business needs. The data will be presented as reports, dashboards, graphs/charts, images, and links to documents that will serve the primary needs of commercial staff to be productive and improve performance.")

    doc.add_heading("2. TERM OF ENGAGEMENT:", level=2)
    p = doc.add_paragraph("The Services under this SOW will commence on the effective date mentioned below:\n")
    p.add_run(f"Effective date: {data.get('effective_date')}\n").bold = True
    p.add_run("Termination Date: 31st Dec’24").bold = True

    doc.add_heading("3. PROJECT MANAGERS / CONTACT:", level=2)
    p = doc.add_paragraph()
    p.add_run("Agilisium Project Contact: ").bold = True
    p.add_run("Manager Name {name@agilisium.com}")
    p = doc.add_paragraph()
    p.add_run("Client Project Contact: ").bold = True
    p.add_run("Chetan Sohagiya (Chetan.Sohagiya@alexion.com)")

    doc.add_heading("4. SCOPE OF SERVICE:", level=2)
    doc.add_paragraph("The Portal will support the RDU Business operations team by consolidating all commercial information and reporting into a single location. This will allow the team to quickly identify information needed for business decisions without time consuming navigation between different platforms.")

    doc.add_paragraph("Phase 1 of our project focuses on implementing core features such as single-sign-on authentication, collaboration through Microsoft Teams, favorites management, search capabilities, self-service options and ensuring accessibility across PC, iPad, and mobile devices.")
    doc.add_paragraph("Phase 2 will bring in additional functionalities, including analytics via Chatbot powered by OpenAI ChatGPT.")

    doc.add_heading("ARCHITECTURE:", level=2)
    doc.add_paragraph("ARCHITECTURE DIAGRAM PLACEHOLDER")
    doc.add_paragraph("Short description about the image. - along with Tech Stack")

    doc.save(output_path)
    return output_path

if __name__ == "__main__":
    # 1. Extract data
    print("Extracting data using DeepSeek-R1 (1.5B)...")
    extracted_data = extract_entities(input_text)
    
    # Print the data to verify mapping
    print("\n--- EXTRACTED DATA ---")
    import json
    print(json.dumps(extracted_data, indent=4))
    print("----------------------\n")
    
    # 2. Generate DOCX
    docx_file = "Statement_Of_Work_Generated.docx"
    try:
        path = create_docx_sow(extracted_data, docx_file)
        print(f"--- DOCX GENERATED ---")
        print(f"File saved to: {os.path.abspath(path)}")
        print("-----------------------")
    except Exception as e:
        print(f"Error generating DOCX: {e}")
        if "Permission denied" in str(e):
            print("\nTIP: Please make sure 'Statement_Of_Work_Generated.docx' is not open in another program.")
