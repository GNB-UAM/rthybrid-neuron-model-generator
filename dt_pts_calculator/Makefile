CC = gcc
CCFLAGS = -Wall --pedantic -O2 -w -g

model_library/neuron/$(FOLDER)/$(MODEL): obj/main_$(MODEL).o obj/nm_$(MODEL).o obj/neuron_models_aux_functions.o obj/integration_methods.o obj/aux_functions.o
	$(CC) $(CCFLAGS) -o model_library/neuron/$(FOLDER)/$(MODEL) obj/main_$(MODEL).o obj/nm_$(MODEL).o obj/neuron_models_aux_functions.o obj/integration_methods.o obj/aux_functions.o -lm

obj/main_$(MODEL).o: model_library/neuron/$(FOLDER)/main_$(MODEL).c model_library/neuron/$(FOLDER)/nm_$(MODEL).h clamp/includes/types_clamp.h common/includes/types.h
	$(CC) $(CCFLAGS) -c model_library/neuron/$(FOLDER)/main_$(MODEL).c -o obj/main_$(MODEL).o -lm

obj/nm_$(MODEL).o: model_library/neuron/$(FOLDER)/nm_$(MODEL).c model_library/neuron/$(FOLDER)/nm_$(MODEL).h clamp/includes/types_clamp.h common/includes/types.h
	$(CC) $(CCFLAGS) -c model_library/neuron/$(FOLDER)/nm_$(MODEL).c -o obj/nm_$(MODEL).o -lm

obj/neuron_models_aux_functions.o: model_library/neuron/neuron_models_aux_functions.c clamp/includes/types_clamp.h
	$(CC) $(CCFLAGS) -c model_library/neuron/neuron_models_aux_functions.c -o obj/neuron_models_aux_functions.o -lm

obj/integration_methods.o: model_library/integration_methods.c model_library/integration_methods.h common/includes/types.h
	$(CC) $(CCFLAGS) -c model_library/integration_methods.c -o obj/integration_methods.o -lm

obj/aux_functions.o: common/src/aux_functions.c common/includes/types.h
	$(CC) $(CCFLAGS) -c common/src/aux_functions.c -o obj/aux_functions.o -lm


clean:
	rm -f model_library/neuron/$(FOLDER)/$(MODEL) obj/*.o

mclan:
	rm -f model_library/neuron/$(FOLDER)/$(MODEL) obj/*.o
	make