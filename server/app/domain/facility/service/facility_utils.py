def get_measurement_code(facility_name):
    mapping = {
        'F1492': 'MASS01',
        'F1494': 'MASS02',
        'F1495': 'MASS04',
        'F1493': 'MASS05',
        'F1500': 'MASS06',
        'F1496': 'MASS07',
        'F1497': 'MASS08',
        'F1498': 'MASS09',
        'F1502': 'MASS10',
        'F1503': 'MASS11',
        'F1501': 'MASS12',
        'F1504': 'MASS13',
        'F1505': 'MASS14',
        'F1507': 'MASS18',
        'F1508': 'MASS22',
    }

    return mapping.get(facility_name, "unknown")
