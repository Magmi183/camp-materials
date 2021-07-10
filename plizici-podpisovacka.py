from fpdf import FPDF
import random

def save_pdf(pdf, name):
    filename = name + '.pdf'
    pdf.output(filename)

def create_podpisovacka(pdf, amount):


    # Landscape = 250 ideal, Portrait = 180 ideal
    pdf.set_font('helvetica', 'B', 180)

    used_codes = set()
    for gamer in range(amount):

        while True:
            code = random.randint(10000,99999)
            codestr = str(code)
            codeset = set(codestr)
            if len(codeset) >= 4 and code not in used_codes:
                break # chci alespon 4 unikatni cislice v kodu

        used_codes.add(code)

        pdf.add_page()
        pdf.cell(w=0,h=pdf.h-20,txt=str(code),align='C')






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create FPDF object
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(False)

    create_podpisovacka(pdf, 50)

    save_pdf(pdf, 'podpisovacka_P')
