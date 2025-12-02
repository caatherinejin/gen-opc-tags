# gen-opc-tags
scripts to import generator opc tags into ignition:
- tag import, tag/folder deletion, history enabled

1. create source folder in desired tag provider _(eg. opc data in ST_POWER)_
2. under tag browser, browse devices --> import OPC tags into source folder _(eg. ST38_GRID_RTAC --> DeviceSet --> Logic --> Resources --> Application --> GlobalVars --> sanchez_emcp2_MODBUS)_
3. 
4. copy path of source folder _(eg. [ST_POWER]Microgrid/Gen Garden/Data Tags/opc data)_\
5. paste into **tag import** file
6. create destination folder _(eg. sanchez_emcp2_modbus)_
7. copy path of destination folder _(eg. [ST_POWER]Microgrid/Gen Garden/Data Tags/sanchez_emcp2_modbus)_
8. paste into **tag import** file
9. navigate to connected devices window/browse devices and copy opc item path _(eg. nsu=CODESYSSPV3/3S/IecVarAccess;s=|var|Logic.Application.sanchez_emcp2_MODBUS)_
10. enter valid tag provider (eg. ST_POWER)
11. enter valid opc server (eg. ST38_GRID_RTAC)
12. run file in ignition script console
13. paste destination folder path into **tag deletion** file
14. run file in ignition script console
15. paste destination folder into **enables history** file
16. paste history provider database into **enables history** file (eg. ST_UTIL_DB_PRI)
17. run file in ignition script console
