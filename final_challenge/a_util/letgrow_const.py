COLID_MAP_NAME = {
    'tair':1593811,
    'rh':1593815,
    'co2':1593819,
    'dx':1593823,
    'vent_lee':1593827,
    'vent_wind':1593831,
    't_rail':1593835,
    'par':1593839,
    'lamps':1593843,
    'scr_enrg':1593845,
    'scr_blck':1593849,
    'co2_reg':1593853,
    'heating_temp_vip':1593857,
    'heating_temp_sp':1593775,
    'vent_templee_vip':1593861,
    'vent_tempwind_vip':1593865,
    'vent_temp_sp':1593779,
    'lee_wind_min_vip':1593869,
    'lee_vent_min_sp':1593783,
    'net_pipe_vip':1593873,
    'net_pipe_sp':1593787,
    'scr_enrg_vip':1593877,
    'scr_enrg_sp':1593791,
    'scr_blck_vip':1593881,
    'scr_blck_sp':1593795,
    'lamps_vip':1608458,
    'lamps_sp':1608460,
    'co2_vip':1593889,
    'co2_sp':1593803,
    'dx_vip':1593893,
    'dx_sp':1593807,
    'sigrow_par':1593485,
    'sigrow_tair':1593489,
    'sigrow_rh':1593493,
    'sigrow_stomata':1593497,
    'ridder_netrad':1593501,
    'ridder_transp':1593503,
    'ridder_leaftem':1593505,
    'plant_density':1602309,
    'day_of_harvest':1602310,
    'fc_tout':611680,
    'fc_rhout':611682,
    'fc_iglob':611684 ,
    'fc_radsum':611686,
    'fc_windsp':611688,
    'fc_cloud':611690,
    'out_tout':611644,
    'out_rhout':611648,  
    'out_iglob':611656,  
    'out_windsp':611660,  
    'out_radsum':611658,  
    'out_winddir':611664,  
    'out_rain':611668,  
    'out_parout':611672,  
    'out_pyrgeo':611676,  
    'out_abshumout':611640
}

COLID_MAP_NUMBER = inv_map = {str(v): k for k, v in COLID_MAP_NAME.items()} 

LETSGROW_CONTROL = ['heating_temp_sp','vent_tempwind_sp','vent_temp_sp','net_pipe_sp','scr_enrg_sp','scr_blck_sp','lamps_sp','co2_sp','dx_sp']

LETSGROW_MOD_COLS_MAP = {
    '42984' : [
                '1593811',
                '1593815',
                '1593819',
                '1593823',
                '1593827',
                '1593831',
                '1593835',
                '1593839',
                '1593843',
                '1593845',
                '1593849',
                '1593853',
                '1593857',
                '1593775',
                '1593861',
                '1593865',
                '1593779',
                '1593869',
                '1593783',
                '1593873',
                '1593787',
                '1593877',
                '1593791',
                '1593881',
                '1593795',
                '1608458',
                '1608460',
                '1593889',
                '1593803',
                '1593893',
                '1593807',
                '1602309',
                '1602310'
    ],
    '42975' : [
                '1593485',
                '1593489',
                '1593493',
                '1593497',
                '1593501',
                '1593503',
                '1593505'
    ],
    '14822' : [
                '611680',
                '611682',
                '611684',
                '611686',
                '611688'
    ],
    '14821' : [
                '611644',
                '611648',
                '611656',
                '611660',
                '611658',
                '611664',
                '611668',
                '611672',
                '611676',
                '611640'    
    ]
}

