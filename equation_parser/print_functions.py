def print_source_begin (diff_variables, variables, params, model_name, output_file):
	output_file.write("#include \"nm_"+model_name.lower()+".h\"\n#include \"../../integration_methods.h\"\n#include \"../neuron_models_aux_functions.h\"\n\n")

	output_file.write("/**\n * @file nm_"+model_name.lower()+".h\n * @brief Source file for the "+model_name+" model functions.\n */\n\n")
	output_file.write("/** @name "+model_name+"\n * "+model_name+" neuron model.\n */\n///@{\n\n")

	for var in variables:
		output_file.write("double nm_"+model_name.lower()+"_"+var+" (double * vars, double * params);\n")
	for var in diff_variables:
		output_file.write("double nm_"+model_name.lower()+"_"+var+" (double * vars, double * params);\n")

	output_file.write("double nm_"+model_name.lower()+"_set_pts_burst (double pts_live, neuron_model * nm);\n")

	output_file.write("\n\n")


def print_source_funcs(diff_variables, variables, params, model_name, min_v, max_v, output_file):
	label_upper = "NM_"+model_name.upper()+"_"
	label_lower = "nm_"+model_name.lower()+"_"

	# Differential equations function
	output_file.write("/**\n * @brief "+model_name+" neuron model differential equations.\n")
	output_file.write(" * @param[in] vars Neuron model variables\n * @param[out] ret Return values array\n")
	output_file.write(" * @param[in] params Neuron models parameters\n * @param[in] syn Synapse input current value\n */\n\n")

	output_file.write("void "+label_lower+"f (double * vars, double * ret, double * params, double syn) {\n")

	output_file.write("\tparams["+label_upper+"SYN] = syn;\n\n")

	for diff_var in diff_variables:
		output_file.write("\tret["+label_upper+diff_var.upper()+"] = "+label_lower+diff_var+"(vars, params);\n")

	output_file.write("}\n\n")

	# Main function
	output_file.write("/**\n * @brief "+model_name+" neuron model.\n * @param[in] nm Neuron model structure\n * @param[in] syn Synapse input current value\n */\n\n")

	output_file.write("void nm_"+model_name.lower()+" (neuron_model nm, double syn) {\n")
	output_file.write("\tnm.method("+label_lower+"f, nm.dim, nm.params["+label_upper+"DT], nm.vars, nm.params, syn);\n\treturn;\n}\n\n")

	# Integration step selection function
	'''
	output_file.write("/**\n * @brief Sets "+model_name+" model number of points per burst and integration step.\n * \n")
	output_file.write(" * If not previously specified by the user, the number of points per burst of the model and its integration step is set according to the living neuron number of points per burst.\n")
	output_file.write(" * @param[in] pts_live Number of points in a living neuron burst\n * @param[in] nm Pointer to the neuron model structure\n */\n\n")

	output_file.write("void "+label_lower+"set_pts_burst (double pts_live, neuron_model * nm) {\n")
	output_file.write("\tdouble * dts, * pts;\n\tint length;\n\n")

	output_file.write("\t"+label_lower+"set_dt_pts_arrays(nm->params["+label_upper+"DT], &dts, &pts, &length);\n")
	output_file.write("\tselect_dt_neuron_model(dts, pts, length, pts_live, &(nm->params["+label_upper+"DT]), &(nm->pts_burst));\n\n\treturn;\n}\n")
	'''

	# Initialization function
	output_file.write("/**\n * @brief Initializes "+model_name+" neuron model.\n")
	output_file.write(" * @param[in] nm Pointer to the neuron model structure\n")
	output_file.write(" * @param[in] vars Array with the initial values of the model variables\n")
	output_file.write(" * @param[in] params Array with the values of the mode parameters\n */\n\n")

	output_file.write("void "+label_lower+"init (neuron_model * nm, double * vars, double * params) {\n")
	output_file.write("\tnm->dim = "+str(len(diff_variables))+";\n\tnm->vars = (double *) malloc (sizeof(double) * nm->dim);\n\tcopy_1d_array(vars, nm->vars, nm->dim);\n\n")
	output_file.write("\tnm->n_params = "+str(len(params))+";\n\tnm->params = (double *) malloc (sizeof(double) * nm->n_params);\n\tcopy_1d_array(params, nm->params, nm->n_params);\n\n")
	output_file.write("\tnm->max = "+str(max_v)+";\n\tnm->min = "+str(min_v)+";\n\tnm->pts_burst = -1.0;\n\n")
	output_file.write("\tnm->func = &nm_"+model_name.lower()+";\n\t//nm->set_pts_burst = &"+label_lower+"set_pts_burst;\n\tnm->method = integration_method_selector(params["+label_upper+"DT]);\n\n")

	output_file.write("\treturn;\n}\n\n")



