# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fpdf import FPDF
import pandas as pd
import cv2

sizes = {1: 43, 2: 34, 3: 27, 5: 42}
pad = 5
edge_margin = 10


def save_pdf(pdf, name):
    filename = name + '.pdf'
    pdf.output(filename)


def load_material_file(name):
    dst = "materials/" + name
    mfile = pd.read_csv(dst, sep=',')

    return mfile


def arrange_num_section(pdf, num, size, amount):
    dct = {'1':'I', '2':'II','3':'III','4':'IV'}
    real_size_x, real_size_y = size

    nnum = []
    for c in num:
        if c in dct.keys():
            nnum.append(dct[c])
        else:
            nnum.append(c)
    num = nnum
    # make space after every icon, except the last one
    icons_per_line = int((pdf.w + pad - 2 * edge_margin) / (real_size_x + pad))
    icons_per_col = int((pdf.h + pad - 2 * edge_margin) / (real_size_y + pad - 1))

    pdf.add_font('hilda', '', '/usr/share/fonts/truetype/fonts-yrsa-rasa/Yrsa-SemiBold.ttf')
    pdf.set_font('hilda', '', int((22-icons_per_col)*(7/len(num)))) # můj z prdele vytažený vzorec na velikost fontu
    # odvíjí se od výšky obrázku a délky řetězce

    pdf.add_page()

    for i in range(amount):
        for j in range(len(num)):
            x_pos = (i % icons_per_line) * (real_size_x + pad) + edge_margin
            y_pos = ( (int(i / icons_per_line) % icons_per_col) * (real_size_y + pad) + edge_margin ) + j*real_size_y/len(num)
            pdf.set_xy(x_pos, y_pos)
            pdf.cell(w=real_size_x, h=real_size_y/len(num), txt=str(num[j]), align='C')


def arrange_section_with_back(pdf, icon, num, size, amount):
    real_size_x = size

    im = cv2.imread(icon)
    ratio = im.shape[0] / im.shape[1]
    real_size_y = real_size_x * ratio

    # make space after every icon, except the last one
    icons_per_line = int((pdf.w + pad - 2 * edge_margin) / (real_size_x + pad))
    icons_per_col = int((pdf.h + pad - 2 * edge_margin) / (real_size_y + pad-1))

    pages = 1
    pdf.add_page()

    for i in range(amount):
        x_pos = (i % icons_per_line) * (real_size_x + pad) + edge_margin
        y_pos = (int(i / icons_per_line) % icons_per_col) * (real_size_y + pad) + edge_margin

        if ((i) % (icons_per_line * icons_per_col) == 0 and i != 0):
            pdf.add_page()
            pages += 1

        pdf.image(icon, x=x_pos, y=y_pos, w=real_size_x)

        if ((i + 1) % (icons_per_line * icons_per_col) == 0 and i != 0):
            arrange_num_section(pdf, num, (real_size_x, real_size_y), icons_per_line * icons_per_col)

            pages += 1

    # how many icons are on last uncompleted page
    last_page = amount % (icons_per_col * icons_per_line)
    if last_page != 0:
        arrange_num_section(pdf, num, (real_size_x, real_size_y), last_page)


def arrange_all(pdf, mfile):
    for _, row in mfile.iterrows():
        icon = row.icon
        size = row["size"]
        amount = row.amount
        otherside_num = row.otherside_num
        arrange_section_with_back(pdf, icon, otherside_num, size, amount)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create FPDF object
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(False)
    material_file = load_material_file("metagame-mece.csv")

    arrange_all(pdf, material_file)

    save_pdf(pdf, 'metagame2022')
