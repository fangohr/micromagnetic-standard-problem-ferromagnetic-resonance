The mesh files here were created from the ``examesh`` mesh creation
utility that comes with Nmag (available at
https://bitbucket.org/fangohr/nmag-src/src/tip/utils/cubicmesh/examesh.c)

The commands to create the mesh files were:
```
   ./examesh mesh.nmesh,120:24,120:24,10:4
   nmeshpp -c mesh.nmesh mesh_555.nmesh.h5
```
and
```
   ./examesh mesh.nmesh,120:60,120:60,10:10
   nmeshpp -c mesh.nmesh mesh_221.nmesh.h5
```


