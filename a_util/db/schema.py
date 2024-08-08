create_measure_table_query = """
-- auto-generated definition
create table measure
(
    time              timestamp not null
        constraint measure_pkey
            primary key,
    SP_plantdensity                                  double precision,
    SP_day_of_harvest_day_number                     double precision,
    SP_heating_temp_setpoint_5min                    double precision,
    SP_vent_ilation_temp_setpoint_5min               double precision,
    SP_leeside_minvent_position_setpoint_5min        double precision,
    SP_net_pipe_minimum_setpoint_5min                double precision,
    SP_Value_to_iSii_1_5min                          double precision,
    SP_energy_screen_setpoint_5min                   double precision,
    SP_blackout_screen_setpoint_5min                 double precision,
    SP_CO2_setpoint_ppm_5min                         double precision,
    SP_humidity_deficit_setpoint_5min                double precision,
    SP_irrigation_interval_time_setpoint_min_5min    double precision,
    temperature_greenhouse_5min                      double precision,
    temperature_greenhouse                           double precision,
    temperature_greenhouse_day                       double precision,
    temperature_greenhousenight                      double precision,
    RH_greenhouse_5min                               double precision,
    RH_greenhouse                                    double precision,
    RH_greenhouse_day                                double precision,
    RH_greenhousenight                               double precision,
    CO2_greenhouse_ppm_5min                          double precision,
    CO2_greenhouse_ppm                               double precision,
    CO2_greenhouse_ppm_day                           double precision,
    CO2_greenhouse_ppm_night                         double precision,
    humidity_deficit_greenhouse_5min                 double precision,
    humidity_deficit_greenhouse                      double precision,
    humidity_deficit_greenhouse_day                  double precision,
    humidity_deficit_greenhouse_night                double precision,
    vent_lee_5min                                    double precision,
    vent_lee                                         double precision,
    vent_lee_day                                     double precision,
    vent_leenight                                    double precision,
    vent_wind_5min                                   double precision,
    vent_wind                                        double precision,
    vent_wind_day                                    double precision,
    vent_wind_night                                  double precision,
    lower_circuit_5min                               double precision,
    lower_circuit                                    double precision,
    lower_circuit_day                                double precision,
    lower_circuitnight                               double precision,
    energy_curtain_5min                              double precision,
    energy_curtain                                   double precision,
    energy_curtain_day                               double precision,
    energy_curtainnight                              double precision,
    blackout_curtain_5min                            double precision,
    blackout_curtain                                 double precision,
    blackout_curtain_day                             double precision,
    blackout_curtainnight                            double precision,
    CO2_actuation_regulation_5min                    double precision,
    CO2_actuation_regulation                         double precision,
    CO2_actuation_regulation_day                     double precision,
    CO2_actuation_regulationnight                    double precision,
    CO2_dosagesum_24h_5min                           double precision,
    CO2_dosagesum_24h                                double precision,
    CO2_dosagesum_24h_day                            double precision,
    CO2_dosagesum_24hnight                           double precision,
    water_supply_minutes_5min                        double precision,
    water_supply_minutes                             double precision,
    drain_5min                                       double precision,
    drain                                            double precision,
    drain_EC_5min                                    double precision,
    drain_EC                                         double precision,
    drain_EC_day                                     double precision,
    drain_EC_night                                   double precision,
    drain_pH_5min                                    double precision,
    drain_pH                                         double precision,
    drain_pH_day                                     double precision,
    drain_pH_night                                   double precision,
    heating_temp_ViP_5min                            double precision,
    heating_temp_ViP                                 double precision,
    heating_temp_ViP_day                             double precision,
    heating_temp_ViP_night                           double precision,
    heating_temp_setpoint                            double precision,
    heating_temp_setpoint_day                        double precision,
    heating_temp_setpoint_night                      double precision,
    vent_ilation_temp_leeside_ViP_5min               double precision,
    vent_ilation_temp_leeside_ViP                    double precision,
    vent_ilation_temp_leeside_ViP_day                double precision,
    vent_ilation_temp_leeside_ViP_night              double precision,
    vent_ilation_tempwind_side_ViP_5min              double precision,
    vent_ilation_tempwind_side_ViP                   double precision,
    vent_ilation_tempwind_side_ViP_day               double precision,
    vent_ilation_tempwind_side_ViP_night             double precision,
    vent_ilation_temp_setpoint                       double precision,
    vent_ilation_temp_setpoint_day                   double precision,
    vent_ilation_temp_setpoint_night                 double precision,
    leeside_window_position_minimum_ViP_5min         double precision,
    leeside_window_position_minimum_ViP              double precision,
    leeside_window_position_minimum_ViP_day          double precision,
    leeside_window_position_minimum_ViP_night        double precision,
    leeside_minvent_position_setpoint                double precision,
    leeside_minvent_position_setpoint_day            double precision,
    leeside_minvent_position_setpoint_night          double precision,
    net_pipe_minimum_ViP_5min                        double precision,
    net_pipe_minimum_ViP                             double precision,
    net_pipe_minimum_ViP_day                         double precision,
    net_pipe_minimum_ViP_night                       double precision,
    net_pipe_minimum_setpoint                        double precision,
    net_pipe_minimum_setpoint_day                    double precision,
    net_pipe_minimum_setpoint_night                  double precision,
    Value_in_iSii_1_5min                             double precision,
    Value_in_iSii_1                                  double precision,
    Value_to_iSii_1                                  double precision,
    energy_screen_ViP_screen_position_5min           double precision,
    energy_screen_ViP_screen_position                double precision,
    energy_screen_ViP_screen_position_day            double precision,
    energy_screen_ViP_screen_position_night          double precision,
    energy_screen_setpoint                           double precision,
    energy_screen_setpoint_day                       double precision,
    energy_screen_setpoint_night                     double precision,
    blackout_screen_ViP_screen_position_5min         double precision,
    blackout_screen_ViP_screen_position              double precision,
    blackout_screen_ViP_screen_position_day          double precision,
    blackout_screen_ViP_screen_position_night        double precision,
    blackout_screen_setpoint                         double precision,
    blackout_screen_setpoint_day                     double precision,
    blackout_screen_setpoint_night                   double precision,
    CO2_ViP_ppm_5min                                 double precision,
    CO2_ViP_ppm                                      double precision,
    CO2_ViP_ppm_day                                  double precision,
    CO2_ViP_ppm_night                                double precision,
    CO2_setpoint_ppm                                 double precision,
    CO2_setpoint_ppm_day                             double precision,
    CO2_setpoint_ppm_night                           double precision,
    humidity_deficit_ViP_5min                        double precision,
    humidity_deficit_ViP                             double precision,
    humidity_deficit_ViP_day                         double precision,
    humidity_deficit_ViP_night                       double precision,
    humidity_deficit_setpoint                        double precision,
    humidity_deficit_setpoint_day                    double precision,
    humidity_deficit_setpoint_night                  double precision,
    water_supply_interval_time_ViP_min_5min          double precision,
    water_supply_interval_time_ViP_min               double precision,
    irrigation_interval_time_setpoint_min            double precision,
    Writeto_iSii_5min                                double precision,
    Writeto_iSii                                     double precision,
    outside_temperature_5min                         double precision,
    outside_temperature                              double precision,
    outside_temperature_day                          double precision,
    outside_temperature_night                        double precision,
    outside_temperature_long_standing_average        double precision,
    outside_RH_5min                                  double precision,
    outside_RH                                       double precision,
    outside_RH_day                                   double precision,
    outside_RH_night                                 double precision,
    humidity_deficit_outside_5min                    double precision,
    humidity_deficit_outside                         double precision,
    humidity_deficit_outside_day                     double precision,
    humidity_deficit_outside_night                   double precision,
    absolute_humidity_content_outside_air_5min       double precision,
    absolute_humidity_content_outside_air            double precision,
    absolute_humidity_content_outside_air_day        double precision,
    absolute_humidity_content_outside_airnight       double precision,
    radiation_5min                                   double precision,
    radiation                                        double precision,
    radiation_sum_5min                               double precision,
    radiation_sum                                    double precision,
    radiation_sum_longstanding_average               double precision,
    wind_speed_5min                                  double precision,
    wind_speed                                       double precision,
    wind_speed_day                                   double precision,
    wind_speednight                                  double precision,
    wind_direction_type                              double precision,
    wind_direction_registration_5min                 double precision,
    wind_direction_registration                      double precision,
    wind_direction_registration_day                  double precision,
    wind_direction_registrationnight                 double precision,
    wind_direction_5min                              double precision,
    wind_direction                                   double precision,
    wind_direction_day                               double precision,
    wind_direction_night                             double precision,
    rain_5min                                        double precision,
    rain                                             double precision,
    rain_day                                         double precision,
    rain_night                                       double precision,
    WE_PAR_outside_measurement_5min                  double precision,
    WE_PAR_outside_measurement                       double precision,
    WE_PAR_outside_measurement_day                   double precision,
    WE_PAR_outside_measurementnight                  double precision,
    WE_heat_emission_pyrgeometer_5min                double precision,
    WE_heat_emission_pyrgeometer                     double precision,
    WE_heat_emission_pyrgeometer_day                 double precision,
    WE_heat_emission_pyrgeometernight                double precision,
    WE_netto_radiation_calc_5min                     double precision,
    WE_netto_radiation_calc                          double precision,
    FC_outside_temperature_5min                      double precision,
    FC_outside_temperature                           double precision,
    FC_outside_RH_5min                               double precision,
    FC_outside_RH                                    double precision,
    FC_radiation_5min                                double precision,
    FC_radiation                                     double precision,
    FC_radiation_sum_5min                            double precision,
    FC_radiation_sum                                 double precision,
    FC_wind_speed_5min                               double precision,
    FC_wind_speed                                    double precision,
    FC_degree_of_cloudiness18_5min                   double precision,
    FC_degree_of_cloudiness18                        double precision
);

alter table measure
    owner to postgres;

"""

