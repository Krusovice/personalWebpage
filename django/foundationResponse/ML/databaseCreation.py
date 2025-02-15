from plxscripting.easy import * 
import random
import math
import json

# Foundation Sizes
foundationWidth = [1,1.5,2,2.5,3,3.5,4]

# Soil E module variations
E_min = 10000
E_max = 100000
soilModel = 'MC'
# Eccentricity variation in relation to foundation with 10
ecc_factor_min = 0
ecc_factor_max = 0.3 # This eccentricity factor is multiplied onto the foundation width.

soilLayerThickness = 0.5
modelWidthFactor = 4 # Model with in total, in relation to the foundation width
modelDepthFactor = 2 # Model depth in relation to the foundation width


plaxis_password = 'w!V+ZGheHT%V!6U^'
dataFile_path = r'C:\Users\jmkir\Ramboll\JMKIR - Documents\personalWebpage\foundationResponse\ML\dataFile_test.json'
calculationsToRun = 2500

s_i, g_i = new_server('localhost', 10000, password=plaxis_password)

def createModel(data,plaxis_password):
	model_width = modelWidthFactor*data['foundationWidth']
	model_depth = modelDepthFactor*data['foundationWidth']

	s_i.new()
	g_i.soilContour.initializerectangular(-model_width/2,-model_depth,model_width/2,0)
	g_i.borehole(0)
	for E_soil in data['soils']:
		createLayer(data['soilModel'],E_soil)

	g_i.gotostructures()
	g_i.plate((-data['foundationWidth']/2,0),(data['foundationWidth']/2,0))
	material = g_i.platemat()
	material.setproperties('MaterialType','Elastic','EA1',10**12,'EI',10**9)
	g_i.plates[0].Material = material
	g_i.pointload((data['eccentricity']*data['foundationWidth'],0))
	g_i.pointloads[-1].setproperties('Fy', -100*data['foundationWidth'])
	g_i.gotomesh()
	g_i.mesh(0.03)
	g_i.gotostages()
	phase_1 = g_i.phase(g_i.Phases[0])
	g_i.plates.activate(phase_1)
	g_i.pointloads.activate(phase_1)
	g_i.calculate()
	output_port = g_i.view(phase_1)
	s_o, g_o = new_server('localhost', output_port, password=plaxis_password)
	if g_i.phases[-1].Reached.SumMstage.value == 1:
		Uy = g_o.getresults(g_o.plates[0], g_o.phases[-1], g_o.Resulttypes.Plate.Uy, 'node')
		Uy_unzipped = [i for i in zip(Uy)]
		Uy_max = max(Uy_unzipped)[0]
		Uy_min = min(Uy_unzipped)[0]
	else:
		Uy_max = 'Calculation failed'
		Uy_min = Uy_max
		print('Calculation failed')
	g_o.close()
	return Uy_max, Uy_min

def createLayer(soilModel,E_soil):
	material = g_i.soilmat()
	if soilModel == 'linear':
		material.setproperties("SoilModel", 1, "gammaUnsat", 20,"gammaSat", 20, "ERef", E_soil, "nu", 0.3)
	elif soilModel == 'MC':
		material.setproperties("SoilModel", 2, "gammaUnsat", 20, "gammaSat", 20, "ERef", E_soil, "nu", 0.3, "phi", 40, "cRef", 300)	
	g_i.soillayer(soilLayerThickness)
	g_i.Soils[-1].Material = material

def datafile_readAndAppend(dataFile_path,data):
	try:
		with open(dataFile_path, "r") as file:
			dataFile = json.load(file)
	except FileNotFoundError:
		dataFile = []

	dataFile.append(data)
	with open(dataFile_path, "w") as file:
		json.dump(dataFile, file, indent=4)

def appendDataFile(dataFile_path, plaxis_password, foundationWidth, E_min, E_max, ecc_factor_min, ecc_factor_max,soilLayerThickness, soilModel):
	data = dict()
	data['foundationWidth'] = float(format(random.choice(foundationWidth),'0.1f'))
	model_depth = modelDepthFactor*data['foundationWidth']
	data['eccentricity'] = float(format(random.uniform(ecc_factor_min,ecc_factor_max),'0.2f'))
	data['soilModel'] = soilModel
	numberOfLayers = model_depth / soilLayerThickness
	#soilE = float(format(random.uniform(E_min,E_max),'.0f')) ## This line is used to create a single E soil layer
	#data['soils'] = [soilE for i in range(int(numberOfLayers))] ## This line is used to create a single E soil layer
	data['soils'] = [float(format(random.uniform(E_min,E_max),'.0f')) for i in range(int(numberOfLayers))]

	Uy_max, Uy_min = createModel(data,plaxis_password)
	if Uy_max == 'Calculation failed':
		data['Uy'] = 'Calculation failed'
		data['rot'] = 'Calculation failed'
	else:
		diffY = Uy_max - Uy_min
		data['Uy'] = (Uy_min + Uy_max)/2
		data['rot'] = math.asin(diffY / data['foundationWidth'])

	datafile_readAndAppend(dataFile_path,data)

print('Calculation initiated')
for i in range(calculationsToRun):
	appendDataFile(dataFile_path, plaxis_password, foundationWidth, E_min, E_max, ecc_factor_min, ecc_factor_max,soilLayerThickness,soilModel)
	print(f'Iteration {i} finalized')
