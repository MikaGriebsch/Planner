from stundenplan.models import Grade, Subject, Teacher, Room, Lesson, Subject_Grade, Class, Week
from random import randint

globalerStundenplan=[[0,1],[1],[2],[3],[4]],[[5],[6],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]
fehlendeZuweisungen=0


def freierRaum(pTag, pTimeslot): #gibt freien Raum zurück
    global globalerStundenplan
    x = 0
    for i in Room.objects.all():
        isFree = True

        for j in globalerStundenplan[pTag][pTimeslot]:
            if j.room_number == i.room_number:
                isFree = False
                break

        if isFree:
            return i
        
    return None

def freierLehrer(pTag, pTimeslot, pFach): #gibt freien Lehrer zurück
    fachlehrer = []
    global globalerStundenplan

    for i in Teacher.objects.all():
        if i.subject == pFach:
            fachlehrer.append(i)

    for i in fachlehrer():
        isFree = True
        for j in globalerStundenplan[pTag][pTimeslot]:
            if j.teacher == i:
                isFree = False
                break

        if isFree:
            return i
        
    return None

def gueltigeStunde(pTag, pTimeslot, pKontingent, pKlasse): #sucht nach gültiger Stunde
    reihenfolge = []
    x = 0
    for i in pKontingent:
        reihenfolge.append(x)
        x += 1

    for i in reihenfolge: #andersrum als Bjarne
        switchIndex = randint(0, len(reihenfolge) - 1)
        temp = reihenfolge[i]
        reihenfolge[i] = reihenfolge[switchIndex]
        reihenfolge[switchIndex] = temp

    for i in range(len(reihenfolge)):
        template = pKontingent[reihenfolge[i]]

        lehrer = freierLehrer(pTag, pTimeslot, template.subject)
        raum = freierRaum(pTag, pTimeslot)

        if lehrer != None and raum != None:
            pKontingent.pop(reihenfolge[i])
            return Lesson(teacher=lehrer, subject=template.subject, klasse=pKlasse, room_number=raum, weekday=pTag, week_choice=0)
        
    return None

def generate(pKurs):
    bricks = []
    slabs = []
    global globalerStundenplan

    for i in Subject_Grade.objects.filter(grade=pKurs.grade).subject.all():
        uebrigeStunden = i.wochenstunden
        if uebrigeStunden%2 == 1:
            slabs.append(Lesson(subject = i))
            uebrigeStunden -= 1
        for j in range(uebrigeStunden//2):
            bricks.append(Lesson(subject = i))

    for i in range(len(globalerStundenplan)):
        for j in range(len(globalerStundenplan[i])):
            if len(bricks) > 0:
                temp = gueltigeStunde(i, j, bricks, pKurs)
                if temp != None:
                    globalerStundenplan[i][j].append(temp)
                else:
                    global fehlendeZuweisungen
                    fehlendeZuweisungen += 1
            elif len(slabs) > 0:
                temp = gueltigeStunde(i, j, slabs, pKurs)
                if temp != None:
                    globalerStundenplan[i][j].append(temp)
                else:
                    global fehlendeZuweisungen
                    fehlendeZuweisungen += 1
            else:
                break
    
def kursFrei(pKurs, pTag, pStunde):
    global globalerStundenplan
    for i in globalerStundenplan[pTag][pStunde]:
        if i.klasse == pKurs:
            return False
    return True

def stundenFuerKurs(pKurs):
    global globalerStundenplan
    ret = [[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]

    for i in range(len(globalerStundenplan)):
        for j in range(len(globalerStundenplan[i])):
            for k in globalerStundenplan[i][j]:
                if k.klasse == pKurs:
                    ret[i][j].append(k)
    return ret

def getFehlendeZuweisungen():
    global fehlendeZuweisungen
    return fehlendeZuweisungen