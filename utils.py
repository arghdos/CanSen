import sys, os

def convert_mech(mech_filename, thermo_filename, convert):
    from cantera import ck2cti
    arg = ['--input='+mech_filename]
    if thermo_filename is not None:
        if os.path.isfile(thermo_filename):
            arg.append('--thermo='+thermo_filename)
        else:
            print('Error: Specify proper thermo file')
            sys.exit(1)
    ck2cti.main(arg)
    if convert:
        print('Mechanism conversion successful. Exiting.')
        sys.exit(0)
    else:
        mech_filename = mech_filename[:-4]+'.cti'
        print('Mechanism conversion successful, written to {}'.format(mech_filename))
        return mech_filename

def read_input_file(input_filename):
    from printer import divider
    keywords = {}
    reactants = []
    oxidizer = {}
    fuel = {}
    complete_products = []
    additional_species = {}
    problem_type = False
    unsupported_keys = ['ADAP',  'AEXT',   'AFRA',     'AGGA',  'AGGB',  'AGGD',   'AGGE',   'AGGFD', 'AGGMN', 
                        'AINT',  'AREA',   'AREAQ',    'AROP',  'ASEN',  'ASTEPS', 'AVALUE', 'AVAR',  'BETA', 
                        'BLKEQ', 'BULK',   'CLSC',     'CLSM',  'CNTN',  'CNTT',   'COLR',   'DIST',  'ENRG', 'EPSG', 
                        'EPSR',  'EPSS',   'EPST',     'ETCH',  'GFAC',  'GMHTC',  'HTC',    'HTRN',  'IPSR', 'IRET', 
                        'ISTP',  'KLIM',   'MAXIT',    'MCUT',  'MMASS', 'NADAP',  'NEWRUN', 'NMOM',  'NNEG', 'NOCG', 
                        'NSOL',  'PNDE',   'PPRO',     'PRNT',  'PROE',  'PVFE',   'QFUN',   'QLOS',  'QPRO', 'QRGEQ', 
                        'QRSEQ', 'RELAXC', 'ROP',      'RSTR',  'SCLM',  'SCLS',   'SCOR',   'SENG',  'SENT', 'SFAC', 
                        'SIZE',  'SOLUTION_TECHNIQUE', 'SSTT',  'SURF',  'TAMB',   'TGIV',   'TIFP',  'TRAN', 'TRES', 
                        'TRST',  'TSRF',   'TSTR',     'UIGN',  'USET',  'WENG',   'XMLI',
                        ]
    with open(input_filename) as input_file:
        print(divider)
        print('Keyword Input:\n')
        for line in input_file:
            print(' '*10,line,end='')
            if line.startswith('!') or line.startswith('.') or line.startswith('/'):
                continue
            elif line.upper().startswith('CONV'):
                if problem_type:
                     print('Error: More than one problem type keyword was specified.')
                     sys.exit(1)
                else:
                    keywords['problemType'] = 1
                    problem_type = True
            elif line.upper().startswith('CONP'):
                if problem_type:
                    print('Error: More than one problem type keyword was specified.')
                    sys.exit(1)
                else:
                    keywords['problemType'] = 2
                    problem_type = True
            elif line.upper().startswith('VPRO'):
                if problem_type and keywords.get('problemType') != 3:
                    print('Error: More than one problem type keyword was specified.')
                    sys.exit(1)
                elif problem_type and keywords.get('problemType') == 3:
                    vproTime.append(float(line.split()[1]))
                    vproVol.append(float(line.split()[2]))
                else:
                    keywords['problemType'] = 3
                    vproTime = [float(line.split()[1])]
                    vproVol = [float(line.split()[2])]
                    problem_type = True
            elif line.upper().startswith('CONT'):
                if problem_type:
                    print('Error: More than one problem type keyword was specified.')
                    sys.exit(1)
                else:
                    keywords['problemType'] = 4
                    problem_type = True
            elif line.upper().startswith('COTV'):
                if problem_type:
                    print('Error: More than one problem type keyword was specified.')
                    sys.exit(1)
                else:
                    keywords['problemType'] = 5
                    problem_type = True
            elif line.upper().startswith('VTIM'):
                if problem_type:
                    print('Error: More than one problem type keyword was specified.')
                    sys.exit(1)
                else:
                    keywords['problemType'] = 6
                    problem_type = True
            elif line.upper().startswith('TTIM'):
                if problem_type:
                    print('Error: More than one problem type keyword was specified.')
                    sys.exit(1)
                else:
                    keywords['problemType'] = 7
                    problem_type = True
            elif line.upper().startswith('TPRO'):
                if problem_type and keywords.get('problemType') != 8:
                    print('Error: More than one problem type keyword was specified.')
                    sys.exit(1)
                elif problem_type and keywords.get('problemType') == 8:
                    TproTime.append(float(line.split()[1]))
                    TproTemp.append(float(line.split()[2]))
                else:
                    keywords['problemType'] = 8
                    TproTime = [float(line.split()[1])]
                    TproTemp = [float(line.split()[2])]
                    problem_type = True
            elif line.upper().startswith('TEMP'):
                keywords['temperature'] = float(line.split()[1])
            elif line.upper().startswith('REAC'):
                species = line.split()[1]
                molefrac = line.split()[2]
                reactants.append(':'.join([species,molefrac]))
            elif line.upper().startswith('PRES'):
                keywords['pressure'] = float(line.split()[1])
            elif line.upper().startswith('TIME'):
                keywords['endTime'] = float(line.split()[1])
            elif line.upper().startswith('TLIM'):
                keywords['tempLimit'] = float(line.split()[1])
            elif line.upper().startswith('DTIGN'):
                keywords['tempThresh'] = float(line.split()[1])
            elif line.upper().startswith('ATOL'):
                keywords['abstol'] = float(line.split()[1])
            elif line.upper().startswith('RTOL'):
                keywords['reltol'] = float(line.split()[1])
            elif line.upper().startswith('DELT'):
                keywords['prntTimeInt'] = float(line.split()[1])
            elif line.upper().startswith('DTSV'):
                keywords['saveTimeInt'] = float(line.split()[1])
            elif line.upper().startswith('STPT'):
                keywords['maxTimeStep'] = float(line.split()[1])
            elif line.upper().startswith('EQUI'):
                keywords['eqRatio'] = float(line.split()[1])
            elif line.upper().startswith('OXID'):
                species = line.split()[1]
                molefrac = float(line.split()[2])
                oxidizer[species] = molefrac
            elif line.upper().startswith('FUEL'):
                species = line.split()[1]
                molefrac = float(line.split()[2])
                fuel[species] = molefrac
            elif line.upper().startswith('CPROD'):
                species = line.split()[1]
                complete_products.append(species)
            elif line.upper().startswith('ADD'):
                species = line.split()[1]
                molefrac = float(line.split()[2])
                additional_species[species] = molefrac
            elif line.upper().startswith('SENS'):
                keywords['sensitivity'] = True
            elif line.upper().startswith('VOL'):
                keywords['reactorVolume'] = float(line.split()[1])/1.0E6
            elif line.upper().startswith('RTLS'):
                keywords['sensRelTol'] = float(line.split()[1])
            elif line.upper().startswith('ATLS'):
                keywords['sensAbsTol'] = float(line.split()[1])
            elif line.upper()[0:3] in unsupported_keys:
                print('Keyword', line.upper()[0:3], 'is not supported yet',
                      'and has been ignored')
                continue
            elif line.upper() == 'END':
                print('\n')
                break
            else:
                print('Keyword not found',line)
                sys.exit(1)
        print(divider,'\n')
        
    if 'endTime' not in keywords:
        print('Error: End time must be specified with keyword TIME')
        sys.exit(1)
        
    if 'temperature' not in keywords:
        print('Error: Temperature must be specified with keyword TEMP')
        sys.exit(1)
        
    if 'pressure' not in keywords:
        print('Error: Pressure must be specified with keyword PRES')
        sys.exit(1)
        
    if 'problemType' not in keywords:
        print('Error: Problem type must be specified with the problem type keywords')
        sys.exit(1)
    elif keywords.get('problemType') == 3:
        keywords['vproTime'] = vproTime
        keywords['vproVol'] = vproVol
    elif keywords.get('problemType') == 8:
        keywords['TproTime'] = TproTime
        keywords['TproTemp'] = TproTemp
    
    if reactants and (oxidizer or fuel or complete_products or additional_species or ('eqRatio' in keywords)):
        print('Error: REAC and EQUI cannot both be specified.')
        sys.exit(1)
    elif 'eqRatio' in keywords and not (oxidizer and fuel and complete_products):
        print('Error: If EQUI is specified, all of FUEL, OXID and CPROD must be as well')
        sys.exit(1)
    elif reactants:
        keywords['reactants'] = reactants
    elif 'eqRatio' in keywords:
        keywords['oxidizer'] = oxidizer
        keywords['fuel'] = fuel
        keywords['completeProducts'] = complete_products
        keywords['additionalSpecies'] = additional_species
    else:
        print('Error: You must specify the reactants with either REAC or EQUI')
        sys.exit(1)
    
    if 'tempThresh' not in keywords:
        keywords['tempThresh'] = 400
            
    return keywords

