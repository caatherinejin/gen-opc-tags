# gen-opc-tags
scripts to import generator opc tags into ignition and create UDT

# import tags
1. create source folder in desired tag provider _(eg. opc data in ST_POWER)_
2. under tag browser, browse devices --> import OPC tags into source folder <br> _(eg. ST38_GRID_RTAC --> DeviceSet --> Logic --> Resources --> Application --> GlobalVars --> sanchez_emcp2_MODBUS)_
4. copy path of source folder _(eg. [ST_POWER]Microgrid/Gen Garden/Data Tags/opc data)_\
5. paste into **tag import** file
6. create destination folder _(eg. sanchez_emcp2_modbus)_
7. copy path of destination folder _(eg. [ST_POWER]Microgrid/Gen Garden/Data Tags/sanchez_emcp2_modbus)_
8. paste into **tag import** file
9. navigate to connected devices window/browse devices and copy opc item path <br> _(eg. nsu=CODESYSSPV3/3S/IecVarAccess;s=|var|Logic.Application.sanchez_emcp2_MODBUS)_
10. enter valid tag provider _(eg. ST_POWER)_
11. enter valid opc server _(eg. ST38_GRID_RTAC)_
12. run file in ignition script console

# delete unnecessary tags
14. paste destination folder path into **tag deletion** file
15. run file in ignition script console

# enable tag historian on tags
17. paste destination folder into **enables history** file
18. paste history provider database into **enables history** file _(eg. ST_UTIL_DB_PRI)_
19. run file in ignition script console

# create udt
21. create a new data type under UDT definitions
22. copy all tags under destination folder and paste into new UDT
23. copy JSON of UDT
24. open JSON file in a text editor and use find and replace opc item path to introduce a parameter <br>_(eg. find: nsu\u003dCODESYSSPV3/3S/IecVarAccess;s\u003d|var|Logic.Application.sanchezEMCP<mark>**2**</mark>MODBUS. <br> --> replace all: nsu\u003dCODESYSSPV3/3S/IecVarAccess;s\u003d|var|Logic.Application.sanchezEMCP<mark>{**genNumber**}</mark>MODBUS.)_
25. run **udt conversion** file in text editor
26. save JSON file and import as JSON as direct tags under tag browser
27. delete old UDT
28. create UDT instances!
