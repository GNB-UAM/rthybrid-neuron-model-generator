import numpy as np
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def simple_burst_duration (data):
	v = data[:,0]
	times = []
	events = []
	flag = 0

	if np.isnan(v).any():
		return -2

	maxv = max(v)
	minv = min(v)
	r = maxv - minv

	for i in range(len(v)):
		if (v[i] > (minv + r*0.9) and flag == 1):
			flag = 0
			times.append(i)
			events.append(v[i])
		elif (v[i] < (minv + r*0.1) and flag == 0):
			flag = 1

	intr = inter_burst_pts(times)

	if not intr:
		return -1
	else:
		return np.mean(intr)



def inter_burst_pts (times):
	inter = []
	if not times:
		return inter

	old = times[0]

	for i in range(1, len(times)):
		inter.append(times[i] - old)
		old = times[i]


	return inter


def print_dt_pts_arrays_func (dicts_methods, model_name):
	label_upper = "NM_"+model_name.upper()+"_"
	label_lower = "nm_"+model_name.lower()+"_"
	output_file = open("model_library/neuron/"+model_name+"/nm_"+model_name.lower()+".c", "a+")

	output_file.write("/**\n * @brief Sets "+model_name+" model number of points per burst and integration step.\n * \n")
	output_file.write(" * If not previously specified by the user, the number of points per burst of the model and its integration step is set according to the living neuron number of points per burst.\n")
	output_file.write(" * @param[in] pts_live Number of points in a living neuron burst\n * @param[in] nm Pointer to the neuron model structure\n */\n\n")

	output_file.write("double "+label_lower+"set_pts_burst (double pts_live, neuron_model * nm) {\n")
	output_file.write("\tint length = 0;\n\tint method = nm->params["+label_upper+"DT];\n\n")
	output_file.write("\tswitch(method) {\n")
	
	dts = list(dicts_methods[0].keys())
	pts = list(dicts_methods[0].values())
	output_file.write("\t\tcase EULER:\n\t\t{\n")
	output_file.write("\t\t\tlength = %f;\n"%(len(dts)))
	output_file.write("\t\t\tdouble dts[] = ")
	output_file.write("{")
	for i in range(len(dts)-1):
		output_file.write("%f, "%(dts[i]))
	output_file.write("%f};\n"%(dts[-1]))

	output_file.write("\t\t\tdouble pts[] = ")
	output_file.write("{")
	for i in range(len(pts)-1):
		output_file.write("%f, "%(pts[i]))

	output_file.write("%f};\n"%(pts[-1]))
	output_file.write("\n\t\t\tselect_dt_neuron_model(dts, pts, length, pts_live, &(nm->params["+label_upper+"DT]), &(nm->pts_burst));\n")
	output_file.write("\t\t\tbreak;\n\t\t}\n")

	dts = list(dicts_methods[1].keys())
	pts = list(dicts_methods[1].values())
	output_file.write("\t\tcase HEUN:\n\t\t{\n")
	output_file.write("\t\t\tlength = %f;\n"%(len(dts)))
	output_file.write("\t\t\tdouble dts[] = ")
	output_file.write("{")
	for i in range(len(dts)-1):
		output_file.write("%f, "%(dts[i]))
	output_file.write("%f};\n"%(dts[-1]))

	output_file.write("\t\t\tdouble pts[] = ")
	output_file.write("{")
	for i in range(len(pts)-1):
		output_file.write("%f, "%(pts[i]))

	output_file.write("%f};\n"%(pts[-1]))
	output_file.write("\n\t\t\tselect_dt_neuron_model(dts, pts, length, pts_live, &(nm->params["+label_upper+"DT]), &(nm->pts_burst));\n")
	output_file.write("\t\t\tbreak;\n\t\t}\n")

	dts = list(dicts_methods[2].keys())
	pts = list(dicts_methods[2].values())
	output_file.write("\t\tcase RK4:\n\t\t{\n")
	output_file.write("\t\t\tlength = %f;\n"%(len(dts)))
	output_file.write("\t\t\tdouble dts[] = ")
	output_file.write("{")
	for i in range(len(dts)-1):
		output_file.write("%f, "%(dts[i]))
	output_file.write("%f};\n"%(dts[-1]))

	output_file.write("\t\t\tdouble pts[] = ")
	output_file.write("{")
	for i in range(len(pts)-1):
		output_file.write("%f, "%(pts[i]))

	output_file.write("%f};\n"%(pts[-1]))
	output_file.write("\n\t\t\tselect_dt_neuron_model(dts, pts, length, pts_live, &(nm->params["+label_upper+"DT]), &(nm->pts_burst));\n")
	output_file.write("\t\t\tbreak;\n\t\t}\n")

	dts = list(dicts_methods[3].keys())
	pts = list(dicts_methods[3].values())
	output_file.write("\t\tcase RK65:\n\t\t{\n")
	output_file.write("\t\t\tlength = %f;\n"%(len(dts)))
	output_file.write("\t\t\tdouble dts[] = ")
	output_file.write("{")
	for i in range(len(dts)-1):
		output_file.write("%f, "%(dts[i]))
	output_file.write("%f};\n"%(dts[-1]))

	output_file.write("\t\t\tdouble pts[] = ")
	output_file.write("{")
	for i in range(len(pts)-1):
		output_file.write("%f, "%(pts[i]))

	output_file.write("%f};\n"%(pts[-1]))
	output_file.write("\n\t\t\tselect_dt_neuron_model(dts, pts, length, pts_live, &(nm->params["+label_upper+"DT]), &(nm->pts_burst));\n")
	output_file.write("\t\t\tbreak;\n\t\t}\n")


	output_file.write("\t}\n")

	output_file.write("\n\treturn nm->params["+label_upper+"DT];\n}\n")
	output_file.write("\n///@}")

	output_file.close()



dts = np.arange(0.00001, 0.0001, 0.00001).tolist() + np.arange(0.0001, 0.1001, 0.0001).tolist()

dicts_methods = [{}, {}, {}, {}]

model_name = sys.argv[1]

os.system("make -f dt_pts_calculator/Makefile FOLDER="+model_name+" MODEL="+model_name.lower()+"")

for method in range(4):
	print("Method %d"%(method))

	for dt in dts:
		filename = "model_library/neuron/"+model_name+"/output_"+str(method)+"_"+str(dt)+".txt"
		
		# Calculate model
		os.system("./model_library/neuron/"+model_name+"/"+model_name.lower()+" "+filename+" "+str(method)+" "+" "+str(dt)+"")

		try:
			dataset = pd.read_csv(filename, delimiter=' ')
			data = dataset.values

			dur = simple_burst_duration(data)
			if dur == -2:
				break

			if dur > 0:
				dicts_methods[method][dt] = dur
		except:
			empty_file = 1
		finally:
			os.system("rm "+filename)


	keys = list(reversed(sorted(dicts_methods[method].keys())))
	last_ref = 0
	thresh = 10 ** (len(str(int(last_ref))) - 2)

	for dt in keys:
		pts = dicts_methods[method][dt]
		
		if (pts - last_ref) < thresh:
			dicts_methods[method].pop(dt)
		else:
			last_ref = pts
			thresh = 10 ** (len(str(int(last_ref))) - 2)

	print(dicts_methods[method])

print_dt_pts_arrays_func(dicts_methods, model_name)

os.system("make -f dt_pts_calculator/Makefile FOLDER="+model_name+" MODEL="+model_name.lower()+" clean")

os.system("sed -i 's/\/\/nm->set_pts_burst\ =/nm->set_pts_burst\ =/g' model_library/neuron/"+model_name+"/nm_"+model_name.lower()+".c")