def cli_parser(argv):
    import getopt
    help = "Haven't written the help yet, sorry!"
    try:
        opts, args = getopt.getopt(argv, "hi:o:c:d:x:",
                                   ["help","convert"])
        options = {}
        for o,a in opts:
            options[o] = a
        
        if args:
            raise getopt.GetoptError('Unknown command line option' + 
                                     repr(' '.join(args))
                                    )
    except getopt.GetoptError as e:
        print('You did not enter an option properly.')
        print(e)
        print(help)
        sys.exit(1)
    if '-h' in options or '--help' in options:
        print(help)
        sys.exit(0)
    
    filenames = {}
    if '-i' in options:
        filenames['input_filename'] = options['-i']
    elif '-i' not in options and '--convert' not in options:
        print('Error: The input file must be specified')
        sys.exit(1)
        
    if '-o' in options:
        filenames['output_filename'] = options['-o']
    else:
        filenames['output_filename'] = 'output.out'

    if '-c' in options:
        filenames['mech_filename'] = options['-c']
    else:
        filenames['mech_filename'] = 'chem.xml'
    
    if '-x' in options:
        filenames['save_filename'] = options['-x']
    else:
        filenames['save_filename'] = 'save.hdf'
    
    if '-d' in options:
        filenames['thermo_filename'] = options['-d']
    else:
        filenames['thermo_filename'] = None
    
    convert = '--convert' in options
    
    return filenames,convert,