create_simulation_table_query = """
-- auto-generated definition
create table simulation
(
    time              timestamp not null
        constraint simulation_pkey
            primary key,
    comp1_air_t                                      double precision,
    comp1_air_rh                                     double precision,
    comp1_air_ppm                                    double precision,
    common_iglob_value                               double precision,
    common_tout_value                                double precision,
    common_rhout_value                               double precision,
    common_windsp_value                              double precision,
    comp1_parsensor_above                            double precision,
    comp1_tpipe1_value                               double precision,
    comp1_conpipes_tsupipe1                          double precision,
    comp1_pconpipe1_value                            double precision,
    comp1_conwin_winlee                              double precision,
    comp1_conwin_winwnd                              double precision,
    comp1_setpoints_spheat                           double precision,
    comp1_setpoints_spvent                           double precision,
    comp1_scr1_pos                                   double precision,
    comp1_scr2_pos                                   double precision,
    comp1_lmp1_elecuse                               double precision,
    comp1_mcpureair_value                            double precision,
    comp1_setpoints_spco2                            double precision,
    comp1_growth_fruitfreshweight                    double precision,
    comp1_growth_dvsfruit                            double precision,
    comp1_growth_drymatterfract                      double precision,
    comp1_growth_cropabs                             double precision,
    comp1_growth_plantdensity                        double precision,
    common_elecprice_peakhour                        double precision,
    comp1_growth_wateruseperpot                      double precision,
    comp1_growth_redfruitsweight                     double precision,
    SP_plantdensity                                  double precision,
    SP_day_of_harvest_day_number                     double precision,
    SP_heating_temp_setpoint_5min                    double precision,
    SP_vent_ilation_temp_setpoint_5min               double precision,
    SP_leeside_minvent_position_setpoint_5min        double precision,
    SP_net_pipe_minimum_setpoint_5min                double precision,
    SP_Value_to_iSii_1_5min                          double precision,
    SP_energy_screen_setpoint_5min                   double precision,
    SP_blackout_screen_setpoint_5min                 double precision,
    SP_CO2_setpoint_ppm_5min                         double precision,
    SP_humidity_deficit_setpoint_5min                double precision,
    SP_irrigation_interval_time_setpoint_min_5min    double precision,
    temperature_greenhouse_5min                      double precision,
    temperature_greenhouse                           double precision,
    temperature_greenhouse_day                       double precision,
    temperature_greenhousenight                      double precision,
    RH_greenhouse_5min                               double precision,
    RH_greenhouse                                    double precision,
    RH_greenhouse_day                                double precision,
    RH_greenhousenight                               double precision,
    CO2_greenhouse_ppm_5min                          double precision,
    CO2_greenhouse_ppm                               double precision,
    CO2_greenhouse_ppm_day                           double precision,
    CO2_greenhouse_ppm_night                         double precision,
    humidity_deficit_greenhouse_5min                 double precision,
    humidity_deficit_greenhouse                      double precision,
    humidity_deficit_greenhouse_day                  double precision,
    humidity_deficit_greenhouse_night                double precision,
    vent_lee_5min                                    double precision,
    vent_lee                                         double precision,
    vent_lee_day                                     double precision,
    vent_leenight                                    double precision,
    vent_wind_5min                                   double precision,
    vent_wind                                        double precision,
    vent_wind_day                                    double precision,
    vent_wind_night                                  double precision,
    lower_circuit_5min                               double precision,
    lower_circuit                                    double precision,
    lower_circuit_day                                double precision,
    lower_circuitnight                               double precision,
    energy_curtain_5min                              double precision,
    energy_curtain                                   double precision,
    energy_curtain_day                               double precision,
    energy_curtainnight                              double precision,
    blackout_curtain_5min                            double precision,
    blackout_curtain                                 double precision,
    blackout_curtain_day                             double precision,
    blackout_curtainnight                            double precision,
    CO2_actuation_regulation_5min                    double precision,
    CO2_actuation_regulation                         double precision,
    CO2_actuation_regulation_day                     double precision,
    CO2_actuation_regulationnight                    double precision,
    CO2_dosagesum_24h_5min                           double precision,
    CO2_dosagesum_24h                                double precision,
    CO2_dosagesum_24h_day                            double precision,
    CO2_dosagesum_24hnight                           double precision,
    water_supply_minutes_5min                        double precision,
    water_supply_minutes                             double precision,
    drain_5min                                       double precision,
    drain                                            double precision,
    drain_EC_5min                                    double precision,
    drain_EC                                         double precision,
    drain_EC_day                                     double precision,
    drain_EC_night                                   double precision,
    drain_pH_5min                                    double precision,
    drain_pH                                         double precision,
    drain_pH_day                                     double precision,
    drain_pH_night                                   double precision,
    heating_temp_ViP_5min                            double precision,
    heating_temp_ViP                                 double precision,
    heating_temp_ViP_day                             double precision,
    heating_temp_ViP_night                           double precision,
    heating_temp_setpoint                            double precision,
    heating_temp_setpoint_day                        double precision,
    heating_temp_setpoint_night                      double precision,
    vent_ilation_temp_leeside_ViP_5min               double precision,
    vent_ilation_temp_leeside_ViP                    double precision,
    vent_ilation_temp_leeside_ViP_day                double precision,
    vent_ilation_temp_leeside_ViP_night              double precision,
    vent_ilation_tempwind_side_ViP_5min              double precision,
    vent_ilation_tempwind_side_ViP                   double precision,
    vent_ilation_tempwind_side_ViP_day               double precision,
    vent_ilation_tempwind_side_ViP_night             double precision,
    vent_ilation_temp_setpoint                       double precision,
    vent_ilation_temp_setpoint_day                   double precision,
    vent_ilation_temp_setpoint_night                 double precision,
    leeside_window_position_minimum_ViP_5min         double precision,
    leeside_window_position_minimum_ViP              double precision,
    leeside_window_position_minimum_ViP_day          double precision,
    leeside_window_position_minimum_ViP_night        double precision,
    leeside_minvent_position_setpoint                double precision,
    leeside_minvent_position_setpoint_day            double precision,
    leeside_minvent_position_setpoint_night          double precision,
    net_pipe_minimum_ViP_5min                        double precision,
    net_pipe_minimum_ViP                             double precision,
    net_pipe_minimum_ViP_day                         double precision,
    net_pipe_minimum_ViP_night                       double precision,
    net_pipe_minimum_setpoint                        double precision,
    net_pipe_minimum_setpoint_day                    double precision,
    net_pipe_minimum_setpoint_night                  double precision,
    Value_in_iSii_1_5min                             double precision,
    Value_in_iSii_1                                  double precision,
    Value_to_iSii_1                                  double precision,
    energy_screen_ViP_screen_position_5min           double precision,
    energy_screen_ViP_screen_position                double precision,
    energy_screen_ViP_screen_position_day            double precision,
    energy_screen_ViP_screen_position_night          double precision,
    energy_screen_setpoint                           double precision,
    energy_screen_setpoint_day                       double precision,
    energy_screen_setpoint_night                     double precision,
    blackout_screen_ViP_screen_position_5min         double precision,
    blackout_screen_ViP_screen_position              double precision,
    blackout_screen_ViP_screen_position_day          double precision,
    blackout_screen_ViP_screen_position_night        double precision,
    blackout_screen_setpoint                         double precision,
    blackout_screen_setpoint_day                     double precision,
    blackout_screen_setpoint_night                   double precision,
    CO2_ViP_ppm_5min                                 double precision,
    CO2_ViP_ppm                                      double precision,
    CO2_ViP_ppm_day                                  double precision,
    CO2_ViP_ppm_night                                double precision,
    CO2_setpoint_ppm                                 double precision,
    CO2_setpoint_ppm_day                             double precision,
    CO2_setpoint_ppm_night                           double precision,
    humidity_deficit_ViP_5min                        double precision,
    humidity_deficit_ViP                             double precision,
    humidity_deficit_ViP_day                         double precision,
    humidity_deficit_ViP_night                       double precision,
    humidity_deficit_setpoint                        double precision,
    humidity_deficit_setpoint_day                    double precision,
    humidity_deficit_setpoint_night                  double precision,
    water_supply_interval_time_ViP_min_5min          double precision,
    water_supply_interval_time_ViP_min               double precision,
    irrigation_interval_time_setpoint_min            double precision,
    Writeto_iSii_5min                                double precision,
    Writeto_iSii                                     double precision,
    outside_temperature_5min                         double precision,
    outside_temperature                              double precision,
    outside_temperature_day                          double precision,
    outside_temperature_night                        double precision,
    outside_temperature_long_standing_average        double precision,
    outside_RH_5min                                  double precision,
    outside_RH                                       double precision,
    outside_RH_day                                   double precision,
    outside_RH_night                                 double precision,
    humidity_deficit_outside_5min                    double precision,
    humidity_deficit_outside                         double precision,
    humidity_deficit_outside_day                     double precision,
    humidity_deficit_outside_night                   double precision,
    absolute_humidity_content_outside_air_5min       double precision,
    absolute_humidity_content_outside_air            double precision,
    absolute_humidity_content_outside_air_day        double precision,
    absolute_humidity_content_outside_airnight       double precision,
    radiation_5min                                   double precision,
    radiation                                        double precision,
    radiation_sum_5min                               double precision,
    radiation_sum                                    double precision,
    radiation_sum_longstanding_average               double precision,
    wind_speed_5min                                  double precision,
    wind_speed                                       double precision,
    wind_speed_day                                   double precision,
    wind_speednight                                  double precision,
    wind_direction_type                              double precision,
    wind_direction_registration_5min                 double precision,
    wind_direction_registration                      double precision,
    wind_direction_registration_day                  double precision,
    wind_direction_registrationnight                 double precision,
    wind_direction_5min                              double precision,
    wind_direction                                   double precision,
    wind_direction_day                               double precision,
    wind_direction_night                             double precision,
    rain_5min                                        double precision,
    rain                                             double precision,
    rain_day                                         double precision,
    rain_night                                       double precision,
    WE_PAR_outside_measurement_5min                  double precision,
    WE_PAR_outside_measurement                       double precision,
    WE_PAR_outside_measurement_day                   double precision,
    WE_PAR_outside_measurementnight                  double precision,
    WE_heat_emission_pyrgeometer_5min                double precision,
    WE_heat_emission_pyrgeometer                     double precision,
    WE_heat_emission_pyrgeometer_day                 double precision,
    WE_heat_emission_pyrgeometernight                double precision,
    WE_netto_radiation_calc_5min                     double precision,
    WE_netto_radiation_calc                          double precision,
    FC_outside_temperature_5min                      double precision,
    FC_outside_temperature                           double precision,
    FC_outside_RH_5min                               double precision,
    FC_outside_RH                                    double precision,
    FC_radiation_5min                                double precision,
    FC_radiation                                     double precision,
    FC_radiation_sum_5min                            double precision,
    FC_radiation_sum                                 double precision,
    FC_wind_speed_5min                               double precision,
    FC_wind_speed                                    double precision,
    FC_degree_of_cloudiness18_5min                   double precision,
    FC_degree_of_cloudiness18                        double precision
);

alter table measure
    owner to postgres;

"""


simulation_data_insert_query = """
INSERT INTO simulation (
    time, comp1_air_t, comp1_air_rh, comp1_air_ppm, common_iglob_value, common_tout_value,
    common_rhout_value, common_windsp_value, comp1_parsensor_above, comp1_tpipe1_value,
    comp1_conpipes_tsupipe1, comp1_pconpipe1_value, comp1_conwin_winlee, comp1_conwin_winwnd,
    comp1_setpoints_spheat, comp1_setpoints_spvent, comp1_scr1_pos, comp1_scr2_pos,
    comp1_lmp1_elecuse, comp1_mcpureair_value, comp1_setpoints_spco2, comp1_growth_fruitfreshweight,
    comp1_growth_dvsfruit, comp1_growth_drymatterfract, comp1_growth_cropabs, comp1_growth_plantdensity,
    common_elecprice_peakhour, comp1_growth_wateruseperpot, comp1_growth_redfruitsweight
) VALUES %s
"""