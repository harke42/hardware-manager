VELOCITY_AT_1 = 206 #[mm/s]
DIST_BETWEEN_MOTORS = 108 #[mm]
TIME_SCALOR = 4/3
RADIUS_SCALOR = 4/5

def vr_vl_from_radius(radius):
        ratio_vr_vl = (RADIUS_SCALOR*2*radius + DIST_BETWEEN_MOTORS)/(RADIUS_SCALOR*2*radius - DIST_BETWEEN_MOTORS)
        v_0 = VELOCITY_AT_1
        v_1 = v_0/ratio_vr_vl
        
        return v_1, v_0

def calculate_time_required(dphi=0, radius=-1):
    '''dphi in [rad], radius in [mm]'''
    v_l = 0
    v_r = 0
    estimated_time = 0
    
    if dphi == 0:
        if radius == 0:
            # stop
            pass
        elif radius > 0:
            v_l = VELOCITY_AT_1
            v_r = VELOCITY_AT_1
            estimated_time = radius/VELOCITY_AT_1
        else:
            raise Exception("Invalid Combination of dphi and radius: dphi = 0 and radius < 0")
        
    else:
        if dphi > 0:
            v_l, v_r = vr_vl_from_radius(radius)
        else:
            v_r, v_l = vr_vl_from_radius(radius)
        
        estimated_time = TIME_SCALOR * (dphi*DIST_BETWEEN_MOTORS)/(v_r - v_l)
    return estimated_time