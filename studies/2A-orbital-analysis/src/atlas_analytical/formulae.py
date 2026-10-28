"""Pure analytical subset from accepted Document 2A-2 code; function bodies unchanged.
No private-reference reads, propagation, production imports or archived-result oracle.
"""
import math
from datetime import datetime, timezone, timedelta
import numpy as np
DAY=86400.;RAD=math.pi/180
WGS_A=6378.137;WGS_F=1/298.257223563
EPOCH=datetime(2026,10,20,12,tzinfo=timezone.utc)

def norm(x):return np.linalg.norm(x,axis=-1)

def unit(x):return np.asarray(x)/np.asarray(norm(x))[...,None]

def rotate_x(a):
    c,s=math.cos(a),math.sin(a);return np.array([[1.,0,0],[0,c,-s],[0,s,c]])

def rotate_y(a):
    c,s=math.cos(a),math.sin(a);return np.array([[c,0,s],[0,1.,0],[-s,0,c]])

def rotate_z(a):
    c,s=math.cos(a),math.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def initial_cartesian(o):
    p=o["a"]*(1-o["e"]**2);f=o["true"];r=p/(1+o["e"]*math.cos(f))
    rp=np.array([r*math.cos(f),r*math.sin(f),0.])
    vp=math.sqrt(o["mu"]/p)*np.array([-math.sin(f),o["e"]+math.cos(f),0.])
    q=rotate_z(o["node"])@rotate_x(o["i"])@rotate_z(o["peri"])
    return q@rp,q@vp

def precession_j2000_to_mod(utc):
    """Explicit IAU76 matrices, GMAT MathSpec 2.31-2.34, using TT.
    Archived leap-second model: TAI-UTC=37 s. GMAT MODEq sets Rdot=0.
    """
    jd=2451545.+(utc-datetime(2000,1,1,12,tzinfo=timezone.utc)).total_seconds()/DAY+69.184/DAY
    t=(jd-2451545.)/36525.
    zeta=(2306.2181*t+.30188*t*t+.017998*t**3)/3600*RAD
    theta=(2004.3109*t-.42665*t*t-.041833*t**3)/3600*RAD
    z=(2306.2181*t+1.09468*t*t+.018203*t**3)/3600*RAD
    return rotate_z(z)@rotate_y(-theta)@rotate_z(zeta),dict(jd_tt=jd,centuries=t,zeta_arcsec=zeta/RAD*3600,theta_arcsec=theta/RAD*3600,z_arcsec=z/RAD*3600)

def stumpff(z):
    """C(z), S(z): positive elliptic and zero cases used by this companion."""
    z=np.asarray(z,float);c=np.empty_like(z);s=np.empty_like(z);small=np.abs(z)<1e-7
    c[small]=.5-z[small]/24+z[small]**2/720
    s[small]=1/6-z[small]/120+z[small]**2/5040
    other=~small
    if np.any(z[other]<0):raise ValueError("Bound-orbit companion only")
    root=np.sqrt(z[other]);c[other]=(1-np.cos(root))/z[other];s[other]=(root-np.sin(root))/root**3
    return c,s

def universal_two_body(r0,v0,times,mu):
    """Independent universal anomaly plus Lagrange f,g; no force integration."""
    times=np.atleast_1d(times).astype(float);radius=float(norm(r0));dot=float(np.dot(r0,v0))
    sq=math.sqrt(mu);alpha=2/radius-float(v0@v0)/mu;chi=sq*alpha*times
    for _ in range(30):
        z=alpha*chi**2;c,s=stumpff(z)
        f=dot/sq*chi**2*c+(1-alpha*radius)*chi**3*s+radius*chi-sq*times
        df=dot/sq*chi*(1-z*s)+(1-alpha*radius)*chi**2*c+radius
        step=f/df;chi-=step
        if np.max(np.abs(step))<1e-10:break
    else:raise ArithmeticError("Universal anomaly did not converge")
    z=alpha*chi**2;c,s=stumpff(z);lf=1-chi**2*c/radius;lg=times-chi**3*s/sq
    r=lf[:,None]*r0+lg[:,None]*v0;rr=norm(r)
    fd=sq/(radius*rr)*(alpha*chi**3*s-chi);gd=1-chi**2*c/rr
    return r,fd[:,None]*r0+gd[:,None]*v0,chi

