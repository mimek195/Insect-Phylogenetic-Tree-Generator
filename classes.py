from os import path, system, name
from sys import path as pa


def clear():
    if name == 'nt':
        x = system('cls')
    else:
        x = system('clear')


class Taxon:

    def __init__(self, taxon_name, taxon_scientific_name, taxon_characteristics, super_taxon=None, sub_taxons=None):
        self.taxon_name = taxon_name
        self.taxon_scientific_name = taxon_scientific_name
        self.taxon_characteristics = taxon_characteristics
        self.super_taxon = super_taxon
        if sub_taxons is None:
            self.sub_taxon = []
        else:
            self.sub_taxon = sub_taxons
        if self.super_taxon is not None:
            self.super_taxon.sub_taxon.append(self)

    def add_argument(self, text):
        while True:
            input_text = input(text)
            clear()
            if any('|' == cha for cha in input_text):
                print("Forbidden symbol '|' detected")
            else:
                return input_text


class Insect(Taxon):

    def __init__(self, name, latin_name, family, legs, antenna, wings, thorax, abdomen, mouthparts, diet):
        Taxon.__init__(self, name, latin_name, '', family)
        self.legs = legs
        self.antenna = antenna
        self.wings = wings
        self.thorax = thorax
        self.abdomen = abdomen
        self.mouthparts = mouthparts
        self.diet = diet