def print_header_file(diff_variables, variables, params, model_name, output_file):
	label_upper = "NM_"+model_name.upper()+"_"
	label_lower = "nm_"+model_name.lower()+"_"

	output_file.write("/**\n * @file nm_"+model_name.lower()+".h\n * @brief Header file for the "+model_name+" model functions.\n */\n\n")

	output_file.write("#ifdef __cplusplus\nextern \"C\" {\n#endif\n\n")
	output_file.write("#ifndef "+label_upper+"H__\n#define "+label_upper+"H__\n\n")

	output_file.write("#include <math.h>\n")
	output_file.write("#include \"../../../clamp/includes/types_clamp.h\"\n\n")

	output_file.write("/** @name "+model_name+"\n * "+model_name+" neuron model.\n */\n///@{\n\n")

	output_file.write("#define "+label_upper+"N_VARS %d\n"%(len(diff_variables)))
	output_file.write("// Variables\n")
	for i in range(len(diff_variables)):
		output_file.write("#define "+label_upper+diff_variables[i].upper()+" %d\n"%(i))

	output_file.write("\n\n#define "+label_upper+"N_PARAMS %d\n"%(len(params)))
	output_file.write("// Parameters\n")
	for i in range(len(params)):
		output_file.write("#define "+label_upper+params[i].upper()+" %d\n"%(i))

	output_file.write("\nvoid "+label_lower+"init (neuron_model * nm, double * vars, double * params);\n")
	output_file.write("void "+label_lower+" (neuron_model nm, double syn);\n")
	output_file.write("double "+label_lower+"set_pts_burst (double pts_live, neuron_model * nm);\n\n///@}\n\n")

	output_file.write("#endif // "+label_upper+"H__\n\n")
	output_file.write("#ifdef __cplusplus\n}\n#endif")


def print_main_file(diff_variables_dict, variables, params_dict, model_name, output_file):
	label_upper = "NM_"+model_name.upper()+"_"
	label_lower = "nm_"+model_name.lower()+"_"

	output_file.write("#include \"nm_"+model_name.lower()+".h\"\n\n")

	# Variables and parameters init functions
	output_file.write("void init_vars_params (double ** vars, double ** params) {\n")
	output_file.write("\t(*vars) = (double*) malloc (sizeof(double) * "+label_upper+"N_VARS);\n")
	output_file.write("\t(*params) = (double*) malloc (sizeof(double) * "+label_upper+"N_PARAMS);\n\n")

	output_file.write("\t// Variables\n")
	for var in diff_variables_dict:
		#output_file.write("\t(*vars)["+label_upper+diff_variables[i].upper()+"] = 0; // Not set yet\n")
		output_file.write("\t(*vars)["+label_upper+var.upper()+"] = "+diff_variables_dict[var]+";\n")

	output_file.write("\n\t// Parameters\n")
	for param in params_dict:
		#output_file.write("\t(*params)["+label_upper+params[i].upper()+"] = 0; // Not set yet\n")
		output_file.write("\t(*params)["+label_upper+param.upper()+"] = "+params_dict[param]+";\n")

	output_file.write("}\n\n")


	# Main function
	output_file.write("int main (int argc, char * argv[]) {\n")
	output_file.write("\tdouble * vars, * params;\n\tint freq = 10000;\n\tneuron_model nm;\n\tunsigned long loop_points = 0, i = 0;\n\tFILE * f;\n\n")

	output_file.write("\tinit_vars_params(&vars, &params);\n")
	output_file.write("\tparams["+label_upper+"DT] = atoi(argv[2]);\n")
	output_file.write("\t"+label_lower+"init(&(nm), vars, params);\n")
	output_file.write("\tfree_pointers(2, &vars, &params);\n\n")
	output_file.write("\tnm.params["+label_upper+"DT] = atof(argv[3]);\n\n")

	output_file.write("\tf = fopen(argv[1], \"w\");\n\tloop_points = 100 * freq;\n\n")
	output_file.write("\tfor (i = 0; i < loop_points; i++) {\n\t\tfprintf(f, \"%f\\n\", nm.vars["+label_upper+"V]);\n\t\tnm.func(nm, 0);\n\t}\n\n")
	output_file.write("\tfclose(f);\n\tfree_pointers(2, &(nm.vars), &(nm.params));\n\treturn 1;\n}")



