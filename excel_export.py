# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:48:47 2024

@author: Lorenzo Bruno
"""

import realtime_main as rtm
import cvxpy as cp
import numpy as np
import pandas as pa
import function_list as ff


#def xlwriter_function():
class RESULTS:
    def __init__(self):
        self.pow_grid_plot_res = rtm.P_grid_plot            
        self.pow_ely_in_plot = rtm.P_ely_in_plot
        self.pow_ely_out_plot = rtm.P_ely_out_plot
        self.pow_ely_out_bur_plot = rtm.P_ely_out_bur_plot
        self.pow_comp_in_plot = rtm.P_comp_in_plot
        self.pow_comp_grid_plot = rtm.P_comp_grid_plot
        self.pow_tank_in_plot = rtm.P_tank_in_plot
        self.pow_tank_out_plot = rtm.P_tank_out_plot
        self.soc_tank_plot = rtm.soc_tank_plot
        self.pow_bur_in_plot = rtm.P_bur_in_plot 
        self.pow_pv_cost_overall_plot = rtm.P_pv_cost_overall_plot
        self.cost_ELY_overall_plot  = rtm.ELY_cost_overall_plot 
        
        self.pow_pv = rtm.P_pv
        self.cost_PV = rtm.PV_cost
        self.pow_hydro = rtm.P_hydro
        self.cost_HYDRO = rtm.HYDRO_cost
        self.pow_load_ele = rtm.P_load_ele
        self.price_grid_purchase = rtm.grid_price_purchase
        self.tot_cost  = rtm.tot_cost 
        self.pow_load_th = rtm.P_load_th
        self.P_comp_cost_plot = rtm.P_comp_cost_plot
        self.P_tank_cost_plot = rtm.P_tank_cost_plot
        self.cost_total_opt_plot = rtm.cost_total_opt_plot

        self.E_PV = rtm.E_PV
        self.E_HYDRO = rtm.E_HYDRO
        self.E_grid = rtm.E_grid
        self.E_load_electric = rtm.E_load_electric
        self.E_load_thermal = rtm.E_load_thermal
        self.mass_h2_tot = rtm.mass_h2_tot
        self.water_h2_tot = rtm.water_h2_tot
        self.E_ely_out = rtm.E_ely_out
        self.E_ely_out_bur = rtm.E_ely_out_bur
        self.E_comp_in = rtm.E_comp_in
        self.perc_h2_ely_out_bur = rtm.perc_h2_ely_out_bur
        self.perc_h2_comp_in = rtm.perc_h2_comp_in
        
        self.mass_h2 = rtm.mass_h2
        self.water_h2 = rtm.water_h2
    
results = RESULTS()

# ===============================================================================================================================================
## EXPORT THE VALUES FROM PYTHON TO EXCEL
# ===============================================================================================================================================
datadict = {} 
datadict['pow_grid_plot_res']= results.pow_grid_plot_res
datadict['pow_ely_in_plot']= results.pow_ely_in_plot
datadict['pow_ely_out_plot']= results.pow_ely_out_plot
datadict['pow_ely_out_bur_plot']= results.pow_ely_out_bur_plot
datadict['pow_comp_in_plot']= results.pow_comp_in_plot
datadict['pow_comp_grid_plot']= results.pow_comp_grid_plot
datadict['pow_tank_in_plot']= results.pow_tank_in_plot    
datadict['pow_tank_out_plot']= results.pow_tank_out_plot
datadict['soc_tank_plot']= results.soc_tank_plot
datadict['pow_bur_in_plot']= results.pow_bur_in_plot
datadict['pow_pv_cost_overall_plot']= results.pow_pv_cost_overall_plot
datadict['cost_ELY_overall_plot']= results.cost_ELY_overall_plot

datadict['pow_pv']= results.pow_pv[0:rtm.time_end-rtm.planning_horizon]
datadict['cost_PV']= results.cost_PV[0:rtm.time_end-rtm.planning_horizon]
datadict['pow_hydro']= results.pow_hydro[0:rtm.time_end-rtm.planning_horizon]
datadict['cost_HYDRO']= results.cost_HYDRO[0:rtm.time_end-rtm.planning_horizon]
datadict['pow_load_ele']= results.pow_load_ele[0:rtm.time_end-rtm.planning_horizon]
datadict['price_grid_purchase']= results.price_grid_purchase[0:rtm.time_end-rtm.planning_horizon]
datadict['tot_cost']= results.tot_cost
datadict['pow_load_th']= results.pow_load_th[0:rtm.time_end-rtm.planning_horizon]
datadict['P_comp_cost_plot']= results.P_comp_cost_plot
datadict['P_tank_cost_plot']= results.P_tank_cost_plot
datadict['cost_total_opt_plot']= results.cost_total_opt_plot

tabla_pow = pa.DataFrame(datadict, index=range(rtm.time_end-rtm.planning_horizon))

datadict_energy = {}
datadict_energy['E_PV'] = results.E_PV
datadict_energy['E_HYDRO'] = results.E_HYDRO
datadict_energy['E_grid'] = results.E_grid
datadict_energy['E_load_electric'] = results.E_load_electric
datadict_energy['E_load_thermal'] = results.E_load_thermal
datadict_energy['mass_h2_tot'] = results.mass_h2_tot
datadict_energy['water_h2_tot'] = results.water_h2_tot
datadict_energy['E_ely_out'] = results.E_ely_out
datadict_energy['E_ely_out_bur'] = results.E_ely_out_bur
datadict_energy['E_comp_in'] = results.E_comp_in
datadict_energy['perc_h2_ely_out_bur'] = results.perc_h2_ely_out_bur
datadict_energy['perc_h2_comp_in'] = results.perc_h2_comp_in

tabla_energy = pa.DataFrame(datadict_energy, index=range(1)) #, 

datadict_mass = {}
datadict_mass['mass_h2'] = results.mass_h2
datadict_mass['water_h2'] = results.water_h2

tabla_mass = pa.DataFrame(datadict_mass, index=range(rtm.time_end-rtm.planning_horizon))


"""
costdict = [['pow_grid_plot_res',results.pow_grid_plot_res,'[kW]'],
            ['pow_ely_in_plot',results.pow_ely_in_plot,'[kW]'],
            ['pow_ely_out_plot',results.pow_ely_out_plot,'[kW]'],
            ['pow_ely_out_bur_plot',results.pow_ely_out_bur_plot,'[kW]'],
            ['pow_comp_in_plot',results.pow_comp_in_plot,'[kW]'],
            ['pow_comp_grid_plot',results.pow_comp_grid_plot,'[kW]'],                
            ['pow_tank_in_plot',results.pow_tank_in_plot,'[kW]'],
            ['pow_tank_out_plot',results.pow_tank_out_plot,'[kW]'],
            ['soc_tank_plot',results.soc_tank_plot,'[kW]'],
            ['pow_bur_in_plot',results.pow_bur_in_plot,'[kW]'],
            ['pow_pv_cost_overall_plot',results.pow_pv_cost_overall_plot,'[kW]'],                
            ['cost_ELY_overall_plot',results.cost_ELY_overall_plot,'[kW]'],
            
            ['opex_fix_act_cp',results.opex_fix_act_cp_res,'[€]'],
            ['opex_fix_act_ht',results.opex_fix_act_ht_res,'[€]'],
            ['opex_fix_act_bur',results.opex_fix_act_bur_res,'[€]'],                
            ['tot_OPEX_fix_act',results.tot_OPEX_fix_act_res,'[€]'],                                
            ['tot_OPEX_var',results.tot_OPEX_var_res,'[€]'],
            ['tot_OPEX_var_act',results.tot_OPEX_var_act_res,'[€]'],                                
            ['supply_grid_elec',results.supply_grid_elec_res,'[€]'],
            ['supply_capex_pv',results.supply_capex_pv_res,'[€]'],
            ['supply_opex_pv',results.supply_opex_pv_res,'[€]'],
            ['tot_SUPPLY_year',results.tot_SUPPLY_year_res,'[€]'],                
            ['supply_grid_elec_act',results.supply_grid_elec_act_res,'[€]'],
            ['supply_opex_pv_act',results.supply_opex_pv_act_res,'[€]'],
            ['tot_SUPPLY act',results.tot_SUPPLY_year_act_res,'[€]'],                 
            ['install_ele',results.install_ele_res,'[€]'],
            ['install_ht',results.install_ht_res,'[€]'],
            ['tot_INSTALL',results.tot_INSTALL_res,'[€]'],                
            ['tot_REPLACE',results.tot_REPLACE_res,'[€]'],
            ['tot_REPLACE_disc_res',results.tot_REPLACE_disc_res,'[€]'],                                
            ['operational_year',results.operational_year_res,'[€]'],                
            ['tot_OPEX_disc',results.tot_OPEX_disc_res,'[€]'],
            ['tot_C_res',results.tot_C_res,'[€]']
            ]

tabla_cost = pa.DataFrame(costdict, columns=['name','value','unit'])


indexdict = [['LCOE',LCOE,'[€/kWh]'],
            ['LCOH',LCOH,'[€/kg]'],
            ['ECI_tot',ECI_tot,'[g_CO2]']]
tabla_index = pd.DataFrame(indexdict, columns=['name','value','unit'])
"""
#elecdict = {} 
#elecdict['cost_elec']= cost_elec
#tabla_costelec = pd.DataFrame(elecdict, index=par.time_vec)

with pa.ExcelWriter('RESULTS_WP3_scenario4_05.xlsx') as writer:
    tabla_pow.to_excel(writer, sheet_name='power values')
    tabla_energy.to_excel(writer, sheet_name='energy values')
    tabla_mass.to_excel(writer, sheet_name='mass values')
    # tabla_index.to_excel(writer, sheet_name='index values')
    # tabla_costelec.to_excel(writer, sheet_name='cost elect values')

    # return results # LCOE, LCOH, ECI_tot,
