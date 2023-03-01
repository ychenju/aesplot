# !/usr/bin/env python3
# -*- coding: utf-8 -*-

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

DATA_LANDPROP_30x15 = {
	'H00V0': 0.0000,	'H00V1': 0.0001,	'H00V2': 0.0003,	'H00V3': 0.0004,	'H00V4': 0.0000,	'H00V5': 0.0032,	
	'H00V6': 0.0000,	'H00V7': 0.0459,	'H00V8': 0.3875,	'H01V0': 0.0000,	'H01V1': 0.0000,	'H01V2': 0.0002,	
	'H01V3': 0.0001,	'H01V4': 0.0000,	'H01V5': 0.0000,	'H01V6': 0.0720,	'H01V7': 0.3106,	'H01V8': 0.6541,	
	'H02V0': 0.0000,	'H02V1': 0.0000,	'H02V2': 0.0000,	'H02V3': 0.0011,	'H02V4': 0.0047,	'H02V5': 0.3681,	
	'H02V6': 0.9546,	'H02V7': 0.9000,	'H02V8': 0.6877,	'H03V0': 0.1368,	'H03V1': 0.3647,	'H03V2': 0.3648,	
	'H03V3': 0.6240,	'H03V4': 0.4753,	'H03V5': 0.1017,	'H03V6': 0.4498,	'H03V7': 0.6647,	'H03V8': 0.3947,	
	'H04V0': 0.0036,	'H04V1': 0.1017,	'H04V2': 0.5356,	'H04V3': 0.7057,	'H04V4': 0.1272,	'H04V5': 0.0000,	
	'H04V6': 0.0000,	'H04V7': 0.0556,	'H04V8': 0.5822,	'H05V0': 0.0001,	'H05V1': 0.0000,	'H05V2': 0.0000,	
	'H05V3': 0.0000,	'H05V4': 0.3065,	'H05V5': 0.5033,	'H05V6': 0.2339,	'H05V7': 0.1092,	'H05V8': 0.1477,	
	'H06V0': 0.0000,	'H06V1': 0.0986,	'H06V2': 0.5284,	'H06V3': 0.5876,	'H06V4': 0.8779,	'H06V5': 0.9999,	
	'H06V6': 0.4982,	'H06V7': 0.7436,	'H06V8': 0.3655,	'H07V0': 0.0002,	'H07V1': 0.0015,	'H07V2': 0.2746,	
	'H07V3': 0.3321,	'H07V4': 0.5712,	'H07V5': 0.7879,	'H07V6': 0.7694,	'H07V7': 0.9397,	'H07V8': 0.5448,	
	'H08V0': 0.0020,	'H08V1': 0.0000,	'H08V2': 0.0000,	'H08V3': 0.0000,	'H08V4': 0.0723,	'H08V5': 0.6421,	
	'H08V6': 0.9885,	'H08V7': 0.9750,	'H08V8': 0.7620,	'H09V0': 0.0000,	'H09V1': 0.0468,	'H09V2': 0.1206,	
	'H09V3': 0.1350,	'H09V4': 0.2510,	'H09V5': 0.7099,	'H09V6': 0.9808,	'H09V7': 0.9787,	'H09V8': 0.9586,	
	'H10V0': 0.0000,	'H10V1': 0.3315,	'H10V2': 0.8958,	'H10V3': 0.2522,	'H10V4': 0.0475,	'H10V5': 0.0307,	
	'H10V6': 0.2664,	'H10V7': 0.6756,	'H10V8': 0.8092,	'H11V0': 0.0121,	'H11V1': 0.0764,	'H11V2': 0.0542,	
	'H11V3': 0.0151,	'H11V4': 0.0001,	'H11V5': 0.0000,	'H11V6': 0.0000,	'H11V7': 0.0920,	'H11V8': 0.5856,	
}	