def reactor_interpolate(interp_time,state1,state2,):
    interp_state = state1 + (state2 - state1)*(interp_time - state1[0])/(state2[0] - state1[0])
    return interp_state
    

def equivalence_ratio(gas,eq_ratio,fuel,oxidizer,complete_products,additional_species,):
    num_H_fuel = 0
    num_C_fuel = 0
    num_O_fuel = 0
    num_H_oxid = 0
    num_C_oxid = 0
    num_O_oxid = 0
    num_H_cprod = 0
    num_C_cprod = 0
    num_O_cprod = 0
    reactants = ''
    #fuel_tot = sum(fuel.values())
    for species, fuel_amt in fuel.items():
        num_H_fuel += gas.n_atoms(species,'H')*fuel_amt
        num_C_fuel += gas.n_atoms(species,'C')*fuel_amt
        num_O_fuel += gas.n_atoms(species,'O')*fuel_amt
    
    #oxid_tot = sum(oxidizer.values())
    for species, oxid_amt in oxidizer.items():
        num_H_oxid += gas.n_atoms(species,'H')*oxid_amt
        num_C_oxid += gas.n_atoms(species,'C')*oxid_amt
        num_O_oxid += gas.n_atoms(species,'O')*oxid_amt
        
    num_H_req = num_H_fuel + num_H_oxid
    num_C_req = num_C_fuel + num_C_oxid
    
    for species in complete_products:
        num_H_cprod += gas.n_atoms(species,'H')
        num_C_cprod += gas.n_atoms(species,'C')
    
    if num_H_cprod > 0:    
        if num_H_req == 0:
            print('Error: All elements specified in the Complete Products must be in the Fuel or Oxidizer')
            sys.exit(1)
            
        H_multiplier = num_H_req/num_H_cprod
    else:
        H_multiplier = 0
    
    if num_C_cprod > 0:
        if num_C_req == 0:
            print('Error: All elements specified in the Complete Products must be in the Fuel or Oxidizer')
            sys.exit(1)
            
        C_multiplier = num_C_req/num_C_cprod
    else:
        C_multiplier = 0
    
    for species in complete_products:
        num_C = gas.n_atoms(species,'C')
        num_H = gas.n_atoms(species,'H')
        num_O = gas.n_atoms(species,'O')
        if num_C > 0:
            num_O_cprod += num_O * C_multiplier
        elif num_H > 0:
            num_O_cprod += num_O * H_multiplier
    
    O_mult = (num_O_cprod - num_O_fuel)/num_O_oxid
    
    total_oxid_moles = sum([O_mult * amt for amt in oxidizer.values()])
    total_fuel_moles = sum([eq_ratio * amt for amt in fuel.values()])
    total_reactant_moles = total_oxid_moles + total_fuel_moles
    
    if additional_species:
        total_additional_species = sum(additional_species.values())
        if total_additional_species >= 1.0:
            print('Error: Additional species must sum to less than 1')
        remain = 1.0 - total_additional_species
        for species, molefrac in additional_species.items():
            add_spec = ':'.join([species,str(molefrac)])
            reactants = ','.join([reactants,add_spec])
    else:
        remain = 1.0
        
    for species,ox_amt in oxidizer.items():
        molefrac = ox_amt * O_mult/total_reactant_moles * remain
        add_spec = ':'.join([species,str(molefrac)])
        reactants = ','.join([reactants,add_spec])
    
    for species, fuel_amt in fuel.items():
        molefrac = fuel_amt * eq_ratio /total_reactant_moles * remain
        add_spec = ':'.join([species,str(molefrac)])
        reactants = ','.join([reactants,add_spec])
        
    #Take off the first character, which is a comma
    reactants = reactants[1:]
        
    return reactants