#!/usr/bin/python3

import numpy as np
import sys
import re

def main():
    if len(sys.argv) < 2:
        print('syntax: %s <diff_legendre filelist>' % sys.argv[0])
    data =  np.loadtxt(sys.argv[1])
    nspec = data.shape[0]
    ntbins = data.shape[1]
    print('ntbins = %i\tnspec = %i' % (ntbins,nspec))
    AMP = np.zeros((nspec,len(sys.argv)-1),dtype=float)
    ARG = np.zeros((nspec,len(sys.argv)-1),dtype=float)
    for fname in sys.argv[1:]:
        print('reading file %s' % fname)
        data =  np.loadtxt(fname)
        m = re.search('(\w+/)(.+)_e(\d+)_g(\d+)_l(\d+)_tspan(.+)\.dat',fname)
        path = str(m.group(1))
        filehead = str(m.group(2))
        eind = int(m.group(3))
        gind = int(m.group(4))
        lind = int(m.group(5))
        tspan = float(m.group(6))
        DATA = np.fft.fft(data,axis=1)
        AMP[:,eind] = np.abs(DATA[:,2])
        ARG[:,eind] = np.angle(DATA[:,2])
        DATA[:,3:-2] = 0.
        DATA[:,0] = 0
        DATA[:,1] = 0
        DATA[:,-1] = 0
        data = np.fft.ifft(DATA,axis=1).real
        ofname = '%s/processed/%s_e%i_g%i_l%i_tspan%.3f.out'%(path,filehead,eind,gind,lind,tspan)
        np.savetxt(ofname,data,fmt='%.4e')
    AMPout = '%s/processed/%s_g%i_l%i_tspan%.3f.amp'%(path,filehead,gind,lind,tspan)
    ARGout = '%s/processed/%s_g%i_l%i_tspan%.3f.arg'%(path,filehead,gind,lind,tspan)
    np.savetxt(AMPout,AMP,fmt='%.3e')
    np.savetxt(ARGout,ARG,fmt='%.3f')


    return

if __name__ == "__main__":
    main()
