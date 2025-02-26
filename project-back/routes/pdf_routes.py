from flask import Blueprint, request, jsonify, send_file
from utils import token_required
from fpdf import FPDF

pdf_bp = Blueprint('pdf', __name__)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "Reporte de Registros", ln=True, align="C")
        self.ln(10)

    def table_header(self):
        self.set_font("Arial", "B", 10)
        self.cell(20, 10, "ID", 1, 0, "C")
        self.cell(30, 10, "Cantidad", 1, 0, "C")
        self.cell(40, 10, "Categoría", 1, 0, "C")
        self.cell(50, 10, "Concepto", 1, 0, "C")
        self.cell(30, 10, "Fecha", 1, 0, "C")
        self.cell(20, 10, "Tipo", 1, 1, "C")

    def add_row(self, registro):
        self.set_font("Arial", "", 10)
        self.cell(20, 10, str(registro["id"]), 1, 0, "C")
        self.cell(30, 10, f"{registro['cantidad']:.2f}" + chr(128), 1, 0, "C")
        self.cell(40, 10, registro["categoria"], 1, 0, "C")
        self.cell(50, 10, registro["concepto"], 1, 0, "C")
        self.cell(30, 10, registro["fecha"], 1, 0, "C")
        self.cell(20, 10, registro["tipo"], 1, 1, "C")

@pdf_bp.route('/generarPdf', methods=['POST'])
@token_required
def generarPdf(decoded):
    data = request.json
    registros = data.get('registros', [])

    pdf = PDF()
    pdf.add_page()
    
    # Agregar encabezado de la tabla
    pdf.table_header()
    
    # Agregar registros a la tabla
    for registro in registros:
        pdf.add_row(registro)

    # Guardar el PDF
    pdf_path = "reporte_registros.pdf"
    pdf.output(pdf_path)

     # Devolver el archivo PDF
    return send_file(pdf_path, as_attachment=True)