DATA_LANDPROP_15x15 = {
	'H00V0': 0.0000,	'H00V1': 0.0002,	'H00V2': 0.0004,	'H00V3': 0.0008,	'H00V4': 0.0000,	'H00V5': 0.0000,	
	'H00V6': 0.0000,	'H00V7': 0.0046,	'H00V8': 0.1328,	'H01V0': 0.0000,	'H01V1': 0.0000,	'H01V2': 0.0002,	
	'H01V3': 0.0000,	'H01V4': 0.0000,	'H01V5': 0.0063,	'H01V6': 0.0000,	'H01V7': 0.0872,	'H01V8': 0.6422,	
	'H02V0': 0.0000,	'H02V1': 0.0000,	'H02V2': 0.0004,	'H02V3': 0.0003,	'H02V4': 0.0000,	'H02V5': 0.0000,	
	'H02V6': 0.0000,	'H02V7': 0.0291,	'H02V8': 0.6315,	'H03V0': 0.0000,	'H03V1': 0.0000,	'H03V2': 0.0000,	
	'H03V3': 0.0000,	'H03V4': 0.0000,	'H03V5': 0.0000,	'H03V6': 0.1440,	'H03V7': 0.5921,	'H03V8': 0.6767,	
	'H04V0': 0.0000,	'H04V1': 0.0000,	'H04V2': 0.0000,	'H04V3': 0.0000,	'H04V4': 0.0000,	'H04V5': 0.1859,	
	'H04V6': 0.9205,	'H04V7': 0.9599,	'H04V8': 0.7396,	'H05V0': 0.0000,	'H05V1': 0.0000,	'H05V2': 0.0000,	
	'H05V3': 0.0022,	'H05V4': 0.0094,	'H05V5': 0.5504,	'H05V6': 0.9887,	'H05V7': 0.8401,	'H05V8': 0.6358,	
	'H06V0': 0.0049,	'H06V1': 0.0001,	'H06V2': 0.0003,	'H06V3': 0.2635,	'H06V4': 0.2412,	'H06V5': 0.1668,	
	'H06V6': 0.7981,	'H06V7': 0.5929,	'H06V8': 0.4483,	'H07V0': 0.2688,	'H07V1': 0.7293,	'H07V2': 0.7293,	
	'H07V3': 0.9845,	'H07V4': 0.7095,	'H07V5': 0.0365,	'H07V6': 0.1016,	'H07V7': 0.7365,	'H07V8': 0.3411,	
	'H08V0': 0.0050,	'H08V1': 0.2033,	'H08V2': 0.8927,	'H08V3': 0.9661,	'H08V4': 0.2545,	'H08V5': 0.0000,	
	'H08V6': 0.0000,	'H08V7': 0.1110,	'H08V8': 0.5002,	'H09V0': 0.0022,	'H09V1': 0.0000,	'H09V2': 0.1784,	
	'H09V3': 0.4453,	'H09V4': 0.0000,	'H09V5': 0.0000,	'H09V6': 0.0001,	'H09V7': 0.0002,	'H09V8': 0.6641,	
	'H10V0': 0.0001,	'H10V1': 0.0000,	'H10V2': 0.0000,	'H10V3': 0.0000,	'H10V4': 0.0242,	'H10V5': 0.0582,	
	'H10V6': 0.0014,	'H10V7': 0.0000,	'H10V8': 0.2855,	'H11V0': 0.0000,	'H11V1': 0.0001,	'H11V2': 0.0001,	
	'H11V3': 0.0000,	'H11V4': 0.5888,	'H11V5': 0.9483,	'H11V6': 0.4663,	'H11V7': 0.2184,	'H11V8': 0.0100,	
	'H12V0': 0.0000,	'H12V1': 0.0000,	'H12V2': 0.0815,	'H12V3': 0.1924,	'H12V4': 0.7591,	'H12V5': 0.9999,	
	'H12V6': 0.5525,	'H12V7': 0.6493,	'H12V8': 0.1848,	'H13V0': 0.0000,	'H13V1': 0.1972,	'H13V2': 0.9753,	
	'H13V3': 0.9828,	'H13V4': 0.9967,	'H13V5': 0.9999,	'H13V6': 0.4438,	'H13V7': 0.8378,	'H13V8': 0.5462,	
	'H14V0': 0.0001,	'H14V1': 0.0030,	'H14V2': 0.3847,	'H14V3': 0.6426,	'H14V4': 0.9508,	'H14V5': 0.8319,	
	'H14V6': 0.7103,	'H14V7': 0.9389,	'H14V8': 0.4721,	'H15V0': 0.0003,	'H15V1': 0.0000,	'H15V2': 0.1645,	
	'H15V3': 0.0217,	'H15V4': 0.1915,	'H15V5': 0.7439,	'H15V6': 0.8284,	'H15V7': 0.9404,	'H15V8': 0.6175,	
	'H16V0': 0.0039,	'H16V1': 0.0000,	'H16V2': 0.0000,	'H16V3': 0.0000,	'H16V4': 0.0038,	'H16V5': 0.4751,	
	'H16V6': 0.9920,	'H16V7': 0.9720,	'H16V8': 0.6695,	'H17V0': 0.0000,	'H17V1': 0.0000,	'H17V2': 0.0000,	
	'H17V3': 0.0000,	'H17V4': 0.1407,	'H17V5': 0.8091,	'H17V6': 0.9850,	'H17V7': 0.9780,	'H17V8': 0.8544,	
	'H18V0': 0.0000,	'H18V1': 0.0000,	'H18V2': 0.0000,	'H18V3': 0.0760,	'H18V4': 0.2438,	'H18V5': 0.8536,	
	'H18V6': 0.9919,	'H18V7': 0.9817,	'H18V8': 0.9847,	'H19V0': 0.0000,	'H19V1': 0.0937,	'H19V2': 0.2412,	
	'H19V3': 0.1939,	'H19V4': 0.2582,	'H19V5': 0.5662,	'H19V6': 0.9697,	'H19V7': 0.9758,	'H19V8': 0.9326,	
	'H20V0': 0.0000,	'H20V1': 0.1702,	'H20V2': 0.9337,	'H20V3': 0.1966,	'H20V4': 0.0948,	'H20V5': 0.0611,	
	'H20V6': 0.4031,	'H20V7': 0.9901,	'H20V8': 0.8116,	'H21V0': 0.0000,	'H21V1': 0.4928,	'H21V2': 0.8578,	
	'H21V3': 0.3077,	'H21V4': 0.0002,	'H21V5': 0.0002,	'H21V6': 0.1296,	'H21V7': 0.3612,	'H21V8': 0.8069,	
	'H22V0': 0.0001,	'H22V1': 0.0496,	'H22V2': 0.0926,	'H22V3': 0.0293,	'H22V4': 0.0001,	'H22V5': 0.0000,	
	'H22V6': 0.0000,	'H22V7': 0.1817,	'H22V8': 0.6333,	'H23V0': 0.0242,	'H23V1': 0.1031,	'H23V2': 0.0159,	
	'H23V3': 0.0009,	'H23V4': 0.0000,	'H23V5': 0.0000,	'H23V6': 0.0000,	'H23V7': 0.0024,	'H23V8': 0.5379,	
}