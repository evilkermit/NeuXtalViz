beamlines = {
    'SNAP': {
        'Name': 'SNAP',
        'InstrumentName': 'SNAP',
        'Facility': 'SNS',
        'Wavelength': [1, 4],
        'Goniometers': ['BL3:Mot:omega,0,1,0,1'],
        'Goniometer': {'BL3:Mot:omega': [0, 1, 0, 1, 0, 360]},
        'Motor': {
            'det_lin1': 0,
            'det_lin2': 0,
            'det_arc1': -75,
            'det_arc2': 105,
        },
        'RawFile': 'nexus/SNAP_{}.nxs.h5',
    },
    'CORELLI': {
        'Name': 'CORELLI',
        'InstrumentName': 'CORELLI',
        'Facility': 'SNS',
        'Wavelength': [0.6, 2.5],
        'Goniometers': [
            'BL9:Mot:Sample:Axis1,0,1,0,1',
            'BL9:Mot:Sample:Axis2,0,1,0,1',
            'BL9:Mot:Sample:Axis3,0,1,0,1',
        ],
        'Goniometer': {
            'BL9:Mot:Sample:Axis1': [0, 1, 0, 1, 0, 0],
            'BL9:Mot:Sample:Axis2': [0, 1, 0, 1, 0, 0],
            'BL9:Mot:Sample:Axis3': [0, 1, 0, 1, 0, 360]
        },
        'RawFile': 'nexus/CORELLI_{}.nxs.h5',
    },
    'TOPAZ': {
        'Name': 'TOPAZ',
        'InstrumentName': 'TOPAZ',
        'Facility': 'SNS',
        'Wavelength': [0.4, 3.5],
        'Goniometers': [
            'BL12:Mot:goniokm:omega,0,1,0,1',
            'BL12:Mot:goniokm:chi,0,0,1,1',
            'BL12:Mot:goniokm:phi,0,1,0,1',
        ],
        'Goniometer': {
            'BL12:Mot:goniokm:omega': [0, 1, 0, 1, 0, 360],
            'BL12:Mot:goniokm:chi': [0, 0, 1, 1, 135, 135],
            'BL12:Mot:goniokm:phi': [0, 1, 0, 1, 0, 360],
        },
        'RawFile': 'nexus/TOPAZ_{}.nxs.h5',
    },
    'MANDI': {
        'Name': 'MANDI',
        'InstrumentName': 'MANDI',
        'Facility': 'SNS',
        'Wavelength': [2, 4],
        'Goniometers': [
            'BL11B:Mot:omega,0,1,0,1',
            'BL11B:Mot:chi,0,0,1,1',
            'BL11B:Mot:phi,0,1,0,1',
        ],
        'Goniometer': {
            'BL11B:Mot:omega': [0, 1, 0, 1, 0, 90],
            'BL11B:Mot:chi': [0, 0, 1, 1, 130, 130],
            'BL11B:Mot:phi': [0, 1, 0, 1, 0, 360],
        },
        'RawFile': 'nexus/MANDI_{}.nxs.h5',
    },
    'WAND²': {
        'Name': 'WAND',
        'InstrumentName': 'HB2C',
        'Facility': 'HFIR',
        'Wavelength': 1.486,
        'Goniometers': ['s1,0,1,0,1'],
        'Goniometer': {
            'HB2C:Mot:sgl': [1, 0, 0, -1, 0, 0],
            'HB2C:Mot:sgu': [0, 0, 1, -1, 0, 0],
            'HB2C:Mot:s1': [0, 1, 0, 1, -180, 180],
        },
        'Motor': {
            'HB2C:Mot:s2.RBV': 30,
            'HB2C:Mot:detz.RBV': 0,
        },
        'RawFile': 'nexus/HB2C_{}.nxs.h5',
    },
    'DEMAND': {
        'Name': 'HB3A',
        'InstrumentName': 'HB3A',
        'Facility': 'HFIR',
        'Wavelength': 1.546,
        'Goniometers': [
            'omega,0,1,0,-1',
            'chi,0,0,1,-1',
            'phi,0,1,0,-1',
        ],
        'Goniometer': {
            'omega': [0, 1, 0, -1],
            'chi': [0, 0, 1, -1],
            'phi': [0, 1, 0, -1],
        },
        'Motor': {
            '2theta': 30,
            'det_trans': 410.38595,
        },
        'RawFile': 'shared/autoreduce/HB3A_exp{:04}_scan{:04}.nxs',
    },
}