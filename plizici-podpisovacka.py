from fpdf import FPDF
import random

def save_pdf(pdf, name):
    filename = name + '.pdf'
    pdf.output(filename)

def create_podpisovacka(pdf, amount):


    # Landscape = 250 ideal, Portrait = 180 ideal


    used_codes = set()
    used_small_codes = set()

    for gamer in range(amount):

        gmod3 = gamer % 3

        pdf.set_font('helvetica', '', 180)
        while True:
            code = random.randint(10000,99999)
            small_code = random.randint(1000,9999)
            codestr = str(code)
            smallcodestr = str(small_code)
            codeset = set(codestr)
            smallcodeset = set(smallcodestr)

            if len(codeset) >= 4 and code not in used_codes and small_code not in used_small_codes:
                break # chci alespon 4 unikatni cislice v kodu

        used_codes.add(code)
        used_small_codes.add(small_code)


        if gmod3==0:
            pdf.add_page()

        pdf.set_xy(0,(pdf.h/3)*gmod3)
        pdf.cell(w=0,h=(pdf.h/3),txt=str(code),align='C',ln=2)

        pdf.set_xy(30,(pdf.h/3)*gmod3+20)
        pdf.set_font('helvetica', '', 18)
        pdf.cell(w=0-30,h=30,txt=str(small_code),align='C')






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create FPDF object
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
    pdf = FPDF('L', 'mm', 'A4')
    pdf.set_auto_page_break(False)

    create_podpisovacka(pdf, 51)

    save_pdf(pdf, 'podpisovacka_L')
