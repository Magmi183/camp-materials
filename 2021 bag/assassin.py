# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fpdf import FPDF
import pandas as pd
import random


def save_pdf(pdf, name):
    filename = name + '.pdf'
    pdf.output(filename)


def load_names(name):

    dst = name
    afile = pd.read_csv(dst, sep=',')

    return afile


def read_names(names_file):

    names = names_file.name.tolist()

    names = [str(name) for name in names]

    return names


def create_assassin_cycle(pdf, names):

    row_h = 40
    row_per_page = int(pdf.h / row_h)

    names_len = len(names)
    names_set = set(names)
    names_len_distinct = len(names_set)

    if names_len != names_len_distinct:
        print("!!!!JMENA NEJSOU UNIKATNI!!!!")
        return

    random.shuffle(names)

    for i in range(-1, names_len-1):

        if i != 0 and i%row_per_page==0:
            pdf.add_page()

        killer_name = names[i]
        victim_name = names[i+1]

        #pdf.set_xy(20, 40*i%pdf.h+10)
        #pdf.cell(w=100,txt=killer_name,ln=0)
        #pdf.set_xy(pdf.w-50, 40*i%pdf.h+10)
        #pdf.cell(w=100,txt=victim_name,ln=0)
        print(f"{i}) {killer_name} --> {victim_name}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # create FPDF object
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))

    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(False)
    pdf.set_font('helvetica', 'B', 20)
    pdf.add_page()

    names_file = load_names("names.csv")

    names = read_names(names_file)

    create_assassin_cycle(pdf, names)


    save_pdf(pdf, 'assassin_cycle')