def j2_acceleration(r,mu,radius,j2):
    r=np.asarray(r);length=float(norm(r));z2=r[2]**2/length**2
    return 1.5*j2*mu*radius**2/length**5*r*np.array([5*z2-1,5*z2-1,5*z2-3])

def j2_potential(r,mu,radius,j2):
    length=float(norm(r));return mu*j2*radius**2/(2*length**3)*(3*r[2]**2/length**2-1)

def energy_mean_sma_estimate(o):
    """First-order time-average osculating SMA from constant central+J2 energy.
    Average the J2 potential along the unperturbed ellipse, then linearize a(epsilon).
    This is not a full canonical osculating-to-mean transformation.
    """
    r0,_=initial_cartesian(o)
    u0=j2_potential(r0,o["mu"],o["radius"],o["j2"])
    ubar=o["mu"]*o["j2"]*o["radius"]**2/(4*o["a"]**3*(1-o["e"]**2)**1.5)*(1-3*math.cos(o["i"])**2)
    shift=2*o["a"]**2/o["mu"]*(u0-ubar)
    return dict(initial_J2_potential_km2_s2=u0,unperturbed_average_J2_potential_km2_s2=ubar,
        first_order_mean_sma_shift_km=shift,estimated_mean_osculating_sma_km=o["a"]+shift)

def secular_rates(a,e,i,mu,radius,j2):
    n=math.sqrt(mu/a**3);p=a*(1-e*e);factor=n*j2*(radius/p)**2
    node=-1.5*factor*math.cos(i);peri=.75*factor*(5*math.cos(i)**2-1)
    mean=n+.75*factor*math.sqrt(1-e*e)*(3*math.cos(i)**2-1)
    return dict(mean_motion_rad_s=n,node_deg_day=node/RAD*DAY,peri_deg_day=peri/RAD*DAY,
        mean_anomaly_rad_s=mean,mean_latitude_period_min=2*math.pi/(mean+peri)/60)

def spherical_reach(angle,radius=6378.137,altitude=550.):
    arg=(radius+altitude)/radius*math.sin(angle)
    if abs(arg)>1:raise ValueError("Ray misses sphere")
    central=math.asin(arg)-angle
    return dict(central_angle_deg=central/RAD,ground_arc_km=radius*central,
        slant_km=math.sqrt((radius+altitude)**2+radius**2-2*radius*(radius+altitude)*math.cos(central)))

def surface_point(lat_deg,lon_deg):
    lat,lon=lat_deg*RAD,lon_deg*RAD;e2=WGS_F*(2-WGS_F)
    prime=WGS_A/math.sqrt(1-e2*math.sin(lat)**2)
    q=np.array([prime*math.cos(lat)*math.cos(lon),prime*math.cos(lat)*math.sin(lon),prime*(1-e2)*math.sin(lat)])
    m=np.array([math.cos(lat)*math.cos(lon),math.cos(lat)*math.sin(lon),math.sin(lat)])
    return q,m

def local_look(r,v,q,roll_limit):
    nadir=-unit(r);along=unit(v-np.dot(v,nadir)*nadir);cross=np.cross(along,nadir);los=q-r
    d,x,y=[float(np.dot(los,u)) for u in (nadir,cross,along)]
    alpha=math.atan2(x,d);roll=max(-roll_limit,min(roll_limit,alpha))
    beta=math.atan2(y,d*math.cos(roll)+x*math.sin(roll))
    return dict(alpha_rad=alpha,beta_rad=beta,roll_rad=roll,down_km=d,cross_km=x,along_km=y,
        r=r.tolist(),v=v.tolist(),los=los.tolist(),down_axis=nadir.tolist(),along_axis=along.tolist(),cross_axis=cross.tolist())

def ellipsoid_ray(r,d):
    axes2=np.array([WGS_A**2,WGS_A**2,(WGS_A*(1-WGS_F))**2])
    a=float(np.sum(d*d/axes2));b=2*float(np.sum(r*d/axes2));c=float(np.sum(r*r/axes2)-1);dis=b*b-4*a*c
    if dis<0:raise ValueError("Ray misses ellipsoid")
    positive=[v for v in ((-b-math.sqrt(dis))/(2*a),(-b+math.sqrt(dis))/(2*a)) if v>=0]
    if not positive:raise ValueError("Intersection behind ray")
    return r+min(positive)*d

