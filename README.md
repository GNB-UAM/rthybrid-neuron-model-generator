
# RTHybrid Neuron Model Generator
Automatic neuron model generator compatible with RTHybrid model library.

It reads the equations that define the model from a text file and generates all the necessary code to use the model in RTHybrid.

## Input file format
This is an example of an input file for the model generator:

    Example_Model_2019 -100 100
    d/dt V = (-(i_k + i_na) + i - syn) / Cm
	i_na = g_na^2 * (1.0 / (1.0 + exp(-0.2 * (V + 45)))) * (V - V_na)
	i_k = g_k * (V - V_k)
	
	Values
	V = -55
	i = 0.0
	Cm = 0.02
	g_na = 0.0231
	g_k = 0.25
	V_k = -70.0
	V_na = 40.0

The first line of the file contains the name of the model (use under scores instead of spaces), and its minimum and maximum amplitude values. It is recommended to use the reference of the paper from which the model is obtained as name (i.e. Hodgkin_Huxley_1952).

The following lines are the equations that define the model:
- Use only parenthesis to set operations precedence, not brackets or curly braces.
- It is case sensitive, but do not name two variables or parameters the same, even with different cases.
- To define a differential equation write **d/dt** before the variable name (e.g. *d/dt V*).
- Power functions can be expressed using **^** (e.g. *n^2*).
- Exponential functions can be expressed using **exp** (e.g. *exp(-0.4 * (V + 31))*).
- There must ALWAYS exist a parameter named **syn** in the voltage equation, which will be used for the synaptic input.
-  Trigonometric functions are not supported yet.

After all the equations there must be a line with the word Values and after it, the initial values for the variables and parameters necessary.

## How to use it
Open a terminal and type

    $ sh generator.sh filename model_name
where filename is the input file (e.g. hodgkin_huxley_1952.txt) and model_name is the name written in the first line of that file (e.g. Hodgkin_Huxley_1952).

This script will first execute the program *equation_parser/file_parser.py*, which will generate the code for the neuron model in the directory model_library/neuron/<model_name>.

Then, it will execute *dt_pts_calculator/calculator.py*, which will compute the model with different integration steps and integration methods (Euler, Heun, Runge-Kutta order 4 and Runge-Kutta order 6(5)) and generate the **set_pts_burst** function, necessary for **RTHybrid** temporal calibration of the models. This may take several minutes.

The program *dt_pts_calculator/test.py* allows you to test the generated model with different integration methods (EULER, HEUN, RK4 or RK65) and integration steps

    python dt_pts_calculator/test.py <model_name> <integration_method> <integration_step>

Finally, the complete code for the neuron model will be at *model_library/neuron/<model_name>*. Copy the <model_name> folder to *model_library/neuron/* directory of RTHybrid (the file main_<model_name>.c can be removed at this point).
