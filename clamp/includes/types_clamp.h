/**
 * @file types_clamp.h
 * @brief Header file containing the main structures used by RTHybrid.
 */

#ifdef __cplusplus
extern "C" {
#endif

#ifndef TYPES_CLAMP_H__
#define TYPES_CLAMP_H__


#include "../../common/includes/types.h"


/* Neuron model struct */
typedef struct neuron_model neuron_model;

/**
 * @brief Structure that stores all the parameters and variables of a neuron model.
 *
 * It will be initialized with the information of an specific model in #init_neuron_model.
 */ 
struct neuron_model {
    void (*func)(neuron_model nm, double);				/**< Pointer to the main function of the model (defined in neuron_models_functions.h) */ 
    double (*set_pts_burst)(double, neuron_model * nm);	/**< Pointer to the function that sets the number of points per burst of the model (defined in neuron_models_functions.h) */
    void (*method)
        (void (*f) (double *, double *, double *, double), 
        int dim, double dt, double * vars, 
        double * params, double aux);                   /**< Pointer to the function with the integration method. */ 
    unsigned int type;									/**< Integer that identifies the model (using the macros defined in neuron_models_functions.h) */
    unsigned int dim;									/**< Dimension (number of variables) of the model */
    unsigned int n_params;								/**< Number of parameters of the model */
    double * vars;										/**< Array with the variables of the model */
    double * params;									/**< Array with the parameters of the model */
    double min;											/**< Minimum membrane potential value of the model */
    double max;											/**< Maximum membrane potential value of the model */
    double pts_burst;									/**< Number of points per burst of the model */
};


#endif // TYPES_CLAMP_H__

#ifdef __cplusplus
}
#endif
