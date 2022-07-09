# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fpdf import FPDF
import pandas as pd

sizes = {2:85, 3:60,4: 42, 5: 34, 6: 27, 8: 22,7:16}
pad = 5
edge_margin = 10

def save_pdf(pdf, name):
    filename = name + '.pdf'
    pdf.output(filename)


def load_material_file(name):
    mfile = pd.read_csv(name, sep=',')

    return mfile


def arrange_section(pdf, icon, size, amount):
    real_size = sizes[size]

    # make space after every icon, except the last one
    icons_per_line = int( (pdf.w + pad - 2*edge_margin) / (real_size + pad) )
    icons_per_col = int( (pdf.h + pad - 2*edge_margin) / (real_size + pad) )

    pages = 1
    pdf.add_page()

    for i in range(amount):

        if((i) % (icons_per_line*icons_per_col) == 0 and i != 0):
            pdf.add_page()
            pages+=1

        x_pos = (i % icons_per_line) * (real_size + pad) + edge_margin
        y_pos = ( int(i / icons_per_line) % icons_per_col ) * (real_size + pad) + edge_margin




        pdf.image(icon, x=x_pos, y=y_pos, w=real_size, h=real_size)

def arrange_num_section(pdf, num, size, amount):
    real_size = sizes[size]
    # make space after every icon, except the last one
    icons_per_line = int( (pdf.w + pad - 2 * edge_margin) / (real_size + pad) )
    icons_per_col = int( (pdf.h + pad - 2 * edge_margin) / (real_size + pad) )

    pdf.add_page()

    for i in range(amount):
        x_pos = (i % icons_per_line) * (real_size + pad) + edge_margin
        y_pos = ( int(i / icons_per_line) % icons_per_col ) * (real_size + pad) + edge_margin

        pdf.set_xy(x_pos, y_pos)
        pdf.cell(w=real_size, h=real_size,txt=str(num),align='C')



def arrange_section_with_back(pdf, icon, num, size, amount):
    real_size = sizes[size]
    pdf.add_font('hilda', '', '/usr/share/fonts/truetype/fonts-yrsa-rasa/Yrsa-SemiBold.ttf')
    pdf.set_font('hilda', '', 30 - int(len(num)**1.2)) # můj z prdele vytažený vzorec na velikost fontu
    # TODO: Velikost fontu by mela byt ve dvojici s velikosti obrazku (mela byse tahat taky ze slovniku)
    # TODO: Vlastne by melo zalezet spise na delce slova.

# make space after every icon, except the last one
    icons_per_line = int( (pdf.w + pad - 2*edge_margin) / (real_size + pad) )
    icons_per_col = int( (pdf.h + pad - 2*edge_margin) / (real_size + pad) )

    pages = 1
    pdf.add_page()

    for i in range(amount):
        x_pos = (i % icons_per_line) * (real_size + pad) + edge_margin
        y_pos = ( int(i / icons_per_line) % icons_per_col ) * (real_size + pad) + edge_margin

        if((i) % (icons_per_line*icons_per_col) == 0 and i != 0):
            pdf.add_page()
            pages+=1

        pdf.image(icon, x=x_pos, y=y_pos, w=real_size, h=real_size)

        if((i+1) % (icons_per_line*icons_per_col) == 0 and i != 0):

            arrange_num_section(pdf,num,size,icons_per_line*icons_per_col)

            pages+=1



    # how many icons are on last uncompleted page
    last_page = amount%(icons_per_col*icons_per_line)
    if last_page!=0:
        arrange_num_section(pdf,num,size,last_page)



def arrange_all(pdf, mfile):
    for _, row in mfile.iterrows():
        icon = row.icon
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
    material_file = load_material_file("2022/zdroje/blood-wars.csv")

    arrange_all(pdf, material_file)

    save_pdf(pdf, '2022/generated/blood-wars-2022-final')
