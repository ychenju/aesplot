# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

GC_MEGAN_SPECIES_CONST = {
    'ISOP': {'beta': 0.13, 'ldf': 1.0, 'ct1': 95.0, 'ceo': 2.00, 'anew': 0.05, 'agro': 0.6, 'amat': 1.0, 'aold': 0.90, 'BI': False},
    'MBOX': {'beta': 0.13, 'ldf': 1.0, 'ct1': 95.0, 'ceo': 2.00, 'anew': 0.05, 'agro': 0.6, 'amat': 1.0, 'aold': 0.90, 'BI': False},
    'MYRC': {'beta': 0.10, 'ldf': 0.6, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'SABI': {'beta': 0.10, 'ldf': 0.6, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'APIN': {'beta': 0.10, 'ldf': 0.6, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'LIMO': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'CARE': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'BPIN': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'OCIM': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'OMON': {'beta': 0.10, 'ldf': 0.4, 'ct1': 80.0, 'ceo': 1.83, 'anew': 2.00, 'agro': 1.8, 'amat': 1.0, 'aold': 1.05, 'BI': False},
    'MOH' : {'beta': 0.08, 'ldf': 0.8, 'ct1': 60.0, 'ceo': 1.60, 'anew': 3.50, 'agro': 3.0, 'amat': 1.0, 'aold': 1.20, 'BI': False},
    'ACET': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'EOH' : {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'CH2O': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'ALD2': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'FAXX': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'AAXX': {'beta': 0.13, 'ldf': 0.8, 'ct1': 95.0, 'ceo': 2.00, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': True },
    'C2H4': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'TOLU': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'HCNX': {'beta': 0.10, 'ldf': 0.8, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'PRPE': {'beta': 0.10, 'ldf': 0.2, 'ct1': 80.0, 'ceo': 1.83, 'anew': 1.00, 'agro': 1.0, 'amat': 1.0, 'aold': 1.00, 'BI': False},
    'FARN': {'beta': 0.17, 'ldf': 0.5, 'ct1': 130., 'ceo': 2.37, 'anew': 0.40, 'agro': 0.6, 'amat': 1.0, 'aold': 0.95, 'BI': False},
    'BCAR': {'beta': 0.17, 'ldf': 0.5, 'ct1': 130., 'ceo': 2.37, 'anew': 0.40, 'agro': 0.6, 'amat': 1.0, 'aold': 0.95, 'BI': False},
    'OSQT': {'beta': 0.17, 'ldf': 0.5, 'ct1': 130., 'ceo': 2.37, 'anew': 0.40, 'agro': 0.6, 'amat': 1.0, 'aold': 0.95, 'BI': False},
}

GC_MEGAN_PFT_EF = {
            #EF1    EF2     EF3     EF4     EF5     EF6     EF7     EF8     EF9     EF10    EF11    EF12    EF13    EF14    EF15 
    'OMON': (180.,  180.,   170.,   150.,   150.,   150.,   150.,   150.,   110.,   200.,   110.,   5.,     5.,     5.,     5.  ),
    'MOH' : (900.,  900.,   900.,   500.,   900.,   500.,   900.,   900.,   900.,   900.,   900.,   500.,   500.,   500.,   900.),
    'ACET': (240.,  240.,   240.,   240.,   240.,   240.,   240.,   240.,   240.,   240.,   240.,   80.,    80.,    80.,    80  ),
    'BIDR': (500.,  500.,   500.,   500.,   500.,   500.,   500.,   500.,   500.,   500.,   500.,   80.,    80.,    80.,    80  ),
    'STRS': (300.,  300.,   300.,   300.,   300.,   300.,   300.,   300.,   300.,   300.,   300.,   300.,   300.,   300.,   300 ),
    'OTHR': (140.,  140.,   140.,   140.,   140.,   140.,   140.,   140.,   140.,   140.,   140.,   140.,   140.,   140.,   140 ),
    'APIN': (500.,  500.,   510.,   600.,   400.,   600.,   400.,   400.,   200.,   300.,   200.,   2.,     2.,     2.,     2   ),
    'MYRC': (70.,   70.,    60.,    80.,    30.,    80.,    30.,    30.,    30.,    50.,    30.,    0.3,    0.3,    0.3,    0.3 ),
    'FARN': (40.,   40.,    40.,    60.,    40.,    60.,    40.,    40.,    40.,    40.,    40.,    3.,     3.,     3.,     4   ),
    'BCAR': (80.,   80.,    80.,    60.,    40.,    60.,    40.,    40.,    50.,    50.,    50.,    1.,     1.,     1.,     4   ),
    'OSQT': (120.,  120.,   120.,   120.,   100.,   120.,   100.,   100.,   100.,   100.,   100.,   2.,     2.,     2.,     2   ),
}

GC_MEGAN_EM_FRAC = {
            #EF1    EF2     EF3     EF4     EF5     EF6     EF7     EF8     EF9     EF10    EF11    EF12    EF13    EF14    EF15 
    'ALD2': (0.4,   0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.25,   0.25,   0.25,   0.25),
    'EOH' : (0.4,   0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.4,    0.25,   0.25,   0.25,   0.25),
    'FAXX': (0.06,  0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.15,   0.15,   0.15,   0.15),
    'AAXX': (0.06,  0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.06,   0.15,   0.15,   0.15,   0.15),
    'CH2O': (0.08,  0.08,   0.08,   0.08,   0.08,   0.08,   0.08,   0.08,   0.08,   0.08,   0.08,   0.20,   0.20,   0.20,   0.20),
}

DATA_EMIS_DIFF_20221023 = {
    'GAMMA_A':{
        'AAXX': {3:- 0.52, 9:- 0.64, 27: - 0.64},   'ACET': {3:- 0.52, 9:- 0.64, 27: - 0.64},
        'ALD2': {3:- 0.52, 9:- 0.64, 27: - 0.64},   'APIN': {3: 17.82, 9: 26.64, 27:  42.10},
        'BCAR': {3:-11.50, 9:-16.93, 27: -26.05},   'BPIN': {3: 17.82, 9: 26.64, 27:  42.10},
        'C2H4': {3:- 0.52, 9:- 0.64, 27: - 0.64},   'CARE': {3: 17.82, 9: 26.64, 27:  42.10},
        'CH2O': {3:- 0.52, 9:- 0.64, 27: - 0.64},   'EOH' : {3:- 0.52, 9:- 0.64, 27: - 0.64},
        'FARN': {3:-11.50, 9:-16.93, 27: -26.05},   'FAXX': {3:- 0.52, 9:- 0.64, 27: - 0.64},
        'HCNX': {3:- 0.52, 9:- 0.64, 27: - 0.64},   'ISOP': {3:-16.36, 9:-24.09, 27: -37.07},
        'LIMO': {3: 17.82, 9: 26.64, 27:  42.10},   'MBOX': {3:-16.36, 9:-24.09, 27: -37.07},
        'MOH' : {3: 48.29, 9: 71.78, 27: 112.47},   'MYRC': {3: 17.82, 9: 26.64, 27:  42.10},
        'OCIM': {3: 17.82, 9: 26.64, 27:  42.10},   'OMON': {3: 17.82, 9: 26.64, 27:  42.10},
        'OSQT': {3:-11.50, 9:-16.93, 27: -26.05},   'PRPE': {3:- 0.52, 9:- 0.64, 27: - 0.64},
        'SABI': {3: 17.82, 9: 26.64, 27:  42.10},   'TOLU': {3:- 0.52, 9:- 0.64, 27: - 0.64},
    },
    'GAMMA_LAI':{
        'AAXX': {3:-46.12, 9:-66.03, 27:-86.79 },   'ACET': {3:-48.23, 9:-63.41, 27:-81.06 },
        'ALD2': {3:-46.12, 9:-66.03, 27:-86.79 },   'APIN': {3:-48.23, 9:-63.41, 27:-81.06 },
        'BCAR': {3:-48.23, 9:-63.41, 27:-81.06 },   'BPIN': {3:-48.23, 9:-63.41, 27:-81.06 },
        'C2H4': {3:-48.23, 9:-63.41, 27:-81.06 },   'CARE': {3:-48.23, 9:-63.41, 27:-81.06 },
        'CH2O': {3:-46.12, 9:-66.03, 27:-86.79 },   'EOH' : {3:-46.12, 9:-66.03, 27:-86.79 },
        'FARN': {3:-48.23, 9:-63.41, 27:-81.06 },   'FAXX': {3:-46.12, 9:-66.03, 27:-86.79 },
        'HCNX': {3:-48.23, 9:-63.41, 27:-81.06 },   'ISOP': {3:-48.23, 9:-63.41, 27:-81.06 },
        'LIMO': {3:-48.23, 9:-63.41, 27:-81.06 },   'MBOX': {3:-48.23, 9:-63.41, 27:-81.06 },
        'MOH' : {3:-48.23, 9:-63.41, 27:-81.06 },   'MYRC': {3:-48.23, 9:-63.41, 27:-81.06 },
        'OCIM': {3:-48.23, 9:-63.41, 27:-81.06 },   'OMON': {3:-48.23, 9:-63.41, 27:-81.06 },
        'OSQT': {3:-48.23, 9:-63.41, 27:-81.06 },   'PRPE': {3:-48.23, 9:-63.41, 27:-81.06 },
        'SABI': {3:-48.23, 9:-63.41, 27:-81.06 },   'TOLU': {3:-48.23, 9:-63.41, 27:-81.06 },
    },
    'GAMMA_SM':{
        'AAXX': {3: 0    , 9: 0    , 27: 0     },   'ACET': {3: 0    , 9: 0    , 27: 0     },
        'ALD2': {3: 8.9  , 9: 5.3  , 27: 1.92  },   'APIN': {3: 0    , 9: 0    , 27: 0     },
        'BCAR': {3: 0    , 9: 0    , 27: 0     },   'BPIN': {3: 0    , 9: 0    , 27: 0     },
        'C2H4': {3: 0    , 9: 0    , 27: 0     },   'CARE': {3: 0    , 9: 0    , 27: 0     },
        'CH2O': {3: 0    , 9: 0    , 27: 0     },   'EOH' : {3: 8.9  , 9: 5.3  , 27: 1.92  },
        'FARN': {3: 0    , 9: 0    , 27: 0     },   'FAXX': {3: 0    , 9: 0    , 27: 0     },
        'HCNX': {3: 0    , 9: 0    , 27: 0     },   'ISOP': {3: 0    , 9: 0    , 27: 0     },
        'LIMO': {3: 0    , 9: 0    , 27: 0     },   'MBOX': {3: 0    , 9: 0    , 27: 0     },
        'MOH' : {3: 0    , 9: 0    , 27: 0     },   'MYRC': {3: 0    , 9: 0    , 27: 0     },
        'OCIM': {3: 0    , 9: 0    , 27: 0     },   'OMON': {3: 0    , 9: 0    , 27: 0     },
        'OSQT': {3: 0    , 9: 0    , 27: 0     },   'PRPE': {3: 0    , 9: 0    , 27: 0     },
        'SABI': {3: 0    , 9: 0    , 27: 0     },   'TOLU': {3: 0    , 9: 0    , 27: 0     },
    },
    'GAMMA_T_LD':{
        'AAXX': {3: 3.42 , 9: 8.99 , 27: 22.36 },   'ACET': {3: 0.81 , 9: 2.09 , 27: 5.24  },
        'ALD2': {3: 3.42 , 9: 8.99 , 27: 22.36 },   'APIN': {3: 2.44 , 9: 6.26 , 27: 15.71 },
        'BCAR': {3: 2.49 , 9: 6.72 , 27: 16.39 },   'BPIN': {3: 0.81 , 9: 2.09 , 27: 5.24  },
        'C2H4': {3: 3.25 , 9: 8.35 , 27: 20.94 },   'CARE': {3: 0.81 , 9: 2.09 , 27: 5.24  },
        'CH2O': {3: 3.42 , 9: 8.99 , 27: 22.36 },   'EOH' : {3: 3.42 , 9: 8.99 , 27: 22.36 },
        'FARN': {3: 2.49 , 9: 6.72 , 27: 16.39 },   'FAXX': {3: 3.42 , 9: 8.99 , 27: 22.36 },
        'HCNX': {3: 3.25 , 9: 8.35 , 27: 20.94 },   'ISOP': {3: 4.27 , 9: 11.23, 27: 27.95 },
        'LIMO': {3: 0.81 , 9: 2.09 , 27: 5.24  },   'MBOX': {3: 4.27 , 9: 11.23, 27: 27.95 },
        'MOH' : {3: 3.11 , 9: 7.61 , 27: 19.15 },   'MYRC': {3: 2.44 , 9: 6.26 , 27: 15.71 },
        'OCIM': {3: 3.25 , 9: 8.35 , 27: 20.94 },   'OMON': {3: 1.62 , 9: 4.17 , 27: 10.47 },
        'OSQT': {3: 2.49 , 9: 6.72 , 27: 16.39 },   'PRPE': {3: 0.81 , 9: 2.09 , 27: 5.24  },
        'SABI': {3: 2.44 , 9: 6.26 , 27: 15.71 },   'TOLU': {3: 3.25 , 9: 8.35 , 27: 20.94 },
    },
    'GAMMA_T_LI':{
        'AAXX': {3: 0.82 , 9: 2.15 , 27: 5.12  },   'ACET': {3: 2.21 , 9: 5.88 , 27: 14.49 },
        'ALD2': {3: 0.82 , 9: 2.15 , 27: 5.12  },   'APIN': {3: 1.10 , 9: 2.94 , 27: 7.25  },
        'BCAR': {3: 3.04 , 9: 7.88 , 27: 17.83 },   'BPIN': {3: 2.21 , 9: 5.88 , 27: 14.49 },
        'C2H4': {3: 0.55 , 9: 1.47 , 27: 3.62  },   'CARE': {3: 2.21 , 9: 5.88 , 27: 14.49 },
        'CH2O': {3: 0.82 , 9: 2.15 , 27: 5.12  },   'EOH' : {3: 0.82 , 9: 2.15 , 27: 5.12  },
        'FARN': {3: 3.04 , 9: 7.88 , 27: 17.83 },   'FAXX': {3: 0.82 , 9: 2.15 , 27: 5.12  },
        'HCNX': {3: 0.55 , 9: 1.47 , 27: 3.62  },   'ISOP': {3: 0    , 9: 0    , 27: 0     },
        'LIMO': {3: 2.21 , 9: 5.88 , 27: 14.49 },   'MBOX': {3: 0    , 9: 0    , 27: 0     },
        'MOH' : {3: 0.39 , 9: 1.05 , 27: 2.65  },   'MYRC': {3: 1.10 , 9: 2.94 , 27: 7.25  },
        'OCIM': {3: 0.55 , 9: 1.47 , 27: 3.62  },   'OMON': {3: 1.65 , 9: 4.51 , 27: 10.87 },
        'OSQT': {3: 3.04 , 9: 7.88 , 27: 17.83 },   'PRPE': {3: 2.21 , 9: 5.88 , 27: 14.49 },
        'SABI': {3: 1.10 , 9: 2.94 , 27: 7.25  },   'TOLU': {3: 0.55 , 9: 1.47 , 27: 3.62  },
    },
}

DATA_EMIS_SIGMA_20221024 = {
    'GAMMA_A':{
        'AAXX': {3:  1.54, 9:  4.54, 27: 10.26 },   'ACET': {3:  1.54, 9:  4.54, 27: 10.26 },
        'ALD2': {3:  1.54, 9:  4.54, 27: 10.26 },   'APIN': {3: 55.31, 9: 67.17, 27: 73.30 },
        'BCAR': {3: 31.22, 9: 37.90, 27: 41.36 },   'BPIN': {3: 55.31, 9: 67.17, 27: 73.30 },
        'C2H4': {3:  1.54, 9:  4.54, 27: 10.26 },   'CARE': {3: 55.31, 9: 67.17, 27: 73.30 },
        'CH2O': {3:  1.54, 9:  4.54, 27: 10.26 },   'EOH' : {3:  1.54, 9:  4.54, 27: 10.26 },
        'FARN': {3: 31.22, 9: 37.90, 27: 41.36 },   'FAXX': {3:  1.54, 9:  4.54, 27: 10.26 },
        'HCNX': {3:  1.54, 9:  4.54, 27: 10.26 },   'ISOP': {3: 41.69, 9: 49.04, 27: 52.15 },
        'LIMO': {3: 55.31, 9: 67.17, 27: 73.30 },   'MBOX': {3: 41.69, 9: 49.04, 27: 52.15 },
        'MOH' : {3:136.75, 9:161.86, 27:174.67 },   'MYRC': {3: 55.31, 9: 67.17, 27: 73.30 },
        'OCIM': {3: 55.31, 9: 67.17, 27: 73.30 },   'OMON': {3: 55.31, 9: 67.17, 27: 73.30 },
        'OSQT': {3: 31.22, 9: 37.90, 27: 41.36 },   'PRPE': {3:  1.54, 9:  4.54, 27: 10.26 },
        'SABI': {3: 55.31, 9: 67.17, 27: 73.30 },   'TOLU': {3:  1.54, 9:  4.54, 27: 10.26 },
    },
    'GAMMA_LAI':{
        'AAXX': {3:110.47, 9:142.61, 27:175.41 },   'ACET': {3:141.26, 9:173.57, 27:198.99 },
        'ALD2': {3:110.47, 9:142.61, 27:175.41 },   'APIN': {3:141.26, 9:173.57, 27:198.99 },
        'BCAR': {3:141.26, 9:173.57, 27:198.99 },   'BPIN': {3:141.26, 9:173.57, 27:198.99 },
        'C2H4': {3:141.26, 9:173.57, 27:198.99 },   'CARE': {3:141.26, 9:173.57, 27:198.99 },
        'CH2O': {3:110.47, 9:142.61, 27:175.41 },   'EOH' : {3:110.47, 9:142.61, 27:175.41 },
        'FARN': {3:141.26, 9:173.57, 27:198.99 },   'FAXX': {3:110.47, 9:142.61, 27:175.41 },
        'HCNX': {3:141.26, 9:173.57, 27:198.99 },   'ISOP': {3:141.26, 9:173.57, 27:198.99 },
        'LIMO': {3:141.26, 9:173.57, 27:198.99 },   'MBOX': {3:141.26, 9:173.57, 27:198.99 },
        'MOH' : {3:141.26, 9:173.57, 27:198.99 },   'MYRC': {3:141.26, 9:173.57, 27:198.99 },
        'OCIM': {3:141.26, 9:173.57, 27:198.99 },   'OMON': {3:141.26, 9:173.57, 27:198.99 },
        'OSQT': {3:141.26, 9:173.57, 27:198.99 },   'PRPE': {3:141.26, 9:173.57, 27:198.99 },
        'SABI': {3:141.26, 9:173.57, 27:198.99 },   'TOLU': {3:141.26, 9:173.57, 27:198.99 },
    },
    'GAMMA_T_LD':{
        'AAXX': {3: 50.76, 9: 91.35, 27: 147.58},   'ACET': {3: 12.58, 9: 22.30, 27: 35.84 },
        'ALD2': {3: 50.76, 9: 91.35, 27: 147.58},   'APIN': {3: 37.74, 9: 66.90, 27: 107.51},
        'BCAR': {3: 33.76, 9: 61.93, 27: 100.77},   'BPIN': {3: 12.58, 9: 22.30, 27: 35.84 },
        'C2H4': {3: 50.32, 9: 89.20, 27: 143.35},   'CARE': {3: 12.58, 9: 22.30, 27: 35.84 },
        'CH2O': {3: 50.76, 9: 91.35, 27: 147.58},   'EOH' : {3: 50.76, 9: 91.35, 27: 147.58},
        'FARN': {3: 33.76, 9: 61.93, 27: 100.77},   'FAXX': {3: 50.76, 9: 91.35, 27: 147.58},
        'HCNX': {3: 50.32, 9: 89.20, 27: 143.35},   'ISOP': {3: 63.45, 9:114.18, 27: 184.47},
        'LIMO': {3: 12.58, 9: 22.30, 27: 35.84 },   'MBOX': {3: 63.45, 9:114.18, 27: 184.47},
        'MOH' : {3: 50.41, 9: 86.74, 27: 137.90},   'MYRC': {3: 37.74, 9: 66.90, 27: 107.51},
        'OCIM': {3: 50.32, 9: 89.20, 27: 143.35},   'OMON': {3: 25.16, 9: 44.60, 27: 71.67 },
        'OSQT': {3: 33.76, 9: 61.93, 27: 100.77},   'PRPE': {3: 12.58, 9: 22.30, 27: 35.84 },
        'SABI': {3: 37.74, 9: 66.90, 27: 107.51},   'TOLU': {3: 50.32, 9: 89.20, 27: 143.35},
    },
    'GAMMA_T_LI':{
        'AAXX': {3: 11.32, 9: 20.70, 27: 33.36 },   'ACET': {3: 38.63, 9: 69.84, 27: 111.52},
        'ALD2': {3: 11.32, 9: 20.70, 27: 33.36 },   'APIN': {3: 19.31, 9: 34.92, 27: 55.76 },
        'BCAR': {3: 33.40, 9: 61.91, 27: 100.80},   'BPIN': {3: 38.63, 9: 69.84, 27: 111.52},
        'C2H4': {3:  9.66, 9: 17.46, 27: 27.88 },   'CARE': {3: 38.63, 9: 69.84, 27: 111.52},
        'CH2O': {3: 11.32, 9: 20.70, 27: 33.36 },   'EOH' : {3: 11.32, 9: 20.70, 27: 33.36 },
        'FARN': {3: 33.40, 9: 61.91, 27: 100.80},   'FAXX': {3: 11.32, 9: 20.70, 27: 33.36 },
        'HCNX': {3:  9.66, 9: 17.46, 27: 27.88 },   'ISOP': {3: 0    , 9: 0    , 27: 0     },
        'LIMO': {3: 38.63, 9: 69.84, 27: 111.52},   'MBOX': {3: 0    , 9: 0    , 27: 0     },
        'MOH' : {3:  8.39, 9: 15.05, 27: 23.87 },   'MYRC': {3: 19.31, 9: 34.92, 27: 55.76 },
        'OCIM': {3:  9.66, 9: 17.46, 27: 27.88 },   'OMON': {3: 28.67, 9: 53.28, 27: 83.64 },
        'OSQT': {3: 33.40, 9: 61.91, 27: 100.80},   'PRPE': {3: 33.40, 9: 69.84, 27: 111.52},
        'SABI': {3: 19.31, 9: 34.92, 27: 55.76 },   'TOLU': {3: 9.66 , 9: 17.46, 27: 27.88 },
    },
}

DATA_22DEC_EFFECTIVE_DOMAINS = {
    (7,1), (7,2), (7,3), (7,6), (7,7), (7,8), (7,9), (7,10),
    (6,2), (6,3), (6,5), (6,6), (6,7), (6,8), (6,9), (6,10),
    (5,2), (5,5), (5,6), (5,7), (5,8), (5,9),
    (4,3), (4,4), (4,5), (4,6), (4,7), (4,9),
    (3,3), (3,4), (3,6), (3,7), (3,10),
    (2,3), (2,4), (2,6), (2,7), (2,10),
    (1,3), (1,10),
}