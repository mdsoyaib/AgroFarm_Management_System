import pdfkit

def pdf_creator(url, output):
    # with open('', 'r') as f:
    #     text = f.read()
    # text = text.replace('price_var', str(price)).replace('quantity_var', str(quantity))
    # print(text)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    pdfkit.from_url(url, output + '.pdf', configuration=config)
    # pdfkit.from_file('templates/core/pdf_order_report.html', 'out.pdf', configuration=config)
    # pdfkit

# pdf_creator()