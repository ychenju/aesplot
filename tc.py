import urllib.request as req
import re
import numpy as np
import pandas as pd
from . import basemap as apb
from . import figure as apf
from . import auxf as aux
from typing import Tuple, NoReturn

RAMMB_URL = r'https://rammb-data.cira.colostate.edu/tc_realtime/storm.asp?storm_identifier='
JTWC_URL = r'https://www.metoc.navy.mil/jtwc/products/best-tracks'

JTWC_SCALE_LIST = ('DB','TD','TS','TY','ST','TC')

def get_JTWC_URL(year:int) -> str:
    return JTWC_URL + f'//{year}//{year}s-bwp//bwp{year}.zip'

def rammb(identifer:str, name:str, path:str) -> NoReturn:
    resp = req.urlopen(RAMMB_URL+identifer)
    fcsv = open(path+'\\'+identifer[-4:]+identifer[:4]+name+'.csv', 'w')
    fhtm = open(path+'\\'+'WEBSOURCE_'+identifer[-4:]+identifer[:4]+name+'.html', 'w')

    html = resp.read().decode('UTF-8')
    rec = re.compile(r'\xa9')
    html = re.sub(rec,'',html)

    print(html)
    fhtm.write(html)
    fhtm.close()

    l1 = html.find('Track History')
    r1 = html.rfind('Track History')

    l2 = html[l1:r1].find('<table>')
    r2 = html[l1:r1].rfind('</table>')

    tb = html[l1:r1][l2+1:r2]
    tb = tb.replace('<tr>','')
    tb = tb.replace('</tr>','')

    tb2 = tb.split()
    for i, s in enumerate(tb2):
        tb2[i] = s.strip('<td>')
        tb2[i] = s.strip('</td>')

    tb3 = tb2[tb2.index('Intensity')+1:]

    vd = tb3[-5::-5]
    vt = tb3[-4::-5]
    vlo = tb3[-3::-5]
    vla = tb3[-2::-5]
    vi = tb3[-1::-5]

    print(len(vi))
    data = []
    for i in range(len(vi)):
        d = str()
        d += (vd[i]+'-'+vt[i])
        d += ',\t'
        d += (vlo[i])
        d += ',\t'
        d += (vla[i])
        d += ',\t'
        d += (vi[i])
        d += '\r'
        data.append(d)
    
    r = str()
    for d in data:
        r += d

    fcsv.write(r)
    fcsv.close()

def boundaries(track:np.ndarray) -> dict:
    bdrs = {
        'lat': [max(track[1].min()-5.,-70), min(track[1].max()+5.,70)],
        'long': [np.array([aux.longfix(x) for x in track[2]]).min()-10., np.array([aux.longfix(x) for x in track[2]]).max()+10.],
    }
    return bdrs

def readSimple(path:str) -> np.ndarray:
        dframe = pd.read_csv(path, header=None)
        return np.array(dframe.iloc[:,:]).T
        
def ace(track:np.ndarray) -> float:
    _r = []
    for inten in track[3]:
        if inten > 34:
            _r.append(inten)
    _r2 = np.array(_r)
    return (_r2**2).sum()/1e4

def report(name:str, track:np.ndarray, path:str):
    _r = []
    for inten in track[3]:
        if inten > 34:
            _r.append(inten)
    _r2 = np.array(_r)
    with open(path, 'a') as f:
        f.write(f'{name}\t\t,\t{len(_r2)}\t,\t{max(track[3])}\t,\t{(_r2**2).sum()/1e4}\r')

def coorproc(t, *args:Tuple[int]):
    for arg in args:
        for tl in t:
            _r = list(tl[arg])
            while _r[0] == ' ':
                _r.remove(' ')
            if _r[-1].upper() == 'S' or _r[-1].upper() == 'W':
                _r.insert(0,'-')
            _r.pop()
            _r.insert(-1,'.')
            tl[arg] = ''.join(_r)
    return t

def readjtwc(ipath:str, opath:str):
    with open(ipath, 'r') as trf:
        trc = trf.read()
    trx = np.array(trc.split('\n'))
    trx = [trxl for trxl in trx if trxl.find('BEST') + 1]
    trx = [trxl.split(',') for trxl in trx]
    trx = [trxl[:3] + trxl[6:11] for trxl in trx if int(trxl[11]) < 35]
    trx = [trxl for trxl in trx if not int(trxl[2][-2:])%6]
    trx = [trxl for trxl in trx if max([trxl[-1].find(sx)+1 for sx in JTWC_SCALE_LIST])]
    trx = coorproc(trx, 3, 4)
    trx = [[x if i else trxl[0]+trxl[1]+trxl[2] for i, x in enumerate(trxl[2:])] for trxl in trx]
    _p = pd.DataFrame(trx)
    _p.to_csv(opath,index=None, header=None)

def tctrack(data:np.ndarray) -> Tuple[apb.bluemarble, apf.track]:
    _b = apb.bluemarble(**boundaries(data), res='l').lls(10, c='w')
    _t = apf.track(x=data[2], y=data[1], z=data[3], f=sshws).lformat(c='w')
    return _b, _t

def sshws(inten:int) -> dict:
        if inten < 25:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([128,204,255])/256.}
        elif inten < 34:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([ 94,186,255])/256.}
        elif inten < 64:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([  0,255,244])/256.}
        elif inten < 82:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,255,204])/256.}
        elif inten < 96:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,231,117])/256.}
        elif inten < 112:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,193, 64])/256.}
        elif inten < 137:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255,143, 32])/256.}
        else:
            return {'marker': '.', 'ms': 7.5, 'zorder': 100, 'c': np.array([255, 96, 96])/256.}