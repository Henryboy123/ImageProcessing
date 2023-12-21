import Letter
import cv2
import numpy as np
from matplotlib import pyplot as plt


def findCorners(bound):
    c1 = [bound[3][0],bound[0][1]]
    c2 = [bound[1][0],bound[0][1]]
    c3 = [bound[1][0],bound[2][1]]
    c4 = [bound[3][0],bound[2][1]]
    return [c1,c2,c3,c4]

def findThresh(data):
    Binsize = 50
    density,bds = np.histogram(data,bins=Binsize)
    norm_dens = (density)/float(sum(density))
    cum_dist = norm_dens.cumsum()
    fn_min = np.inf
    thresh = -1
    bounds = range(1,Binsize)

    for itr in range(0,Binsize):
        if(itr == Binsize-1):
            break;
        p1 = np.asarray(norm_dens[0:itr])
        p2 = np.asarray(norm_dens[itr+1:])
        q1 = cum_dist[itr]
        q2 = cum_dist[-1] - q1
        b1 = np.asarray(bounds[0:itr])
        b2 = np.asarray(bounds[itr:])
        m1 = np.sum(p1*b1)/q1
        m2 = np.sum(p2*b2)/q2
        v1 = np.sum(((b1-m1)**2)*p1)/q1
        v2 = np.sum(((b2-m2)**2)*p2)/q2

        fn = v1*q1 + v2*q2
        if fn < fn_min:
            fn_min = fn
            thresh = itr

    return thresh,bds[thresh]

def dist(P1,P2):
    return np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)

def mergeBoxes(c1,c2):
    newRect = []
    cx = min(c1[0][0],c2[0][0])
    cy = min(c1[0][1],c2[0][1])

    newRect.append([cx,cy])

    cx = max(c1[1][0],c2[1][0])
    cy = min(c1[1][1],c2[1][1])

    newRect.append([cx,cy])

    cx = max(c1[2][0],c2[2][0])
    cy = max(c1[2][1],c2[2][1])

    newRect.append([cx,cy])

    cx = min(c1[3][0],c2[3][0])
    cy = max(c1[3][1],c2[3][1])

    newRect.append([cx,cy])

    return newRect

def findCenterCoor(c1):
    width = abs(c1[0][0]-c1[1][0])
    height = abs(c1[0][1]-c1[3][1])
    return([c1[0][0]+(width/2.0), c1[0][1]+(height/2.0)])

def findSlope(p1,p2):
    if(p1[0]-p2[0] == 0):
        return np.inf

    return (p1[1]-p2[1])/(p1[0]-p2[0])

def isInside(p1,c1):
    if(p1[0] >= c1[0][0] and p1[0] <= c1[1][0] and p1[1] >= c1[0][1] and p1[1] <= c1[2][1]):
        return True
    else:
        return False

def findArea(c1):
    return abs(c1[0][0]-c1[1][0])*abs(c1[0][1]-c1[3][1])