class Database:

    def __init__(self, taxon_list=[Taxon('Arthropod', 'Arthropoda', 'classification_characteristics', sub_taxons=[])]):
        self.taxon_list = taxon_list

    def read_file(self, file):
        if len(self.taxon_list) > 1:
            self.taxon_list = [Taxon('Arthropod', 'Arthropoda', 'classification_characteristics', sub_taxons=[])]
        working_file = file.read().splitlines()
        for line in working_file:
            split_line = line.split('|')
            if len(split_line) >= 7:
                for searching_super_taxons in self.taxon_list:
                    if split_line[2] == searching_super_taxons.taxon_scientific_name:
                        new_classification = Insect(split_line[0], split_line[1], searching_super_taxons, split_line[3],
                                                    split_line[4], split_line[5], split_line[6], split_line[7],
                                                    split_line[8], split_line[9])
                        self.taxon_list.append(new_classification)
                        break
            else:
                for searching_super_taxons in self.taxon_list:
                    if split_line[3] == searching_super_taxons.taxon_scientific_name:
                        new_classification = Taxon(split_line[0], split_line[1], split_line[2], searching_super_taxons)
                        self.taxon_list.append(new_classification)
                        break

    def write_file(self, file, entry):
        if type(entry) is not Insect:
            file.write(entry.taxon_name + '|')
            file.write(entry.taxon_scientific_name + '|')
            file.write(entry.taxon_characteristics + '|')
            file.write(entry.super_taxon.taxon_scientific_name + '\n')
            if len(entry.sub_taxon) != 0:
                for sub in entry.sub_taxon:
                    self.write_file(file, sub)
        else:
            file.write(entry.taxon_name + '|')
            file.write(entry.taxon_scientific_name + '|')
            file.write(entry.super_taxon.taxon_scientific_name + '|')
            file.write(entry.legs + '|')
            file.write(entry.antenna + '|')
            file.write(entry.wings + '|')
            file.write(entry.thorax + '|')
            file.write(entry.abdomen + '|')
            file.write(entry.mouthparts + '|')
            file.write(entry.diet + '\n')

    def read_file_loop(self, file_name):
        try:
            with open(path.join(pa[0], file_name), 'r+') as file:
                self.read_file(file)
        except:
            print("Couldn't load the file")

    def write_file_loop(self, file_name):
        if len(self.taxon_list) > 1:
            try:
                with open(path.join(pa[0], file_name), 'w+') as file:
                    self.write_file(file, self.taxon_list[1])
            except:
                print("Incorrect file name")
        else:
            print("No data")

    def read_or_edit_details(self, taxon_list, mode):
        searching = True
        while searching:
            if mode == 0:
                choice_taxon = input('\nExit [Q] | Choose the taxon which you wish to view: ')
            elif mode == 1:
                choice_taxon = input('\nExit [Q] | Choose the taxon which you wish to edit: ')
            clear()
            if choice_taxon.lower() == 'q':
                return False
            for i in taxon_list[1:]:
                if choice_taxon.lower() == i.taxon_scientific_name.lower():
                    searching = False
                    if type(i) is Insect:
                        print("[0]Common name: " + i.taxon_name, "[-]Scientific name: " + i.taxon_scientific_name,
                              "[-]Belongs to: " + i.super_taxon.taxon_name, "[3]Leg characteristics: " + i.legs,
                              "[4]Antenna characteristics: " + i.antenna,
                              "[5]Wings characteristics: " + i.wings, "[6]Thorax characteristics: " + i.thorax,
                              "[7]Abdomen characteristics: " + i.abdomen,
                              "[8]Mouthparts characteristics: " + i.mouthparts, "[9]Diet characteristics: " + i.diet,
                              "", sep='\n')
                        if mode == 1:
                            editing = True
                            while editing:
                                choice_edit = input('Exit [Q] | Choose what you wish to edit: ')
                                if choice_edit == '1' or choice_edit == '2':
                                    print('Unknown option')
                                elif choice_edit == 'q':
                                    editing = False
                                elif choice_edit == '0':
                                    i.taxon_name = Taxon.add_argument(Taxon, 'Input new common name: ')
                                    editing = False
                                elif choice_edit == '3':
                                    i.legs = Taxon.add_argument(Taxon, 'Input new legs characteristics: ')
                                    editing = False
                                elif choice_edit == '4':
                                    i.antenna = Taxon.add_argument(Taxon, 'Input new antenna characteristics: ')
                                    editing = False
                                elif choice_edit == '5':
                                    i.wings = Taxon.add_argument(Taxon, 'Input new wings characteristics: ')
                                    editing = False
                                elif choice_edit == '6':
                                    i.thorax = Taxon.add_argument(Taxon, 'Input new thorax characteristics: ')
                                    editing = False
                                elif choice_edit == '7':
                                    i.abdomen = Taxon.add_argument(Taxon, 'Input new abdomen characteristics: ')
                                    editing = False
                                elif choice_edit == '8':
                                    i.mouthparts = Taxon.add_argument(Taxon, 'Input new mouthparts characteristics: ')
                                    editing = False
                                elif choice_edit == '9':
                                    i.diet = Taxon.add_argument(Taxon, 'Input new diet characteristics: ')
                                    editing = False
                                else:
                                    print('Unknown option')
                        return True
                    else:
                        print("[0]Common name: " + i.taxon_name, "[-]Scientific name: " + i.taxon_scientific_name,
                              "[2]Taxon characteristics: " + i.taxon_characteristics,
                              "[-]Belongs to: " + i.super_taxon.taxon_name,
                              "", sep='\n')
                        if mode == 1:
                            editing = True
                            while editing:
                                choice_edit = input('Exit [Q] | Choose what you wish to edit: ')
                                if choice_edit == '1' or choice_edit == '3':
                                    print('Unknown option')
                                elif choice_edit.lower() == 'q':
                                    editing = False
                                elif choice_edit == '0':
                                    i.taxon_name = Taxon.add_argument(Taxon, 'Input new common name: ')
                                    editing = False
                                elif choice_edit == '2':
                                    i.taxon_characteristics = Taxon.add_argument(Taxon, 'Input new taxon characteristics: ')
                                    editing = False
                                else:
                                    print('Unknown option')

                        return True

            if searching:
                print('Taxon not found\n')
                return True

    def read_or_edit_details_loop(self, mode):
        if len(self.taxon_list) > 1:
            tree_loop = True
            while tree_loop:
                self.generate_tree(self.taxon_list[1])
                tree_loop = self.read_or_edit_details(self.taxon_list, mode)
        else:
            print("No data")

    def add_entry(self):
        choice = input('Add taxon [1], Add species[2]: ')
        clear()
        if choice == '1':
            searching = True
            while searching:
                super_taxon_name = Taxon.add_argument(Taxon, 'Taxon name of higher rank: ')
                for t in self.taxon_list:
                    if super_taxon_name.lower() == t.taxon_scientific_name.lower():
                        super_taxon = t
                        searching = False
                if searching:
                    searching_2 = True
                    while searching_2:
                        choice_2 = input('Taxon not found. Abort adding new taxon? [T/N]: ')
                        if choice_2.lower() == 't':
                            return "quit"
                        elif choice_2.lower() == 'n':
                            break
            taxon_scientific_name = Taxon.add_argument(Taxon, 'Scientific name: ')
            taxon_name = Taxon.add_argument(Taxon, 'Common name: ')
            taxon_characteristics = Taxon.add_argument(Taxon, 'Characteristics: ')
            self.taxon_list.append(Taxon(taxon_name, taxon_scientific_name, taxon_characteristics, super_taxon))

        elif choice == '2':
            searching = True
            while searching:
                clear()
                family_name = input('Taxon name of higher rank: ')
                for t in self.taxon_list:
                    if family_name.lower() == t.taxon_scientific_name.lower():
                        family = t
                        searching = False
                if searching:
                    searching_2 = True
                    while searching_2:
                        clear()
                        choice_2 = input('Taxon not found. Abort adding new taxon? [T/N]: ')
                        if choice_2.lower() == 't':
                            return "quit"
                        elif choice_2.lower() == 'n':
                            break
            clear()
            species_name = Insect.add_argument(Insect, 'Common name: ')
            species_scientific_name = Insect.add_argument(Insect, 'Scientific name: ')
            legs_characteristics = Insect.add_argument(Insect, 'Legs characteristics: ')
            antenna_characteristics = Insect.add_argument(Insect, 'Antenna characteristics: ')
            wings_characteristics = Insect.add_argument(Insect, 'Wings characteristics: ')
            thorax_characteristics = Insect.add_argument(Insect, 'Thorax characteristics: ')
            abdomen_characteristics = Insect.add_argument(Insect, 'Abdomen characteristics: ')
            mouthparts_characteristics = Insect.add_argument(Insect, 'Mouthparts characteristics: ')
            diet_characteristics = Insect.add_argument(Insect, 'Diet characteristics: ')
            self.taxon_list.append((Insect(species_name, species_scientific_name, family, legs_characteristics,
                                           antenna_characteristics,
                                           wings_characteristics, thorax_characteristics, abdomen_characteristics,
                                           mouthparts_characteristics, diet_characteristics)))

    def generate_tree(self, entry, level=0):
        if type(entry) is Insect:
            print("|   " * level + ">>" + entry.taxon_scientific_name)
        else:
            print("|   " * level + "|>" + entry.taxon_scientific_name)
        for sub in entry.sub_taxon:
            self.generate_tree(sub, level=level + 1)

    def menu_loop(self):
        while True:
            choice = input('Load [1], Add [2], Edit [3], View [4], Save [5], Exit [Q]: ')
            clear()
            if choice == '1':
                self.read_file_loop(input("Input the file name: ") + '.txt')
            elif choice == '2':
                self.add_entry()
            elif choice == '3':
                self.read_or_edit_details_loop(1)
            elif choice == '4':
                self.read_or_edit_details_loop(0)
            elif choice == '5':
                self.write_file_loop(input("Input the file name: ") + '.txt')
            elif choice.lower() == 'q':
                exit()
            else:
                print('Unknown option')
