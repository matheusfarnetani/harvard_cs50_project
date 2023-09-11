# Populates Database

import genEntry 
from random import randint, choice
from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
from itertools import permutations, product

# Track number of equipments created by 'make_equipments()'
TRACK_EQUIPMENTS = 1

# Track current 'card_id' see create and make registers
TRACK_CARD = 1

def main():

    # Create 'places' and 'equipments' data
    places = create_places()
    print(places)
    equipments = make_equipments(places=places)
    print(equipments)
    global TRACK_EQUIPMENTS
    arduinos = create_arduinos(number_of_arduinos=TRACK_EQUIPMENTS)
    print(arduinos)

    # Create student/collaborator objective
    courses = create_courses(number_of_courses=10)
    work_sectors = create_work_sectors(number_of_sectors=6)

    cards = create_cards(char1="A", char2="C", group1=2, group2=4)
    number_of_cards = len(cards)
    people_per_group = int(number_of_cards / 9)
    student_group = people_per_group * 6
    collaborator_group = people_per_group * 2

    students = create_students(number_of_students=student_group, courses=courses)
    collaborators = create_collaborators(number_of_collaborators=collaborator_group, work_sectors=work_sectors, people_per_group=people_per_group)
    visitants = create_visitants(number_of_visitants=people_per_group)
    
    registers = make_registers(number_of_cards=number_of_cards, days=3, equipments=equipments)
    print(students[-1])
    print(collaborators[-1])
    print(visitants[-1])
    print(registers[-1])
    print(len(registers))


def create_arduinos(number_of_arduinos: int) -> list:
    """Creates one arduino for each equipment."""
    arduinos = list()
    for i in range(number_of_arduinos):
        arduino = dict()
        arduino["description"] = f"Arduino {i + 1}"
        arduino["code_version"] = "0.0.1"
        arduinos.append(arduino)

    return arduinos


def create_cards(char1: str, char2: str, group1: int, group2: int) -> list:
    """Generates all possibilities of strings;\n
        Strings format; 'AA AA AA AA';\n
        from 'A' to 'C'."""

    cards = list()

    # Create list of characters from A to C
    characters = [chr(i) for i in range(ord(char1), ord(char2) + 1)]

    # Create all combinations of the instance in list, in groups of 'repeat'
    combinations = list(product(characters, repeat=group1))

    # Clean combinations
    clean_combinations = [''.join(combination) for combination in combinations]

    # Generate all possible strings in groups
    combined_strings = list(product(clean_combinations, repeat=group2))

    # Clean combinations
    result_strings = [' '.join(combined) for combined in combined_strings]

    number_of_cards = len(result_strings) # 6561
    people_per_group = number_of_cards / 9
    number_of_students = people_per_group * 6
    number_of_collaborators = (people_per_group * 2) + number_of_students

    # Group combinations in 3 options
    for i in range(number_of_cards):
        if i < number_of_students:
            card_type = "student"
        elif i < number_of_collaborators:
            card_type = "collaborator"
        else:
            card_type = "visitant"

        card = dict()
        card["uid"] = result_strings[i]
        card["type"] = card_type
        cards.append(card)

    return cards


def create_collaborators(number_of_collaborators: int, work_sectors: list, people_per_group: int) -> list:
    """Create 'x' collaborators."""
    collaborators = list()
    card_id_start = people_per_group * 6
    for i in range(number_of_collaborators):
        collaborator = dict()
        collaborator["name"] = f"collaborator {i + 1}"
        collaborator["birthday"] = random_date(1960, 2000)
        collaborator["work_sector"] = choice(work_sectors)
        if i < people_per_group:
            collaborator["work_shift_starts"] = time(hour=8, minute=0, second=0)
            collaborator["work_shift_ends"] = time(hour=17, minute=0, second=0)
        else:
            collaborator["work_shift_starts"] = time(hour=14, minute=0, second=0)
            collaborator["work_shift_ends"] = time(hour=23, minute=0, second=0)

        collaborator["card_id"] = i + card_id_start
        collaborators.append(collaborator)

    return collaborators


def create_courses(number_of_courses: int) -> list:
    """Create 'x' courses"""
    courses = list()
    for i in range(number_of_courses):
        courses.append(f"course {i + 1}")
    
    return courses


def create_equipments(number_of_equipments: int, place_id: int, place_name: str) -> list:
    """Create 'x' equipments per place."""
    global TRACK_EQUIPMENTS
    temp_equipments = list()
    for i in range(number_of_equipments):
        equipment = dict()
        equipment["id"] = TRACK_EQUIPMENTS
        TRACK_EQUIPMENTS += 1
        equipment["description"] = f"{place_name} Equipment {i + 1}"
        equipment["eqp_type"] = "walls"
        equipment["date_last_inspection"] = random_date(start_year=2023, end_year=2023)
        equipment["date_next_inspection"] = equipment["date_last_inspection"] + relativedelta(months=6)
        equipment["place_id"] = place_id
        temp_equipments.append(equipment)
    
    return temp_equipments