if __name__ == "__main__":
    bndingBx = []
    corners = []

    img = cv2.imread('MIDTERM/2M113/OOP.MT2.240315.m113.p1 copy.jpg',0)
    blur = cv2.GaussianBlur(img,(5,5),0)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    th3 = cv2.bitwise_not(th3)
    contours, heirar = cv2.findContours(th3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for num in range(0,len(contours)):
        if(heirar[0][num][3] == -1):
            left = tuple(contours[num][contours[num][:,:,0].argmin()][0])
            right = tuple(contours[num][contours[num][:,:,0].argmax()][0])
            top = tuple(contours[num][contours[num][:,:,1].argmin()][0])
            bottom = tuple(contours[num][contours[num][:,:,1].argmax()][0])
            bndingBx.append([top,right,bottom,left])

    for bx in bndingBx:
        corners.append(findCorners(bx))

    imgplot = plt.imshow(img,'gray')

    plt.clf()

    err = 2
    Area = []

    for corner in corners:
        Area.append(findArea(corner))

    Area = np.asarray(Area)
    avgArea = np.mean(Area)
    stdArea = np.std(Area)
    outlier = (Area < avgArea - stdArea)

    for num in range(0,len(outlier)):
        dot = False

        if(outlier[num]):
            black = np.zeros((len(img),len(img[0])),np.uint8)

            cv2.rectangle(black,(corners[num][0][0],corners[num][0][1]),(corners[num][2][0],corners[num][2][1]),(255,255),-1)

            fin =  cv2.bitwise_and(th3,black)

            tempCnt,tempH = cv2.findContours(fin,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in tempCnt:

                rect = cv2.minAreaRect(cnt)
                axis1 = rect[1][0]/2.0
                axis2 = rect[1][1]/2.0

                if(axis1 != 0 and axis2 != 0):
                    ratio = axis1/axis2

                    if ratio > 1.0 - err and ratio < err + 1.0:
                        dot = True
            if dot:
                bestCorner = corners[num]
                closest = np.inf

                for crn in corners:
                    width = abs(crn[0][0]-crn[1][0])
                    height = abs(crn[0][1]-crn[3][1])
                    if(corners[num][0][1] > crn[0][1]):
                        continue
                    elif dist(corners[num][0],crn[0]) < closest and crn != corners[num]:
                        cent = findCenterCoor(crn)
                        bestCorner = crn
                        closest = dist(corners[num][0],crn[0])

                newCorners = mergeBoxes(corners[num],bestCorner)

                corners.append(newCorners)

                corners[num][0][0] = 0
                corners[num][0][1] = 0
                corners[num][1][0] = 0
                corners[num][1][1] = 0
                corners[num][2][0] = 0
                corners[num][2][1] = 0
                corners[num][3][0] = 0
                corners[num][3][1] = 0
                bestCorner[0][0] = 0
                bestCorner[0][1] = 0
                bestCorner[1][0] = 0
                bestCorner[1][1] = 0
                bestCorner[2][0] = 0
                bestCorner[2][1] = 0
                bestCorner[3][0] = 0
                bestCorner[3][1] = 0

    AllLetters = []
    counter = 0

    for bx in corners:
        width = abs(bx[1][0] - bx[0][0])
        height = abs(bx[3][1] - bx[0][1])
        if width*height == 0:
            continue

        plt.plot([bx[0][0],bx[1][0]],[bx[0][1],bx[1][1]],'g-',linewidth=2)
        plt.plot([bx[1][0],bx[2][0]],[bx[1][1],bx[2][1]],'g-',linewidth=2)
        plt.plot([bx[2][0],bx[3][0]],[bx[2][1],bx[3][1]],'g-',linewidth=2)
        plt.plot([bx[3][0],bx[0][0]],[bx[3][1],bx[0][1]],'g-',linewidth=2)

        newLetter = Letter.Letter([bx[0][0],bx[0][1]],[height,width],counter)

        AllLetters.append(newLetter)

        counter+=1

    plt.imshow(th3,'gray')
    plt.show()
    plt.clf()
    AllLetters.sort(key=lambda letter: letter.getY()+letter.getHeight())

    prjYCoords = []

    for letter in AllLetters:
        prjYCoords.append(letter.getY()+letter.getHeight())
        plt.plot([letter.getX(),letter.getX()+letter.getWidth()],[letter.getY(),letter.getY()],'b-',linewidth=2)
        plt.plot([letter.getX()+letter.getWidth(),letter.getX()+letter.getWidth()],[letter.getY(),letter.getY()+letter.getHeight()],'b-',linewidth=2)
        plt.plot([letter.getX()+letter.getWidth(),letter.getX()],[letter.getY()+letter.getHeight(),letter.getY()+letter.getHeight()],'b-',linewidth=2)
        plt.plot([letter.getX(),letter.getX()],[letter.getY()+letter.getHeight(),letter.getY()],'b-',linewidth=2)


    for c in prjYCoords:
        plt.plot(0,c,'ro');

    coorDists = [0]

    for num in range(1,len(prjYCoords)):
        valCur = prjYCoords[num]
        valPast = prjYCoords[num-1]

        coorDists.append(valCur-valPast)

    coorDists_c = []

    for num in range(0,len(coorDists)):
        if(coorDists[num] > 5):
            coorDists_c.append(coorDists[num])

    res,thval = findThresh(coorDists)

    lines = [[AllLetters[0]]]
    IDS = [[AllLetters[0].getID()]]
    count = 0
    start = 0
    end = 0
    asd = 1.0
    meanCoord = float(sum(coorDists))/float(len(coorDists))
    stdCoord = np.std(coorDists)

    plt.clf()
    plt.plot(coorDists)
    plt.plot([0,400],[meanCoord+asd*stdCoord,meanCoord+asd*stdCoord],'r-')
    plt.show()

    medPoints = []

    for num in range(0,len(coorDists)):
        if coorDists[num] > meanCoord + asd*stdCoord and end == 0:
            start = num
        if coorDists[num] > meanCoord + asd*stdCoord and start > 0:
            end = num
            medPoints.append(int(start+(end-start)/2.0))
            start = num

    medPoints.append(start)

    medPoints.insert(0,0)

    lines = []

    for num in range(0,len(medPoints)):
        lines.append(prjYCoords[medPoints[num]])
        print(medPoints[num])
        plt.plot([0,5000],[prjYCoords[medPoints[num]],prjYCoords[medPoints[num]]],'r-')

    imgplot = plt.imshow(img,'gray')

    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()