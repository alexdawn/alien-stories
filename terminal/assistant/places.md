start list need a way of working on region of space ownership, remoteness

when plotting route from a to b check if it goes close to another system
https://forum.unity.com/threads/how-do-i-find-the-closest-point-on-a-line.340058/

pregen places should have some of the following attributes:

'systems': {
    'id': {
        'name': '',
        'sector': '',
        'region': '',
        'affiliation': '',
        'stars': [{
            'name': '',
            'type': '',
            'brightness': '',
            'colour': ''
        }]
        'planets': [
            {
                'name': '',
                'designation': '',
                'type': 'terrestrial|gas|ice|belt',
                'size': '',
                'atmosphere': '',
                'temperature': '',
                'hydrosphere': '',
                'feature': '',
                'colonies': [{
                    'name': '',
                    'age': '',
                    'size': '',
                    'description/history': '',
                    'mission': '',
                    'factions': '',
                    'sponsor': '',
                    'jobs': '',
                    'event': ''
                }],
                'orbital_objects': []
                'moons': [{if gas giant like planet}]
            }
        ]
    }
}
