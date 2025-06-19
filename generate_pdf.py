from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Intelligent PDF Summarizer Test", ln=True, align="C")
pdf.multi_cell(0, 10, txt=(
    "This PDF is used for testing the Azure Durable Functions "
    "summarizer app. It contains a few sentences meant to represent "
    "sample content for summarization using Azure Cognitive Services "
    "and Azure OpenAI."
))
pdf.output("sample.pdf")

print("✅ sample.pdf created successfully.")
