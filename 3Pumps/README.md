
    """
    This function calculates the purchase costs of each single pump and motor, the total purchase costs of all pumps and motors combined, and the head, flowrate and pump break of each pump modelled in Aspen Plus, by retrieving values from Aspen Plus.
    It is necessary to name all pumps in the Aspen Plus simulation according to "P01", "P02", "P03", etc. 
    Parameters
    ----------
    Application : Aspen Plus python connection
    No_pumps : how many pumps
    pump_material_factor : material factor for the material of the pumps (e.g. 2 for stainless steel, see Seider et al. (2009))
    current_cost_index : cost index of the year where CAPEX is to be calculated (e.g. 600 for 2019)

    Returns
    -------
    pump_total_costs : array, purchase costs of all pumps in a vector
    pump_motor_purchase_costs_current : array, purchase costs of all motors of the pumps in a vector
    pump_purchase_costs_current : float, sum of the costs of all pumps and motors
    pump_head : array, pump head of all pumps stored in a vector (meters)
    pump_flowrate : array,pump flowrate of all pumps in a vector (in m3/s) 
