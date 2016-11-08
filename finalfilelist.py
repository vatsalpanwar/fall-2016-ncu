
def finalfilelist(path):
    import os
    os.chdir(path) # Change Directory
    nowpath = os.getcwd()
    filenamelist = filter(lambda x: x.startswith('ktwo'), os.listdir(nowpath))
    writelist = [ i +'\n' for i in filenamelist]
    with open('list.txt','w') as f:
        map( f.write , writelist)
    f.close()                                       #making the folder list

    Q10up = 'list.txt'
    Q10_file = file(Q10up).readlines()

    ktwoID = []
    ktwofilelist = []

    ktwo_detID = []
    ktwo_detfilelist = []

    for i in Q10_file:
        pathn = i.replace('\n','')
        os.chdir(path + "/%s"%pathn)

        foldername = i.strip().split(' ')
        folderlistfile = '%s_list.txt' %foldername[0]


        #1 Read names of all files ending with .fits
        nowpath = os.getcwd()
        filenamelist = filter(lambda x: x.endswith('.fits'), os.listdir(nowpath))

        #1.5 Write Raw data file into txt list (.fits)
        writelist = [ i +'\n' for i in filenamelist]
        with open('%s_Fits_list.txt' %foldername[0],'w') as f:
            map(f.write , writelist)

        #2 Read needed file data
        Kepler = '%s_Fits_list.txt' %foldername[0]
        LC_file= file(Kepler).readlines()



        for j in LC_file:
            if(j.startswith('ktwo')):
                a = re.findall('\d+', j)
                ktwoID.append(a[0])
                ktwofilelist.append(j)

            elif(j.startswith('EPIC')):
                a = re.findall('\d+', j)
                ktwo_detID.append(a[0])
                ktwo_detfilelist.append(j)

    com_ID =  [i for i in set(ktwoID) & set(ktwo_detID)]      #list of IDs common to both original and detrended list of files-
                                                              #essentially the ones that have to be analysed




    #Make a list of tuples containing names of common files from both folder

    ktwofilelist = zip([np.float(k) for k in ktwoID],ktwofilelist)
    ktwo_detfilelist = zip([np.float(l) for l in ktwo_detID],ktwo_detfilelist)


    ktwofilelist.sort(key=lambda x: x[0])
    ktwo_detfilelist.sort(key=lambda x: x[0])

    print len(ktwofilelist)
    print len(ktwo_detfilelist)

    comlist = zip([k[1] for k in ktwofilelist],[k[1] for k in ktwo_detfilelist])

    return comlist
