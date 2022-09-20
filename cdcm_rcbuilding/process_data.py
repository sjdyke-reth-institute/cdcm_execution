import h5py # pip install h5py

f = h5py.File("test_rc.h5", "r")

print(f["/everything/zone_rc_sys/T_room_sensor"][:])

