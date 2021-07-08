# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fpdf import FPDF
import pandas as pd

sizes = {1: 50, 2: 39, 3: 31}
pad = 5

def save_pdf(pdf, name):
    filename = name + '.pdf'
    pdf.output(filename)


def load_material_file(name):
    dst = "materials/" + name
    mfile = pd.read_csv(dst, sep=';')

    return mfile


def arrange_section(pdf, icon, size, amount):
    real_size = sizes[size]

    # make space after every icon, except the last one
    icons_per_line = int( (pdf.w + pad) / (real_size + pad) )
    icons_per_col = int( (pdf.h + pad) / (real_size + pad) )

    pages = 1
    pdf.add_page()

    for i in range(amount):
        x_pos = (i % icons_per_line) * (real_size + pad)
        y_pos = ( int(i / icons_per_line) % icons_per_col ) * (real_size + pad)

        if(i/icons_per_line>=pages*icons_per_col):
            pdf.add_page()
            pages+=1


        pdf.image(icon, x=x_pos, y=y_pos, w=real_size, h=real_size)



def arrange_all(pdf, mfile):
    for _, row in mfile.iterrows():
        icon = "images/" + row.icon
        size = row["size"]
        amount = row.amount

        arrange_section(pdf, icon, size, amount)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create FPDF object
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
    pdf = FPDF('P', 'mm', 'Letter')

    material_file = load_material_file("test.csv")

    arrange_all(pdf, material_file)

    save_pdf(pdf, 'test')
