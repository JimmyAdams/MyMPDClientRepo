#import matplotlib.pyplot as plt
from scipy.fftpack import fft, fft2, ifft
import math
from numpy import floor, zeros, power, real
import scipy.io.wavfile as wav
from scipy import misc, cos, pi
from os import path
from pydub import AudioSegment
import wave
import time

def stereoToMono(audiodata):
    """ Two monos in one file cut to one

        Parameters
        ----------
        audiodata : numpy array
            number of seconds from metadata of file

        Returns
        -------
        numpy array : mono audio file
    """
    d = audiodata.sum(axis=1) / 2
    return d

def getBPM(songName):#song as file
    """ Get BPM of song from wav file

        Parameters
        ----------
        songName : str
            name of Wav file with path for loading

        Returns
        -------
        str : real BPM of song
    """
    # frequencies for bands
    bandlimits = [0, 200, 400, 800, 1600, 3200]
    # maximal frequencie
    maxfreq = 4096
    #reading file, if error -> return 0
    try:
        fs,sig = wav.read(songName)
    except Exception:
        return 0
    signal = wave.open(songName, "rb")
    #control of stereo
    if(signal.getnchannels() == 2):
        x = stereoToMono(sig)
        sig = x

    # get size of 2seconds to sample
    length = (sig.size)
    sample_size = floor(2.2*2*maxfreq)
    start = floor(length/2 - sample_size/2)
    start = int(start)
    stop = floor(length/2 + sample_size/2)
    stop = int(stop)

    short_sample = sig[start:stop]

    # furier transform in short sample of original song
    dft = fft(short_sample)


    n = len(dft)
    bandCount = len(bandlimits)

    valuesA = []
    valuesB = []

    for i in range(0, bandCount-1): # differ signal to bands
        valuesA.append(int(floor(bandlimits[i]/maxfreq*n/2)+1))
        valuesB.append(int(floor(bandlimits[i+1]/maxfreq*n/2)))

    valuesB.append(int(floor(n/2)))
    valuesA.append(int(floor(bandlimits[bandCount-1]/maxfreq*n/2)+1))

    output = zeros((n,bandCount),dtype=complex)

    for a in range(0, bandCount): #getting to matrix
        output[valuesA[a]:valuesB[a], a] = dft[valuesA[a]:valuesB[a]]
        output[n+1-valuesB[a]:n+1-valuesA[a],a] = dft[n+1-valuesB[a]:n+1-valuesA[a]]

    output[0][0] = 0

    """
        Hann window
        smoothing signal, get rid of zeros
        used formula raised cosine
    """
    winLength = 0.2
    hanLength = winLength*2*maxfreq;
    hanLength = int(hanLength)

    hann = zeros((n,1),dtype=complex)

    for a in range(0, hanLength-1): # application of Hanning window
        val = (cos(a*pi/hanLength/2))
        hann[a] = power(val, 2)

    funcW = zeros((n,bandCount),dtype=complex) # convert bands to time part
    for i in range(0, bandCount):
        funcW[:,i] = real(ifft(output[:,i]))

    freq = zeros((n,bandCount),dtype=complex)
    for i in range(0, bandCount-1): #getting absulte value from negative numbers
        for j in range(0, n):
            if(funcW[j,i] < 0):
                funcW[j,i] = - funcW[j,i]
        freq[:,i] = fft(funcW[:,i]) # set values back to frquencies

        # temp variables as matrices
    filtered = zeros((n,bandCount),dtype=complex)
    output2 = zeros((n,bandCount),dtype=complex)

    #correlation of signals
    for i in range(0, bandCount-1):
        filtered[:,i] = freq[:,i]*fft(hann[:,0])
        output2[:,i] = real(ifft(filtered[:,i]))

    # tempo valuaziation
    n = len(output2)
    sig = output2

    output3 = zeros((n,bandCount),dtype=complex)

    for i in range(0, bandCount-1):# get only positive values from sub
        for j in range(4, n-1):
            d = sig[j,i] - sig[j-1,i]

            if d > 0:
                output3[j,i] = d


    sig = output3

    n = len(sig)

    npulses = 3;
    sc = 0.75
    dft = zeros((n,bandCount),dtype=complex)

    for i in range(0, bandCount-1):
        dft[:,i] = fft(sig[:,i])

    maxe = 0
    minbpm =  60 # set minimal bpm for loop
    maxbpm =  180 #max bpm value
    sbpm = 1
    graph = zeros((70,1), float) # graph for print in thes
    index = 0
    for bpm in range(minbpm,maxbpm,2):

        e = 0
        x = 0
        val = 0
        fil = zeros((n,1), float)

        nstep = floor(120/bpm*maxfreq)
        nstep = int(nstep)

        for a in range(0, npulses-1):
            fil[a*nstep+1] = 1

        dftfil = fft(fil) # filter value


        for i in range(0, bandCount-1): # goes on convolution
            val = (abs(dftfil[:,0]*dft[:,i])) # value of energie
            x = power(val, 2)
            e = e + sum(x)

        if e > maxe: # get max energy and save bpm at this energy
            sbpm = bpm*sc
            maxe = e
    return sbpm
