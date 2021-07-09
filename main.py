# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fpdf import FPDF
import pandas as pd

sizes = {1: 48, 2: 38, 3: 30}
pad = 5

def save_pdf(pdf, name):
    filename = name + '.pdf'
    pdf.output(filename)


def load_material_file(name):
    dst = "materials/" + name
    mfile = pd.read_csv(dst, sep=',')

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

def arrange_num_section(pdf, num, size, amount):
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


        pdf.set_xy(x_pos, y_pos)
        pdf.cell(w=real_size, h=real_size,txt=str(num),align='C')



def arrange_section_with_back(pdf, icon, num, size, amount):
    real_size = sizes[size]
    pdf.set_font('helvetica', 'B', real_size-10)
    # make space after every icon, except the last one
    icons_per_line = int( (pdf.w + pad) / (real_size + pad) )
    icons_per_col = int( (pdf.h + pad) / (real_size + pad) )

    pages = 1
    pdf.add_page()

    for i in range(amount):
        x_pos = (i % icons_per_line) * (real_size + pad)
        y_pos = ( int(i / icons_per_line) % icons_per_col ) * (real_size + pad)

        if(i/icons_per_line>=pages*icons_per_col):

            arrange_num_section(pdf,num,size,icons_per_line*icons_per_col)

            pdf.add_page()
            pages+=1

        pdf.image(icon, x=x_pos, y=y_pos, w=real_size, h=real_size)

    # how many icons are on last uncompleted page
    last_page = amount%(icons_per_col*icons_per_line)
    if last_page!=0:
        arrange_num_section(pdf,num,size,last_page)



def arrange_all(pdf, mfile):
    for _, row in mfile.iterrows():
        icon = "images/" + row.icon
        size = row["size"]
        amount = row.amount


        if 'otherside_num' in row:
            otherside_num = row.otherside_num
            arrange_section_with_back(pdf, icon, otherside_num, size, amount)
        else:
            arrange_section(pdf, icon, size, amount)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create FPDF object
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(False)
    material_file = load_material_file("wicked.csv")

    arrange_all(pdf, material_file)

    save_pdf(pdf, 'test')
