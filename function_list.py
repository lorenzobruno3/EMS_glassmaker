            # -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:12:15 2024

@author: Lorenzo Bruno
"""
import cvxpy as cp
import numpy as np
import pandas as pa
import numpy as np

# =============================================================================
# PV DATA
# =============================================================================
def function_dataPV(time_end):
    dataPV = pa.read_excel("PV_timeseries_avignon.xlsx", sheet_name="PV_irradiance_Wm2")
    def dict_func(xx):
        dict_build = {}
        dict_build = {ii: xx.iloc[ii, 1]/1e3*14.400 for ii in range(0,time_end)}          #[W/m2]*[kW/W]*[m2]=[] where AREA = 14.400 m2 
        return dict_build
    PV_dict = dict_func(dataPV)
    PV = []
    for ii in range(time_end):
        PV.append(PV_dict[ii])    
    return PV
def function_PV_cost(time_end):
    dataPV_cost = pa.read_excel("PV_timeseries_avignon.xlsx", sheet_name="PV_opex_€kW")
    def dict_func_PV_cost(xx):
        dict_build_PV_cost = {}
        dict_build_PV_cost = {ii: xx.iloc[ii, 1] for ii in range(0,time_end)}          #[€/kW] 
        return dict_build_PV_cost
    PV_cost_dict = dict_func_PV_cost(dataPV_cost)
    PV_cost = []
    for ii in range(time_end):
        PV_cost.append(PV_cost_dict[ii])    
    return PV_cost
# =============================================================================
# HYDRO DATA
# =============================================================================
def function_dataHYDRO(time_end):
    dataHYDRO = pa.read_excel("HYDRO_timeseries_avignon.xlsx", sheet_name="HYDRO_capacity_kWh")
    def dict_func(xx):
        dict_build = {}
        dict_build = {ii: xx.iloc[ii, 1]/1 for ii in range(0,time_end)}          #[kW] 
        return dict_build
    HYDRO_dict = dict_func(dataHYDRO)
    HYDRO = []
    for ii in range(time_end):
        HYDRO.append(HYDRO_dict[ii])    
    return HYDRO
def function_HYDRO_cost(time_end):
    dataHYDRO_cost = pa.read_excel("HYDRO_timeseries_avignon.xlsx", sheet_name="HYDRO_opex_€kW")
    def dict_func_HYDRO_cost(xx):
        dict_build_HYDRO_cost = {}
        dict_build_HYDRO_cost = {ii: xx.iloc[ii, 1] for ii in range(0,time_end)}          #[€/kW]
        return dict_build_HYDRO_cost
    HYDRO_cost_dict = dict_func_HYDRO_cost(dataHYDRO_cost)
    HYDRO_cost = []
    for ii in range(time_end):
        HYDRO_cost.append(HYDRO_cost_dict[ii])    
    return HYDRO_cost
# =============================================================================
# GRID PURCHASE
# =============================================================================
def function_grid_price_purchase(time_end):
    dataGRIDCOST = pa.read_excel("cost_france_2023_real.xlsx", sheet_name="cost_france_2023_real")
    # dataGRIDCOST = pa.read_excel("cost_france_2023_hour.xlsx", sheet_name="cost_france_2023_hour")
    def dict_func(xx):
        dict_build_gridcost_pur = {}
        dict_build_gridcost_pur = {ii: xx.iloc[ii, 0] for ii in range(0,time_end)}          #[€/kWhe]
        return dict_build_gridcost_pur
    GRIDCOST_PUR_dict = dict_func(dataGRIDCOST)
    GRIDCOST_PUR = []
    for ii in range(time_end):
        GRIDCOST_PUR.append(GRIDCOST_PUR_dict[ii])    
    return GRIDCOST_PUR
# =============================================================================
# ELECTRICAL LOAD
# =============================================================================
def function_loadSET_ele(time_end):
    loadSET_ele = pa.read_excel("syndata_load_electric_WP3.xlsx", sheet_name="syndata_load_electric_kW")        # THESE are the synthetic DATA
    def dict_func_ele(xx):
        dict_build_ele = {}
        dict_build_ele = {ii: xx.iloc[ii, 0] for ii in range(0,time_end)}          #[kW]
        return dict_build_ele
    load_dict_ele = dict_func_ele(loadSET_ele)
    load_ele = []
    for ii in range(time_end):
       load_ele.append(load_dict_ele[ii])
    return load_ele
# =============================================================================
# THERMAL LOAD
# =============================================================================
def function_loadSET_th(time_end):
    loadSET_th = pa.read_excel("syndata_load_thermal_WP3.xlsx", sheet_name="syndata_load_thermal_kW")
    def dict_func_th(xx):
        dict_build_th = {}
        dict_build_th = {ii: xx.iloc[ii, 0] for ii in range(0,time_end)}          #[kW]
        return dict_build_th
    load_dict_th = dict_func_th(loadSET_th)
    load_th = []
    for ii in range(time_end):
       load_th.append(load_dict_th[ii])
    return load_th
def function_burner_th(time_end):
    burner_set_th = pa.read_excel("burner_load_thermal.xlsx", sheet_name="burner_efficiency")
    def dict_func_burner_th(xx):
        dict_build_burner_th = {}
        dict_build_burner_th = {ii: xx.iloc[ii, 0] for ii in range(0,time_end)}          #[kW]
        return dict_build_burner_th
    load_dict_burner_th = dict_func_burner_th(burner_set_th)
    burner_th_eff = []
    for ii in range(time_end):
       burner_th_eff.append(load_dict_burner_th[ii])
    return burner_th_eff
# =============================================================================
# ELECTROLYSER
# =============================================================================
# OPERABILITY RANGE 1-100 AAAAAAAAAAAAAAAAAAAAAAA
class elyclass(object):
    def __init__(self, planning_horizon, info, tipo): #rated_power, efficiency, low_range, high_range, pressure, stack_lifetime, bop_lifetime, CAPEX, OPEX_fix, OPEX_var, installation_cost, replacement_cost, LCOE, LCOH):
        self.tipo = tipo
        self.planning_horizon = planning_horizon
        self.rated_power = info["rated_power"]                                      # [kW]
        self.efficiency = info["efficiency"]
        self.low_range = info["low_range"]
        self.high_range = info["high_range"]                                      # [kW]
        self.pressure = info["pressure"]
        self.stack_lifetime = info["stack_lifetime"]
        self.bop_lifetime = info["bop_lifetime"]                                      # [kW]
        self.CAPEX = info["CAPEX"]
        self.OPEX_fix = info["OPEX_fix"]
        self.OPEX_var = info["OPEX_var"]                                      # [kW]
        self.installation_cost = info["installation_cost"]
        self.replacement_cost = info["replacement_cost"]
        self.LCOE = info["LCOE"]
        self.LCOH = info["LCOH"]
        self.RAMP = info["RAMP"]
        self.c_ON = info["c_ON"]/1000                                      # [EUR/kWh]
        self.c_STB = info["c_STB"]/1000                                      # [EUR/kWh]
        self.c_OFF = info["c_OFF"]/1000                                      # [EUR/kWh]
        self.c_STB_ON = info["c_STB_ON"]                                # [EUR]
        self.c_ON_STB = info["c_ON_STB"]                                      # [EUR]
        self.c_STB_OFF = info["c_STB_OFF"]                                      # [EUR]
        self.c_OFF_STB = info["c_OFF_STB"]                                      # [EUR]
        self.c_OFF_ON = info["c_OFF_ON"]                                      # [EUR]
        self.c_ON_OFF = info["c_ON_OFF"]                                      # [EUR]
        self.P_ely_0 = info["P_ely_0"]                                      # [kW]
        self.P_ely_STB = info["P_ely_STB"]                                      # [kW]
        self.P_ely_ON_min = info["P_ely_ON_min"]                                      # [kW]
        self.P_ely_in = cp.Variable(planning_horizon, nonneg=True)
        self.P_ely_out = cp.Variable(planning_horizon, nonneg=True)
        self.power_prev = cp.Parameter(value=0, nonneg=True)
        self.DeltaOFF  = cp.Variable(self.planning_horizon, boolean=True, name="DeltaOFF", value=np.ones(self.planning_horizon))
        self.DeltaSTB  = cp.Variable(self.planning_horizon, boolean=True, name="DeltaSTB", value=np.zeros(self.planning_horizon))
        self.DeltaON  = cp.Variable(self.planning_horizon, boolean=True, name="DeltaON", value=np.zeros(self.planning_horizon))
        self.SigmaOFFSTB = cp.Variable(self.planning_horizon, boolean=True, name="SigmaOFFSTB")  #[STATE TRANSITIONS] Defining state transitions
        self.SigmaSTBOFF = cp.Variable(self.planning_horizon, boolean=True, name="SigmaSTBOFF")
        self.SigmaSTBON = cp.Variable(self.planning_horizon, boolean=True, name="SigmaSTBON")
        self.SigmaONSTB = cp.Variable(self.planning_horizon, boolean=True, name="SigmaONSTB")
        self.SigmaOFFON = cp.Variable(self.planning_horizon, boolean=True, name="SigmaOFFON") #FOR THIS WE SHOULD FIX A CONDITION BEFORE 
        self.SigmaONOFF = cp.Variable(self.planning_horizon, boolean=True, name="SigmaONOFF")
        self.power_standby = cp.Variable(planning_horizon, nonneg=True)
        
        

    def get_constraints_MOMO(self, P_0, P_STB, P_ON, P_max, M, d_0_OFFely, d_0_STBely, d_0_ONely):
        
        # [Power] THIS I DON'T UNDERSTAND FULLY
        self.power_ely = self.P_ely_in
        
        #Set up optimization
        constraints = []
        
        ###### Define k --- control horizon
        for k in range(self.planning_horizon):
            
            if k > 0:
                # Electrolyzer
                DeltaOFFprev_ely = self.DeltaOFF[k - 1]
                DeltaSTBprev_ely = self.DeltaSTB[k - 1]
                DeltaONprev_ely = self.DeltaON[k - 1]
                
            else:
                # Electrolyzer
                DeltaOFFprev_ely = d_0_OFFely
                DeltaSTBprev_ely = d_0_STBely
                DeltaONprev_ely = d_0_ONely
                #print(DeltaOFFprev_ely, DeltaSTBprev_ely, DeltaONprev_ely)
                #self.DeltaOFF[k] <= DeltaOFFprev_ely
                #self.DeltaOFF[k] >= DeltaOFFprev_ely
                #self.DeltaOFF[k] == d_0_OFFely
                ####################print(self.DeltaOFF[k].value)
                #self.DeltaSTB[k] <= DeltaSTBprev_ely
                #self.DeltaSTB[k] >= DeltaSTBprev_ely
                #self.DeltaSTB[k] == d_0_STBely
                ####################print(self.DeltaSTB[k].value)
                #self.DeltaON[k] <= DeltaONprev_ely 
                #self.DeltaON[k] >= DeltaONprev_ely
                #self.DeltaON[k] == d_0_ONely
                ####################print(self.DeltaON[k].value)
                #self.DeltaSTB[k] + self.DeltaON[k] + self.DeltaOFF[k] == 1 
                ####################print(self.DeltaSTB[k] + self.DeltaON[k] + self.DeltaOFF[k])
                
            # ONE STATE AT THE TIME
            constraints.append( self.DeltaSTB[k] + self.DeltaON[k] + self.DeltaOFF[k] == 1 )
            
            # ABSOLUTE VALUE:     
            constraints.append( self.power_ely[k] <= P_max*self.DeltaON[k] +  P_0*self.DeltaOFF[k] ) #+  P_STB*self.DeltaSTB[k]
            constraints.append( self.power_ely[k] >= P_ON*self.DeltaON[k] + P_0*self.DeltaOFF[k] ) #+  P_STB*self.DeltaSTB[k]
            
            ####################print(self.DeltaOFF[0].value)
            ####################print(self.DeltaSTB[0].value)
            ####################print(self.DeltaON[0].value)
            
            constraints.append( self.power_standby[k] <= P_STB*self.DeltaSTB[k]) 
            constraints.append( self.power_standby[k] >= P_STB*self.DeltaSTB[k])
            
            # STATE TRANSITION
            constraints.append( self.SigmaONOFF[k] <= DeltaONprev_ely )
            constraints.append( self.SigmaONOFF[k] <= self.DeltaOFF[k] )
            constraints.append( self.SigmaONOFF[k] >= DeltaONprev_ely + self.DeltaOFF[k] -1 )  
            
            constraints.append( self.SigmaOFFON[k] <= DeltaOFFprev_ely )
            constraints.append( self.SigmaOFFON[k] <= self.DeltaON[k] )
            constraints.append( self.SigmaOFFON[k] >= DeltaOFFprev_ely + self.DeltaON[k] -1 )    
            
            constraints.append( self.SigmaOFFSTB[k] <= DeltaOFFprev_ely )
            constraints.append( self.SigmaOFFSTB[k] <= self.DeltaSTB[k] )
            constraints.append( self.SigmaOFFSTB[k] >= DeltaOFFprev_ely + self.DeltaSTB[k] -1 ) 
            
            constraints.append( self.SigmaSTBOFF[k] <= DeltaSTBprev_ely )
            constraints.append( self.SigmaSTBOFF[k] <= self.DeltaOFF[k] )
            constraints.append( self.SigmaSTBOFF[k] >= DeltaSTBprev_ely + self.DeltaOFF[k] -1 )                     
            
            constraints.append( self.SigmaONSTB[k] <= DeltaONprev_ely )
            constraints.append( self.SigmaONSTB[k] <= self.DeltaSTB[k] )
            constraints.append( self.SigmaONSTB[k] >= DeltaONprev_ely + self.DeltaSTB[k] -1 ) 
            
            constraints.append( self.SigmaSTBON[k] <= DeltaSTBprev_ely )
            constraints.append( self.SigmaSTBON[k] <= self.DeltaON[k] )
            constraints.append( self.SigmaSTBON[k] >= DeltaSTBprev_ely + self.DeltaON[k] -1 )    

            #power balance equation
            
            ####################print(self.DeltaOFF[0].value)
            ####################print(self.DeltaSTB[0].value)
            ####################print(self.DeltaON[0].value)
            
        return constraints
        
def function_electro1class(planning_horizon, electro_type):
    PEM_ely_set_sheet = pa.read_excel("electrolyser.xlsx", sheet_name=electro_type)
    def dict_func_PEM(xx):
        dict_build_PEM = {}
        dict_build_PEM = {xx.iloc[ii,0] : xx.iloc[ii, 1] for ii in range(0,27)}       
        return dict_build_PEM
    PEM_ely_set = dict_func_PEM(PEM_ely_set_sheet)
    
    electrolizador = elyclass(planning_horizon,PEM_ely_set,electro_type)
    return electrolizador
# =============================================================================
# COMPRESSOR
# =============================================================================
class compressorclass(object):
    def __init__(self, info, tipo): 
        self.tipo = tipo
        self.rated_power_kW = info["rated_power_kW"]                                        # [kW]
        self.compressor_work = info["compressor_work"]                                  # [-]
        self.pressure_ratio = info["pressure_ratio"]                                                    # [-]
        self.lifetime = info["lifetime"]                                                    # [yr]
        self.CAPEX = info["CAPEX"]                                                          # [€/kgH2]
        self.OPEX = info["OPEX"]                                                            # [€/kgH2]
        self.installation_cost = info["installation_cost"]                                  # [€/kgH2]
        self.replacement_cost = info["replacement_cost"]                                    # [€/kgH2]
        self.LCOE = info["LCOE"]                                                            # [€/kgH2]
        self.LCOH = info["LCOH"]                                                            # [€/kgH2]
        
def function_compressorclass(compressor_type):
    compressor_set_sheet = pa.read_excel("compressor.xlsx", sheet_name=compressor_type)
    def dict_func_compressor(xx):
        dict_build_compressor = {}
        dict_build_compressor = {xx.iloc[ii,0] : xx.iloc[ii, 1] for ii in range(0,10)}       
        return dict_build_compressor
    compressor_set = dict_func_compressor(compressor_set_sheet)
    
    compressor_h2 = compressorclass(compressor_set,compressor_type)
    return compressor_h2    
# =============================================================================
# TANK
# =============================================================================
class tankclass(object):
    def __init__(self, planning_horizon, info, tipo): 
        self.tipo = tipo
        self.planning_horizon = planning_horizon
        self.rated_capacity_kg = info["rated_capacity_kg"]/1000000000                                        # [kg]
        self.rated_capacity_kWh = info["rated_capacity_kWh"]                                      # [kWh]
        self.efficiency_charge = info["efficiency_charge"]                                  # [-]
        self.efficiency_discharge = info["efficiency_discharge"]                            # [-]
        self.soc_initial = info["soc_initial"]                                              # [-]
        self.soc_max = info["soc_max"]                                                      # [-]
        self.soc_min = info["soc_min"]                                                      # [-]
        self.pressure = info["pressure"]                                                    # [bar]
        self.lifetime = info["lifetime"]                                                    # [yr]
        self.CAPEX = info["CAPEX"]                                                          # [€/kgH2]
        self.OPEX = info["OPEX"]                                                            # [€/kgH2]
        self.installation_cost = info["installation_cost"]                                  # [€/kgH2]
        self.replacement_cost = info["replacement_cost"]                                    # [€/kgH2]
        self.LCOE = info["LCOE"]                                                            # [€/kgH2]
        self.LCOH = info["LCOH"]                                                            # [€/kgH2]
        self.soc = cp.Variable(planning_horizon, nonneg=True)
        self.P_tank_in = cp.Variable(planning_horizon, nonneg=True)
        self.P_tank_out = cp.Variable(planning_horizon, nonneg=True)
      
    def get_constraints(self):
        tank_constrains = []
        for t in range(self.planning_horizon):
            if t == 0:
                tank_constrains += [self.soc[t] == self.soc_initial*1.0]  #################### 
            else:
                tank_constrains += [self.soc[t] == self.soc[t-1] 
                                   + self.P_tank_in[t-1]*self.efficiency_charge/self.rated_capacity_kWh 
                                   - self.P_tank_out[t-1]/self.efficiency_discharge/self.rated_capacity_kWh,
                                   ]
        
        tank_constrains += [self.soc <= self.soc_max,
                            self.soc >= self.soc_min,
                            #Restricion sobre potencia de descarga
                            #Restricion sobre la maxima potencia de carga
                            ] #CONSTRAINTS
        return tank_constrains

    def update(self):
        self.soc_initial = self.soc[1].value

        
def function_tankclass(planning_horizon, tank_type):
    tank_set_sheet = pa.read_excel("tank.xlsx", sheet_name=tank_type)
    def dict_func_TANK(xx):
        dict_build_TANK = {}
        dict_build_TANK = {xx.iloc[ii,0] : xx.iloc[ii, 1] for ii in range(0,15)}       
        return dict_build_TANK
    TANK_set = dict_func_TANK(tank_set_sheet)
    
    tank_h2 = tankclass(planning_horizon, TANK_set, tank_type)
    return tank_h2
# =============================================================================
# ENVIRONMENTAL
# =============================================================================
class environmentalclass(object):
    def __init__(self, info, tipo):
        self.tipo = tipo
        self.carbon_cost_indirect = info["carbon_cost_indirect"]    # [€/kWh]
        self.carbon_cost = info["carbon_cost"]                      # [€/kgCO2]
        self.low_range = info["low_range"]
        self.high_range = info["high_range"]                                      # [kW]
        self.pressure = info["pressure"]
        self.stack_lifetime = info["stack_lifetime"]
        self.bop_lifetime = info["bop_lifetime"]                                      # [kW]
        self.CAPEX = info["CAPEX"]
        self.OPEX_fix = info["OPEX_fix"]
        self.OPEX_var = info["OPEX_var"]                                      # [kW]
        self.installation_cost = info["installation_cost"]
        self.replacement_cost = info["replacement_cost"]
        self.LCOE = info["LCOE"]
        self.LCOH = info["LCOH"]
        self.RAMP = info["RAMP"]
        self.ECI = info["ECI"]                                      # [kgCO2/kWh]
        
def function_environmentalclass(environmental_type):
    environmental_set_sheet = pa.read_excel("environmental.xlsx", sheet_name=environmental_type)
    def dict_func_environmental(xx):
        dict_build_environmental = {}
        dict_build_environmental = {xx.iloc[ii,0] : xx.iloc[ii, 1] for ii in range(0,16)}       
        return dict_build_environmental
    environmental_set = dict_func_environmental(environmental_set_sheet)
    
    environmental = environmentalclass(environmental_set,environmental_type)
    return environmental
# =============================================================================
# NATURAL GAS
# =============================================================================
def function_NG_cost(time_end):
    dataNG_cost = pa.read_excel("price_naturalgas.xlsx", sheet_name="naturalgas")
    def dict_func_NG_cost(xx):
        dict_build_NG_cost = {}
        dict_build_NG_cost = {ii: xx.iloc[ii+1, 1]*10 for ii in range(0,time_end)}          #[€/kWh*h]
        return dict_build_NG_cost
    NG_cost_dict = dict_func_NG_cost(dataNG_cost)
    NG_cost = []
    for ii in range(time_end):
        NG_cost.append(NG_cost_dict[ii])    
    return NG_cost























"""
lista=["PEM","SOEC","AEM"] 
test=list(map(function_electro1class,lista)) 
"""



def function_gridclass(time_end):
    class gridclass:
        def __init__(self, buy_price, sell_price):
            self.buy_price = buy_price
            self.sell_price = sell_price
    g_buy_price = []
    g_sell_price = []
    for ii in range(time_end):
        if ii <= round(time_end/3):
            g_buy_price.append(2*10)
            g_sell_price.append(1*10)
            
        elif ii > round(time_end/3) and ii <= round(time_end*2/3):  
            g_buy_price.append(5*10)
            g_sell_price.append(1*10)

        else:
            g_buy_price.append(1*10)
            g_sell_price.append(0.5*10)
    grid = gridclass(g_buy_price, g_sell_price)
    return grid
    ###########  GRID balance  ######################################################################
    #grid_buy_price = [2*10, 2*10, 5*10, 5*10, 1*10]
    #grid_sell_price = [1*10, 1*10, 1*10, 1*10, 0.5*10]



def get_battery_curves(time_end):
    batt1_max = []
    batt1_min = []
    batt1_cost = []
    for ii in range(time_end):
        if ii <= round(time_end/3):
            batt1_max.append(2*10)
            batt1_min.append(0.5*10)
            batt1_cost.append(0.1*10)
            
        elif ii > round(time_end/3) and ii <= round(time_end*2/3):  
            batt1_max.append(2*10)
            batt1_min.append(0.5*10)
            batt1_cost.append(0.1*10)

        else:
            batt1_max.append(2*10)
            batt1_min.append(0.5*10)
            batt1_cost.append(0.1*10)
    return  batt1_max, batt1_min, batt1_cost

    

class BatteryClass:
    def __init__(self, planning_horizon, efficiency_ch, efficiency_dis, soc_ini, soc_max,  soc_min, capacity):
        self.planning_horizon = planning_horizon
        self.maximo = cp.Parameter(planning_horizon)
        self.minimo = cp.Parameter(planning_horizon)
        self.cost = cp.Parameter(planning_horizon)
        self.efficiency_ch = efficiency_ch
        self.efficiency_dis = efficiency_dis
        self.soc_ini = soc_ini
        self.soc_max = soc_max
        self.soc_min = soc_min
        self.capacity = capacity
#        self.pp_class = cp.Variable(1)     #planning_horizon, nonneg=True
        self.P_ch_b1_class = cp.Variable(planning_horizon, nonneg=True)
        self.P_dis_b1_class = cp.Variable(planning_horizon, nonneg=True)
        self.soc = cp.Variable(planning_horizon, nonneg=True)
       
        
    def get_constraints(self):
        b_constraints = []
        for t in range(self.planning_horizon):
            if t == 0:
                b_constraints += [self.soc[t] == self.soc_ini]                           # b1_soc_ini
            else:
                b_constraints += [self.soc[t] == self.soc[t-1] 
                                  + self.P_ch_b1_class[t - 1]*self.efficiency_ch/self.capacity   # b1_ef_ch/b1_capacity
                                  - self.P_dis_b1_class[t - 1]/self.efficiency_dis/self.capacity  # b1_ef_dis/b1_capacity                   
                                  ]
        b_constraints += [self.soc <= self.soc_max, 
                          self.soc >= self.soc_min,
                          -self.P_ch_b1_class + self.P_dis_b1_class <= self.maximo,
                          -self.P_ch_b1_class + self.P_dis_b1_class >= self.minimo]         # b1_soc_max,
        
        return b_constraints
        

    def get_cost(self):
        return self.P_dis_b1_class @ self.cost
    
    def update_parameters(self, minimo, maximo, cost):
        self.minimo.value = minimo
        self.maximo.value = maximo
        self.cost.value = cost

    ##########  definition of BATTERY as a CLASS  ######################################################################
    #class battery:
    #    def __init__(self, max, min, cost, ef_ch, ef_dis, soc_ini, soc_max, 
    #                 soc_min, capacity):
    #        self.max = max
    #        self.min = min
    #        self.cost = cost
    #        self.ef_ch = ef_ch
    #        self.ef_dis = ef_dis
    #        self.soc_ini = soc_ini
    #        self.soc_max = soc_max
    #        self.soc_min = soc_min
    #        self.capacity = capacity
            
    #b1 = battery(np.array([2*10, 2*10, 2*10, 2*10, 2*10]), np.array([0*10, 0*10, 0*10, 0*10, 0*10]), 
    #             [0.1*10, 0.1*10, 0.1*10, 0.1*10, 0.1*10], 0.9*10, 0.92*10, 0.5*10, 0.8*10, 0.2*10, 10*10)
    #b1_max = b1.max
    #b1_min = b1.min
    #b1_cost = b1.cost
    #b1_ef_ch = b1.ef_ch
    #b1_ef_dis = b1.ef_dis
    #b1_soc_ini = b1.soc_ini
    #b1_soc_max = b1.soc_max
    #b1_soc_min = b1.soc_min
    #b1_capacity = b1.capacity

    #def get_constraints(self):
    #    func_constraints = [self.pp_class <= self.maximo,
    #                   self.p >= self.p_min]
    #    return func_constraints
    

    
    
    
    
    