def print_cpp_source_file (diff_variables, variables, params, model_name, output_file):
	label_upper = "NM_"+model_name.upper()+"_"
	label_lower = "nm_"+model_name.lower()+"_"

	output_file.write("#include \"nm_gui_"+model_name.lower()+".h\"\n")
	output_file.write("#include \"ui_nm_gui_"+model_name.lower()+".h\"\n\n")

	# Constructor
	output_file.write("NM_GUI_"+model_name+"::NM_GUI_"+model_name+"(clamp_args * args, QWidget *parent) :\n\tQDialog(parent),\n\tui(new Ui::NM_GUI_"+model_name+")\n{\n")
	output_file.write("\tthis->settings = new QSettings(\"RTHybrid\", \"NM_"+model_name+"\");\n")
	output_file.write("\tthis->args = args;\n\tui->setupUi(this);\n\tloadSettings();\n}\n\n")

	# Destructor
	output_file.write("NM_GUI_"+model_name+"::~NM_GUI_"+model_name+"(){\n\t delete ui;\n}\n\n")

	# Accept button
	output_file.write("void NM_GUI_"+model_name+"::on_pushButton_accept_clicked() {\n")
	output_file.write("\targs->vars = (double*) malloc (sizeof(double) * %d);\n"%(len(diff_variables)))
	output_file.write("\targs->params = (double *) malloc (sizeof(double) * %d);\n\n"%(len(params)))

	for var in diff_variables:
		output_file.write("\targs->vars["+label_upper+var.upper()+"] = ui->doubleSpinBox_"+var+"->value();\n")

	output_file.write("\n")

	for param in params:
		if param == "dt":
			continue
		output_file.write("\targs->params["+label_upper+param.upper()+"] = ui->doubleSpinBox_"+param+"->value();\n")

	output_file.write("\targs->params["+label_upper+"DT] = ui->comboBoxIntegrationMethod->currentIndex();\n\n")
	output_file.write("\tsaveSettings();\n\tthis->close();\n}\n\n")

	# Save settings
	output_file.write("void NM_GUI_"+model_name+"::saveSettings() {\n")
	for var in diff_variables:
		output_file.write("\tsettings->setValue(\""+label_upper+var.upper()+"\", ui->doubleSpinBox_"+var+"->value());\n")

	output_file.write("\n")

	for param in params:
		if param == "dt":
			continue
		output_file.write("\tsettings->setValue(\""+label_upper+param.upper()+"\", ui->doubleSpinBox_"+param+"->value());\n")

	output_file.write("\tsettings->setValue(\""+label_upper+"DT\", ui->comboBoxIntegrationMethod->currentIndex());\n}\n\n")

	# Load settings
	output_file.write("void NM_GUI_"+model_name+"::loadSettings() {\n")
	output_file.write("\tif (settings->value(\""+label_upper+"DT\", -1).toInt() == -1) return; //No settings saved yet\n\n")

	for var in diff_variables:
		output_file.write("\tui->doubleSpinBox_"+var+"->setValue(settings->value(\""+label_upper+var.upper()+"\").toDouble());\n")

	output_file.write("\n")

	for param in params:
		if param == "dt":
			continue
		output_file.write("\tui->doubleSpinBox_"+param+"->setValue(settings->value(\""+label_upper+param.upper()+"\").toDouble());\n")

	output_file.write("\tui->comboBoxIntegrationMethod->setCurrentIndex(settings->value(\""+label_upper+"DT\").toInt());\n}")


def print_cpp_header_file (diff_variables, variables, params, model_name, output_file):
	output_file.write("#ifndef NM_GUI_"+model_name.upper()+"_H\n")
	output_file.write("#define NM_GUI_"+model_name.upper()+"_H\n\n")

	output_file.write("#include <QDialog>\n")
	output_file.write("#include <QSettings>\n")
	output_file.write("#include \"nm_"+model_name.lower()+".h\"\n\n")

	output_file.write("namespace Ui {\n")
	output_file.write("class NM_GUI_"+model_name+";\n")
	output_file.write("}\n\n")

	output_file.write("class NM_GUI_"+model_name+" : public QDialog\n")
	output_file.write("{\n")
	output_file.write("\tQ_OBJECT\n\n")

	output_file.write("public:\n")
	output_file.write("\texplicit NM_GUI_"+model_name+"(clamp_args * args = NULL, QWidget *parent = 0);\n")
	output_file.write("\t~NM_GUI_"+model_name+"();\n\n")

	output_file.write("private slots:\n")
	output_file.write("\tvoid on_pushButton_accept_clicked();\n\n")

	output_file.write("private:\n")
	output_file.write("\tUi::NM_GUI_"+model_name+" *ui;\n")
	output_file.write("\tclamp_args * args;\n")
	output_file.write("\tQSettings * settings;\n\n")

	output_file.write("\tvoid saveSettings();\n")
	output_file.write("\tvoid loadSettings();\n")
	output_file.write("};\n\n")

	output_file.write("#endif // NM_GUI_"+model_name.upper()+"_H")


