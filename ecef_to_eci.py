# eci_to_ecef.py
#
# Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km
#  Converts a set of ECEF coordinates at a given time to the respective ECI coordinates
# Parameters:
#  year
#  month
#  day
#  hour
#  minute
#  second
#  ecef_x_km: x coordinate of the object in ECEF frame
#  ecef_y_km: y coordinate of the object in ECEF frame
#  ecef_z_km: z coordinate of the object in ECEF frame
# Output:
#  Print the eci coordinates for the given ecef position
#
# Written by Austin Zary
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math # math module
import sys # argv

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456
W_Rad = 0.00007292115

# helper functions

## function description
# def calc_something(param1, param2):
#   pass

# initialize script arguments
year = float('nan')
month = float('nan')
day = float('nan')
hour = float('nan')
minute = float('nan')
second = float('nan')
ecef_x_km = float('nan')
ecef_y_km = float('nan')
ecef_z_km = float('nan')

# parse script arguments
if len(sys.argv)==10:
    year = float(sys.argv[1])
    month = float(sys.argv[2])
    day = float(sys.argv[3])
    hour = float(sys.argv[4])
    minute = float(sys.argv[5])
    second = float(sys.argv[6])
    ecef_x_km = float(sys.argv[7])
    ecef_y_km = float(sys.argv[8])
    ecef_z_km = float(sys.argv[9])
else:
    print(\
        'Usage: '\
        'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
    )
    exit()

# write script below this line
## Calculate JDfractional
# Line 1:
div1 = (month-14.0)/12.0
if div1 > 0:
    div1 = math.floor(div1)
elif div1 < 0:
    div1 = math.ceil(div1)

div2 = 1461.0*(year + 4800.0 + div1)/4.0
if div2 > 0:
    Line1 = math.floor(div2)
elif div2 < 0:
    Line1 = math.ceil(div2)

# Line 2:
div3 = (month-14.0)/12.0
if div3 > 0:
    div3 = math.floor(div3)
elif div3 < 0:
    div3 = math.ceil(div3)

div4 = 367.0*(month - 2.0 - 12.0*div3)/12.0
if div4 > 0:
    Line2 = math.floor(div4)
elif div4 < 0:
    Line2 = math.ceil(div4)

# Line 3:
div5 = (year + 4900.0 + div3)/100.0
if div5 > 0:
    div5 = math.floor(div5)
elif div5 < 0:
    div5 = math.ceil(div5)

div6 = -3.0*div5/4.0
if div6 > 0:
    Line3 = math.floor(div6)
elif div6 < 0:
    Line3 = math.ceil(div6)

# Adding Lines:
JD = day -32075 + Line1 + Line2 + Line3

# Calculate Fractional Day
D = (second + 60.0 * (minute + 60.0*hour))/86400.0

# Final Julian Fractional Date Calculation
JDfractional = JD - 0.5 + D

## Calculate the GMST angle
TUT1 = (JDfractional - 2451545.0)/36525.0

GMST_sec = 67310.54841 + (876600.0*60.0*60.0 + 8640184.812866)*TUT1 + 0.093104*TUT1*TUT1 + (-6.2*10**(-6) * TUT1**3)
GMST_one_day = math.fmod(GMST_sec, 86400)
GMST = W_Rad*GMST_one_day

## Matrix rotation to finish coordinate transform
r_x = ecef_x_km*math.cos(GMST)-ecef_y_km*math.sin(GMST)
r_y = ecef_x_km*math.sin(GMST)+ecef_y_km*math.cos(GMST)
r_z = ecef_z_km

print(r_x)
print(r_y)
print(r_z)
