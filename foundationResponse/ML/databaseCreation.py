from plxscripting.easy import * 
import random
import math
import json

# Foundation Sizes
w_min = 1
w_max = 4
# Soil E module variations
E_min = 5000
E_max = 200000
# Eccentricity variation in relation to foundation with10
ecc_min = 0
ecc_max = 0.3

plaxis_password = '12333333344342sdfdf'
dataFile_path = r'C:\Users\jmkir\Ramboll\JMKIR - Documents\10. projects\94. ML, Rocking foundation\dataFile.json'
calculationsToRun = 1000

s_i, g_i = new_server('localhost', 10000, password=plaxis_password)

def createModel(data,plaxis_password):
	model_width = 4*data['foundationWidth']
	model_depth = 2*data['foundationWidth']

	s_i.new()
	g_i.soilContour.initializerectangular(-model_width/2,-model_depth,model_width/2,0)
	g_i.borehole(0)
	for E_soil in data['soils']:
		createLayer(E_soil)

	g_i.gotostructures()
	g_i.plate((-data['foundationWidth']/2,0),(data['foundationWidth']/2,0))
	material = g_i.platemat()
	material.setproperties('MaterialType','Elastic','EA1',10**12,'EI',10**9)
	g_i.plates[0].Material = material
	g_i.pointload((data['eccentricity'],0))
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
	Uy = g_o.getresults(g_o.plates[0], g_o.phases[-1], g_o.Resulttypes.Plate.Uy, 'node')
	Uy_unzipped = [i for i in zip(Uy)]
	Uy_max = max(Uy_unzipped[0])
	Uy_min = min(Uy_unzipped[0])
	g_o.close()
	return Uy_max, Uy_min

def createLayer(E_soil):
	material = g_i.soilmat()
	material.setproperties("SoilModel", 2, "gammaUnsat", 20, 
	"gammaSat", 20, "ERef", E_soil, "nu", 0.3, "phi", 40, "cRef", 300)
	g_i.soillayer(0.1)
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

def appendDataFile(dataFile_path, plaxis_password, w_min, w_max, E_min, E_max, ecc_min, ecc_max):
	data = dict()
	data['foundationWidth'] = float(format(random.uniform(w_min,w_max),'0.1f'))
	model_depth = 2*data['foundationWidth']
	data['eccentricity'] = float(format(random.uniform(ecc_min,ecc_max)*data['foundationWidth'],'0.2f'))
	data['soils'] = [float(format(random.uniform(E_min,E_max),'.0f')) for i in range(int(model_depth*10))]

	Uy_max, Uy_min = createModel(data,plaxis_password)
	diffY = Uy_max - Uy_min
	data['Uy'] = (Uy_min + Uy_max)/2
	data['rot'] = math.asin(diffY / data['foundationWidth'])

	datafile_readAndAppend(dataFile_path,data)

print('Calculation initiated')
for i in range(calculationsToRun):
	appendDataFile(dataFile_path, plaxis_password, w_min, w_max, E_min, E_max, ecc_min, ecc_max)
	print(f'Iteration {i} finalized')
