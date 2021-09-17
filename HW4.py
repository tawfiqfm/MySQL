import mysql.connector as mysql


def print_room_details(db, bcode, rnum):
    cursor = db.cursor()
    query = '''SELECT  BNAME, ROOM.BCODE, RNUMBER, CAP, LAYOUT, TYPE, DEPT
               FROM ROOM, BUILDING
               WHERE BUILDING.BCODE = 
               %s AND RNUMBER = %s
               AND room.bcode = building.bcode'''
    cursor.execute(query, (bcode, rnum,))

    for (bname, bcode, rnumber, cap, layout, type, dept,) in cursor:
        print(" bldg       {0:15s} ({1:4s}) "
              "\n rnumber    {2:} "
              "\n cap        {3:} "
              "\n layout     {4:15s} "
              "\n type       {5:2s} "
              "\n dept       {6:15s} "
              .format(bname, bcode, rnumber, cap, layout, type, dept, ))
        print("\n")

    cursor.close()


def print_rooms_with_cap(db, cap_lower, cap_upper,):
    cursor = db.cursor()
    query = '''Select room.bcode, min(cap) , max(cap)
               from room
               where cap > %s and cap < %s
               group by room.bcode'''
    cursor.execute(query, (cap_lower, cap_upper,))
    for (bcode, min, max,) in cursor:
        print("{0:6s}   {1:3d}    {2:3d}".format(bcode, min, max))
    cursor.close()


def update_room_cap(db, bcode, rnum, cap,):
    cursor = db.cursor()
    query = '''update ROOM set cap = %s where bcode = %s and rnumber = %s'''
    cursor.execute(query, (cap, bcode, rnum,))
    print("Room Capacity Updated")
    cursor.close()


def main():
    # please update database, user, and passwd to suit your database
    db = mysql.connect(
        host="localhost",
        database="company",
        user="fmoham3",
        passwd="f123",
        auth_plugin='mysql_native_password'
    )
    print()
    while True:
        s = input("r b:r, c n:m, u b:r:n, q for quit: ")
        if s[0] == 'r':
            room = s[1:].strip().split(":")
            bcode = room[0]
            rnum = room[1]
            print_room_details(db, bcode, rnum)
        elif s[0] == 'c':
            caps = s[1:].strip().split(":")
            cap_lower = int(caps[0])
            cap_upper = int(caps[1])
            print_rooms_with_cap(db, cap_lower, cap_upper)
        elif s[0] == 'u':
            room = s[1:].strip().split(":")
            bcode = room[0]
            rnum = room[1]
            cap = int(room[2])
            update_room_cap(db, bcode, rnum, cap)
        elif s[0] == 'q':
            break
        else:
            print("Invalid option")
    db.close()


main()