def make_equipments(places: dict) -> dict():
    equipments = dict()
    equipments["library"] = list()
    equipments["hovet"] = list()
    equipments["entrances"] = list()
    equipments["classes"] = list()
    equipments["work"] = list()

    for key, value in places.items():
        if key == "library":
            equipments["library"].append(create_equipments(number_of_equipments=6, place_id=1, place_name=key))
        elif key == "hovet":
            equipments["hovet"].append(create_equipments(number_of_equipments=3, place_id=2, place_name=key))
        elif key == "entrances":
            for item in value:
                equipments["entrances"].extend(create_equipments(number_of_equipments=5, place_id=item[0], place_name=key))
        elif key == "classes":
            for item in value:
                equipments["classes"].extend(create_equipments(number_of_equipments=1, place_id=item[0], place_name=key))
        elif key == "work":
            for item in value:
                equipments["work"].extend(create_equipments(number_of_equipments=2, place_id=item[0], place_name=key))


    return equipments


def create_places() -> dict:
    """Create dict of places to guide other creations."""
    places = dict()
    places["library"] = (1, "library")
    places["hovet"] = (2, "hovet")
    places["entrances"] = list()
    places["classes"] = list()
    places["work"] = list()
    for i in range(15):
        if i < 3:
            places["entrances"].append((i + 3, f"entrance {i + 1}"))
        elif i < 13:
            places["classes"].append((i + 3, f"class {i - 2}"))
        else:
            places["work"].append((i + 3, f"work {i - 12}"))

    return places


def flatten_dict(dict):
    temp_list = []

    for key in dict:
        if isinstance(dict[key], list):
            temp_list.extend(dict[key])
        elif isinstance(dict[key], tuple):
            temp_list.append(dict[key])
    
    return temp_list


def make_registers(number_of_cards: int, days: int, equipments: dict) -> list:
    """Creates 'x' registers of 'y' cards"""
    registers = list()

    group_of_cards = number_of_cards / 9
    number_of_students = group_of_cards * 6
    half_students = number_of_students / 2
    number_of_collaborators = (group_of_cards * 2) + number_of_students
    half_collaborators = group_of_cards + number_of_students
    half_visitants = number_of_collaborators + (group_of_cards / 2)

    # Create day object
    today = datetime.today()
    register_day = (today - timedelta(days=days)).date()

    # Helpers
    all_equipments = flatten_dict(equipments)
    entrance_visitor = equipments["entrances"][0]["id"]

    for i in range(days):
        for j in range(number_of_cards):
            if j < number_of_students:
                if j < half_students:
                    # Half students (morning)
                    registers.extend(genEntry.register_sm(equipments, all_equipments, register_day, j))
                # Half students (nocturne)
                registers.extend(genEntry.register_sn(equipments, all_equipments, register_day, j))
            elif j < number_of_collaborators:
                if j < half_collaborators:
                    # Half collaborators (monrning)
                    registers.extend(genEntry.register_cm(equipments, register_day, j))
                # Half collaborators (nocturne)
                registers.extend(genEntry.register_cn(equipments, register_day, j))
            elif j < half_visitants:
                # Half visitant (morning)
                registers.extend(genEntry.register_vm(entrance=entrance_visitor, equipments=all_equipments, day=register_day, card_id=j))
            else:
                # Half visitant (nocturne)
                registers.extend(genEntry.register_vn(entrance=entrance_visitor, equipments=all_equipments, day=register_day, card_id=j))
        
        register_day = register_day + timedelta(days=1)

    return registers

def create_students(number_of_students: int, courses: list) -> list:
    """Create 'x' students."""
    students = list()
    for i in range(number_of_students):
        student = dict()
        student["name"] = f"student {i + 1}"
        student["birthday"] = random_date(1980, 2005)
        student["course"] = choice(courses)
        student["course_start"] = date(randint(2019, 2023), 1, 1)
        student["card_id"] = i + 1
        students.append(student)
    
    return students


def create_visitants(number_of_visitants: int) -> list:
    """Create 'x' visitants."""
    visitants = list()
    card_id_starts = number_of_visitants * 8
    for i in range(number_of_visitants):
        visitant = dict()
        visitant["name"] = f"visitant {i + 1}"
        visitant["birthday"] = random_date(1960, 2011)
        visitant["document"] = "valid document"
        visitant["card_id"] = i + card_id_starts
        visitants.append(visitant)
    
    return visitants


def create_work_sectors(number_of_sectors: int) -> list:
    """Creates 'x' sectors."""
    work_sectors = list()
    for i in range(number_of_sectors):
        work_sectors.append(f"sector {i + 1}")
    
    return work_sectors


def random_date(start_year: int, end_year: int) -> date:
    """Generate random birthday between years."""
    random_year = randint(start_year, end_year)
    random_month = randint(1, 12)
    if random_month == 2:
        random_day = randint(1, 28)
    elif random_month in {4, 6, 9, 11}:
        random_day = randint(1, 30)
    else:
        random_day = randint(1, 31)
    
    return date(random_year, random_month, random_day)


if __name__ == "__main__":
    main()