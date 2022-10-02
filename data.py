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