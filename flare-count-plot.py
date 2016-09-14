
kl = file('/home/vatsal/UThesis/K2/data/kepler/ktwo-detrended/ktwo-detrended_Fits_list.txt').readlines()

kli = [i.replace('\n','') for i in kl]
flist = [i+'.rdb' for i in kli]

print flist
print len(flist)


# binsize = 4

# countlist = []

for s in flist:
    
    f = open('/home/vatsal/UThesis/K2/data/kepler/ktwo-detrended/'+s, 'r')  

    d = f.read()
    table = ascii.read(d)
    time_det = np.float64(table['jdb'][1:])
    flux_det = np.float64(table['flux'][1:])
    trend_t = np.float64(table['trendt'][1:])
    trend_p = np.float64(table['trendp'][1:])



    f.close()


    #mask the nan point
    # masknan = -np.isnan(data['flux'])
    # time = data['time'][masknan]
    # flux = data['flux'][masknan]/np.mean(data['flux'][masknan])
    # flux_raw = data['flux'][masknan]/np.mean(data['flux'][masknan])


    mnanm = -np.isnan(flux_det)
    time = time_det[mnanm]
    flux_d = 100.*norm(flux_det[mnanm])-100.*norm(trend_p[mnanm])-100.*norm(trend_t[mnanm])
    flux_r = 100.*norm(flux_det[mnanm])-100.*norm(trend_p[mnanm])-100.*norm(trend_t[mnanm])

    #make empty array as same length as masked flux
    fluxC = np.zeros(len(flux_d))


    #separate gap when time step > 3*time step 
    separationtime = []
    separationtime.append(0)
    for i in range(len(time)-1):
        if time[i+1] - time[i] > 3*(time[2] - time[1]):
            separationtime.append(i)
    separationtime.append(len(time))

    #print separationtime

    #do j times
    for j in range(2):
        for k in range(len(separationtime)-1):
            #take 10 point median and replace it
            for i in range(separationtime[k],separationtime[k+1]):
                if i >= (separationtime[k]+binsize) and i <= (separationtime[k+1]-binsize): 
                    fluxC[i] = np.median(flux_d[i-binsize:i+binsize])
                else :
                    fluxC[i] = flux_d[i]


            #Observed subtract Caculate 

            fluxdiff = flux_d-fluxC

            #move out the peak value > 1 sigma
            maskpeak = fluxdiff > 1.0*fluxdiff.std()

            #if the peak larger than standard deviation then replace the number by 10 point median
            for n, i in enumerate(maskpeak):
                if i:
                    if n >= (separationtime[k]+binsize) and n <= (separationtime[k+1]-binsize):
                        flux_d[n] = np.median(flux_d[n-binsize:n+binsize])
                    else:
                        flux_d[n] = flux_d[n]


    #Plotting the O-C flux

    OminusC = flux_r - fluxC

    #plt.plot(time,flux_raw,'o-')
    #plt.plot(time,fluxC,'o-')
    #     plt.plot(time,OminusC,'.-')
    #     plt.show()

    flare = np.where(OminusC > 3.0*OminusC.std())

    #############

    OminusC = flux_r-fluxC

    flares = np.zeros(len(OminusC))

    flareselection = OminusC > 3.0*OminusC.std()
    #print 3.0*OminusC.std()
    #print 3.0*fluxC.std()

    for n, i in enumerate(flareselection):
        if i:
            if OminusC[n-2] > 0.05*OminusC[n]:
                flares[n-2] = OminusC[n-2]

            if OminusC[n-1] > 0.05*OminusC[n]:
                flares[n-1] = OminusC[n-1]

            flares[n] = OminusC[n]

            if OminusC[n] > OminusC[n+1] or OminusC[n+1] > 0.05*OminusC[n]:
                flares[n+1] = OminusC[n+1]

            if OminusC[n+1] > OminusC[n+2] or OminusC[n+2] > 0.05*OminusC[n]:
                flares[n+2] = OminusC[n+2]

            if OminusC[n+2] > OminusC[n+3] or OminusC[n+3] > 0.05*OminusC[n]:
                flares[n+3] = OminusC[n+3]

            if n+4 < len(flareselection):
                if OminusC[n+3] > OminusC[n+4] or OminusC[n+4] > 0.05*OminusC[n]:
                    flares[n+4] = OminusC[n+4]

            if n+5 < len(flareselection):
                if OminusC[n+4] > OminusC[n+5] or OminusC[n+5] > 0.05*OminusC[n]:
                    flares[n+5] = OminusC[n+5]

    #change all minus value to 0

    for i in range(len(flares)):
        if flares[i] < 0:
            flares[i] = 0

    #remove fake flares

    for i in range(len(flares)-1):        
        if  flares[i] < 3.0*fluxC.std() and \
            flares[i-1] == 0 and \
            flares[i+1] == 0 :
                flares[i] = 0   
        elif \
            flares[i] < 3.0*fluxC.std() and \
            flares[i-2] == 0 and \
            flares[i+1] == 0 :
                flares[i] = 0
        elif \
            flares[i] < 3.0*fluxC.std() and \
            flares[i-1] == 0 and \
            flares[i+2] == 0 :
                flares[i] = 0
    for i in range(len(flares)-1):        
        if  flares[i-1] == 0 and \
            flares[i+1] == 0 :
                flares[i] = 0


    R = 0.569
    Rsun = 6.96e08
    sigma = 5.67e-8
    Teff = 3702
    L = 4*np.pi*(R*Rsun)**2*sigma*(Teff**4)*(10**7)
    #counting flares and find their position
    flarecount = []
    flareposition = []

    def findlocalmax(queue):
        maximum = 0
        for i in range(len(queue)):
            if (queue[i] > maximum):
                maximum = queue[i]
                max_position = len(queue) - i
        return maximum, max_position

    is_zero = 1
    queue = []

    for i in range(len(flares)):
        if ((not is_zero) and flares[i] == 0):
            is_zero = 1

            #print (findlocalmax(queue))
            #find flareposition
            index = i - findlocalmax(queue)[1]
            flareposition.append(index)

            #sum the each point of the data in one flare
            total = sum(queue)
            flarecount.append(np.log10(total*30*60*L))

            queue = []
            continue
        if (is_zero and flares[i] != 0):
            is_zero = 0
        queue.append(flares[i])

    #print flareposition
    #print flarecount
    #print L
    #print len(flareposition)

    tup = (re.findall('\d+', s)[0],len(flareposition))
    countlist.append(tup)
    print s

#     plt.plot(time,flares,'.-')
#     plt.show()

#     plt.plot(time,100.*norm(flux_det[mnanm])-20,'b.-')
#     plt.plot(time,100.*norm(flux_det[mnanm])-100.*norm(trend_p[mnanm]),'k.-')

#     plt.plot(time,flux_d+20,'g.-')


#     plt.show()
    
print countlist
