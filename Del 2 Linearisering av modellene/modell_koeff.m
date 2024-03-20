clc;clear
g = 9.81;
masse = 20; % kg
tetthet_vann = 1000; % kg/m^3
Fb = 18.8*g; % Oppdriftskraften i N
r_Fb = 0.0206; % Avstand COM til COB

areal_front = 0.111624; % m^2
areal_side = 0.224606; % m^2
areal_topp = 0.304475; % m^2

Cd_front = 1.261;
Cd_topp = 1.257;
Cd_side = 1.410;

karakteristikk_prosentpaadrag = [0 12.5000 25.0000 37.5000 50.0000 62.5000 75.0000 87.5000 100.0000];
karakteristikk_kraftbidrag= [0 0.0370 0.2589 0.5675 0.8927 1.2590 1.7264 2.2152 2.7880]; % kg

theta_motor_gir = deg2rad(90-79.7);
r_motor_gir = 0.3144;

theta_motor_rull= deg2rad(90-62.4);
r_motor_rull = 0.3170;

theta_motor_stamp= deg2rad(90-57.3);
r_motor_stamp = 0.2715;

treghetsmoment_gir = 0.869830; % Fra inventor
bidrag_gir_front = 2*0.000327511; % A*r^3*sin(theta) for 2 halve frontsider
bidrag_gir_side = 0.00202665; % A*r^3*sin(theta) for en hel side

treghetsmoment_rull = 0.496497; % Fra inventor
bidrag_rull_topp = 2*0.000709818; % A*r^3*sin(theta) for 2 halve toppsider
bidrag_rull_side = 0.000429746; % A*r^3*sin(theta) for en hel side

treghetsmoment_stamp = 0.792810; % Fra inventor
bidrag_stamp_front = 0.000170539; % A*r^3*sin(theta) for en hel frontside
bidrag_stamp_topp = 0.002722379; % A*r^3*sin(theta) for en hel toppside

samplefrekvens = 20; % Hz

Kp_hiv = 0.334;
Ki_hiv = 0.334/3.360;
Kd_hiv = 0.334*0.084;
N_hiv = 0.35*(Kd_hiv/Kp_hiv);