def bisection(function,a,b,tolerance=2e-10):
    fa,fb=function(a),function(b)
    if fa==0:return a
    if fb==0:return b
    if fa*fb>0:raise ValueError("Root not bracketed")
    for _ in range(100):
        mid=(a+b)/2;fm=function(mid)
        if b-a<tolerance or mid==a or mid==b:return mid
        if fa*fm<=0:b=mid
        else:a=mid;fa=fm
    raise ArithmeticError("Bisection failed")

def radial_groundtrack(r):
    """Centre-directed ray on the adopted ellipsoid, then geodetic coordinates."""
    axes2=np.array([WGS_A**2,WGS_A**2,(WGS_A*(1-WGS_F))**2])
    q=np.asarray(r)/math.sqrt(float(np.sum(np.asarray(r)**2/axes2)))
    latitude=math.atan2(q[2]*axes2[0],math.hypot(q[0],q[1])*axes2[2])/RAD
    longitude=math.atan2(q[1],q[0])/RAD
    return dict(intercept_km=q.tolist(),latitude_deg=latitude,longitude_deg=longitude,
        geocentric_latitude_deg=math.atan2(r[2],math.hypot(r[0],r[1]))/RAD)

def noaa_solar_approx(utc,lat,lon):
    """Independent NOAA fractional-year approximation, a gross sign/scale check only."""
    hour=utc.hour+utc.minute/60+(utc.second+utc.microsecond/1e6)/3600
    gamma=2*math.pi/365*(utc.timetuple().tm_yday-1+(hour-12)/24)
    equation=229.18*(.000075+.001868*math.cos(gamma)-.032077*math.sin(gamma)-.014615*math.cos(2*gamma)-.040849*math.sin(2*gamma))
    decl=.006918-.399912*math.cos(gamma)+.070257*math.sin(gamma)-.006758*math.cos(2*gamma)+.000907*math.sin(2*gamma)-.002697*math.cos(3*gamma)+.00148*math.sin(3*gamma)
    angle=(hour*60+equation+4*lon)/4-180
    sine=math.sin(lat*RAD)*math.sin(decl)+math.cos(lat*RAD)*math.cos(decl)*math.cos(angle*RAD)
    return dict(fractional_year_rad=gamma,equation_of_time_min=equation,declination_deg=decl/RAD,hour_angle_deg=angle,
        UTC_based_LMST_h=(hour+lon/15)%24,approximate_apparent_solar_time_h=((angle+180)/15)%24,
        elevation_deg=math.asin(max(-1,min(1,sine)))/RAD)

def merged_intervals(intervals):
    answer=[]
    for start,end in sorted(intervals):
        if end<start:raise ValueError("Invalid interval")
        if answer and start<=answer[-1][1]:answer[-1][1]=max(end,answer[-1][1])
        else:answer.append([start,end])
    return answer

def exact_gaps(intervals,duration):
    intervals=merged_intervals(intervals)
    if not intervals:return dict(complete_gaps_h=[],leading_h=None,trailing_h=None,fully_censored_h=duration/3600,maximum_observed_h=duration/3600)
    complete=[(b[0]-a[1])/3600 for a,b in zip(intervals,intervals[1:])]
    leading=intervals[0][0]/3600;trailing=(duration-intervals[-1][1])/3600
    return dict(complete_gaps_h=complete,leading_h=leading,trailing_h=trailing,fully_censored_h=None,maximum_observed_h=max(complete+[leading,trailing]))

def coverage_from_saved_events(targets,events,hours,duration=30*DAY):
    """Independent event-to-integer-start union; no production searchsorted function."""
    horizon=hours*3600;n=int((duration-horizon)//3600)+1;delta=np.zeros(n+1)
    total=math.fsum(float(t["weight_km2"]) for t in targets)
    for target in targets:
        spans=[]
        for mid in events.get(target["id"],[]):
            lo=max(0,math.ceil((mid-horizon)/3600));hi=min(n-1,math.floor(mid/3600))
            if lo<=hi:spans.append((lo,hi+1))
        for lo,hi in merged_intervals(spans):
            delta[int(lo)]+=float(target["weight_km2"])/total;delta[int(hi)]-=float(target["weight_km2"])/total
    return np.cumsum(delta[:-1])