def print_xml_header_file (diff_variables, variables, params, model_name, output_file):
	output_file.write("/**\n")
	output_file.write(" * @file nm_xml_"+model_name.lower()+".h\n")
	output_file.write(" * @brief Header file for the "+model_name+" neuron model functions XML parser functions.\n")
	output_file.write(" */\n\n")


	output_file.write("#ifndef NM_XML_"+model_name.upper()+"_H\n")
	output_file.write("#define NM_XML_"+model_name.upper()+"_H\n\n")


	output_file.write("#include \"../../../common/includes/xml_parser_functions.h\"\n\n") 

	output_file.write("#ifdef __cplusplus\n")
	output_file.write("extern \"C\" {\n")
	output_file.write("#endif\n\n")

	output_file.write("#include \"nm_"+model_name.lower()+".h\"\n\n")

	output_file.write("int parse_nm_"+model_name.lower()+" (xmlDocPtr doc, xmlNodePtr cur, clamp_args * args);\n\n")

	output_file.write("#ifdef __cplusplus\n")
	output_file.write("}\n")
	output_file.write("#endif\n\n")

	output_file.write("#endif // NM_XML_"+model_name.upper()+"_H")


def print_xml_source_file (diff_variables, variables, params, model_name, output_file):
	label_upper = "NM_"+model_name.upper()+"_"
	label_lower = "nm_"+model_name.lower()+"_"

	output_file.write("#include \"nm_xml_"+model_name.lower()+".h\"\n\n")

	output_file.write("/**\n")
	output_file.write(" * @file nm_xml_"+model_name.lower()+".c\n")
	output_file.write(" * @brief Source file with the "+model_name+" neuron model functions.\n")
	output_file.write(" */\n\n")

	output_file.write("/**\n")
	output_file.write(" * @brief Imports the parameters of the "+model_name+" neuron model from an XML file.\n")
	output_file.write(" * @param[in] doc XML pointer to the document\n")
	output_file.write(" * @param[in] cur Cursor to navigate the XML file.\n")
	output_file.write(" * @param[in/out] args Pointer to the main arguments structure\n")
	output_file.write(" * @return #OK if it works, #ERR if there is an error\n")
	output_file.write(" */\n\n")

	output_file.write("int parse_nm_"+model_name.lower()+" (xmlDocPtr doc, xmlNodePtr cur, clamp_args * args) {\n")
	output_file.write("\txmlNodePtr child =  NULL;\n")
	output_file.write("\tint ret = OK;\n\n")

	output_file.write("\tif ((!doc) || (!cur) || (!args)) return ERR;\n\n")

	output_file.write("\targs->vars = (double*) malloc (sizeof(double) * %d);\n"%(len(diff_variables)))
	output_file.write("\targs->params = (double *) malloc (sizeof(double) * %d);\n\n"%(len(params)))

	output_file.write("\twhile (cur != NULL) {\n")
	output_file.write("\t\tif (xmlStrcmp(cur->name, (const xmlChar *) \"vars\") == 0) {\n")
	output_file.write("\t\t\tchild = cur->xmlChildrenNode;\n\n")

	output_file.write("\t\t\twhile (child != NULL) {\n\n")
	for var in diff_variables:
		output_file.write("\t\t\t\tif (xmlStrcmp(child->name, (const xmlChar *) \""+var+"\") == 0) ret = parse_double(doc, child, &args->vars["+label_upper+""+var.upper()+"], (const xmlChar*) VALUE);\n")

	output_file.write("\t\t\t\tif (ret != OK) return ret;\n\n")

	output_file.write("\t\t\t\tchild = child->next;\n")
	output_file.write("\t\t\t}\n")
	output_file.write("\t\t}\n")
	output_file.write("\t\telse if (xmlStrcmp(cur->name, (const xmlChar *) \"params\") == 0) {\n")
	output_file.write("\t\t\tchild = cur->xmlChildrenNode;\n\n")

	output_file.write("\t\t\twhile (child != NULL) {\n\n")
	for param in params:
		if param == "dt":
			continue
		output_file.write("\t\t\t\tif (xmlStrcmp(child->name, (const xmlChar *) \""+param+"\") == 0) ret = parse_double(doc, child, &args->params["+label_upper+""+param.upper()+"], (const xmlChar*) VALUE);\n")

	output_file.write("\t\t\t\tif (xmlStrcmp(child->name, (const xmlChar *) \"method\") == 0) ret = parse_double(doc, child, &args->params["+label_upper+"DT], (const xmlChar*) VALUE);\n\n")

	output_file.write("\t\t\t\tif (ret != OK) return ret;\n\n")

	output_file.write("\t\t\t\tchild = child->next;\n")
	output_file.write("\t\t\t}\n")
	output_file.write("\t\t}\n\n")

	output_file.write("\tcur = cur->next;\n")
	output_file.write("\t}\n\n")

	output_file.write("\treturn OK;\n")
	output_file.write("}")