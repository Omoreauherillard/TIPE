# Author : Oscar Moreau--Hérillard
# Date : 06/08/2025
# Version : 1.0




#===========================================| Modules |==============================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys


#=============================================| SNR |===============================================

def Extract(file_name):
    Sample_rate, all_data = wavfile.read(file_name)
    data = all_data.T[0]
    N = len(data) # Number of samples
    Sample_step = 1 / Sample_rate # Step of a sample (in s) 
    time = np.linspace(0, (N-1)*Sample_step, N) # Creation of time axis (in s)
    
    K = 4
    i=0
    while(i<N and abs(data[i])<=K):
        i+=1
    data_signal = data[i: i+int((4/Sample_step))]
    data_noise = data[0: i-1]
    
    """"
    fig, ax = plt.subplots(1,1)
    ax.plot(time, data)
    plt.show()
    """


    return data_signal, data_noise



def Snr(file_name):
    data_signal, data_noise = Extract(file_name)
    Puissance_signal = np.mean(data_signal**2)
    Puissance_noise = np.mean(data_noise**2)
    return Puissance_signal/Puissance_noise, np.max(data_signal), np.max(data_noise)


def Snr_pack(path1, file_name1, nb1, path2, file_name2, nb2):
    Snr_simple = []
    Snr_double = []
    Amplitude_simple = []
    Amplitude_double= []
    noise_simple = []
    noise_double= []
    print("Simple coil processing")
    for i in range (1, nb1+1-20):
        print(i)
        if (i != 27-20 and i!=49-20):
            res, max_s, max_n = Snr(path1+file_name1+str(i+9+20)+").wav")
            if (not (np.isnan(res))): 
                Snr_simple.append(res)
                Amplitude_simple.append(max_s)
                noise_simple.append(max_n)

    print("Double coil processing")
    for i in range(1, nb2+1):
        print(i)
        res, max_s, max_n= Snr(path2+file_name2+str(i+9)+").wav")
        Snr_double.append(res)
        Amplitude_double.append(max_s)
        noise_double.append(max_n)

    Snr_simple = np.array(Snr_simple)
    Snr_double = np.array(Snr_double) 
    
    return Snr_simple, Snr_double


    
def Cleaning(Snr, p):
    print("Variance avant traitement : ", np.var(Snr))
    indices = np.array([], dtype = int)
    E = np.mean(Snr)
    for i in range(0, int(p*len(Snr))):
        j_max = 0
        for j in range(0, len(Snr)):
            if ((not (j in indices)) and abs(Snr[j]-E)>abs(Snr[j_max])-E):
                j_max = j
        indices = np.append(indices, j_max)
    print(indices)
    new_snr = np.delete(Snr, indices)
    print("Variance apres traitement :", np.var(new_snr))
    print("valeurs suppr : ")
    for i in indices:
        print(Snr[i])
    print("Fini")
    return new_snr
    


#=============================================| Test |===============================================





Snr_s, Snr_d = Snr_pack("Signal + Bruit/100 Samples/Simple/", "Enregistrement (", 100, "Signal + Bruit/100 Samples/Double/", "Enregistrement (", 100)

Snr_double = Cleaning(Snr_d, 0.0)
Snr_simple = Cleaning(Snr_s, 0.0)

# 0.1 et 0.05

u_simple = np.std(Snr_simple)/np.sqrt(len(Snr_simple))
u_double = np.std(Snr_double)/np.sqrt(len(Snr_double))

ratio_snr = np.mean(Snr_double)/np.mean(Snr_simple)
u_ratio = ratio_snr*(u_simple/np.mean(Snr_simple) + u_double/np.mean(Snr_double))

print(np.mean(Snr_simple),np.median(Snr_simple), np.std(Snr_simple))
print(np.mean(Snr_double),np.median(Snr_double), np.std(Snr_double))

abscisse_simple = np.array([])
for i in range(0, np.size(Snr_simple)):
    abscisse_simple = np.append(abscisse_simple, i)

abscisse_double = np.array([])
for i in range(0, np.size(Snr_double)):
    abscisse_double = np.append(abscisse_double, i)

mean_simple = np.ones(np.size(Snr_simple))*np.mean(Snr_simple)
mean_double = np.ones(np.size(Snr_double))*np.mean(Snr_double)

fig, (ax1,ax2) = plt.subplots(1, 2)
ax1.plot(abscisse_simple, Snr_simple, linestyle = '', marker = '.', color = '#ff8000')
ax2.plot(abscisse_double, Snr_double, linestyle = '', marker = '.', color = '#ff8000')
ax1.plot(abscisse_simple, mean_simple, color = '#000000')
ax2.plot(abscisse_double, mean_double, color = '#000000')
ax1.set_xlabel('n° échantillon')
ax2.set_xlabel('n° échantillon')
ax1.set_ylabel('SNR')
ax2.set_ylabel('SNR')
plt.show()

print("Rapport des Snr : ", ratio_snr, " +- ", u_ratio)

